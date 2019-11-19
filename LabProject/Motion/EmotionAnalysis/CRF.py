import pandas as pd
import jieba.posseg
import sklearn_crfsuite
from sklearn_crfsuite import metrics
from sklearn.externals import joblib
import time
import copy


# 部署时改为服务器的绝对路径
jieba.load_userdict('/home/mark/GitHub/Lab/LabProject/Motion/EmotionAnalysis/dict.txt')
data = pd.read_csv('/home/mark/GitHub/Lab/LabProject/Motion/EmotionAnalysis/train.csv')

start = time.perf_counter()

themes = []
sentiments = []
anls = []  # 极性

sentiment_words = []
theme_words = []
tags = []


def getPosseg():
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
            tags.append(i.strip().split(';')[0:-1])
        else:
            tags.append([])


def constructTextBylabeling(data, theme_words, sentiment_words, tags):
    train = []
    for con, thl, seml, tag in zip(data['content'], theme_words, sentiment_words, tags):
        i = jieba.posseg.cut(con)  # 词性标注
        res = []
        tmp = []
        for p, q in i:  # p是词，q是词性
            tmp.append((p, q))  # [(词, 词性)]
        for each in tmp:
            w = each[0]
            p = each[1]  # w是词，p是词性
            if w in thl:
                res.append((w, p, 't'))
            elif w in seml:
                t = tag[seml.index(w)]
                if t == '1':
                    res.append((w, p, 'p'))
                elif t == '-1':
                    res.append((w, p, 'n'))
                else:
                    res.append((w, p, 'm'))
            else:
                res.append((w, p, 'null'))
        train.append(res)
    return train


# 特征提取
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = {
        'bias': 1.0,
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2]}
    if i > 0:
        #        word1 = sent[i-1][0]
        postag1 = sent[i - 1][1]
        features.update({
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2]
        })
    else:
        features['BOS'] = True  # BOS开始标志

    if i < len(sent) - 1:
        #        word1 = sent[i+1][0]
        postag1 = sent[i + 1][1]  # 后一个词的词性
        features.update({
            '+1:postag': postag1,
            '-1:postag[:2]': postag1[:2]
        })
    else:
        features['EOS'] = True  # EOS结束标志
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, tag, label in sent]


def getTheme(i, j, l, con):
    k = j - 1
    while (k > j - 6 and k >= 0):
        if l[k] == 't':
            return con[i][k][0]
        elif l[k] != 'null':
            return 'NULL'
        else:
            k -= 1
    '''k = j+1
    while(k < j+4 and k < len(con[i])):
        if l[k] == 't':
            return con[i][k][0]
        else:
            k +=1'''
    return 'NULL'


def getPred(y_pred, con):
    gro = []
    i = 0
    for l in y_pred:
        pred_th = []
        pred_se = []
        pred_tag = []
        j = 0
        for p in l:
            if 'n' == p:
                pred_se.append(con[i][j][0])
                pred_tag.append('-1')
                th = getTheme(i, j, l, con)
                pred_th.append(th)
                gro.append([th, con[i][j][0], '-1'])
            elif 'p' == p:
                pred_se.append(con[i][j][0])
                pred_tag.append('1')
                th = getTheme(i, j, l, con)
                pred_th.append(th)
                gro.append([th, con[i][j][0], '1'])
            elif 'm' == p:
                pred_se.append(con[i][j][0])
                pred_tag.append('0')
                th = getTheme(i, j, l, con)
                pred_th.append(th)
                gro.append([th, con[i][j][0], '0'])
            j += 1
        sentiments.append(pred_se)
        themes.append(pred_th)
        anls.append(pred_tag)
        i += 1
    return gro


