# KVS：本地命令词典（多用法彩色显示）

## 简介

**KVS** 是一个基于命令行的本地命令词典工具，旨在帮助开发者和系统管理员高效地管理和查找常用的 Shell 命令及其用法。它支持为同一条主命令添加多个用法示例、中文名称、备注和标签，并通过丰富的终端输出提供友好的用户体验。

在日常工作中，我们经常会用到一些复杂的、不常用的命令，或者同一命令有多种不同的用法。KVS 解决了这些痛点，让您能够：

*   **集中管理：** 将所有常用的、不常用的命令及其详细用法、备注和标签统一存储。
*   **快速查找：** 通过主命令名、中文名、用法关键词、备注或标签进行模糊搜索。
*   **清晰展示：** 借助 `rich` 库，提供美观、易读的彩色终端输出。
*   **交互模式：** 部分命令支持交互式操作，提升使用便利性。
*   **数据便携：** 数据遵循 XDG Base Directory 规范存储，方便备份和迁移。

## 功能特性

*   **添加命令 (`add`)：**
    *   为新主命令添加中文名、用法、备注和标签。
    *   为已有主命令添加新的用法示例。
    *   支持命令行参数和交互式模式 (`-i`/`--interactive`)。
*   **列出命令 (`list`)：**
    *   列出所有已收录的主命令及其中文名、用法数量和标签。
    *   列出特定主命令的所有用法示例（包含序号、用法和备注）。
*   **更新命令 (`update`)：**
    *   更新主命令的中文名。
    *   更新主命令的标签。
*   **删除命令 (`delete`)：**
    *   根据序号或关键词删除特定主命令下的用法。
    *   当主命令的所有用法都被删除时，自动移除该主命令。
    *   支持交互式模式 (`-i`/`--interactive`)。
*   **编辑命令 (`edit`)：**
    *   根据序号编辑特定主命令下用法的示例和备注。
    *   支持交互式模式 (`-i`/`--interactive`)。
*   **查找命令 (`find`)：**
    *   根据关键词在主命令、中文名、用法或备注中进行模糊查找。
*   **复制用法 (`copy`)：**
    *   将指定主命令的某个用法复制到剪贴板。
*   **导入/导出数据 (`import`/`export`)：**
    *   将所有命令数据导出到 JSON 文件，便于备份和分享。
    *   从 JSON 文件导入命令数据，支持合并或覆盖现有数据。
*   **美观输出：** 借助 `rich` 库提供彩色、格式化的终端输出。
*   **数据存储：** 遵循 XDG Base Directory 规范，数据文件默认存储在 `~/.local/share/kvs/commands.json`。

## 安装

### 先决条件

*   Python 3.8+
*   `pip` (Python 包管理器)

### 步骤

1.  **克隆仓库：**
    ```bash
    git clone https://github.com/yourusername/kvs_tools.git # 请替换为您的仓库地址
    cd kvs_tools
    ```

2.  **安装 Python 依赖：**
    ```bash
    pip install -r requirements.txt
    ```
    这将安装 `rich` 和 `pyperclip` 等库。`pyperclip` 可能需要额外的系统剪贴板工具（例如 Linux 上的 `xclip` 或 `xsel`）。

3.  **设置 `kvs` 命令别名：**
    运行项目根目录下的 `setup.sh` 脚本，它将自动检测您的 Python 路径和项目路径，并设置一个全局的 `kvs` 别名。
    ```bash
    chmod +x setup.sh  # 赋予执行权限
    ./setup.sh
    ```
    脚本会提示别名已成功添加到您的 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）。

4.  **激活别名：**
    按照脚本的提示，运行 `source` 命令来立即激活别名：
    ```bash
    source ~/.zshrc  # 如果您是 zsh 用户
    # 或 source ~/.bashrc  # 如果您是 bash 用户
    # 或 source ~/.profile  # 如果您的 shell 无法自动识别
    ```
    或者，您可以关闭当前终端窗口，重新打开一个新的终端会话。

现在，您应该可以在任何目录下直接使用 `kvs` 命令了！

