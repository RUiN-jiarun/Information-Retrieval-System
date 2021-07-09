# encoding: utf-8  
import re, collections
import utils


# 构建先验概率
def tolower(text):
    return re.findall('[a-z]+',text.lower())

def prior(cwords):
    model = collections.defaultdict(lambda:1)
    for f in cwords:
        model[f]+=1
    return model

# 从wordlist.json中读出资料库中的所有词
cwords = utils.get_from_file('wordlist')
# cwords = utils.get_from_gz('wordlist')

# 计算词项频率
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model
	
# get P(c)
nwords = train(cwords) 


# 类条件概率

alpha = 'abcdefghijklmnopqrstuvwxyz'

# 一步调整

def version1(word):

    n = len(word)
    add_a_char = [word[0:i] + c + word[i:] for i in range(n+1) for c in alpha]
    delete_a_char = [word[0:i] + word[i+1:] for i in range(n)]
    revise_a_char = [word[0:i] + c + word[i+1:] for i in range(n) for c in alpha]
    swap_adjacent_two_chars = [word[0:i] + word[i+1]+ word[i]+ word[i+2:] for i in range(n-1)] 
    return set( add_a_char + delete_a_char +
               revise_a_char +  swap_adjacent_two_chars)

# 两步调整           

def version2(word):
    return set(e2 for e1 in version1(word) for e2 in version1(e1))


def identify(words):
    return set(w for w in words if w in nwords)


def getMax(wanteds):
    options=[]
    maxword = max(wanteds,key=lambda w : nwords[w])
    options.append(maxword)
    wanteds.remove(maxword)

    if len(wanteds)>0:
        maxword = max(wanteds,key=lambda w : nwords[w])
        options.append(maxword)
        wanteds.remove(maxword)
        if len(wanteds)>0:
            maxword = max(wanteds,key=lambda w : nwords[w])
            options.append(maxword)   
    return options

# 朴素贝叶斯分类器
def bayesClassifier(word):
    #如果字典中有输入的单词，直接返回
    if identify([word]):
        return 0
    # 一步调整
    wanteds = identify(version1(word)) 
    if len(wanteds)>0:
        return '您要找的可能是：' + str(getMax(wanteds))
    # 两步调整
    wanteds = identify(version2(word))
    if len(wanteds)>0:
        return '您要找的可能是：' + str(getMax(wanteds))
    # 不再修正，直接提示这个单词不在当前的词典中
    else:    
        return word + ' 不在当前词典中!' 

# 调用该函数进行拼写矫正
def spelling_correct(x):
    correct = x
    y = re.findall(r"\w+",x)
    for word in y:
        hint = bayesClassifier(word)
        if hint != 0:
            print(hint)
            if hint[0] == '您':
                # op = ""
                # while op != 'y' or op != 'n':
                op = input('您是否要使用替换词项进行搜索？[y/n]：\n')
                if op == 'y':
                    # print(eval(hint[8:]))
                    if len(eval(hint[8:])) == 2:
                        # choice = ''
                        # while choice != '1' or choice != '2':
                        choice = input('请输入序号选择替换项：\n')
                        if choice == '1':
                            correct = correct.replace(word, eval(hint[8:])[0])
                        if choice == '2':
                            correct = correct.replace(word, eval(hint[8:])[1])
                        else:
                            print("错误序号！")
                    elif len(eval(hint[8:])) == 3:
                        # choice = ''
                        # while choice != '1' or choice != '2' or choice != '3':
                        choice = input('请输入序号选择替换项：\n')
                        if choice == '1':
                            correct = correct.replace(word, eval(hint[8:])[0])
                        if choice == '2':
                            correct = correct.replace(word, eval(hint[8:])[1])
                        if choice == '3':
                            correct = correct.replace(word, eval(hint[8:])[2])
                        else:
                            print("错误序号！")
                    elif len(eval(hint[8:])) == 1:
                        # print(word)
                        # print(eval(hint[8:])[0])
                        correct = correct.replace(word,eval(hint[8:])[0])
                        

                elif op =='n':
                    continue
    # print(correct)
    return correct



# query = "prider and prejudice "
# spelling_correct(query)