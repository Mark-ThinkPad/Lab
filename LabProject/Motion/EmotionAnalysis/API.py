from sklearn.externals import joblib
from Motion.EmotionAnalysis import CRF
from Motion.EmotionAnalysis import baseDict
import pandas as pd
import jieba.posseg
import random
import csv


class API:
    def __init__(self):
        # 需要延时加载的部分, 前端需要做loading动画
        # 部署时修改为服务器上的相对路径
        jieba.load_userdict('/home/mark/GitHub/Lab/LabProject/Motion/EmotionAnalysis/dict.txt')
        self.data = pd.read_csv('/home/mark/GitHub/Lab/LabProject/Motion/EmotionAnalysis/train.csv')
        self.crf = joblib.load('/home/mark/GitHub/Lab/LabProject/Motion/EmotionAnalysis/train_model')
        self.X_test, self.y_test, self.megCRF, self.f1, self.result, self.y_pred = joblib.load(
            open('/home/mark/GitHub/Lab/LabProject/Motion/EmotionAnalysis/variableCRF', 'rb'))
        self.tuple_pred, self.tuple_poss, self.megDict = joblib.load(
            open('/home/mark/GitHub/Lab/LabProject/Motion/EmotionAnalysis/VariableDict', 'rb'))

    def getFile(self, csvFile) -> str:
        filename = csvFile.name
        if filename[-4:] != '.csv':
            return '文件格式错误，请选择.csv文件'

    def getTuple(self, content) -> list:
        i = jieba.posseg.cut(content)  # 词性标注
        s = []
        for p, q in i:  # p是词，q是词性
            s.append((p, q, ''))  # [(词, 词性)]
        # print("s:{}".format(s))
        X_test = [CRF.sent2features(s)]
        pred = self.crf.predict(X_test)
        # print("pred:{}".format(pred))
        gro = CRF.getPred(pred, [s])
        return gro

    # 手动输入一句话，输出预测结果
    def getContent(self, words: str) -> str:
        res = words + '\n\n基于情感词典的结果：\n'
        analysis: list = baseDict.getSentiment(words)
        res += str(analysis) + '\n\n基于条件随机场的结果：\n'
        gro: list = self.getTuple(words)
        res += str(gro)
        return res

    # 返回模型F1值
    def getCRFModel(self) -> str:
        res = '基于条件随机场的模型:\n' + str(self.f1) + self.megCRF + '\n\n' + self.result
        return res

    def getDictModel(self) -> str:
        res = '基于情感词典的模型:\n' + self.megDict
        return res

    # 随机获取一句评论并输出预测及标注
    def getAtrain(self) -> str:
        data_ = []
        for i in self.data['content']:
            data_.append(i)
        con = data_[int(len(data_) * 0.8):]
        x = random.randint(0, len(con))
        print(len(con))
        print(x)
        res = '抽取出第{}句:\n'.format(x + 1) + con[x]
        try:
            DictPoss = self.tuple_poss[int(len(self.data) * 0.8):]
            res += '\n\n标注<主题，情感，极性>三元组：\n' + DictPoss[x]
        except IndexError:
            error_again = True
        try:
            DictPred = self.tuple_pred[int(len(self.data) * 0.8):]
            res += '\n\n情感词典预测<主题，情感，极性>三元组：\n' + DictPred[x]
        except IndexError:
            error_again = True
        gro: list = self.getTuple(con[x])
        res += '\n\n条件随机场预测<主题，情感，极性>三元组：\n' + str(gro)
        return res


if __name__ == '__main__':
    pass