## 使用指南

### 1. 添加命令 (`kvs add`)

*   **基本添加：** 为 `ls` 命令添加一个中文名、用法和备注，并加上标签。
    ```bash
    kvs add ls "列文件" "ls -l" "详细显示" --tags file,basic
    ```
*   **为已有命令添加新用法：**
    ```bash
    kvs add ls "" "ls -a" "显示隐藏文件" # 无需重复中文名
    ```
*   **交互式添加：** 按照提示一步步输入信息。
    ```bash
    kvs add --interactive
    # 或 kvs add -i
    ```

### 2. 列出命令 (`kvs list`)

*   **列出所有主命令：**
    ```bash
    kvs list
    ```
*   **列出特定命令的用法：**
    ```bash
    kvs list git
    ```

### 3. 更新命令 (`kvs update`)

*   **更新中文名：** 将 `ls` 的中文名更新为 "文件列表"。
    ```bash
    kvs update name ls "文件列表"
    ```
*   **更新标签：** 将 `git` 的标签更新为 `dev,version`。
    ```bash
    kvs update tag git dev,version
    ```

### 4. 删除用法 (`kvs delete`)

*   **按序号删除：** 删除 `git` 命令的第 0 条用法。
    ```bash
    kvs delete git 0
    ```
*   **按关键词模糊删除：** 删除 `git` 命令中包含关键词 "远程" 的用法。
    ```bash
    kvs delete git 远程
    ```
*   **交互式删除：**
    ```bash
    kvs delete --interactive
    # 或 kvs delete -i
    ```

### 5. 编辑用法 (`kvs edit`)

*   **按序号编辑：** 编辑 `git` 命令的第 1 条用法，更新其用法示例。
    ```bash
    kvs edit git 1 --new-usage "git branch -a"
    ```
*   **同时编辑用法和备注：**
    ```bash
    kvs edit git 1 --new-usage "git branch -a" --new-note "查看所有分支"
    ```
*   **交互式编辑：**
    ```bash
    kvs edit --interactive
    # 或 kvs edit -i
    ```

### 6. 查找命令 (`kvs find`)

*   **按关键词查找：** 查找包含 "分支" 关键词的命令或用法。
    ```bash
    kvs find 分支
    ```
*   **多关键词查找：**
    ```bash
    kvs find "提交 本地"
    ```

### 7. 复制用法 (`kvs copy`)

*   **复制指定用法：** 复制 `git` 命令的第 0 条用法到剪贴板。
    ```bash
    kvs copy git 0
    ```

### 8. 导出数据 (`kvs export`)

*   **导出所有命令数据到 JSON 文件：**
    ```bash
    kvs export ~/kvs_backup.json
    ```

### 9. 导入数据 (`kvs import`)

*   **从 JSON 文件导入数据（合并模式）：** 默认情况下，导入会合并用法，不会覆盖现有命令。
    ```bash
    kvs import ~/kvs_backup.json
    ```
*   **从 JSON 文件导入数据（覆盖模式）：** 强制覆盖同名主命令的现有数据。
    ```bash
    kvs import ~/kvs_backup.json --overwrite
    ```

## 开发与测试

如果您想参与开发或运行测试：

1.  **运行测试：**
    ```bash
    python3 test.py
    ```
    此命令将运行 `test.py` 中定义的所有单元测试，确保代码的正确性。

## 数据存储

KVS 遵循 XDG Base Directory Specification 来存储其数据文件。这意味着您的命令词典数据默认位于：

*   **Linux/macOS：** `~/.local/share/kvs/commands.json`
*   **Windows：** `%LOCALAPPDATA%\kvs\commands.json` (或类似的路径)

您也可以通过设置 `XDG_DATA_HOME` 环境变量来改变数据存储路径。例如：
`export XDG_DATA_HOME="/path/to/your/custom/data"`

请注意备份此文件，以防数据丢失。

## 许可证

本项目采用 MIT 许可证。详见 `LICENSE` 文件 (如果存在)。

---

感谢您使用 KVS！希望它能提高您的命令行效率。
