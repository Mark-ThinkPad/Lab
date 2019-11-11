from pyltp import Parser
import jieba.posseg
import pandas as pd
import time
start =time.clock()
data = pd.read_csv('try.csv')    
contents = data['content']
sentiment_words = []
for i in data['sentiment_word']:
    if type(i) == str:
        sentiment_words.append(i.strip().split(';')[0:-1])
senti = []
for s in sentiment_words:
    for ss in s:
        senti.append(ss)
#依存语义分析
def parse(words, postags):
    parser = Parser() # 初始化实例
    parser.load('D:\\Users\\xz\\Desktop\\ltp-data-v3.3.1\\ltp_data\\parser.model')  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    #arc.head 表示依存弧的父节点词的索引，arc.relation 表示依存弧的关系。
    i = 1
    for arc in arcs:
        #print(str(i) + words[i-1])
        #print("\t".join("%d:%s" % (arc.head, arc.relation) ))
        i += 1
    parser.release()  # 释放模型
    return arcs

def getTuple(arcs,words,p):
    i = 0
    for arc in arcs:
        if words[i] in senti:
            #print(arc.relation + ':'+words[i]+p[i] +'--'+words[arc.head-1]+p[arc.head-1])
            if arc.relation=='VOB':
                if words[i] in senti or words[arc.head-1] in senti:
                    print('VOB:{}--{}'.format(i, arc.head))
                    print(words[i]+'--'+words[arc.head-1])
                    print()
        i += 1
    print('*'*30)
    i = 0
    for arc in arcs:
        if words[arc.head-1] in senti:
            #print(arc.relation + ':'+words[i]+p[i] +'--'+words[arc.head-1]+p[arc.head-1])
            if arc.relation=='VOB':
                if words[i] in senti or words[arc.head-1] in senti:
                    print('VOB:{}--{}'.format(i, arc.head))
                    print(words[i]+'--'+words[arc.head-1])
                    print()
        '''
        if arc.relation=='SBV':
            if words[arc.head-1] in senti:
                print('SBV:{}--{}'.format(i, arc.head))
                print(words[i]+'--'+words[arc.head-1])
                print()'''
            
        '''
        if arc.relation=='ATT':
            if words[i] in senti or words[arc.head-1] in senti:
                print('ATT:{}--{}'.format(i, arc.head))
                print(words[i]+'--'+words[arc.head-1])
                print()
        '''
        i += 1

def segmentor(e):
    cons = jieba.posseg.cut(e) #句子被分词后
    words = [] #句子分词
    p = []
    for con in cons: 
        words.append(con.word)
        p.append(con.flag) #存储这个词以及它的词性，为找出特征词做准备
    return words,p

x = 1
for e in contents:#words为分词后的一句话
    words,p = segmentor(e)
    arcs = parse(words,p)
    #print('###############第{}句###############'.format(x))
    getTuple(arcs,words,p)
    x += 1
    
    
end = time.clock()
meg = '\nbaseDict Running time: %s Seconds'%(end-start)
print(meg)