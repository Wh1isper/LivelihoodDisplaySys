#-*-coding:utf-8-*-
from PIL import Image, ImageDraw, ImageFont
from glob import glob
import random
import numpy as np
import codecs
import os
import cv2
#DIR = os.getcwd()+'/dataset'

def draw_text(labels,size):
    """
    :param labels: 文本
    :param size: 图片大小
    :return: 一个batch大小训练数据，格式为：{"label":img}
    """
    backPaths = glob(DIR+'/bg_img/*.*')  ##背景图像
    fonts = glob(DIR+'/fonts/C_fonts/*.*')  ##字体集
    #图片尺寸
    X,Y = size
    fontType = random.choice(fonts)  ##随机获取一种字体
    #fontType = './fonts/simsun.ttc'
    fontSize = random.randint(13, 30)  # 字体大小
    font = ImageFont.truetype(fontType, fontSize)
    #保存训练数据及label
    image = []
    for label in labels:
        # 写入本起始尺寸
        cX = 2
        cY = random.randint(2,size[1]-40)
        # 字体颜色
        fill = 'black'
        p = random.randint(0,10)
        if p < 8 :
            # 70%的概率选择白底黑字
            im = Image.new(mode='RGB', size=(X, Y), color='white')  # color 背景颜色，size 图片大小

        else:
            #10%的概率黑底白字
            fill = 'white'
            im = Image.new(mode='RGB', size=(X, Y))  # color 背景颜色，size 图片大小

        drawer = ImageDraw.Draw(im)
        #保存每个字符的box
        lineBox = []
        for char in label:
            charX,charY = drawer.textsize(char,font=font)##字符所占的宽度
            #保存每个字符的box
            lineBox.append([cX,cY,cX+charX,cY+charY])
            #将字写入图片
            drawer.text(xy=(cX,cY), text=str(char), fill=fill,font=font)
            #下一个字符起始横坐标
            cX = cX+charX-2
        #根据每个字符位置，得到文本行的box
        box = merge_line_box(lineBox)
        img = im.crop(box)
        img = img.resize((256,32),Image.BILINEAR)
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
        ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = Image.fromarray(th2)

        #根据文本行box，截取图片
        image.append(img)
    image = resize(image)
    return image

def resize(img):
    """
    :param img:
    :return: 返回resize之后的图片，每张图高度32
    """
    maxw = max([i.size[0] for i in img])
    image = [i.resize((maxw,32),Image.BILINEAR) for i in img]
    return image


def read_text_split(length,batchsize):
    """
    :param length: 每张图片中字符长度
    :param batchsize:
    :return: 返回字符串数组，数组长度batchsize，没行字符串长度length
    """
    crupsPaths = glob(DIR+'/text/*.txt')  ##语料库
    dataList = []
    data = u''
    while length*batchsize*2 >= len(data):
        temptext = []
        txtfile = random.choice(crupsPaths)
        with codecs.open(txtfile,'r',encoding='utf-8') as f:
            d = f.read()
            for line in d.split('\n'):
                if line.strip()!=u'' and len(line.strip())>1:
                    temptext.append(line.strip())
        #将5个文件内容分段，去掉空格
        dataList.extend(temptext)
        # 将文件中的内容串联成一个字符串
        data = ','.join(dataList)
    #去空格
    data = data.strip()
    #文本随机起始值
    startindex = random.randint(0,len(data)-length*batchsize-1)
    splitData = []
    for i in range(batchsize):
        #从startindex处开始读取文本
        tx =  data[i*length+startindex:(i+1)*length+startindex]
        if tx!=u'':
           splitData.append(tx)
    return splitData

def get_batch(length,batchsize):
    """
    :param length: 文本序列长度
    :param batchsize:
    :return: 返回一个batch的训练数据，数据格式:{"label":image}
    """
    #图片尺寸
    SizeList = [650,1024]
    #随机选择图片尺寸
    Size = random.choice(SizeList)
    #获取一个batch的文本，每行文本长度为length
    texts = read_text_split(length,batchsize)
    #获取训练数据
    image  = draw_text(texts,size=(Size,Size))
    return texts , image

def merge_line_box(lineBoxes):
    """
    :param lineBoxes: 每个字符box列表
    :return: 整个文本行的box
    """
    lineBox = np.array(lineBoxes)
    if len(lineBox) != 0 :
        x0,y0 = lineBox[:,::2].min(),lineBox[:,1::2].min()
        x2,y2 = lineBox[:,::2].max(),lineBox[:,1::2].max()

    return [int(x0),int(y0),int(x2),int(y2)]

def crop_img(image,texts):
    """
    :param img_label:
    :return: 保存训练数据中的图片
    """
    global index
    for i in range(len(texts)):
        image[i].save("./data/"+str(index)+'.jpg')
        with open('./data/'+str(index)+'.txt','w') as f:
            f.write(texts[i])
        index = index + 1

index = 0
if __name__ == '__main__':

    DIR = 'display/static/display/ocrdata'
    #标签长度
    #length = random.randint(2,20)
    length = 10

    #获取训练数据
    for i in range(2):
        texts , image = get_batch(length,batchsize=10)
        print(texts[:])
        crop_img(image,texts)

