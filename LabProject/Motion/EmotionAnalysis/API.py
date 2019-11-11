import jieba.posseg
from sklearn.externals import joblib
from sklearn_crfsuite import metrics
import CRF
import baseDict
import random
import csv
import pandas as pd

# 需要延时加载的部分, 前端需要做loading动画
jieba.load_userdict('dict.txt')
data = pd.read_csv('train.csv')
crf = joblib.load('train_model')
X_test, y_test, megCRF, f1, result, y_pred = joblib.load(open('variableCRF', 'rb'))
tuple_pred, tuple_poss, megDict = joblib.load(open('VariableDict', 'rb'))

def getFile():
    pass

def getTuple(content):
    pass

#手动输入一句话，输出预测结果
def getContent():
    pass

#返回模型F1值
def getCRFModel():
    pass

def getDictModel():
    pass