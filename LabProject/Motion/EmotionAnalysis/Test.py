import pandas as pd 
import jieba.posseg
import sklearn_crfsuite
from sklearn_crfsuite import metrics
#from sklearn.externals import joblib
import time
import copy
from pyltp import Parser

jieba.load_userdict('dict.txt')
data = pd.read_csv('train.csv')

start =time.clock()

themes = []
sentiments = []
anls = [] #极性

sentiment_words = []
theme_words = []
tags = []
parser = Parser() # 初始化实例
#依存语义分析
def parse(words, postags):
    parser.load('/parser.model')  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    #arc.head 表示依存弧的父节点词的索引，arc.relation 表示依存弧的关系。
    return arcs

#特征提取
def word2features(sent,i,arcs):
    word = sent[i][0]
    postag = sent[i][1]
    arc = arcs[i]
    features = {
        'bias': 1.0,
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
        'arc.relation':arc.relation,
        'arc.headpostag':sent[arc.head][1]
        }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            #'-1:word':word1,
            #'-1:word[:2]':word1 + word,
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2]
        })
    else:
        features['BOS'] = True #BOS开始标志
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1] #后一个词的词性
        features.update({
            #'+1:word':word1,
            #'+1:word[:2]':word + word1,
            '+1:postag': postag1, 
            '+1:postag[:2]': postag1[:2]
        })
    else:
        features['EOS'] = True  #EOS结束标志
    return features

def sent2features(sent):
    w=[]
    p=[]
    for s in sent:
        w.append(s[0])
        p.append(s[1])
    arcs = parse(w,p)
    return [word2features(sent, i, arcs) for i in range(len(sent))]

def constructTextBylabeling(data,theme_words,sentiment_words,tags):
    train = []
    for con,thl,seml,tag in zip(data['content'],theme_words,sentiment_words,tags):
        i = jieba.posseg.cut(con) #词性标注
        res = []
        tmp = [] 
        for p,q in i: # p是词，q是词性
            tmp.append((p,q)) #[(词, 词性)]
        for each in tmp:
            w = each[0]
            p = each[1]  # w是词，p是词性
            if w in thl:
                res.append((w,p,'t'))
            elif w in seml:
                t = tag[seml.index(w)]
                if t == '1':
                    res.append((w,p,'p'))
                elif t == '-1':
                    res.append((w,p,'n'))
                else:
                    res.append((w,p,'m'))
            else:
                res.append((w,p,'null'))
        train.append(res)
    return train  

def main():
    data_ = constructTextBylabeling(data,theme_words,sentiment_words,tags)
    X_train = [sent2features(s) for s in data_]


if __name__ == '__main__':
    main()


                   


end = time.clock()
print('\nCRF Running time: %s Seconds'%(end-start))