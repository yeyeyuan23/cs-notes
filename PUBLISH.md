# 笔记的发布与维护

仓库：[yeyeyuan23/learning-notes](https://github.com/yeyeyuan23/learning-notes)。

文章直接在 GitHub 仓库中阅读；这与启用 GitHub Pages 独立网站是两件事。本仓库没有配置 Pages，也不需要域名或单独租用服务器来阅读这些 Markdown 笔记。

## 在网页上修改文章

打开 [`systems/how-python-runs.md`](systems/how-python-runs.md)，使用 GitHub 的文件编辑功能修改正文，预览后提交。文中的两张流程图是 Mermaid 代码块，可以随正文一起修改。

目录和文章简介位于 [`README.md`](README.md)。配套代码位于 [`examples/program-execution/`](examples/program-execution/)。

## 在本地修改

首次获取仓库：

```bash
git clone https://github.com/yeyeyuan23/learning-notes.git
cd learning-notes
```

已有本地副本时，在工作区没有未处理修改的情况下先同步远端：

```bash
git pull --ff-only
```

修改文章或示例后检查差异，再按需暂存、提交和推送：

```bash
git diff
git add systems/how-python-runs.md
git diff --cached
git commit -m "Revise program execution note"
git push origin main
```

示例只暂存正文文件。修改其他文件时，显式添加对应路径；提交前检查暂存区，不要把访问令牌、环境配置或其他项目数据放进公开仓库。推送需要在自己的电脑上完成 GitHub 身份验证，不要把密码或令牌发到聊天中。

## 重新验证实验

以下脚本针对 Linux、Python 3、GCC 与 GNU Binutils，另外需要 `file` 命令：

```bash
python3 examples/program-execution/verify.py
```

它会在临时目录构建 C 示例，并更新 [`VERIFICATION.md`](examples/program-execution/VERIFICATION.md)。它不会替你提交或推送；需要保留新记录时，再检查并提交该文件。

验证记录只证明列明环境中的实验结果，不证明所有平台输出相同，也不等于验证了网页排版。

## 官方文档

- [编辑仓库文件](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
- [Markdown 中的 Mermaid 图](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [GitHub Pages 是什么](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
