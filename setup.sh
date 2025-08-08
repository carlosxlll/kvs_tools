#!/bin/bash

# 定义要设置的别名名称
ALIAS_NAME="kvs"

echo "尝试为 kvs_tools src.cli 设置 '$ALIAS_NAME' 别名..."

# 1. 查找 python3 可执行文件的完整路径
PYTHON_BIN=$(command -v python3 || which python3)

if [ -z "$PYTHON_BIN" ]; then
    echo "错误: 未找到 'python3' 可执行文件。请确保 Python 3 已安装且在您的 PATH 中。"
    exit 1
fi

echo "检测到 Python 3 可执行文件: $PYTHON_BIN"

# 2. 获取 kvs_tools 项目的根目录 (假设此脚本在项目根目录运行)
# 使用 dirname $0 获取脚本所在目录，然后使用 readlink -f 获取真实路径，防止符号链接问题
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
KVS_PRO_ROOT="$SCRIPT_DIR" # 确保这是 src 模块的父目录 (即项目的根目录)

# 检查 src 模块目录和 cli.py 入口文件是否存在
# 新的结构中，cli.py 位于 src 目录下
if [ ! -f "$KVS_PRO_ROOT/src/cli.py" ]; then
    echo "错误: 未找到 'src/cli.py' 文件。请确保此脚本在项目根目录运行，且 'src' 目录及其内容结构正确。"
    echo "期望的目录结构: $KVS_PRO_ROOT/src/cli.py"
    exit 1
fi

echo "检测到 kvs 项目根目录: $KVS_PRO_ROOT"

# 定义完整的别名命令
# 关键：通过设置 PYTHONPATH 环境变量来确保 Python 能够找到 'src' 模块
# 双引号和反斜杠是必要的，以正确处理路径中的空格和 shell 展开
ALIAS_COMMAND="alias $ALIAS_NAME=\"PYTHONPATH=\\\"$KVS_PRO_ROOT\\\" \\\"$PYTHON_BIN\\\" -m src.cli\""

# 确定用户的 shell 类型和对应的配置文件
SHELL_TYPE=$(basename "$SHELL")
CONFIG_FILE=""

case "$SHELL_TYPE" in
    "bash")
        CONFIG_FILE="$HOME/.bashrc"
        ;;
    "zsh")
        CONFIG_FILE="$HOME/.zshrc"
        ;;
    *)
        # 默认使用 .profile，它通常在登录时被加载
        CONFIG_FILE="$HOME/.profile"
        echo "警告: 检测到 shell 类型为 '$SHELL_TYPE'。将尝试使用默认配置文件 '$CONFIG_FILE'。"
        echo "如果别名未生效，请手动将别名添加到您的 shell 配置文件中。"
        ;;
esac

# 检查配置文件是否存在，如果不存在则创建它
if [ ! -f "$CONFIG_FILE" ]; then
    echo "配置文件 '$CONFIG_FILE' 不存在，正在创建..."
    touch "$CONFIG_FILE"
    if [ $? -ne 0 ]; then
        echo "错误: 无法创建配置文件 '$CONFIG_FILE'。请检查权限。"
        exit 1
    fi
fi

# 检查别名是否已存在于配置文件中
# 使用 grep -F 进行固定字符串匹配，防止正则表达式问题
# 使用 grep -q 静默模式
if grep -qF "$ALIAS_COMMAND" "$CONFIG_FILE"; then
    echo "别名 '$ALIAS_NAME' 已经存在于 '$CONFIG_FILE' 中。无需修改。"
else
    # 将别名追加到配置文件
    echo "" >> "$CONFIG_FILE" # 添加一个空行，保持文件整洁
    echo "# Alias for kvs command-line tool, generated on $(date)" >> "$CONFIG_FILE"
    echo "$ALIAS_COMMAND" >> "$CONFIG_FILE"
    
    if [ $? -eq 0 ]; then
        echo "别名 '$ALIAS_NAME' 已成功添加到 '$CONFIG_FILE'。"
        echo "要立即生效，请运行以下命令："
        echo "  source $CONFIG_FILE"
        echo "或者，在下次打开新的终端会话时，别名将自动可用。"
    else
        echo "错误: 无法将别名写入 '$CONFIG_FILE'。请检查权限。"
        exit 1
    fi
fi

echo "设置完成。"
