# 配套实验：实际验证记录

验证时间（UTC）：2026-10-11T10:33:48+00:00

这些结果来自文章生成时的执行环境，不是作者个人电脑或远程 GitHub CI 的结果。

| 项目 | 实际值 |
| --- | --- |
| Python 实现与版本 | CPython 3.13.5 |
| 操作系统与架构 | Linux x86_64 |
| GCC | `gcc (Debian 14.2.0-19) 14.2.0` |

## 验证结果

- C 的预处理、编译、汇编、链接均成功，`demo` 输出 `5\n`。
- 故意漏掉 `add.o` 后，链接失败，错误指向未定义的 `add`。
- 单独执行 `compile(source, ...)` 时，捕获的标准输出是空字符串。
- 执行产生的代码对象时，标准输出严格等于 `5\n`。
- 配套 `main.py` 与 `inspect_python.py` 均成功执行。
- `nm` 显示 `main.o` 对 `add` 的未定义引用，以及 `add.o` 对它的定义。

以上检查全部通过。此记录不证明其他操作系统、编译器或 Python 版本的输出完全相同。

## C 命令

```bash
gcc -E main.c -o main.i
gcc -S -O0 main.i -o main.s
gcc -c main.s -o main.o
gcc -c -O0 add.c -o add.o
gcc main.o add.o -o demo
./demo
```

## 文件类型

```text
main.i: C source, ASCII text
main.s: assembler source, ASCII text
main.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
demo:   ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c55ab8bf4e668c59253a6dc28b96fc8cecccbd5a, for GNU/Linux 3.2.0, not stripped
```

## 符号

`nm main.o`：

```text
                 U add
0000000000000000 T main
                 U printf
```

`nm add.o`：

```text
0000000000000000 T add
```

## 目标文件的机器码反汇编

```text

add.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <add>:
   0:	55                   	push   %rbp
   1:	48 89 e5             	mov    %rsp,%rbp
   4:	89 7d fc             	mov    %edi,-0x4(%rbp)
   7:	89 75 f8             	mov    %esi,-0x8(%rbp)
   a:	8b 55 fc             	mov    -0x4(%rbp),%edx
   d:	8b 45 f8             	mov    -0x8(%rbp),%eax
  10:	01 d0                	add    %edx,%eax
  12:	5d                   	pop    %rbp
  13:	c3                   	ret
```

## 预期的链接失败

命令：`gcc main.o -o missing-add`；退出码：`1`。

```text
/usr/bin/ld: main.o: in function `main':
main.c:(.text+0xf): undefined reference to `add'
collect2: error: ld returned 1 exit status
```

## Python 字节码

此输出属于上表列明的 Python 版本，不是跨版本固定格式。

```text
  0           RESUME                   0

  2           LOAD_CONST               0 (<code object add at 0x7f349954f4b0, file "<example>", line 2>)
              MAKE_FUNCTION
              STORE_NAME               0 (add)

  5           LOAD_NAME                1 (print)
              PUSH_NULL
              LOAD_NAME                0 (add)
              PUSH_NULL
              LOAD_CONST               1 (2)
              LOAD_CONST               2 (3)
              CALL                     2
              CALL                     1
              POP_TOP
              RETURN_CONST             3 (None)

Disassembly of <code object add at 0x7f349954f4b0, file "<example>", line 2>:
  2           RESUME                   0

  3           LOAD_FAST_LOAD_FAST      1 (a, b)
              BINARY_OP                0 (+)
              RETURN_VALUE
```

## 重复验证

在 Linux 环境安装 Python 3、GCC 和 GNU Binutils 后，从仓库根目录执行：

```bash
python3 examples/program-execution/verify.py
```

该脚本只生成本地验证记录，不会创建远程仓库或推送文件。
