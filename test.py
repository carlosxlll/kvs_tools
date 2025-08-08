import subprocess
import os
import tempfile
import shutil
import json
import time

# --- 辅助函数 ---

def run_kvs_command(temp_data_dir: str, args: list, input_str: str = None) -> tuple[str, str, int]:
    """
    在指定的临时数据目录下运行 kvs.cli 命令。
    
    参数:
        temp_data_dir (str): 临时 XDG_DATA_HOME 目录的路径。
        args (list): 要传递给 kvs.cli 的命令行参数列表。
        input_str (str, optional): 如果命令需要交互式输入，则提供此字符串。
                                   多行输入使用 '\n' 分隔。
    返回:
        tuple[str, str, int]: (stdout, stderr, returncode)。
    """
    env = os.environ.copy()
    # 设置 XDG_DATA_HOME 环境变量，强制 kvs 将数据存储到临时目录
    env["XDG_DATA_HOME"] = temp_data_dir
    
    command = ["python3", "-m", "src.cli"] + args
    
    print(f"Executing: {' '.join(command)}")
    if input_str:
        print(f"  (with input: {repr(input_str.strip())})") # Repr for visibility of newlines
    
    process = subprocess.run(
        command,
        env=env,
        input=input_str,
        text=True,  # 编码 stdin/stdout 为文本
        capture_output=True,  # 捕获标准输出和标准错误
        check=False  # 不在非零退出码时抛出 CalledProcessError，以便我们检查 returncode
    )
    
    print(f"  Return code: {process.returncode}")
    if process.stdout:
        print(f"  Stdout:\n{process.stdout.strip()}")
    if process.stderr:
        print(f"  Stderr:\n{process.stderr.strip()}")
    
    return process.stdout, process.stderr, process.returncode

def get_db_content(temp_data_dir: str) -> dict:
    """从临时数据目录读取当前的 commands.json 文件内容。"""
    # 根据 kvs 的 XDG 规范，数据文件通常在 $XDG_DATA_HOME/kvs/commands.json
    db_path = os.path.join(temp_data_dir, "kvs", "commands.json")
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {db_path}. File might be empty or corrupted.")
                return {}
    return {}

# --- 测试套件 ---

