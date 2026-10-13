# 笔记的发布与维护

仓库：[yeyeyuan23/learning-notes](https://github.com/yeyeyuan23/learning-notes)。

文章直接在 GitHub 仓库中阅读；这与启用 GitHub Pages 独立网站是两件事。本仓库没有配置 Pages，也不需要域名或单独租用服务器来阅读这些 Markdown 笔记。

## 在网页上修改文章

打开 [`systems/how-python-runs/README.md`](systems/how-python-runs/README.md)，使用 GitHub 的文件编辑功能修改正文，预览后提交。文中的流程图是 Mermaid 代码块，可以随正文一起修改。

目录和文章简介位于 [`README.md`](README.md)。代码和 Linux 实际输出集中在 [`experiments.ipynb`](systems/how-python-runs/experiments.ipynb)，与正文放在同一个章节目录。

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
git add systems/how-python-runs/README.md
git diff --cached
git commit -m "Revise program execution note"
git push origin main
```

示例只暂存正文文件。修改其他文件时，显式添加对应路径；提交前检查暂存区，不要把访问令牌、环境配置或其他项目数据放进公开仓库。推送需要在自己的电脑上完成 GitHub 身份验证，不要把密码或令牌发到聊天中。

## 查看与复现实验

在 GitHub 上打开 [实验 notebook](systems/how-python-runs/experiments.ipynb)，即可阅读代码与原有 Linux 输出。已有输出的环境、时间和来源在 notebook 开头注明。

复现 C 实验需要 Linux、Python 3、GCC、GNU Binutils 和 `file`。安装 Jupyter 相关工具后，可以交互式打开：

```bash
python3 -m pip install notebook nbconvert ipykernel
python3 -m notebook systems/how-python-runs/experiments.ipynb
```

选择 Python 3 内核，从上到下运行。也可以从仓库根目录执行并保存新输出：

```bash
python3 -m jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=120 \
  systems/how-python-runs/experiments.ipynb
```

实验在临时目录中创建源文件和构建产物，最后清理。重新运行会替换已有输出；提交前应检查输出变化，并更新正文或记录中的相关环境说明。

## 官方文档

- [编辑仓库文件](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
- [Markdown 中的 Mermaid 图](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [GitHub Pages 是什么](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
