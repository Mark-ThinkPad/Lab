# 情感分析本地版运行依赖分析

## GUI.py 运行依赖 (重点)

### 引用的第三方库

- `tk`: GUI库, 在web中自动忽视
- `jieba`: 中文分词
- `sklearn`: 机器学习

> Warning: Button映射的函数需要重写

## 其他文件

基于GUI.py的原调用关系即可, 不予细究