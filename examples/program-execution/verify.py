"""Reproduce the note's checks. Requires Python 3 and GNU C tools on Linux.

Run: python3 examples/program-execution/verify.py
Writes VERIFICATION.md beside this script. C build products stay in a
TemporaryDirectory and are removed automatically; no repository is published.
"""
from __future__ import annotations

import ast
import contextlib
import datetime as dt
import dis
import io
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def run(argv: list[str], cwd: Path, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=30)
    if expect_success and result.returncode != 0:
        raise RuntimeError(f"Command failed: {shlex.join(argv)}\n{result.stderr}")
    return result


def main() -> None:
    tools = ('gcc', 'file', 'nm', 'objdump')
    missing = [tool for tool in tools if shutil.which(tool) is None]
    if missing:
        raise SystemExit('Missing tools: ' + ', '.join(missing))
    if platform.system() != 'Linux':
        raise SystemExit('This reproduction script targets Linux and GNU tools.')

    tree = ast.parse((ROOT / 'inspect_python.py').read_text(encoding='utf-8'))
    source = next(
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == 'source' for t in node.targets)
    )
    compile_capture = io.StringIO()
    with contextlib.redirect_stdout(compile_capture):
        code = compile(source, '<example>', 'exec')
    if compile_capture.getvalue() != '':
        raise AssertionError('Compiling source unexpectedly produced stdout.')
    exec_capture = io.StringIO()
    with contextlib.redirect_stdout(exec_capture):
        exec(code, {})
    if exec_capture.getvalue() != '5\n':
        raise AssertionError('Executing source did not produce exactly 5 and newline.')
    bytecode = io.StringIO()
    dis.dis(code, file=bytecode)

    python_main = run([sys.executable, 'main.py'], ROOT)
    if python_main.stdout != '5\n':
        raise AssertionError('Python main.py returned unexpected output.')
    inspected = run([sys.executable, 'inspect_python.py'], ROOT)
    if not inspected.stdout.endswith('4. 开始执行 source\n5\n'):
        raise AssertionError('The inspection example did not reach execution correctly.')

    stages = [
        ['gcc', '-E', 'main.c', '-o', 'main.i'],
        ['gcc', '-S', '-O0', 'main.i', '-o', 'main.s'],
        ['gcc', '-c', 'main.s', '-o', 'main.o'],
        ['gcc', '-c', '-O0', 'add.c', '-o', 'add.o'],
        ['gcc', 'main.o', 'add.o', '-o', 'demo'],
        ['./demo'],
    ]
    with tempfile.TemporaryDirectory(prefix='program-execution-') as tmp:
        work = Path(tmp)
        for name in ('main.c', 'add.c'):
            shutil.copy2(ROOT / name, work / name)
        for argv in stages:
            result = run(argv, work)
            if argv == ['./demo'] and result.stdout != '5\n':
                raise AssertionError('C demo returned unexpected output.')
        file_output = run(['file', 'main.i', 'main.s', 'main.o', 'demo'], work).stdout
        nm_main = run(['nm', 'main.o'], work).stdout
        nm_add = run(['nm', 'add.o'], work).stdout
        assembly = run(['objdump', '-d', 'add.o'], work).stdout
        failed = run(['gcc', 'main.o', '-o', 'missing-add'], work, expect_success=False)
        if failed.returncode == 0 or 'add' not in failed.stderr:
            raise AssertionError('Omitting add.o did not fail with a reference to add.')
        if ' U add' not in nm_main or ' T add' not in nm_add:
            raise AssertionError('Expected GNU nm symbol classification not found.')

    gcc_version = run(['gcc', '--version'], ROOT).stdout.splitlines()[0]
    record = f'''# 配套实验：实际验证记录

验证时间（UTC）：{dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}

这些结果来自文章生成时的执行环境，不是作者个人电脑或远程 GitHub CI 的结果。

| 项目 | 实际值 |
| --- | --- |
| Python 实现与版本 | {platform.python_implementation()} {platform.python_version()} |
| 操作系统与架构 | {platform.system()} {platform.machine()} |
| GCC | `{gcc_version}` |

## 验证结果

- C 的预处理、编译、汇编、链接均成功，`demo` 输出 `5\\n`。
- 故意漏掉 `add.o` 后，链接失败，错误指向未定义的 `add`。
- 单独执行 `compile(source, ...)` 时，捕获的标准输出是空字符串。
- 执行产生的代码对象时，标准输出严格等于 `5\\n`。
- 配套 `main.py` 与 `inspect_python.py` 均成功执行。
- `nm` 显示 `main.o` 对 `add` 的未定义引用，以及 `add.o` 对它的定义。

以上检查全部通过。此记录不证明其他操作系统、编译器或 Python 版本的输出完全相同。

## C 命令

```bash
{chr(10).join(shlex.join(argv) for argv in stages)}
```

## 文件类型

```text
{file_output.rstrip()}
```

## 符号

`nm main.o`：

```text
{nm_main.rstrip()}
```

`nm add.o`：

```text
{nm_add.rstrip()}
```

## 目标文件的机器码反汇编

```text
{assembly.rstrip()}
```

## 预期的链接失败

命令：`gcc main.o -o missing-add`；退出码：`{failed.returncode}`。

```text
{failed.stderr.rstrip()}
```

## Python 字节码

此输出属于上表列明的 Python 版本，不是跨版本固定格式。

```text
{bytecode.getvalue().rstrip()}
```

## 重复验证

在 Linux 环境安装 Python 3、GCC 和 GNU Binutils 后，从仓库根目录执行：

```bash
python3 examples/program-execution/verify.py
```

该脚本只生成本地验证记录，不会创建远程仓库或推送文件。
'''
    (ROOT / 'VERIFICATION.md').write_text(record, encoding='utf-8')
    print('PASS: C build/run; expected link failure; Python compile/exec separation; both Python examples; GNU nm symbols.')
    print('Wrote:', ROOT / 'VERIFICATION.md')


if __name__ == '__main__':
    main()
