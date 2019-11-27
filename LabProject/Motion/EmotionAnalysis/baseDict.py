import pandas as pd
import jieba.posseg
import time
import copy
from sklearn.externals import joblib
from pyltp import Parser
from LabProject import settings

start = time.perf_counter()

# 部署时更改为服务器上的绝对路径
jieba.load_userdict(settings.BASE_DIR + '/Motion/EmotionAnalysis/dict.txt')
data = pd.read_csv(settings.BASE_DIR + '/Motion/EmotionAnalysis/try20.csv')
# data = data[int(len(data)*0.80):]
pos = (open(settings.BASE_DIR + "/Motion/EmotionAnalysis/pos.txt", 'r', encoding="utf-8")).readlines()
neg = (open(settings.BASE_DIR + "/Motion/EmotionAnalysis/neg.txt", 'r', encoding="utf-8")).readlines()
neu = (open(settings.BASE_DIR + "/Motion/EmotionAnalysis/neu.txt", 'r', encoding="utf-8")).readlines()
stop = (open(settings.BASE_DIR + "/Motion/EmotionAnalysis/stopword.txt", 'r', encoding="utf-8")).readlines()
output = (open(settings.BASE_DIR + "/Motion/EmotionAnalysis/output.txt", 'w', encoding="utf-8"))

'''
分词并标注，与情感词典匹配，与哪一个匹配成功则打对应标签
'''
p = []  # 词性

themes = []
sentiments = []
anls = []  # 极性

sentiment_words = []
theme_words = []
r_anls = []
tuple_pred = []
tuple_poss = []


def getPossegTuple(data):
    for i in data['sentiment_word']:
        if type(i) == str:
            sentiment_words.append(i.strip().split(';')[0:-1])
        else:
            sentiment_words.append([])
    for i in data['theme']:
        if type(i) == str:
            theme_words.append(i.strip().split(';')[0:-1])
        else:
            theme_words.append([])
    for i in data['sentiment_anls']:
        if type(i) == str:
            r_anls.append(i.strip().split(';')[0:-1])
        else:
            r_anls.append([])
    for i in range(len(sentiment_words)):
        gro = []
        j = 0
        for s in sentiment_words[i]:
            gro.append((theme_words[i][j], s, r_anls[i][j]))
            j += 1
        tuple_poss.append(gro)
    return tuple_poss


def segmentor(e):
    cons = jieba.posseg.cut(e)  # 句子被分词后
    words = []  # 句子分词
    p = []
    for con in cons:
        words.append(con.word)
        p.append(con.flag)  # 存储这个词以及它的词性，为找出特征词做准备
    return words, p


parser = Parser()  # 初始化实例
parser.load('./parser.model')  # 加载模型


# 依存语义分析
def parse(words, postags):
    arcs = parser.parse(words, postags)  # 句法分析
    # arc.head 表示依存弧的父节点词的索引，arc.relation 表示依存弧的关系。
    return arcs


def getTheme(arcs, words, p, senti):
    i = 0
    for arc in arcs:
        if arc.relation == 'SBV' or arc.relation == 'ATT':
            if words[arc.head - 1] == senti:
                if 'n' in p[i]:
                    return words[i]
        i += 1
    return 'NULL'


def getSentiment(e) -> list:  # 传入一句话
    cons, p = segmentor(e)
    arcs = parse(cons, p)
    csentiment = []  # 该句中的情感词
    canls = []
    ctheme = []
    gro = []
    for word in cons:
        # 判断这个词是不是情感词
        senti = ""
        tag = ""
        thl = ""
        word += '\n'
        if word not in stop:
            if word in pos:
                senti = word.rstrip('\n')
                thl = getTheme(arcs, cons, p, senti)
                tag = '1'
            if word in neg:
                senti = word.rstrip('\n')
                thl = getTheme(arcs, cons, p, senti)
                tag = '-1'
            if word in neu:
                senti = word.rstrip('\n')
                thl = getTheme(arcs, cons, p, senti)
                tag = '0'
        # 如果该词是情感词
        if (senti):
            gro.append((thl, senti, tag))
            csentiment.append(senti)  # 情感词列表
            canls.append(tag)  # 对应极性列表
            ctheme.append(thl)
    sentiments.append(csentiment)
    themes.append(ctheme)
    anls.append(canls)
    return gro


def getContents(data_new):
    # 遍历每句评论
    for e in data_new:
        gro = getSentiment(e)
        tuple_pred.append(gro)
    return tuple_pred


'''
计算F值
“主题词-情感词-情感值”为最小粒度逐条与标注数据进行比对，若三者均与答案相符，则判为情感匹配正确
情感词准确数tp，错误数fp，漏数fn1，多数fn2
准确率 P = (tp/(tp+fp+fn2))
召回率 R = (tp/(tp+fp+fn1))
F1 = (1+P*R)/(P+R)

每行的情感词放在列表里，自己提取词列表的与原列表匹配
若存在则将该词从两个列表删除，tp+1
删完后两列表皆有剩余，先判断长短，若相等则全为错判，fp+len
若原列表短则为多判，fp+len(原)，fn2+len(取-原)
若原列表长则为漏判，fp+len(取)，fn1+len(原-取)
'''


