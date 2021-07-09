# README

Group 2

组员：刘佳润 陈诚

## 工程环境说明

* 编写语言：Python 3.7
* 操作系统：Windows 10 或 CentOS 7 均可运行
* 实验用CPU：AMD Ryzen 7 5800H

## 工程结构说明

```
IRProject
|  en_thesaurus.jsonl	// 未经处理的同义词表
│  BooleanQuery.py		// 布尔查询模块
│  GlobbingQuery.py		// 通配符查询模块
│  InvertedIndex.py		// 预处理模块
│  main.py				// 主程序入口
│  PhraseQuery.py		// 词语查询模块
│  README.md			// 本文件
│  SpellingCorrect.py	// 拼写检查模块
│  synonymslist.jsonl	// 经处理过的同义词表
│  SynonymsWords.py		// 同义词扩展模块
│  topk.py				// Top-K排序显示模块
│  utils.py				// 一些工具类函数
│  
├─index
│      doc_size.json	// 预处理判断的有效文件目录
│      index.json		// 倒排索引
│      VSM.json			// VSM
│      wordlist.json	// 词表（词典）
│      
└─Reuters				// 语料库
```

## 部署与运行方法

* 下载依赖库

  ```
  $ pip install nltk
  $ pip install chardet
  $ pip install jsonlines
  ```

* 因为已经构建好索引，所以直接运行main.py，不需要任何改动

  ```
  $ python main.py
  ```

## 功能测试与说明

### 构建倒排索引与VSM

这一部分构建倒排索引、构建词表、构建空间向量模型。为了加速后续的检索、排序等，我们在预处理阶段将所有文档的空间向量全部计算好。空间向量的每一项与词表中的位置对应。

倒排索引结构如下：

```
{word1: {docID1: [pos1, pos2, …, posn], docID2 : [pos1, pos2, …, posn], …}, word2:…}
```

向量空间结构如下：

```
{docID1: [tfidf1, tfidf2, …, tfidfn], docID2 : [tfidf1, tfidf2, …, tfidfn], …}
```

向量空间压缩方法如下：

![image-20210628143250736](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628143250736.png)

*本来我们希望使用gzip进行压缩，以二进制的格式储存，但是发现python对于gzip解压缩的速度太慢，与我们的预期效果不符，因此我们最终放弃了这个方法，仅使用json来进行存储和读取。*

**测试结果：**预处理时间总共1~2分钟

### 单词查询

**进入方式：**使用2.短语查询功能即可

![image-20210628143907112](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628143907112.png)

### 布尔查询

**进入方式：**使用1.布尔查询

**语法：**查询词使用正常拼写，布尔关系词使用全大写的AND/OR/NOT

![image-20210628150118599](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628150118599.png)

![image-20210628150208176](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628150208176.png)

![image-20210628150244101](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628150244101.png)

### 通配查询

**进入方式：**使用3.通配符查询

**语法：**使用*代替模糊部分

![image-20210628150714168](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628150714168.png)

### 短语查询

**进入方式：**使用2.短语查询

![image-20210628150822665](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628150822665.png)

![image-20210628150903146](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628150903146.png)

### 拼写校正

**进入方式：**使用2.短语查询，对于可能输错的词，自动进行判断与提示

![image-20210628150950969](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628150950969.png)

![image-20210628151008851](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628151008851.png)

![image-20210628151029924](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628151029924.png)

### 同义词查询

**进入方式：**使用2.短语查询，用户可以选择是否进行同义词查询

![image-20210628151042437](https://ruin-typora.oss-cn-beijing.aliyuncs.com/image-20210628151042437.png)
