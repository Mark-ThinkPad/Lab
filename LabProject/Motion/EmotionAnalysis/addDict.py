import csv
#情感词典扩建
posFile = open("pos.txt","r",encoding = "utf-8")
negFile = open("neg.txt",'r',encoding = "utf-8")
neuFile = open("neu.txt",'r',encoding = "utf-8")
posDic = []
negDic = []
neuDic = []

train = csv.reader(open("train.csv", encoding = "utf-8"))
str = posFile.readlines()

for w in str:
    posDic.append(w.rstrip("\n"))

str = negFile.readlines()
for w in str:
    negDic.append(w.rstrip("\n"))
    
str = neuFile.readlines()
for w in str:
    neuDic.append(w.rstrip("\n"))

for row in train:
    sentiList = row[3].rstrip('')
    tagList = row[4]
    senti = sentiList.split(";")
    tag = tagList.split(";")
    i = 0
    for w in senti:
        if(tag[i] == '1'):
            if w not in posDic :
                posDic.append(w)
                w = w + '\n'
                posFile.writelines(w)
        if(tag[i] == '-1'):
            if w not in negDic :
                negDic.append(w)
                w = w + '\n'
                negFile.writelines(w)
        if(tag[i] == '0'):
            if w not in neuDic :
                neuDic.append(w)
                w = w + '\n'
                neuFile.writelines(w)
        i = i + 1