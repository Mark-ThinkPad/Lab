# Emotion Analyze on Web Version 2 with Flask

## development environment

- `Python 3.8.2`

## system environment

- `Arch Linux`

## web framework

- `Bootstrap 4`

## website backend

-  `Python Flask` v1.1.1

## precautions

- **一定请先安装`pyltp`库**, `pyltp`库安装时的翻车几率较大
- 首先实践成功的安装方式为`Python 3.6` + `pip安装本地的pyltp-0.2.1-cp36-cp36m-win_amd64.whl`(项目文件里附带), 系统环境为Windows7/10
- 目前在`Python 3.6` + `Ubuntu Server 18.10` 直接用 `pip install pyltp` 安装成功, 注意要提前安装以下几个包: `gcc`, `g++`, `cmake`, `python3-dev`, 同时注意服务器内存是否够用, 否则当内存不足时, gcc会停止编译并报错提示内存不足, 项目文件中附带了编译完成后自动生成的whl文件(`pyltp-0.2.1-cp36-cp36m-linux_x86_64.whl`), 方便后人使用
- 同时在`Arch Linux` + `Python 3.7/3.8` 上安装成功(gcc v9.2.0), 解决方法见: [pyltp-issues#172](https://github.com/HIT-SCIR/pyltp/issues/172) (一个强制转换空指针的解决方案)
- 其他使用的第三方库见 [requirements.txt](./requirements.txt), 可使用pip一键安装

## development notes

- 上个版本使用的是Django框架开发, 在后期反思中认识到django框架内集成的许多功能并未使用, 换用更轻巧灵活的flask框架是更好的选择, 于是在近日做了后端迁移的工作, 仅耗时一个晚上, 也证明了使用django框架可以但没有必要
- 由于在 `Python3.8` 中 `time.clock()` 方法被正式移除, 将此方法替换为 `time.perf_counter()`
- 部分文件读取路径由相对路径改为绝对路径, 包括`CRF.py`, `baseDict.py` 和 `API.py`
```python
# 部署时改为服务器的绝对路径
# CRF.py 和 baseDict.py 共有的部分
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
- 使用本地缓存机制, 目的是在某个单独回话中保持情绪分析类的实体对象的存在, 而且多用户访问时不冲突
```python
from flask_caching import Cache

config = {
    'CACHE_TYPE': 'filesystem',  # Flask-Caching related configs
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24 * 1,  # cache files save for 1 day
    'CACHE_IGNORE_ERRORS': True,
    'CACHE_DIR': BASE_DIR + '/cache',
    'CACHE_THRESHOLD': 128,
}

cache = Cache(config=config)
cache.init_app(app)
```

## deployment matters
- [ ] 延长服务器超时时间
- [ ] [Python Flask使用Nginx做代理时如何获取真实IP](https://www.yyqblog.com/161.html)
- [ ] 测试完成后debug模式关闭