def countF():
    i = 0
    tp = 0
    fp = 0
    fn1 = 0
    fn2 = 0
    meg = ''
    for e in sentiment_words:
        # 现在是每一句的情感词了
        len1 = len(e)
        len2 = len(sentiments[i])  # 第i句评论
        j = 0
        for s in sentiments[i]:
            if s in e:
                index = e.index(s)
                theme_ = theme_words[i][index]
                anl_ = r_anls[i][index]
                theme = themes[i][j]
                anl = anls[i][j]
                if (theme_ == theme and anl_ == anl):
                    tp += 1
                    len1 -= 1
                    len2 -= 1
                    if i < 5:
                        meg += "第{}句：[{},{},{}]提取成功\n".format(i + 1, theme, s, anl)
                        # print(meg)
                        # output.writelines(meg+'\n')
                    del sentiment_words[i][index]
                    del theme_words[i][index]
                    del r_anls[i][index]
                else:
                    if i < 5:
                        meg += "第{}句标注数据为[{},{},{}]\n".format(i, theme_, e[index], anl_)
                        # print(meg)
                        # output.writelines(meg+'\n')
                        meg += "       你提取得[{},{},{}]\n".format(theme, s, anl)
                        # print(meg)
                        # output.writelines(meg+'\n')
            else:
                if i < 5:
                    meg += "第{}句你多提取了：[{},{},{}]\n".format(i + 1, themes[i][j], s, anls[i][j])
                    # print(meg)
                    # output.writelines(meg+'\n')
            j += 1
        if (len1 != 0 or len2 != 0):
            if (len1 == len2):
                fp += len2
            elif (len1 > len2):
                fp += len2
                fn1 = fn1 + len1 - len2
                k = 0
                if i < 5:
                    meg += "第{}句你未提取出：".format(i + 1)
                    # print(meg)
                    # output.writelines(meg+'\n')
                for sf in sentiment_words[i]:
                    if i < 5:
                        meg += "   [{},{},{}]\n".format(theme_words[i][k], sf, r_anls[i][k])
                        # print(meg)
                        # output.writelines(meg+'\n')
                    k += 1
            else:
                fp += len1
                fn2 = fn2 + len2 - len1
        else:
            if i < 5:
                meg += "第{}条全对\n".format(i + 1)
                # print(meg)
                # output.writelines(meg+'\n')
        i += 1
    meg1 = "\n<特征，情感词，极性>三元组的评价结果：\n判对{}个，判错{}个，多判{}个，漏判{}个\n".format(tp, fp, fn2, fn1)
    # output.writelines(meg+'\n')
    P = (tp / (tp + fp + fn2))
    R = (tp / (tp + fp + fn1))
    F1 = (2 * P * R) / (P + R)
    meg1 += "P = {:.2} , R = {:.2} , F1 = {:.2}\n\n".format(P, R, F1)
    meg = meg1 + meg
    print(meg)
    # output.writelines(meg+'\n')
    return meg


def countF_S():
    i = 0
    tp = 0
    fp = 0
    fn1 = 0
    fn2 = 0
    meg = ''
    sentiment_word = copy.deepcopy(sentiment_words)
    for e in sentiment_word:
        # 现在是每一句的情感词了
        len1 = len(e)
        len2 = len(sentiments[i])  # 第i句评论
        j = 0

        for s in sentiments[i]:
            if s in e:
                index = e.index(s)
                tp += 1
                len1 -= 1
                len2 -= 1
                del sentiment_word[i][index]
            j += 1
        if (len1 != 0 or len2 != 0):
            if (len1 == len2):
                fp += len2
            elif (len1 > len2):
                fp += len2
                fn1 = fn1 + len1 - len2
            else:
                fp += len1
                fn2 = fn2 + len2 - len1
        i += 1
    meg1 = "\n只判断情感词的评价结果：\n判对{}个，判错{}个，多判{}个，漏判{}个\n".format(tp, fp, fn2, fn1)
    # output.writelines(meg+'\n')
    P = (tp / (tp + fp + fn2))
    R = (tp / (tp + fp + fn1))
    F1 = (2 * P * R) / (P + R)
    meg1 += "P = {:.2} , R = {:.2} , F1 = {:.2}\n".format(P, R, F1)
    meg = meg1 + meg
    print(meg)
    # output.writelines(meg+'\n')
    return meg


def main():
    getPossegTuple(data)
    getContents(data['content'])
    meg = countF_S()
    meg += countF()
    f = open('VariableDict ', 'wb')
    joblib.dump([tuple_pred, tuple_poss, meg], f)
    parser.release()  # 释放模型


if __name__ == "__main__":
    main()

end = time.perf_counter()
meg = '\nbaseDict Running time: %.12f Seconds' % (end - start)
print(meg)
# output.writelines(meg)
