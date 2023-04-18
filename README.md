# Chinese-LangChain

> Chinese-LangChain：中文langchain项目，基于ChatGLM-6b+langchain实现本地化知识库检索与智能答案生成

## 🔥 效果演示

![](https://github.com/yanqiangmiffy/Chinese-LangChain/blob/master/images/web_demo.png)

## 🚀 特性

- 🚀 2023/04/18 webui增加知识库选择功能
- 🚀 2023/04/18 修复推理预测超时5s报错问题
- 🎉 2023/04/17 支持多种文档上传与内容解析：pdf、docx，ppt等
- 🎉 2023/04/17 支持知识增量更新

[//]: # (- 支持检索结果与LLM生成结果对比)

## 🧰 知识库

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
* [ ] 互联网检索结果接入
* [ ] 模型初始化有问题
* [ ] 增加非LangChain策略

## 交流

欢迎多提建议、Bad cases，目前尚不完善，欢迎进群及时交流，也欢迎大家多提PR
<img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/ch.jpg" width="300px">
<img src="https://raw.githubusercontent.com/yanqiangmiffy/Chinese-LangChain/master/images/chatgroup.jpg" width="300px">

## ❤️引用

- webui参考：https://github.com/thomas-yanxin/LangChain-ChatGLM-Webui
- knowledge问答参考：https://github.com/imClumsyPanda/langchain-ChatGLM
- LLM模型：https://github.com/THUDM/ChatGLM-6B
