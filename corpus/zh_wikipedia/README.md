## 知识库构建


###  1 Wikipedia构建

参考教程：https://blog.51cto.com/u_15127535/2697309


一、维基百科

维基百科（Wikipedia），是一个基于维基技术的多语言百科全书协作计划，也是一部用不同语言写成的网络百科全书。维基百科是由吉米·威尔士与拉里·桑格两人合作创建的，于2001年1月13日在互联网上推出网站服务，并在2001年1月15日正式展开网络百科全书的项目。



二、维基百科处理

1 环境配置（1）编程语言采用 python3（2）Gensim第三方库，Gensim是一个Python的工具包，其中有包含了中文维基百科数据处理的类，使用方便。
Gensim : https://github.com/RaRe-Technologies/gensim

使用 pip install gensim 安装gensim。

（3）OpenCC第三方库，是中文字符转换，包括中文简体繁体相互转换等。

OpenCC：https://github.com/BYVoid/OpenCC，OpenCC源码采用c++实现，如果会用c++的可以使用根据介绍，make编译源码。

OpenCC也有python版本实现，可以通过pip安装（pip install opencc-python），速度要比c++版慢，但是使用方便，安装简单，推荐使用pip安装。



2 数据下载

中文维基百科数据按月进行更新备份，一般情况下，下载当前最新的数据，下载地址（https://dumps.wikimedia.org/zhwiki/latest/），我们下载的数据是：zhwiki-latest-pages-articles.xml.bz2。

中文维基百科数据一般包含如下几个部分：



训练词向量采用的数据是正文数据，下面我们将对正文数据进行处理。



3 数据抽取

下载下来的数据是压缩文件（bz2，gz），不需要解压，这里已经写好了一份利用gensim处理维基百科数据的脚本

wikidata_processhttps://github.com/bamtercelboo/corpus_process_script/tree/master/wikidata_process

使用：

python wiki_process.py zhwiki-latest-pages-articles.xml.bz2 zhwiki-latest.txt

这部分需要一些的时间，处理过后的得到一份中文维基百科正文数据（zhwiki-latest.txt）。

输出文件类似于：

歐幾里得 西元前三世紀的古希臘數學家 現在被認為是幾何之父 此畫為拉斐爾的作品 雅典學院 数学 是利用符号语言研究數量 结构 变化以及空间等概念的一門学科



4 中文繁体转简体

经过上述脚本得到的文件包含了大量的中文繁体字，我们需要将其转换成中文简体字。

我们利用OpenCC进行繁体转简体的操作，这里已经写好了一份python版本的脚本来进行处理

chinese_t2s

https://github.com/bamtercelboo/corpus_process_script/tree/master/chinese_t2s

使用：

python chinese_t2s.py –input input_file –output output_file

like:

python chinese_t2s.py –input zhwiki-latest.txt –output zhwiki-latest-simplified.txt

输出文件类似于

欧几里得 西元前三世纪的古希腊数学家 现在被认为是几何之父 此画为拉斐尔的作品 雅典学院 数学 是利用符号语言研究数量 结构 变化以及空间等概念的一门学科

      5.清洗语料

上述处理已经得到了我们想要的数据，但是在其他的一些任务中，还需要对这份数据进行简单的处理，像词向量任务，在这得到的数据里，还包含很多的英文，日文，德语，中文标点，乱码等一些字符，我们要把这些字符清洗掉，只留下中文字符，仅仅留下中文字符只是一种处理方案，不同的任务需要不同的处理，这里已经写好了一份脚本

clean

https://github.com/bamtercelboo/corpus_process_script/tree/master/clean

使用：

python clean_corpus.py –input input_file –output output_file

like：

python clean_corpus.py –input zhwiki-latest-simplified.txt –output zhwiki-latest-simplified_cleaned.txt

效果：

input:

哲学	哲学（英语：philosophy）是对普遍的和基本的问题的研究，这些问题通常和存在、知识、价值、理性、心灵、语言等有关。

output:

哲学哲学英语是对普遍的和基本的问题的研究这些问题通常和存在知识价值理性心灵语言等有关



三、数据处理脚本

近在github上新开了一个Repositorycorpus-process-scripthttps://github.com/bamtercelboo/corpus_process_script在这个repo，将存放中英文数据处理脚本，语言不限，会有详细的README，希望对大家能有一些帮助。
References

