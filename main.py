# !/usr/bin/env python
import os
import utils
import InvertedIndex
import BooleanQuery
import PhraseQuery
import GlobbingQuery
import SpellingCorrect
import SynonymsWords
import nltk
import time

def preprocessing():
    # ------------
    # 构建索引/VSM
    # ------------
    nltk.download('punkt')
    start_time = time.time()
    print('构建倒排索引...')
    # 构建倒排索引和每篇文档的词数
    index, doc_size = InvertedIndex.create_index()
    # 用倒排索引生成词表
    print('构建词表...')
    wordlist = InvertedIndex.get_wordlist(index)
    end_time_index = time.time()
    print('用时%fms' % ((end_time_index - start_time)*1000))
    # 构建同义词表
    print('构建同义词表...')
    # InvertedIndex.create_synonymslist(wordlist)
    # 生成 VSM
    print('构建VSM模型...')
    VSM = InvertedIndex.create_VSM(index, doc_size, wordlist)

    end_time = time.time()
    print('用时%fms' % ((end_time - end_time_index)*1000))

    # 将文件存档
    print('文件存档...')
    utils.write_to_file(index, utils.ipath+'index.json')
    utils.write_to_file(wordlist, utils.ipath+'wordlist.json')
    utils.write_to_file(doc_size, utils.ipath+'doc_size.json')
    utils.write_to_file(VSM, utils.ipath+'VSM.json')

    # utils.zip_file(index, utils.ipath+'index.gz')
    # utils.zip_file(wordlist, utils.ipath+'wordlist.gz')
    # utils.zip_file(doc_size, utils.ipath+'doc_size.gz')
    # utils.zip_file(VSM, utils.ipath+'VSM.gz')


    
    #
    
def main():
    print('初始化...')
    print('读取索引...')
    # index = utils.get_from_gz('index')
    wordlist = utils.get_from_file('wordlist')
    # doc_size = utils.get_from_gz('doc_size')
    # VSM = utils.get_from_gz('VSM')
    btree, btree_rev = GlobbingQuery.BuildTree(wordlist)
    print('*'*25)
    print('  欢迎使用文档搜索引擎!')
    print('      Ver. 1.1')
    while True:
        print("*"*25)
        number = input("  请输入指令:\n      1.布尔查询\n      2.词语查询\n      3.通配符查询\n      0.退出系统\n")
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
            correct_query = SpellingCorrect.spelling_correct(query)
            opt = input("\n是否需要进行同义词搜索？[y/n]\n")
            if (opt == 'N' or opt == 'n'):
                print("不进行同义词搜索！\n")
                PhraseQuery.phrasequery(correct_query)
            else:
                print("开始执行同义词搜索：")
                synonyms_query = SynonymsWords.get_synonyms_words(correct_query)
                BooleanQuery.controller(synonyms_query)
            # PhraseQuery.phrasequery(synonyms_query)
        # 通配符查询
        if int(number)==3:
            GlobbingQuery.controller(query, btree, btree_rev,wordlist)
        # # 拼写校正
        # if int(number)==4:
        #     SpellingCorrect.spelling_correct(query)



if __name__ == "__main__":
    # preprocessing()
    main()
