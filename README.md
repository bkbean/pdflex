PDF 文件工具，可以拆分文档、合并文件、转换文件格式

# 用法
``` Bash
./pdftool.py [-h] [-o 输出路径] [-s | -m | -c] [-p 拆分文件时每个文件的页数] [-f 输入文件类型] [-t 输出文件类型] [input]
```
如果是 Windows 系统，前面加上 python.exe，需保证 Python 可执行文件的路径已加入系统变量 Path。

``` CMD
python.exe ./pdftool.py [-h] [-o 输出路径] [-s | -m | -c] [-p 拆分文件时每个文件的页数] [-f 输入文件类型] [-t 输出文件类型] [input]
```

## 文件拆分
```
./pdftool.py -s pdf-split.pdf
```
将当前目录的pdf-split.pdf文件拆分为单页文件，默认输出目录为同目录下的 {原文件名-split}，输出文件格式为 pdf。


```
./pdftool.py -s pdf-test.pdf -p 2 -o test-dir -t png
```
将当前目录的pdf-split.pdf文件每2页拆分为一个文件，输出目录为同目录下的 test-dir，输出文件格式为 png。

## 文件合并

```
./pdftool.py -m test
```
将子目录 test 下所有支持的文件合并为单个 PDF 文件，默认输出文件为同目录下的 {原目录名-merge.pdf}。


```
./pdftool.py -m test -o a100.jpg -t jpg
```
将子目录 test 下所有支持的文件合并为单个 JPG 文件，输出文件为同目录下的 a100.jpg，输出文件格式为 jpg。
文件合并将忽略输入文件类型参数 -f，如不指定输出文件类型参数 -t，将通过指定的输出文件扩展名判断；不指定扩展名，默认为PDF输出。


## 文件转换

```
./pdftool.py -c a100.jpg -o a100.png
```
将当前目录下文件 a100.jpg 转换为 png格式的文件 a100.png。

省略输入输出的类型参数将通过文件扩展名判断，省略输出文件将转换为同名的 PDF文件。
