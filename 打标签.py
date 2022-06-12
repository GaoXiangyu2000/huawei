# 调用包从图像识别包中调用，图像标签,工具包
from image_sdk.utils import encode_to_base64
from image_sdk.image_tagging import image_tagging_aksk
from image_sdk.utils import init_global_env
# 调用 json 解析传回的结果
import json
# 操作系统文件/文件夹的包
import os
import shutil
# 图像处理展示相关的包
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

init_global_env('cn-north-4')
# 准备 ak,sk
app_key = 'ZUONXVK9NX7MI76UN8NP'
app_secret = 'x684wxrH9bX92miRZtIcNqEEpfW5AXCa3HsX0c55'

# 确定电子相册位置
file_path ='data/'
# 保存图片标签的字典
labels = {}
items = os.listdir(file_path)
for i in items:
    # 判断是否为文件，而不是文件夹
    if os.path.isfile:
        # 华为云 EI 目前支持 JPG/PNG/BMP 格式的图片
        if i.endswith('jpg') or i.endswith('jpeg') or i.endswith('bmp') or i.endswith('png'):
             # 为图片打上标签
            result = image_tagging_aksk(app_key, app_secret, encode_to_base64(file_path + i), '', 'zh',5, 60)
            # 解析返回的结果
            result_dic = json.loads(result)
            # 将文件名与图片对齐
            labels[i] = result_dic['result']['tags']

# 显示结果
print(labels)

#将标签字典保存到文件
save_path = './label'
# 如果文件夹不存在则创建文件
if not os.path.exists(save_path):
    os.mkdir(save_path)
# 创建文件,执行写入操作，并关闭
with open(save_path + '/labels.json', 'w+') as f:
    f.write(json.dumps(labels))

