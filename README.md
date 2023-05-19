---
license: openrail
title: 'Chinese-LangChain '
sdk: gradio
emoji: 🚀
colorFrom: yellow
colorTo: yellow
pinned: true
app_file: app.py
---

# Chinese-LangChain

> Chinese-LangChain：中文langchain项目，基于ChatGLM-6b+langchain实现本地化知识库检索与智能答案生成

https://github.com/yanqiangmiffy/Chinese-LangChain

俗称：小必应，Q.Talk，强聊，QiangTalk

## 🔥 效果演示

![](https://github.com/yanqiangmiffy/Chinese-LangChain/blob/master/images/web_demos/v1.png)
![](https://github.com/yanqiangmiffy/Chinese-LangChain/blob/master/images/web_demos/v3.png)

## 🚋 使用教程

- 选择知识库询问相关领域的问题

## 🏗️ 部署教程

### 运行配置

- 显存：12g，实际运行9g够了
- 运行内存：32g

### 运行环境

```text
langchain
gradio
transformers
sentence_transformers
faiss-cpu
unstructured
duckduckgo_search
mdtex2html
chardet
cchardet
```

### 启动Gradio

```shell
python main.py
```

## 🚀 特性
- 🚀 2023/05/19 [yanlijun573](https://github.com/yanlijun573)提供[streamlit](https://github.com/yanqiangmiffy/Chinese-LangChain/tree/streamlit)分支
- 🚀 2023/04/22 支持模型多机多卡推理
- 🔭 2023/04/20 支持模型问答与检索问答模式切换
- 💻 2023/04/20 感谢HF官方提供免费算力，添加HuggingFace
  Spaces在线体验[[🤗 DEMO](https://huggingface.co/spaces/ChallengeHub/Chinese-LangChain)
- 🧫 2023/04/19 发布45万Wikipedia的文本预处理语料以及FAISS索引向量
- 🐯 2023/04/19 引入ChuanhuChatGPT皮肤
- 📱 2023/04/19 增加web search功能，需要确保网络畅通！(感谢[@wanghao07456](https://github.com/wanghao07456),提供的idea)
- 📚 2023/04/18 webui增加知识库选择功能
- 🚀 2023/04/18 修复推理预测超时5s报错问题
- 🎉 2023/04/17 支持多种文档上传与内容解析：pdf、docx，ppt等
- 🎉 2023/04/17 支持知识增量更新

[//]: # (- 支持检索结果与LLM生成结果对比)

## 🧰 知识库

### 构建知识库

- Wikipedia-zh

> 详情见：corpus/zh_wikipedia/README.md

### 知识库向量索引

| 知识库数据                                                                         | FAISS向量                                                              |
|-------------------------------------------------------------------------------|----------------------------------------------------------------------|
| 中文维基百科截止4月份数据，45万                                                             | 链接：https://pan.baidu.com/s/1VQeA_dq92fxKOtLL3u3Zpg?pwd=l3pn 提取码：l3pn |
| 截止去年九月的130w条中文维基百科处理结果和对应faiss向量文件 @[yubuyuabc](https://github.com/yubuyuabc) | 链接：https://pan.baidu.com/s/1Yls_Qtg15W1gneNuFP9O_w?pwd=exij 提取码：exij |
| 💹 [大规模金融研报知识图谱](http://openkg.cn/dataset/fr2kg)                              | 链接：https://pan.baidu.com/s/1FcIH5Fi3EfpS346DnDu51Q?pwd=ujjv 提取码：ujjv |

## 🔨 TODO

* [x] 支持上下文
* [x] 支持知识增量更新
* [x] 支持加载不同知识库
* [x] 支持检索结果与LLM生成结果对比
* [ ] 支持检索生成结果与原始LLM生成结果对比
* [ ] 支持模型问答与检索问答
* [ ] 检索结果过滤与排序
* [x] 互联网检索结果接入
* [ ] 模型初始化有问题
* [ ] 增加非LangChain策略
* [ ] 显示当前对话策略
* [ ] 构建一个垂直业务场景知识库，非通用性

## 交流

欢迎多提建议、Bad cases，目前尚不完善，欢迎进群及时交流，也欢迎大家多提PR</br>

<figure class="third">
  <img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/ch.jpg" width="180px">
  <img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/chatgroup.jpg" width="180px" height="270px">

</figure>

合作交流可以联系：

<img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/personal.jpg" width="180px">

## ❤️引用

- webui参考：https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui
- knowledge问答参考：https://github.com/imClumsyPanda/langchain-ChatGLM
- LLM模型：https://github.com/THUDM/ChatGLM-6B
- CSS：https://huggingface.co/spaces/JohnSmith9982/ChuanhuChatGPT



## ⭐️ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yanqiangmiffy/Chinese-LangChain&type=Date)](https://star-history.com/#yanqiangmiffy/Chinese-LangChain&Date)
