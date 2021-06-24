import json
import utils
import chardet
import tokenize
import html
import topk

# input word and return the inverted index of the word
def boolquery(query):
    all_doc = utils.get_doc_list()
    all_doc.sort()

    isAnd = False
    isOr = False
    isNot = False
    query_words = []
    result = []
    sub_result = []
    word = ''
    word_last = ''

    i = 0
    while i < len(query):
        if query[i] == '(': 
            lcount = 1
            rcount = 0
            isclose = False
            i += 1
            while i < len(query):
                if query[i] == '(':
                    lcount += 1
                if query[i] == ')':
                    rcount += 1
                    if rcount < lcount:
                        word += ')'
                        i += 1
                        continue
                    isclose = True
                    break
                else:
                    word += query[i]
                i += 1
            if isclose == False: 
                print("语法错误！")
                return []
            else:
                if isAnd: 
                    if isNot: # AND NOT ()
                        sub_result = handle_not(boolquery(word), all_doc)
                        isNot = False
                    else:
                        sub_result = boolquery(word)
                    result = handle_and(result, sub_result)
                    isAnd = False
                elif isOr: 
                    if isNot: # OR NOT ()
                        isNot = False
                        sub_result = handle_not(boolquery(word), all_doc)
                    else:
                        sub_result = boolquery(word)
                    result = handle_or(result, sub_result)
                    isOr = False
                else: 
                    if isNot:  # NOT ()
                        isNot = False
                        result = handle_not(boolquery(word), all_doc)
                    else:
                        result = boolquery(word)

        elif query[i] == 'A':
            if i + 2 < len(query) and i - 1 > 0:
                if query[i+1] == 'N' and query[i+2] == 'D' and query[i-1] == ' ':
                    isAnd = True
                    i += 2
                else:
                    word += 'a'
            else:
                word += 'a'

        elif query[i] == 'O':
            if i + 1 < len(query) and i - 1 > 0:
                if query[i+1] == 'R' and query[i-1] == ' ':
                    isOr = True
                    i += 1
                else:
                    word += 'o'
            else:
                word += 'o'

        elif query[i] == 'N':
            if i + 2 < len(query) and word == '':
                if query[i+1] == 'O' and query[i+2] == 'T':
                    isNot = True
                    i += 2
                else:
                    word += 'n'
            else:
                word += 'n'

        # 空格
        elif query[i] == ' ':
            if word != '':
                word = word.lower()
                query_words.append(word)
                if isAnd: 
                    if word_last == '':
                        print("语法错误！")
                        return []
                    if isNot: # AND NOT ()
                        sub_result = handle_not(utils.loadIndex(word)[1], all_doc)
                        isNot = False
                    else:
                        sub_result = utils.loadIndex(word)[1]
                    result = handle_and(result, sub_result)
                    isAnd = False
                elif isOr: 
                    if word_last == '':
                        print("语法错误！")
                        return []
                    if isNot: # OR NOT ()
                        isNot = False
                        sub_result = handle_not(utils.loadIndex(word)[1], all_doc)
                    else:
                        sub_result = utils.loadIndex(word)[1]
                    result = handle_or(result, sub_result)
                    isOr = False
                else: #() is in the front
                    if isNot:# like: NOT ()
                        isNot = False
                        result = handle_not(utils.loadIndex(word)[1], all_doc)
                    else:
                        result = utils.loadIndex(word)[1]
                word_last = word
                word = ''

        else:
            word += query[i]
            if i == len(query) - 1: # 查询的结尾
                word = word.lower()
                query_words.append(word)
                if isAnd:  # () is after AND
                    if word_last == '':
                        print("语法错误！")
                        return []
                    if isNot:  # AND NOT ()
                        sub_result = handle_not(utils.loadIndex(word)[1], all_doc)
                        isNot = False
                    else:
                        sub_result = utils.loadIndex(word)[1]
                    result = handle_and(result, sub_result)
                    isAnd = False
                elif isOr:  # () is after OR
                    if word_last == '':
                        print("Bad Query! Meet OR First!")
                        return []
                    if isNot:  # OR NOT ()
                        isNot = False
                        sub_result = handle_not(utils.loadIndex(word)[1], all_doc)
                    else:
                        sub_result = utils.loadIndex(word)[1]
                    result = handle_or(result, sub_result)
                    isOr = False
                else:  # () is in the front
                    if isNot:  # NOT ()
                        isNot = False
                        result = handle_not(utils.loadIndex(word)[1], all_doc)
                    else:
                        result = utils.loadIndex(word)[1]
                word_last = word
                word = ''
        i += 1
    return result



# 读取输入
def controller(query):
    index = boolquery(query)
    query.replace('NOT','')
    query.replace('AND','')
    query.replace('OR','')
    query.replace('(','')
    query.replace(')','')
    query.replace('  ',' ')
    wordlist = []
    wordlist = query.split(' ')
    docID = topk.topK(wordlist,index)
    utils.printtext(wordlist,docID)


def handle_and(index1, index2):
    index1.sort()
    index2.sort()
    i = 0
    j = 0
    result = []
    while i < len(index1) and j < len(index2):
        if index1[i] == index2[j]:
            result.append(index1[i])
            i += 1
            j += 1
        elif index1[i]<index2[j]:
            i += 1
        else:
            j += 1
    return result


def handle_or(index1, index2):
    index1.sort()
    index2.sort()
    i = 0
    j = 0
    result = []
    while i < len(index1) and j < len(index2):
        if index1[i] == index2[j]:
            result.append(index1[i])
            i += 1
            j += 1
        elif index1[i]<index2[j]:
            result.append(index1[i])
            i += 1
        else:
            result.append(index2[j])
            j += 1
    if i == len(index1):
        while j < len(index2):
            result.append(index2[j])
            j += 1
    else:
        while i < len(index1):
            result.append(index1[i])
            i += 1
    return result


def handle_not(index, all_doc):
    index.sort()
    i = 0
    j = 0
    result = []
    while i < len(index) and j < len(all_doc):
        if index[i] == all_doc[j]:
            i += 1
            j += 1
        elif all_doc[j] < index[i]:
            result.append(all_doc[j])
            j += 1
    while j < len(all_doc):
        result.append(all_doc[j])
        j += 1
    return result