def countF():
    i = 0
    tp = 0
    fp = 0
    fn1 = 0
    fn2 = 0
    meg = ''
    sentiment_word = sentiment_words[int(len(data) * 0.8):]
    theme_word = theme_words[int(len(data) * 0.8):]
    tag = tags[int(len(data) * 0.8):]
    for e in sentiment_word:
        # 现在是每一句的情感词了
        len1 = len(e)
        len2 = len(sentiments[i])  # 第i句评论
        j = 0
        for s in sentiments[i]:
            if s in e:
                index = e.index(s)
                theme_ = theme_word[i][index]
                anl_ = tag[i][index]
                theme = themes[i][j]
                anl = anls[i][j]
                if (theme_ == theme and anl_ == anl):
                    tp += 1
                    len1 -= 1
                    len2 -= 1
                    if i < 5:
                        meg += "\n第{}句：[{},{},{}]提取成功".format(i + 1, theme, s, anl)
                        # print(meg)
                        # output.writelines(meg+'\n')
                    del sentiment_word[i][index]
                    del theme_word[i][index]
                    del tag[i][index]
                else:
                    if i < 5:
                        meg += "\n第{}句标注数据为[{},{},{}]".format(i, theme_, e[index], anl_)
                        # print(meg)
                        # output.writelines(meg+'\n')
                        meg += "\n       你提取得[{},{},{}]".format(theme, s, anl)
                        # print(meg)
                        # output.writelines(meg+'\n')
            else:
                if i < 5:
                    meg += "\n第{}句你多提取了：[{},{},{}]".format(i + 1, themes[i][j], s, anls[i][j])
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
                for sf in sentiment_word[i]:
                    if i < 5:
                        meg += "   [{},{},{},]".format(theme_word[i][k], sf, tag[i][k])
                        # print(meg)
                        # output.writelines(meg+'\n')
                    k += 1
            else:
                fp += len1
                fn2 = fn2 + len2 - len1
        else:
            if i < 5:
                meg += "第{}条全对".format(i + 1)
                # print(meg)
                # output.writelines(meg+'\n')
        i += 1
    meg1 = "\n<特征，情感词，极性>三元组的评价结果：\n判对{}个，判错{}个，多判{}个，漏判{}个".format(tp, fp, fn2, fn1)
    P = (tp / (tp + fp + fn2))
    R = (tp / (tp + fp + fn1))
    F1 = (2 * P * R) / (P + R)
    meg1 += "\nP = {:.2} , R = {:.2} , F1 = {:.2}\n".format(P, R, F1)
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
    sentiment_word = copy.deepcopy(sentiment_words[int(len(data) * 0.8):])
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
    meg += "\n只判断情感词的评价结果：\n判对{}个，判错{}个，多判{}个，漏判{}个".format(tp, fp, fn2, fn1)
    P = (tp / (tp + fp + fn2))
    R = (tp / (tp + fp + fn1))
    F1 = (2 * P * R) / (P + R)
    meg += "\nP = {:.2} , R = {:.2} , F1 = {:.2}\n".format(P, R, F1)
    print(meg)
    # output.writelines(meg+'\n')
    return meg


def getCRFresult(crf, X_test, y_test):
    labels = list(crf.classes_)  # A list of class labels.
    labels.remove('null')
    y_pred = crf.predict(X_test)
    f1 = metrics.flat_f1_score(y_test, y_pred,
                               average='weighted', labels=labels)
    result = metrics.flat_classification_report(
        y_test, y_pred, labels=labels, digits=3)
    return f1, result, y_pred


def main():
    getPosseg()
    data_ = constructTextBylabeling(data, theme_words, sentiment_words, tags)
    train = data_[:int(len(data_) * 0.80)]  # 75%作为训练，剩下25%测试
    test = data_[int(len(data_) * 0.80):]
    X_train = [sent2features(s) for s in train]
    y_train = [sent2labels(s) for s in train]
    X_test = [sent2features(s) for s in test]
    y_test = [sent2labels(s) for s in test]
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',  # Gradient descent using the L-BFGS method
        c1=0.1,  # The coefficient for L1 regularization.
        c2=0.1,
        max_iterations=100,  # The maximum number of iterations for optimization algorithms.
        all_possible_transitions=True  # When True, CRFsuite generates transition features
        # that associate all of possible label pairs.
    )
    crf.fit(X_train, y_train)
    f1, result, y_pred = getCRFresult(crf, X_test, y_test)
    print('ornginal:')
    print(f1)
    print(result)
    # 评估
    getPred(y_pred, test)
    joblib.dump(crf, 'train_model')

    f = open('variableCRF', 'wb')
    meg = countF_S()
    meg += countF()
    joblib.dump([X_test, y_test, meg, f1, result, y_pred], f)

    return X_test, y_test, meg


if __name__ == '__main__':
    main()

end = time.perf_counter()
print('\nCRF Running time: %.12f Seconds' % (end - start))
