# 计算机学习笔记

从具体问题出发，记录概念、推导、可复现实验和原始参考资料。

## 计算机系统

### 知识架构总览

这是一张用于组织笔记的**系统抽象与依赖关系图**，不是程序执行时的逐层调用流程。主干展示一台计算机从硬件到软件的关系；侧面展示程序构建、计算机网络与多机协作。

```mermaid
flowchart BT
    subgraph ONE["单机系统：从实现到抽象"]
        direction BT
        LOGIC["数字逻辑与硬件实现<br/>逻辑门 · 时序电路 · 微体系结构"]
        ARCH["计算机组成与体系结构<br/>CPU · ISA · 寄存器 · Cache<br/>内存 · 存储 · I/O 设备"]
        OS["操作系统与系统软件<br/>进程与线程 · 调度 · 虚拟内存<br/>文件系统 · 设备驱动 · 网络协议栈"]
        APP["用户态程序与运行时<br/>C 原生程序 · CPython / JVM<br/>Web 服务 · 数据库管理系统"]
        LOGIC -->|"实现处理器等硬件"| ARCH
        ARCH -->|"提供硬件能力"| OS
        OS -->|"提供资源管理和系统服务"| APP
        ARCH -.->|"CPU 直接执行用户态机器指令"| APP
    end

    BUILD["程序语言与构建工具（跨层主题）<br/>C / Python · 编译器 · 汇编器 · 链接器"]
    NET["计算机网络（跨层主题）<br/>网卡 · TCP/IP · Socket · 应用协议"]
    DIST["分布式系统（多个节点协作）<br/>远程调用 · 复制 · 一致性 · 容错"]

    BUILD -.->|"构建或支持运行程序"| APP
    ARCH -.->|"网络硬件"| NET
    OS -.->|"内核网络功能"| NET
    APP -.->|"网络应用"| NET
    NET -->|"通信基础"| DIST
    APP -.->|"多个节点上的服务"| DIST
```

**读图方式：**实线表示实现或主要支撑关系，虚线表示跨层联系。操作系统提供资源管理和系统服务，但普通用户态机器指令由 CPU 直接执行，并不需要内核逐条解释。网络跨越硬件、内核和应用；分布式系统依靠多台计算机与网络协作，**不是单机应用之上必经的第六层**。这张图只展示知识结构，不代表每个模块都必须有单独笔记。

概念参考：[《Computer Systems: A Programmer's Perspective》](https://csapp.cs.cmu.edu/) · [MIT 6.5840 Distributed Systems](https://pdos.lcs.mit.edu/6.824/index.html)

### 已整理的笔记

- [运行程序时，到底是谁在执行谁？](systems/how-python-runs.md)

对比 C 的预处理、编译、汇编、链接，与 CPython 的字节码解释执行；区分解释器与 CPU 的执行角色。配有 Mermaid 流程图及 C / Python 实验。

[配套实验](examples/program-execution/) · [实际验证结果](examples/program-execution/VERIFICATION.md)

## 阅读方式

在 GitHub 中打开 [文章 Markdown](systems/how-python-runs.md) 阅读正文。文中的流程图使用 Mermaid：它是可编辑的图表描述，GitHub 支持把相应代码块渲染成流程图。在本地阅读时，需要支持 Mermaid 的 Markdown 阅读器；普通文本编辑器会显示图表源码。

## 内容边界

文章说明适用的实现与环境，不把某个工具版本的表现当作所有平台的规定。实验记录只反映列明环境中实际执行过的检查，不冒充用户本人电脑上的结果。
