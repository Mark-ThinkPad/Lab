# 情感分析Web版

## 开发环境

- `Python 3.8.0`

## 系统环境

- `Arch Linux`

## 前端方案

- `Bootstrap4`

## 后端方案

-  `Python Django` v2.2.6

## 需要安装的Python第三方库

- **一定请先安装`pyltp`库**, `pyltp`库安装时的翻车几率较大
- 首先实践成功的安装方式为`Python 3.6` + `pip安装本地的pyltp-0.2.1-cp36-cp36m-win_amd64.whl`(项目文件里附带), 系统环境为Windows7/10
- 目前在`Python 3.6` + `Ubuntu Server 18.10` 直接用 `pip install pyltp` 安装成功, 注意要提前安装以下几个包: `gcc`, `g++`, `cmake`, `python3-dev`, 同时注意服务器内存是否够用, 否则当内存不足时, gcc会停止编译并报错提示内存不足, 项目文件中附带了编译完成后自动生成的whl文件(`pyltp-0.2.1-cp36-cp36m-linux_x86_64.whl`), 方便后人使用
- 同时在`Arch Linux` + `Python 3.7/3.8` 上安装成功(gcc v9.2.0), 解决方法见: [pyltp-issues#172](https://github.com/HIT-SCIR/pyltp/issues/172) (一个强制转换空指针的解决方案)
- 其他使用的第三方库见 [requirement.txt](./requirement.txt), 可使用pip一键安装

## 开发小记

- 由于在 `Python3.8` 中 `time.clock()` 方法被正式移除, 将此方法替换为 `time.perf_counter()`
- 部分文件读取路径由相对路径改为绝对路径, 包括`CRF.py`, `baseDict.py` 和 `API.py`
```python
# 部署时改为服务器的绝对路径
# CRF.py 和 base.py 中共有的部分
jieba.load_userdict('dict.txt')
data = pd.read_csv('train.csv')
```

```python
# baseDict.py
pos = (open("pos.txt", 'r', encoding="utf-8")).readlines()
neg = (open("neg.txt", 'r', encoding="utf-8")).readlines()
neu = (open("neu.txt", 'r', encoding="utf-8")).readlines()
stop = (open("stopword.txt", 'r', encoding="utf-8")).readlines()
output = (open("output.txt", 'w', encoding="utf-8"))
```
- `API.py` 中也有多处被修改为绝对路径
```python
# API.py
jieba.load_userdict('dict.txt')
data = pd.read_csv('train.csv')
crf = joblib.load('train_model')
X_test, y_test, megCRF, f1, result, y_pred = joblib.load(open('variableCRF', 'rb'))
tuple_pred, tuple_poss, megDict = joblib.load(open('VariableDict', 'rb'))
```
- 新增本地缓存机制, 目的是在某个单独回话中保持情绪分析类的实体对象的存在, 而且多用户访问时不冲突
```python
# settings.py
# Cache in File System
# https://docs.djangoproject.com/zh-hans/2.2/topics/cache/
# 部署后修改绝对路径
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/home/mark/GitHub/Lab/cache',
    }
}
```

## To-Do List

- input text 输入判空
- input text 回车触发按钮
- input file 输入判空(点击上传按钮时)
- 五个按钮五个ajax
- 对应的五个后端api
