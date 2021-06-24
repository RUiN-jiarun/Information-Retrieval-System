# !/usr/bin/env python
import os
import utils
import InvertedIndex
import BooleanQuery
import PhraseQuery
import GlobbingQuery
import SpellingCorrect
import nltk

def preprocessing():
    # ------------
    # 构建索引/VSM
    # ------------
    # 跑一遍来构建文件，第二遍就可以注释掉了
    nltk.download('punkt')
    print('构建倒排索引...')
    # 构建倒排索引和每篇文档的词数
    index, doc_size = InvertedIndex.create_index()
    # 用倒排索引生成词表
    print('构建词表...')
    wordlist = InvertedIndex.get_wordlist(index)
    # 生成 VSM
    print('构建VSM模型...')
    VSM = InvertedIndex.create_VSM(index, doc_size, wordlist)
    # # 为 Top K 暴力查表做计算
    VSM_sum = InvertedIndex.VSM_sum(VSM)
    # # 将文件存档
    print('文件存档...')
    utils.write_to_file(index, utils.ppath+'index.json')
    utils.write_to_file(wordlist, utils.ppath+'wordlist.json')
    utils.write_to_file(doc_size, utils.ppath+'doc_size.json')
    utils.write_to_file(VSM, utils.ppath+'VSM.json')
    utils.write_to_file(VSM_sum, utils.ppath+'VSM_sum.json')
    #
    
    

# ------------
# 搜索 etc.
# ------------
def main():
    # 从 JSON 读取数据， JSON 文件默认放在 IRProject 下
    print('读取索引...')
    index = utils.get_from_file('index')
    wordlist = utils.get_from_file('wordlist')
    doc_size = utils.get_from_file('doc_size')
    VSM = utils.get_from_file('VSM')
    btree, btree_rev = GlobbingQuery.BuildTree(wordlist)
    while True:
        print("\n", "*"*50)
        number = input("选择查询类型:\n  1.布尔查询\n  2.词语查询\n  3.通配符查询\n  4.拼写矫正\n  0.退出系统\n")
        if int(number)==0:
            break
        if int(number) > 4 or int(number) < 0:
            print("未知指令！")
            continue
        query = input("请输入查询:\n")
        # 布尔检索
        if int(number)==1:
            BooleanQuery.controller(query)
        # 短语查询
        if int(number)==2:
            PhraseQuery.phrasequery(query)
        # 通配符查询
        if int(number)==3:
            GlobbingQuery.controller(query, btree, btree_rev,wordlist)
        # 拼写校正
        if int(number)==4:
            SpellingCorrect.spelling_correct(query)

        #merge
        #if query.find('*')!=-1:
            #GlobbingQuery.controller(query, btree, btree_rev, wordlist)


if __name__ == "__main__":
    # preprocessing()
    main()
