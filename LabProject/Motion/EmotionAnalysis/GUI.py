import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import filedialog
import jieba.posseg
from sklearn.externals import joblib
from sklearn_crfsuite import metrics
import CRF
import baseDict
import random
import csv
import pandas as pd

jieba.load_userdict('dict.txt')
data = pd.read_csv('train.csv')
crf = joblib.load("train_model")
X_test, y_test, megCRF, f1, result, y_pred = joblib.load(open('variableCRF', 'rb'))
tuple_pred, tuple_poss, megDict = joblib.load(open('VariableDict', 'rb'))


def getFile():
    file_path = tk.filedialog.askopenfilename()
    e_file.delete(0, 'end')
    e_file.insert('insert', file_path)  # 'insert'——在鼠标焦点处插入输入内容，'end'——在末尾输入内容
    out.delete('1.0', 'end')
    if file_path[-4:] != ".csv":
        out.insert('end', '文件格式错误，请选择.csv文件')
        return
    data = pd.read_csv(file_path)
    x = random.randint(0, 20000)
    outFile = "result{}.csv".format(x)
    f = open(outFile, encoding='utf-8', mode='w', newline='', errors='ignore')
    if "content" not in list(data):
        out.insert('end', '文件内容错误，请选择列名为“content”的csv文件')
        return
    writer = csv.writer(f)
    writer.writerow(["content", "theme", "sentiment", "anls"])  # 写列名
    out.insert('end', "文件已写入{}\n\n".format(outFile))
    for content in data["content"]:
        gro = getTuple(content)
        theme = ''
        sentiment = ''
        anls = ''
        for g in gro:
            theme += g[0] + ';'
            sentiment += g[1] + ';'
            anls += g[2] + ';'
        row = [content, theme, sentiment, anls]
        print(row)
        writer.writerow(row)
        out.insert('end', content + '\n')
        out.insert('end', 'theme:     ' + theme + '\n')
        out.insert('end', 'sentiment: ' + sentiment + '\n')
        out.insert('end', 'anls:      ' + anls + '\n\n')
    out.insert('end', "\n\n-----------------------已写完-----------------------\n\n")


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
def getContent():
    content = e_in.get()
    out.delete('1.0', 'end')
    out.insert('end', content)
    out.insert('end', '\n')
    out.insert('end', "\n基于情感词典的结果：\n")
    result = baseDict.getSentiment(content)
    out.insert('end', result)
    out.insert('end', "\n\n基于条件随机场的结果：\n")
    gro = getTuple(content)
    out.insert('end', gro)


# 返回模型F1值
def getCRFModel():
    out.delete('1.0', 'end')
    out.insert('end', "基于条件随机场的模型:\n")
    out.insert('end', f1)
    out.insert('end', megCRF)
    out.insert('end', '\n\n')
    out.insert('end', result)


def getDictModel():
    out.delete('1.0', 'end')
    out.insert('end', "基于情感词典的模型:\n")
    out.insert('end', megDict)


# 随机获取一句评论并输出预测及标注
def getAtrain():
    data_ = []
    for i in data['content']:
        data_.append(i)
    con = data_[int(len(data_) * 0.8):]
    x = random.randint(0, len(con))
    print(len(con))
    print(x)
    out.delete('1.0', 'end')
    out.insert('end', '抽取出第{}句:\n'.format(x + 1))
    out.insert('end', con[x])
    # out.insert('end', '\n\n标注<主题，情感，极性>三元组：\n')
    # DictPoss = tuple_poss[int(len(data) * 0.8):]
    # out.insert('end', DictPoss[x])
    # out.insert('end', '\n\n情感词典预测<主题，情感，极性>三元组：\n')
    # DictPred = tuple_pred[int(len(data) * 0.8):]
    # out.insert('end', DictPred[x])
    out.insert('end', '\n\n条件随机场预测<主题，情感，极性>三元组：\n')
    gro = getTuple(con[x])
    out.insert('end', gro)


if __name__ == '__main__':
    window = tk.Tk()
    window.title('文本情感分析系统')
    window.resizable(0, 0)
    # 将label标签的内容设置为字符类型，用var来接收函数的传出内容用以显示在标签上
    # var = tk.StringVar()
    # Label控件, 显示Input字样, 不是输入框, 相当于HTML中的<labek>
    label1 = tk.Label(window, width=5, text="Input", font=('Arial', 16))
    label1.grid(row=0, column=0)
    # Entry, 文本输入
    e_in = tk.Entry(window, width=40, bg='white', font=('Arial', 16))
    e_in.grid(row=0, column=1)
    e_file = tk.Entry(window, width=45, bg='white', font=('Arial', 16))
    e_file.grid(row=1, columnspan=2)
    # Text控件, 显示文本
    out = tk.Text(window, width=52, height=30, bg='white', font=(16))
    out.grid(rowspan=30, columnspan=2)

    # Button控件, command参数指定需要执行的函数名
    b1 = tk.Button(window, text='确认', width=8, command=getContent, font=(16))
    b1.grid(row=0, column=2)
    b0 = tk.Button(window, text='选择文件', width=8, command=getFile, font=(16))
    b0.grid(row=1, column=2)
    b2 = tk.Button(window, text='查看CRF模型准确率', width=18, command=getCRFModel, font=(16))
    b2.grid(row=3, column=2)
    b3 = tk.Button(window, text='查看情感词典准确率', width=18, command=getDictModel, font=(16))
    b3.grid(row=4, column=2)
    b4 = tk.Button(window, text='随机抽取一句评论', width=18, command=getAtrain, font=(16))
    b4.grid(row=5, column=2)

    window.mainloop()
