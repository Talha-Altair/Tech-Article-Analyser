import nltk
from nltk import tokenize
from operator import itemgetter
import math

from newspaper import Article
 
url = "https://www.aplustopper.com/article-on-women-empowerment/"

article = Article(url)
article.download()
article.parse()

doc = article.text

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english'))

total_words = doc.split()
total_word_length = len(total_words)

total_sentences = tokenize.sent_tokenize(doc)
total_sent_len = len(total_sentences)

tf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in tf_score:
            tf_score[each_word] += 1
        else:
            tf_score[each_word] = 1

def check_sent(word, sentences): 
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

idf_score = {}
for each_word in total_words:
    each_word = each_word.replace('.','')
    if each_word not in stop_words:
        if each_word in idf_score:
            idf_score[each_word] = check_sent(each_word, total_sentences)
        else:
            idf_score[each_word] = 1

tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}

def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result

final=get_top_n(tf_idf_score, 10)


if 'technology' in final:
    print("yes,its a Tech related Article")
else:
    print("nah,its not a tech related article")