def run_tests():
    """执行 kvs 命令的测试套件。"""
    # 创建一个临时目录作为 XDG_DATA_HOME
    temp_dir = tempfile.mkdtemp()
    print(f"--- 测试开始 ---")
    print(f"将使用临时数据目录: {temp_dir}")

    try:
        # --- 测试用例定义 ---

        print("\n--- 测试 1: 添加新命令 'mycmd' ---")
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["add", "mycmd", "我的命令", "echo 'hello kvs'", "一个简单的测试命令", "--tags", "test,simple"])
        assert "成功添加" in stdout and retcode == 0, f"测试失败: 无法添加命令。Stdout: {stdout}, Stderr: {stderr}"
        db_content = get_db_content(temp_dir)
        assert "mycmd" in db_content and db_content["mycmd"]["name"] == "我的命令", "测试失败: 命令未正确添加到数据库。"
        print("测试 1: 通过。")

        print("\n--- 测试 2: 为 'mycmd' 添加另一个用法 ---")
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["add", "mycmd", "我的命令", "echo 'world kvs'", "另一个测试用法"])
        assert "成功添加" in stdout and retcode == 0, f"测试失败: 无法添加用法。Stdout: {stdout}, Stderr: {stderr}"
        db_content = get_db_content(temp_dir)
        assert len(db_content["mycmd"]["examples"]) == 2, "测试失败: 用法数量不正确。"
        print("测试 2: 通过。")

        print("\n--- 测试 3: 列出所有命令 (kvs list) ---")
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["list"])
        assert "mycmd" in stdout and "我的命令" in stdout and retcode == 0, f"测试失败: 列出所有命令失败。Stdout: {stdout}, Stderr: {stderr}"
        print("测试 3: 通过。")

        print("\n--- 测试 4: 列出特定命令的详细信息 (kvs list mycmd) ---")
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["list", "mycmd"])
        assert "echo 'hello kvs'" in stdout and "echo 'world kvs'" in stdout and retcode == 0, f"测试失败: 列出特定命令失败。Stdout: {stdout}, Stderr: {stderr}"
        print("测试 4: 通过。")
        
        print("\n--- 测试 5: 使用交互模式添加命令 'intercmd' ---")
        # 模拟交互式输入: 命令名\n中文名\n用法示例\n备注说明\n标签\n
        interactive_add_input = "intercmd\n交互命令\ninter_usage\n交互备注\ninteractive,test\n"
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["add", "--interactive"], input_str=interactive_add_input)
        assert "成功添加" in stdout and retcode == 0, f"测试失败: 交互式添加命令失败。Stdout: {stdout}, Stderr: {stderr}"
        db_content = get_db_content(temp_dir)
        assert "intercmd" in db_content and db_content["intercmd"]["name"] == "交互命令", "测试失败: 交互式命令未正确添加。"
        print("测试 5: 通过。")

        print("\n--- 测试 6: 更新命令 'mycmd' 的中文名 ---")
        # 修正: 添加 'name' 参数，明确指定更新类型
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["update", "name", "mycmd", "全新的我的命令"])
        # 修正断言条件，匹配实际输出文本
        assert "的中文名已更新为" in stdout and retcode == 0, f"测试失败: 无法更新命令中文名。Stdout: {stdout}, Stderr: {stderr}"
        db_content = get_db_content(temp_dir)
        assert db_content["mycmd"]["name"] == "全新的我的命令", "测试失败: 命令中文名未更新。"
        print("测试 6: 通过。")

        print("\n--- 测试 7: 更新命令 'mycmd' 的标签 ---")
        # 修正: 使用 'update tag'，与 'update name' 保持一致
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["update", "tag", "mycmd", "updated,tag"])
        # 修正断言条件，匹配实际输出文本
        assert "的标签已更新为" in stdout and retcode == 0, f"测试失败: 无法更新命令标签。Stdout: {stdout}, Stderr: {stderr}"
        db_content = get_db_content(temp_dir)
        assert "updated" in db_content["mycmd"]["tags"] and "tag" in db_content["mycmd"]["tags"], "测试失败: 命令标签未更新。"
        print("测试 7: 通过。")

        print("\n--- 测试 8: 查找用法关键词 'world' ---")
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["find", "world"])
        assert "mycmd" in stdout and "echo 'world kvs'" in stdout and retcode == 0, f"测试失败: 关键词查找失败。Stdout: {stdout}, Stderr: {stderr}"
        print("测试 8: 通过。")

        print("\n--- 测试 9: 编辑 'mycmd' 的用法 (序号 0) ---")
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["edit", "mycmd", "0", "--new-usage", "echo 'edited kvs'", "--new-note", "修改过的备注 kvs"])
        # 修正断言条件，匹配实际输出文本
        assert "已成功编辑" in stdout and retcode == 0, f"测试失败: 无法编辑用法。Stdout: {stdout}, Stderr: {stderr}"
        db_content = get_db_content(temp_dir)
        assert db_content["mycmd"]["examples"][0]["usage"] == "echo 'edited kvs'", "测试失败: 用法未被编辑。"
        assert db_content["mycmd"]["examples"][0]["note"] == "修改过的备注 kvs", "测试失败: 备注未被编辑。"
        print("测试 9: 通过。")
        
        print("\n--- 测试 10: 复制 'mycmd' 的用法 (序号 0) ---")
        # 复制命令通常只打印到剪贴板，很难直接验证，这里只检查返回码
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["copy", "mycmd", "0"])
        assert retcode == 0, f"测试失败: 复制命令失败。Stdout: {stdout}, Stderr: {stderr}"
        print("测试 10: 通过。(只检查了返回码)")

        print("\n--- 测试 11: 导出命令数据 ---")
        export_file_path = os.path.join(temp_dir, "exported_commands.json")
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["export", export_file_path])
        assert "成功导出" in stdout and retcode == 0, f"测试失败: 无法导出命令。Stdout: {stdout}, Stderr: {stderr}"
        assert os.path.exists(export_file_path), "测试失败: 导出文件未创建。"
        with open(export_file_path, 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
        assert "mycmd" in exported_data and "intercmd" in exported_data, "测试失败: 导出数据不完整。"
        print("测试 11: 通过。")


        print("\n--- 测试 12: 交互式删除 'intercmd' 命令 (包括其用法) ---")
        # 模拟交互式输入: 主命令名\n用法序号或关键词\n确认\n
        interactive_delete_input = "intercmd\n0\ny\n"
        stdout, stderr, retcode = run_kvs_command(temp_dir, ["delete", "--interactive"], input_str=interactive_delete_input)
        assert "已删除" in stdout and retcode == 0, f"测试失败: 交互式删除失败。Stdout: {stdout}, Stderr: {stderr}"
        db_content = get_db_content(temp_dir)
        assert "intercmd" not in db_content, "测试失败: 交互式删除未移除命令。"
        print("测试 12: 通过。")

        print("\n--- 所有测试通过！ ---")

    except AssertionError as e:
        print(f"\n!!! 测试失败: {e}")
    except Exception as e:
        print(f"\n!!! 发生未预期错误: {e}")
    finally:
        # 清理临时目录
        print(f"\n正在清理临时数据目录: {temp_dir}")
        shutil.rmtree(temp_dir)
        print("--- 测试结束 ---")

if __name__ == "__main__":
    run_tests()
