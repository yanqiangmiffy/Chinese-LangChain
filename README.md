# Chinese-LangChain

> Chinese-LangChain：中文langchain项目，基于ChatGLM-6b+langchain实现本地化知识库检索与智能答案生成

https://github.com/yanqiangmiffy/Chinese-LangChain

俗称：小必应，Q.Talk，强聊，QiangTalk

## 🔥 效果演示

![](https://github.com/yanqiangmiffy/Chinese-LangChain/blob/master/images/web_demo.png)
![](https://github.com/yanqiangmiffy/Chinese-LangChain/blob/master/images/web_demo_new.png)

## 🚋 使用教程

- 选择知识库询问相关领域的问题

## 🏗️ 部署教程

### 运行配置

- 显存：12g，实际运行9g够了
- 运行内存：32g

## 🚀 特性

- 📝 2023/04/19 发布45万Wikipedia的文本预处理语料以及FAISS索引向量
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

| 知识库数据  |FAISS向量|
|--------|----|
|💹 [大规模金融研报知识图谱](http://openkg.cn/dataset/fr2kg)|链接：https://pan.baidu.com/s/1FcIH5Fi3EfpS346DnDu51Q?pwd=ujjv 提取码：ujjv |

## 🔨 TODO

* [x] 支持上下文
* [x] 支持知识增量更新
* [x] 支持加载不同知识库
* [x] 支持检索结果与LLM生成结果对比
* [ ] 支持检索生成结果与原始LLM生成结果对比
* [ ] 检索结果过滤与排序
* [x] 互联网检索结果接入
* [ ] 模型初始化有问题
* [ ] 增加非LangChain策略

## 交流

欢迎多提建议、Bad cases，目前尚不完善，欢迎进群及时交流，也欢迎大家多提PR</br>

<figure class="third">
    <img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/ch.jpg" width="180px"><img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/chatgroup.jpg" width="180px" height="270px"><img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/personal.jpg" width="180px">
</figure>



## ❤️引用

- webui参考：https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui
- knowledge问答参考：https://github.com/imClumsyPanda/langchain-ChatGLM
- LLM模型：https://github.com/THUDM/ChatGLM-6B
- CSS：https://huggingface.co/spaces/JohnSmith9982/ChuanhuChatGPT
