# 计算机学习笔记

从具体问题出发，记录概念、推导、可复现实验和原始参考资料。

## 计算机系统

### [运行程序时，到底是谁在执行谁？](systems/how-python-runs.md)

对比 C 的预处理、编译、汇编、链接，与 CPython 的字节码解释执行；区分解释器、操作系统和 CPU 的职责。配有两张 Mermaid 图及 C / Python 实验。

[配套实验](examples/program-execution/) · [实际验证结果](examples/program-execution/VERIFICATION.md)

## 阅读方式

在 GitHub 中打开 [文章 Markdown](systems/how-python-runs.md) 阅读正文。文中的两张图使用 Mermaid：它是可编辑的图表描述，GitHub 支持把相应代码块渲染成流程图。在本地阅读时，需要支持 Mermaid 的 Markdown 阅读器；普通文本编辑器会显示图表源码。

后续修改以 `systems/how-python-runs.md` 为正文源文件。

## 内容边界

文章说明适用的实现与环境，不把某个工具版本的表现当作所有平台的规定。实验记录只反映列明环境中实际执行过的检查，不冒充用户本人电脑上的结果。

后续编辑、提交与本地验证说明见 [PUBLISH.md](PUBLISH.md)。
