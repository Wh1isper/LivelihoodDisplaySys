#coding:utf-8
"""
转换文件编码，提供文件所在文件夹或者文件路径，默认转换成utf-8编码
"""
from glob import glob
import codecs
import chardet

# 获取文件编码类型
def get_encoding(file):
    """
    :param file: 目标文件名
    :return: 返回目标文件的编码
    """
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

def getdata(path,encode):
    """
    :param path: 目标文件
    :param encode: 文件的编码格式
    :return: 文件内容
    """
    with codecs.open(path,'r',encoding=encode) as f:
        return f.read()

def writefile(path,encode,data):
    """
    :param path: 目标文件
    :param encode: 写入文件的编码格式
    :param data: 写入内容
    :return:
    """
    with codecs.open(path,'w',encoding=encode) as f:
        f.write(data)

def change_encode(file_dir, target_encode):
    """
    :param file_dir: 目标文件夹
    :param target_encode: 目标编码
    :return: 将目标文件夹下所有文件全部转换成目标编码，保存在./encode/文件夹下
    """
    filepath = glob(file_dir)
    for path in filepath:
        file = './encode/'+str(path.split('/')[-1])
        encode = get_encoding(path)
        if encode != target_encode:
            if encode == 'GB2312' or encode == 'GBK' or encode == None:
                encode = 'gb18030'
            data = getdata(path,encode)
            writefile(file,target_encode,data)

def remove_space(src_dir,tar_dir):
    filenames = glob(src_dir+'/*.txt')
    for filename in filenames:
        try:
            data = getdata(filename,'utf-8')
            data.replace(' ','')
            data.replace('\n','')
            data = data.split()
            text = ''
            for d in data:
                text += d
            save_file = tar_dir+'/'+filename.split('/')[-1]
            print(save_file)
            writefile(save_file,'utf-8',text)
        except UnicodeDecodeError:
            print(filename+" error !")
    print('done !')

if __name__ == '__main__':
    #file_dir = ''
    #target_encode = 'utf-8'
    #change_encode(file_dir,target_encode)
    remove_space('./E_text','./E_texts')
