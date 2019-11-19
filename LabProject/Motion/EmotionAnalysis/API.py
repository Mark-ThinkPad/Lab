import jieba.posseg
from sklearn.externals import joblib
from sklearn_crfsuite import metrics
from Motion.EmotionAnalysis import CRF
from Motion.EmotionAnalysis import baseDict
import random
import csv
import pandas as pd

# 需要延时加载的部分, 前端需要做loading动画
jieba.load_userdict('./EmotionAnalysis/dict.txt')
data = pd.read_csv('train.csv')
crf = joblib.load('train_model')
X_test, y_test, megCRF, f1, result, y_pred = joblib.load(open('variableCRF', 'rb'))
tuple_pred, tuple_poss, megDict = joblib.load(open('VariableDict', 'rb'))


def getFile():
    pass


def getTuple(content):
    i = jieba.posseg.cut(content)  # 词性标注
    s = []
    for p, q in i:  # p是词，q是词性
        s.append((p, q, ''))  # [(词, 词性)]
    # print("s:{}".format(s))
    X_test = [CRF.sent2features(s)]
    pred = crf.predict(X_test)
    # print("pred:{}".format(pred))
    gro = CRF.getPred(pred, [s])
    return gro


# 手动输入一句话，输出预测结果
def getContent(words: str) -> str:
    res = words + '\n\n基于情感词典的结果：\n'
    analysis = baseDict.getSentiment(words)
    res += analysis + '\n\n基于条件随机场的结果：\n'
    return res


# 返回模型F1值
def getCRFModel():
    pass


def getDictModel():
    pass
