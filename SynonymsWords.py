import json
import jsonlines
import utils

synonyms_words_file = 'synonymslist'

def get_synonyms_words(query):
    if_has_synonyms = 0
    wordlist = query.split(' ')

    synonymslist = utils.get_from_file_L(synonyms_words_file)
    app_wordlist=[]

    for word in wordlist:
        # print(word)
        for synonymsword in synonymslist:
            # print(synonymsword["word"])
            # synonymsword_json = json.loads(synonymsword)
            if(synonymsword["word"] == word):
                synonyms = synonymsword["synonyms"]
                for word_t in synonyms:
                    # print("发现同义词： " + word_t)
                    word_t = word_t.lower()
                    index, result = utils.loadIndex(word_t)
                    if index is not None and word_t != word:
                        print("发现同义词： " + word_t)
                        query += ' OR ' + word_t
                        if_has_synonyms = 1
                        # app_wordlist.append(word_t)
    if if_has_synonyms == 0:
        print("未发现同义词！")
    print("同义词搜索结束！\n")

    # for word in app_wordlist:
    #     wordlist += ' ' + word
    return query
