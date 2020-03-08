from sklearn.externals import joblib
from EmotionAnalysis import CRF
from EmotionAnalysis import baseDict
from EmotionAnalysis.paths import EA_DIR, P_DIR
import pandas as pd
import jieba.posseg
import random
import csv


class API:
    def __init__(self):
        # 需要延时加载的部分, 前端需要做loading动画
        # 部署时修改为服务器上的相对路径
        jieba.load_userdict(EA_DIR + '/dict.txt')
        self.data = pd.read_csv(EA_DIR + '/train.csv')
        self.crf = joblib.load(EA_DIR + '/train_model')
        self.X_test, self.y_test, self.megCRF, self.f1, self.result, self.y_pred = joblib.load(
            open(EA_DIR + '/variableCRF', 'rb'))
        self.tuple_pred, self.tuple_poss, self.megDict = joblib.load(
            open(EA_DIR + '/VariableDict', 'rb'))

    def getFile(self, csvFile) -> str:
        filename = csvFile
        if filename[-4:] != '.csv':
            return '文件格式错误，请选择.csv文件'
        self.data = pd.read_csv(csvFile)
        x = random.randint(0, 100000)
        outFileName = 'result{}.csv'.format(x)
        outFilePath = P_DIR + '/media/temp/' + outFileName
        res = ''
        with open(outFilePath, encoding='utf-8', mode='w', newline='', errors='ignore') as f:
            if 'content' not in list(self.data):
                return '文件内容错误，请选择列名为"content"的csv文件'
            writer = csv.writer(f)
            writer.writerow(['content', 'theme', 'sentiment', 'anls'])  # 写列名
            res = '文件已写入{}\n\n'.format(outFileName)
            for content in self.data['content']:
                gro = self.getTuple(content)
                theme = ''
                sentiment = ''
                anls = ''
                for g in gro:
                    theme += g[0] + ';'
                    sentiment += g[1] + ';'
                    anls += g[2] + ';'
                row = [content, theme, sentiment, anls]
                # print(row)
                writer.writerow(row)
                res += content + '\n'
                res += 'theme:     ' + theme + '\n'
                res += 'sentiment: ' + sentiment + '\n'
                res += 'anls:      ' + anls + '\n\n'
            res += '\n\n-----------------------已写完-----------------------\n\n'
        return res

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
        res = words + '\n\n基于情感词典的命中结果：\n'
        analysis: list = baseDict.getSentiment(words)
        temp1 = ','.join([f'"{a[1]}"' for a in analysis])
        res += temp1 + '\n\n基于条件随机场的命中结果：\n'
        gro: list = self.getTuple(words)
        temp2 = ','.join([f'"{g[1]}"' for g in gro])
        res += str(temp2)
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
