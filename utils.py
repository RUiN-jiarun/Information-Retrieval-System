import os
import json
import jsonlines
from nltk import word_tokenize
import chardet
import tokenize
import html
import gzip

# todo: 
# - nltk 词干还原
# - 优化词表过滤规则

# 非 Linux 环境下记得自己改路径
ppath = os.getcwd()+'/'
ipath = ppath + '/index/'
rpath = ppath + '/Reuters/'
# 语料数量是常数 by 文件夹下文件数量
D = 10788 

# 将数据写入文件
def write_to_file(data, filename):
    file = open(filename, 'w')
    str = json.JSONEncoder().encode(data)
    file.write(str)
    file.close()

# 使用gzip压缩算法
def zip_file(data, filename):
    with gzip.GzipFile(filename,'w') as fid_gz:
        s = json.JSONEncoder().encode(data)
        B = bytes(s,'utf8')
        fid_gz.write(B)






# 获取语料库的所有文件列表
def get_doc_list():
    filelist = []
    files = os.listdir('./Reuters/')
    for file in files:
        filelist.append(get_doc_ID(file))
    return sorted(filelist)

# 从文档名中截取文档 ID
def get_doc_ID(filename):
    docID = os.path.splitext(filename)[0]
    return int(docID)

# 处理语料库文档的内容
def process_doc_content(filename):
    # 处理 ASCII 格式的语料
    with open(filename, 'r', encoding='ISO-8859-1') as file:
        content = file.read()
    res = []
    result = []
    # 标点符号和数字
    punc_digit = [',', '.', ';', ':', '&', '>', "'", '"','`', '+', '*', '?', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for word in word_tokenize(content):
        # 转换为小写
        word = word.lower()
        # 处理标点符号
        for c in punc_digit:
            word = word.replace(c, '')
        # 处理空字符串
        if len(word) == 0 or word[0] == '-':
            continue
        # 处理 's
        if word[0] == '\'':
            continue
        # 处理 March/April 中的 / ：分成两个单词
        if word.find('/') > 0:
            res = word.split('/')
            for w in res:
                result.append(w)
            continue
        result.append(word)
    return result

# 从 JSON 中读取倒排索引/词表
def get_from_file(filename):
    file = open(ipath + filename + '.json', 'r')
    res = json.JSONDecoder().decode(file.read())
    return res

# 从压缩过的二进制文件中读取索引/词表
def get_from_gz(filename):
    with gzip.GzipFile(ipath + filename + '.gz','r') as fid_gz :
        res = eval(fid_gz.read())
    return res

# 从 JSON 中读取同义词表
def get_from_file_L(filename):
    file = filename + '.jsonl'
    res = jsonlines.open(file)
    return res

# 读取位置索引
def loadIndex(word):
    # with gzip.GzipFile('index/index.gz','r') as fid_gz :
    #     raw = fid_gz.read()
    #     dictionary = json.JSONDecoder().decode(raw)
    f = open("index/index.json", encoding='utf-8')
    dictionary = json.load(f)
    index = dictionary[word] if word in dictionary.keys() else None
    result = []
    if index is not None:
        for item in index:
            result.append(int(item))
    else:
        result = []
    return index, result

# 打印结果
def printtext(wordlist, doclist):
    directory = "./Reuters"
    highlights = []
    for word in wordlist:
        highlights.append(word)
        highlights.append(word.upper())
        highlights.append(word.title())
    for docid in doclist:
        with open(directory + '/' + str(docid) + '.html', 'rb') as htmlfile:
            rawdata = htmlfile.read()
            encoding = chardet.detect(rawdata)['encoding']
            text = rawdata.decode(encoding)
            text = html.unescape(text)
        print("************** 文档显示 **************")
        print("\033[1;33;40m"+str(docid)+".html"+"\033[0m")
        for word in highlights:
            text = text.replace(word, "\033[1;31;40m" + word + "\033[0m")
        print(text)
