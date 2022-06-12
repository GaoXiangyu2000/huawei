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


# 打开刚刚保存的文件
label_path = 'label/labels.json'
with open(label_path,'r') as f:
    labels = json.load(f)

# 搜索关键词
key_word = input('请输入搜索词：')
# 设置可信百分比
threshold = 60
# 设置一个集合（集合存放照片文件名）
valid_list = set()

# 遍历 labels 中的字典获取所有包含关键字的图片名字
# label是一个字典，键：文件名 值：list[]
for k,v in labels.items():
    for item in v:
        if key_word in item['tag'] and float(item['confidence']) >= threshold:
            valid_list.add(k)
# 展示结果
valid_list = list(valid_list)
print("查询到的复合要求的照片文件名如下：")
print(valid_list)

# 设置画布大小
plt.figure(24)
# 将每张图片依次排列到画布上
for k,v in enumerate(valid_list[:9]):
    pic_path = 'data/' + v
    img = Image.open(pic_path)
    img = img.resize((640,400))
    plt.subplot(331 + k)
    plt.axis('off')
    plt.imshow(img)
plt.show()

# 生成一个临时文件夹
if not os.path.exists('tmp'):
    os.mkdir('tmp')
# 将所有搜索到的图像转化为 gif 格式，并存储在临时文件夹中
gif_list = []
for k, pic in enumerate(valid_list):
    pic_path = 'data/' + pic
    img = Image.open(pic_path)
    img = img.resize((640,380))
    save_name = 'tmp/'+ str(k) + '.gif'
    img.save(save_name)
    gif_list.append(save_name)

# 打开已经所有静止的 gif 图片
images=[]
for i in gif_list:
    pic_path = i
    images.append(Image.open(pic_path))

# 存储成动图 gif
images[0].save('相册动图.gif',save_all=True,append_images=images[1:],duration=1000,loop=0)
# 释放内存
del images
# 删除临时文件夹
shutil.rmtree('tmp')
print('gif 相册制作完成')


# 获取置信度最高的文件分类
classes =[[v[0]['tag'],k] for k, v in labels.items()]

for cls in classes:
    if not os.path.exists('data/' + cls[0]):
        os.mkdir('data/'+ cls[0])
    # 复制被对应的图片
    shutil.copy('data/'+ cls[1], 'data/'+ cls[0]+ '/' + cls[1])
print('已完成移复制!')