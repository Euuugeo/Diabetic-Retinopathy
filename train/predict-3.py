import os
import numpy as np
import torch
import SimpleITK as sitk
import cv2  # 新增导入
from PIL import Image
from torchvision import transforms
from collections import OrderedDict
from Transforms_v2 import Resize, CenterCrop, ApplyCLAHE, ToTensor
from nets.CAUNet import CAUNet
from nets import U2Net, UNet, unetpp, ENet

# 定义病灶颜色映射
LESION_COLORS = {
    'EX': (255, 0, 0),    # 红色
    'MA': (0, 255, 0),    # 绿色
    'HE': (0, 0, 255),    # 蓝色
    'SE': (128, 0, 128)   # 紫色
}

def load_image(image_path):
    """加载并预处理输入图片，保持原始色调"""

    # 使用SimpleITK进行预处理
    image = sitk.ReadImage(image_path)
    image_array = sitk.GetArrayFromImage(image)
    
    transform_origin = transforms.Compose([
        Resize(640),
        CenterCrop(640)
    ])

    sample_origin = {'image': image_array, 'masks': np.zeros((5, 640, 640))}
    sample_origin = transform_origin(sample_origin)

    transform = transforms.Compose([
        Resize(640),
        CenterCrop(640),
        ToTensor(green=False)
    ])
    
    sample = {'image': image_array, 'masks': np.zeros((5, 640, 640))}
    sample = transform(sample)
    
    return sample['image'].unsqueeze(0), sample_origin['image']

def create_colored_mask(prediction):
    """将预测结果转换为彩色mask"""
    prob = torch.softmax(prediction, dim=1)
    pred_mask = torch.argmax(prob, dim=1).squeeze().cpu().numpy()
    
    print(f"Unique predicted classes after softmax: {np.unique(pred_mask)}")
    
    h, w = pred_mask.shape
    colored_mask = np.zeros((h, w, 3), dtype=np.uint8)
    
    colored_mask[pred_mask == 1] = LESION_COLORS['EX']
    colored_mask[pred_mask == 2] = LESION_COLORS['HE']
    colored_mask[pred_mask == 3] = LESION_COLORS['MA']
    colored_mask[pred_mask == 4] = LESION_COLORS['SE']
    
    return colored_mask

def predict(model, image_tensor):
    """使用模型进行预测"""
    model.eval()
    with torch.no_grad():
        # 将输入转换为float32类型
        image_tensor = image_tensor.float()
        output = model(image_tensor)
        
        # 处理UNet++的多输出情况
        if isinstance(output, tuple):
            output = output[-1]  # 使用最后一个输出
            
        if output.shape[1] != 5:
            output = output.permute(0, 3, 1, 2)
        output = torch.softmax(output, dim=1)
    return output

def save_result(original_img, colored_mask, output_path):
    """保持原始色调的叠加方法"""
    # 确保原始图像是numpy数组
    if isinstance(original_img, torch.Tensor):
        original_img = original_img.cpu().numpy()
    
    # 调整原始图像尺寸以匹配掩码(640x640)
    if original_img.shape[0] != 640 or original_img.shape[1] != 640:
        original_img = cv2.resize(original_img, (640, 640))
    
    # 确保掩码大小与原图一致
    if colored_mask.shape[0] != 640 or colored_mask.shape[1] != 640:
        colored_mask = cv2.resize(colored_mask, (640, 640))
    
    # 如果原始图像是单通道，转换为3通道
    if len(original_img.shape) == 2:
        original_img = np.stack([original_img]*3, axis=-1)
    elif original_img.shape[2] == 1:
        original_img = np.repeat(original_img, 3, axis=2)
    
    # 确保值在0-255范围内
    if original_img.max() <= 1.0:
        original_img = (original_img * 255).astype(np.uint8)
    else:
        original_img = original_img.astype(np.uint8)
    
    # 创建叠加图像
    overlay = original_img.copy()
    
    # 只在不完全黑色的区域叠加预测结果
    mask = (colored_mask != 0).any(axis=2)
    
    # 使用加权叠加
    overlay[mask] = cv2.addWeighted(original_img[mask], 0.5, colored_mask[mask], 0.5, 0)
    
    # 保存结果
    #Image.fromarray(original_img).save('/root/autodl-tmp/re/LKD/output/origin.jpg')
    Image.fromarray(overlay).save(output_path)


def main():
    # 参数设置
    model_type = 'McaUnet'  # 可选: Unet, U2net, McaUnet, Unet++
    image_path = '/root/autodl-tmp/LKD/input/007-7175-400.jpg'
    
    # 从image_path中提取文件名
    image_name = image_path.split('/')[-1]  # 获取路径最后一段
    base_name = image_name.split('.')[0]    # 移除扩展名
    output_path = f'/root/autodl-tmp/LKD/output/{base_name}_{model_type}_pred.jpg'
    
    # 根据model_type加载不同的模型
    if model_type == 'Unet':
        model_path = 'weight/model.LBTW_WeightedDiceBCE--unet--147.pth.tar'
        model = UNet.UNet(n_channels=3, n_classes=5)
    elif model_type == 'U2net':
        model_path = 'weight/model.LBTW_WeightedDiceBCE--u2net--127.pth.tar'
        model = U2Net.U2NET(3, 5)
    elif model_type == 'McaUnet':
        model_path = 'weight/model.LBTW_WeightedDiceBCE--mcaunet--149.pth.tar'
        model = CAUNet(3, 5)
    elif model_type == 'Unet++':
        model_path = 'weight/model.LBTW_WeightedDiceBCE--unet++--148.pth.tar'
        model = unetpp.NestedUNet(3, 5, deepsupervision=True)
    else:
        raise ValueError(f"不支持的模型类型: {model_type}")
    
    # 处理多GPU保存的模型参数
    checkpoint = torch.load(model_path, map_location='cpu')
    new_state_dict = OrderedDict()
    for k, v in checkpoint['state_dict'].items():
        name = k[7:] if k.startswith('module.') else k
        new_state_dict[name] = v
    model.load_state_dict(new_state_dict)
    model = model.to('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 修改加载图像的部分
    image_tensor, original_img = load_image(image_path)
    image_tensor = image_tensor.to('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 进行预测
    prediction = predict(model, image_tensor)
    print(f"Model output shape: {prediction.shape}")
    print(f"Model output min/max: {prediction.min()}, {prediction.max()}")
    
    # 创建彩色mask
    colored_mask = create_colored_mask(prediction)
    
    # 修改保存结果的部分
    save_result(original_img, colored_mask, output_path)
    print(f"预测结果已保存到: {output_path}")

if __name__ == '__main__':
    main()