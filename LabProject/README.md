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

## 开发过程小记

- 由于在 `Python3.8` 中 `time.clock()` 方法被正式移除, 将此方法替换为 `time.perf_counter()`