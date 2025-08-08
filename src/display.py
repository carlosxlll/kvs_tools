from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from .db import get_theme_setting, save_theme_setting

console = Console()

# 重新设计的颜色方案 - 更加鲜明的差异
COLOR_SCHEMES = {
    "default": {
        "even_row": "#2a2a2a",
        "header": "bold cyan",
        "title": "bold white",
        "main_command": "bold green",
        "command_name": "white",
        "usage_count": "grey70",
        "tags": "blue",
        "usage": "cyan",
        "note": "grey70",
        "index": "grey42",
        "success": "green",
        "warning": "yellow", 
        "error": "red",
        "help_title": "bold deep_sky_blue1",
        "help_operation": "bold yellow",
        "help_command": "bold green",
        "help_desc": "white",
        "help_example": "cyan",
        "help_tip": "bold magenta",
        "help_tip_text": "grey50",
        "panel_border_success": "green",
        "panel_border_warning": "yellow",
        "panel_border_error": "red",
        "panel_border_help": "deep_sky_blue1"
    },
    "dark": {
        # 深色主题 - 更亮的颜色，强烈对比
        "even_row": "#1a1a2e",
        "header": "bold bright_magenta",
        "title": "bold bright_yellow",
        "main_command": "bold bright_green",
        "command_name": "bright_white",
        "usage_count": "bright_blue",
        "tags": "bright_cyan",
        "usage": "bright_yellow",
        "note": "bright_white",
        "index": "bright_red",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "help_title": "bold bright_magenta",
        "help_operation": "bold bright_cyan",
        "help_command": "bold bright_green",
        "help_desc": "bright_white",
        "help_example": "bright_yellow",
        "help_tip": "bold bright_red",
        "help_tip_text": "bright_blue",
        "panel_border_success": "bright_green",
        "panel_border_warning": "bright_yellow",
        "panel_border_error": "bright_red",
        "panel_border_help": "bright_magenta"
    },
    "light": {
        # 浅色主题 - 深色字体，适合浅色背景
        "even_row": "#f8f8f8",
        "header": "bold blue",
        "title": "bold black",
        "main_command": "bold dark_green",
        "command_name": "black",
        "usage_count": "dark_blue",
        "tags": "purple",
        "usage": "dark_cyan",
        "note": "grey37",
        "index": "red",
        "success": "dark_green",
        "warning": "dark_orange",
        "error": "dark_red",
        "help_title": "bold blue",
        "help_operation": "bold dark_orange",
        "help_command": "bold dark_green",
        "help_desc": "black",
        "help_example": "dark_cyan",
        "help_tip": "bold purple",
        "help_tip_text": "grey37",
        "panel_border_success": "dark_green",
        "panel_border_warning": "dark_orange",
        "panel_border_error": "dark_red",
        "panel_border_help": "blue"
    },
    "neon": {
        # 霓虹主题 - 非常鲜艳的颜色
        "even_row": "#0a0a0a",
        "header": "bold magenta",
        "title": "bold bright_yellow",
        "main_command": "bold bright_green",
        "command_name": "bright_magenta",
        "usage_count": "bright_cyan",
        "tags": "bright_blue",
        "usage": "bright_yellow",
        "note": "bright_white",
        "index": "bright_red",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "help_title": "bold bright_magenta",
        "help_operation": "bold bright_yellow",
        "help_command": "bold bright_green",
        "help_desc": "bright_cyan",
        "help_example": "bright_yellow",
        "help_tip": "bold bright_red",
        "help_tip_text": "bright_blue",
        "panel_border_success": "bright_green",
        "panel_border_warning": "bright_yellow",
        "panel_border_error": "bright_red",
        "panel_border_help": "bright_magenta"
    },
    "ocean": {
        # 海洋主题 - 蓝绿色系
        "even_row": "#001122",
        "header": "bold cyan",
        "title": "bold bright_cyan",
        "main_command": "bold sea_green2",
        "command_name": "turquoise2",
        "usage_count": "sky_blue1",
        "tags": "medium_turquoise",
        "usage": "pale_turquoise1",
        "note": "light_cyan1",
        "index": "aquamarine1",
        "success": "sea_green2",
        "warning": "light_goldenrod1",
        "error": "light_coral",
        "help_title": "bold bright_cyan",
        "help_operation": "bold light_goldenrod1",
        "help_command": "bold sea_green2",
        "help_desc": "light_cyan1",
        "help_example": "pale_turquoise1",
        "help_tip": "bold medium_turquoise",
        "help_tip_text": "sky_blue1",
        "panel_border_success": "sea_green2",
        "panel_border_warning": "light_goldenrod1",
        "panel_border_error": "light_coral",
        "panel_border_help": "bright_cyan"
    },
    "rainbow": {
        # 彩虹主题 - 每种元素不同颜色
        "even_row": "#1a1a2e",
        "header": "bold red",
        "title": "bold yellow",
        "main_command": "bold green",
        "command_name": "blue",
        "usage_count": "magenta",
        "tags": "cyan",
        "usage": "bright_yellow",
        "note": "bright_white",
        "index": "bright_red",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "help_title": "bold bright_blue",
        "help_operation": "bold bright_magenta",
        "help_command": "bold bright_green",
        "help_desc": "bright_cyan",
        "help_example": "bright_yellow",
        "help_tip": "bold bright_red",
        "help_tip_text": "bright_white",
        "panel_border_success": "bright_green",
        "panel_border_warning": "bright_yellow",
        "panel_border_error": "bright_red",
        "panel_border_help": "bright_blue"
    }
}
# 修改 _current_scheme 初始化
try:
    _current_scheme = get_theme_setting()
except Exception:
    _current_scheme = "default"

def set_color_scheme(scheme_name: str):
    """设置颜色方案并保存"""
    global _current_scheme
    if scheme_name in COLOR_SCHEMES:
        _current_scheme = scheme_name
        save_theme_setting(scheme_name)  # 保存到配置文件
        return True
    return False

def get_color(color_key: str) -> str:
    """获取当前颜色方案中的指定颜色"""
    return COLOR_SCHEMES[_current_scheme].get(color_key, "white")

def get_current_scheme() -> str:
    """获取当前使用的颜色方案名称"""
    return _current_scheme

def list_color_schemes() -> list:
    """获取所有可用的颜色方案"""
    return list(COLOR_SCHEMES.keys())

def show_main_cmds(db: dict):
    if not db:
        console.print()
        console.print(Panel("[grey70]暂无收录任何主命令，可以用 'kvs add' 新增。[/grey70]", border_style=get_color("panel_border_warning")))
        console.print()
        return

    table = Table(
        show_header=True,
        header_style=get_color("header"),
        # row_styles=["none", get_color("even_row")],
        box=box.SIMPLE,
        title=f"[{get_color('title')}]命令主目录[/{get_color('title')}]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("命令", style=get_color("main_command"), no_wrap=False)
    table.add_column("中文名", style=get_color("command_name"))
    table.add_column("用法数量", style=get_color("usage_count"), justify="right")
    table.add_column("标签", style=get_color("tags"))

    for cmd, v in db.items():
        name = v.get('name', "")
        usage_len = len(v.get("examples", []))
        tags = ", ".join(v.get("tags", []))
        table.add_row(cmd, name or "-", str(usage_len), tags or "-")

    console.print()
    console.print(table)
    console.print(f"\n[{get_color('help_tip_text')}]当前主题: {_current_scheme}[/{get_color('help_tip_text')}]")
    console.print()

def show_cmd_examples(db: dict, cmd: str):
    if cmd not in db:
        console.print()
        console.print(Panel(f"[{get_color('error')}]未找到主命令：'{cmd}'[/{get_color('error')}]\n请检查拼写，或用 'kvs add' 添加新命令。", border_style=get_color("panel_border_error")))
        console.print()
        return

    v = db[cmd]
    name = v.get("name", "")
    exs = v.get("examples", [])
    if not exs:
        console.print()
        console.print(Panel(f"[{get_color('warning')}]主命令 '{cmd}'（{name or '无中文名'}）暂无用法示例。[/{get_color('warning')}]\n可用 'kvs add' 补充。", border_style=get_color("panel_border_warning")))
        console.print()
        return

    table = Table(
        show_header=True,
        header_style=get_color("header"),
        # row_styles=["none", get_color("even_row")],
        box=box.SIMPLE,
        title=f"[{get_color('title')}]{cmd} 用法列表 ({name or '无中文名'})[/{get_color('title')}]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("序号", style=get_color("index"), justify="left", no_wrap=False)
    table.add_column("用法示例", style=get_color("usage"), no_wrap=False)
    table.add_column("备注说明", style=get_color("note"), no_wrap=False)

    for idx, ex in enumerate(exs):
        table.add_row(str(idx), ex.get("usage",""), ex.get("note",""))

    console.print()
    console.print(table)
    console.print(f"\n[{get_color('help_tip_text')}]当前主题: {_current_scheme}[/{get_color('help_tip_text')}]")
    console.print()

def show_add_result(cmd: str, cmd_data: dict, usage: str, note: str, index: int):
    table = Table(
        show_header=True,
        header_style=get_color("header"),
        # row_styles=["none", get_color("even_row")],
        box=box.SIMPLE,
        title=f"[{get_color('title')}]已添加的命令用法[/{get_color('title')}]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("主命令", style=get_color("main_command"), no_wrap=False)
    table.add_column("中文名", style=get_color("command_name"))
    table.add_column("用法示例", style=get_color("usage"))
    table.add_column("备注说明", style=get_color("note"))
    table.add_column("序号", style=get_color("index"), justify="right")

    table.add_row(cmd, cmd_data.get('name', ''), usage, note, str(index))
    console.print()
    console.print(table)
    console.print()

def show_find_results(results: list, query: str):
    if not results:
        console.print()
        console.print(Panel(f"[{get_color('warning')}]未找到包含关键词 '{query}' 的任何主命令或用法。[/{get_color('warning')}]", border_style=get_color("panel_border_warning")))
        console.print()
        return

    table = Table(
        show_header=True,
        header_style=get_color("header"),
        # row_styles=["none", get_color("even_row")],
        box=box.SIMPLE,
        title=f"[{get_color('title')}]关键词'{query}'查找结果[/{get_color('title')}]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("主命令", style=get_color("main_command"))
    table.add_column("中文名", style=get_color("command_name"))
    table.add_column("序号", style=get_color("index"), justify="left")
    table.add_column("用法示例", style=get_color("usage"))
    table.add_column("备注说明", style=get_color("note"))

    for row in results:
        cmd, name, idx, usage, note = row
        # 简单高亮，如果需要更复杂的正则高亮，可以结合re模块
        highlighted_usage = usage.replace(query, f"[bold yellow]{query}[/bold yellow]")
        highlighted_note = note.replace(query, f"[bold yellow]{query}[/bold yellow]")
        table.add_row(cmd, name, str(idx), highlighted_usage, highlighted_note)

    console.print()
    console.print(table)
    console.print()

def show_help():
    """显示简洁的帮助信息"""
    title = f"[{get_color('help_title')}]kvs 本地命令词典[/{get_color('help_title')}]"
    console.print(Panel(title, expand=False, border_style=get_color("panel_border_help")))
    
    console.print(f"[{get_color('help_operation')}]常用命令：[/{get_color('help_operation')}]")
    console.print(f"[{get_color('help_command')}]  kvs list[/{get_color('help_command')}][{get_color('help_desc')}]              查看全部命令[/{get_color('help_desc')}]")
    console.print(f"[{get_color('help_command')}]  kvs list <命令>[/{get_color('help_command')}][{get_color('help_desc')}]       查看命令用法[/{get_color('help_desc')}]")
    console.print(f"[{get_color('help_command')}]  kvs add[/{get_color('help_command')}][{get_color('help_desc')}]               添加命令用法[/{get_color('help_desc')}]")
    console.print(f"[{get_color('help_command')}]  kvs find <关键词>[/{get_color('help_command')}][{get_color('help_desc')}]     搜索命令[/{get_color('help_desc')}]")
    console.print(f"[{get_color('help_command')}]  kvs theme <主题名>[/{get_color('help_command')}][{get_color('help_desc')}]    切换主题[/{get_color('help_desc')}]")
    console.print()
    console.print(f"[{get_color('help_tip')}]更多命令：[/{get_color('help_tip')}][{get_color('help_tip_text')}]kvs examples[/{get_color('help_tip_text')}] | [{get_color('help_tip_text')}]当前主题: {_current_scheme}[/{get_color('help_tip_text')}]")
    console.print()

def show_examples():
    """显示详细的使用示例"""
    title = f"[{get_color('help_title')}]kvs 详细使用示例[/{get_color('help_title')}]"
    console.print(Panel(title, expand=False, border_style=get_color("panel_border_help")))
    
    console.print(f"[{get_color('help_operation')}]基础操作：[/{get_color('help_operation')}]")
    eg = Text()
    eg.append("  kvs add git \"版本控制\" \"git status\" \"查看状态\"\n", get_color("help_example"))
    eg.append("  kvs add --interactive                    # 交互式添加\n", get_color("help_example"))
    eg.append("  kvs list                                 # 查看所有命令\n", get_color("help_example"))
    eg.append("  kvs list git                             # 查看git用法\n", get_color("help_example"))
    console.print(eg)
    
    console.print(f"[{get_color('help_operation')}]管理操作：[/{get_color('help_operation')}]")
    eg2 = Text()
    eg2.append("  kvs update name git \"Git版本控制\"        # 更新中文名\n", get_color("help_example"))
    eg2.append("  kvs update tag git dev,version          # 更新标签\n", get_color("help_example"))
    eg2.append("  kvs edit git 0 --new-usage \"git log\"    # 编辑用法\n", get_color("help_example"))
    eg2.append("  kvs delete git 0                        # 删除用法\n", get_color("help_example"))
    console.print(eg2)
    
    console.print(f"[{get_color('help_operation')}]实用功能：[/{get_color('help_operation')}]")
    eg3 = Text()
    eg3.append("  kvs find 分支                            # 关键词搜索\n", get_color("help_example"))
    eg3.append("  kvs copy git 0                          # 复制到剪贴板\n", get_color("help_example"))
    eg3.append("  kvs export ~/backup.json                # 导出数据\n", get_color("help_example"))
    eg3.append("  kvs import ~/backup.json                # 导入数据\n", get_color("help_example"))
    console.print(eg3)
    
    console.print(f"[{get_color('help_operation')}]主题切换：[/{get_color('help_operation')}]")
    eg4 = Text()
    eg4.append("  kvs theme list                          # 查看所有主题\n", get_color("help_example"))
    eg4.append("  kvs theme neon                          # 切换霓虹主题\n", get_color("help_example"))
    eg4.append("  kvs theme demo                          # 演示当前主题\n", get_color("help_example"))
    console.print(eg4)
    
    console.print(f"\n[{get_color('help_tip')}]Tip：[/{get_color('help_tip')}][{get_color('help_tip_text')}]大部分命令支持 --interactive 进入交互模式[/{get_color('help_tip_text')}]")
    console.print()

def show_all_commands():
    """显示所有可用命令的简要说明"""
    title = f"[{get_color('help_title')}]kvs 完整命令列表[/{get_color('help_title')}]"
    console.print(Panel(title, expand=False, border_style=get_color("panel_border_help")))
    
    table = Table(
        show_header=True,
        header_style=get_color("header"),
        # row_styles=["none", get_color("even_row")],
        box=box.SIMPLE,
        pad_edge=True,
        expand=True,
        padding=(0,1),
    )
    table.add_column("命令", style=get_color("main_command"), width=20)
    table.add_column("说明", style=get_color("help_desc"))
    
    commands_info = [
        ("kvs list", "查看所有命令或指定命令的用法"),
        ("kvs add", "添加新命令或用法"),
        ("kvs find", "搜索命令和用法"),
        ("kvs copy", "复制用法到剪贴板"),
        ("kvs update name", "更新命令的中文名"),
        ("kvs update tag", "更新命令的标签"),
        ("kvs edit", "编辑现有用法"),
        ("kvs delete", "删除用法或命令"),
        ("kvs import", "从JSON文件导入数据"),
        ("kvs export", "导出数据到JSON文件"),
        ("kvs theme", "主题相关操作"),
        ("kvs examples", "查看详细使用示例"),
        ("kvs commands", "查看完整命令列表"),
    ]
    
    for cmd, desc in commands_info:
        table.add_row(cmd, desc)
    
    console.print()
    console.print(table)
    console.print(f"\n[{get_color('help_tip_text')}]使用 'kvs <命令> --help' 查看具体命令的详细说明[/{get_color('help_tip_text')}]")
    console.print()

def show_success(message: str):
    console.print(Panel(f"[{get_color('success')}]{message}[/{get_color('success')}]", border_style=get_color("panel_border_success")))

def show_warning(message: str):
    console.print(Panel(f"[{get_color('warning')}]{message}[/{get_color('warning')}]", border_style=get_color("panel_border_warning")))

def show_error(message: str):
    console.print(Panel(f"[{get_color('error')}]{message}[/{get_color('error')}]", border_style=get_color("panel_border_error")))

def show_color_schemes():
    """显示所有可用的颜色方案"""
    table = Table(
        show_header=True,
        header_style=get_color("header"),
        # row_styles=["none", get_color("even_row")],
        box=box.SIMPLE,
        title=f"[{get_color('title')}]可用颜色方案[/{get_color('title')}]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("方案名", style=get_color("main_command"))
    table.add_column("说明", style=get_color("command_name"))
    table.add_column("状态", style=get_color("tags"))
    table.add_column("预览", style="none")  # 不设置样式，让每行显示不同颜色
    
    scheme_descriptions = {
        "default": "默认方案，适合大多数终端",
        "dark": "深色方案，高亮颜色适合深色背景",
        "light": "浅色方案，深色字体适合浅色背景",
        "neon": "霓虹方案，非常鲜艳的颜色效果",
        "ocean": "海洋方案，蓝绿色系主题",
        "rainbow": "彩虹方案，每种元素不同颜色"
    }
    
    for scheme in COLOR_SCHEMES.keys():
        status = "✓ 当前使用" if scheme == _current_scheme else ""
        description = scheme_descriptions.get(scheme, "")
        
        # 使用该方案的颜色显示预览
        preview_colors = COLOR_SCHEMES[scheme]
        preview = f"[{preview_colors['main_command']}]命令[/{preview_colors['main_command']}] [{preview_colors['usage']}]用法[/{preview_colors['usage']}] [{preview_colors['tags']}]标签[/{preview_colors['tags']}]"
        
        table.add_row(scheme, description, status, preview)
    
    console.print()
    console.print(table)
    console.print()
    console.print(f"[{get_color('help_desc')}]使用 'kvs theme <方案名>' 切换颜色方案[/{get_color('help_desc')}]")

def show_theme_demo():
    """演示当前主题的所有颜色效果"""
    console.print(f"\n[{get_color('title')}]当前主题 '{_current_scheme}' 颜色演示[/{get_color('title')}]")
    
    # 创建演示表格
    table = Table(
        show_header=True,
        header_style=get_color("header"),
        # row_styles=["none", get_color("even_row")],
        box=box.SIMPLE,
        title=f"[{get_color('title')}]颜色效果演示[/{get_color('title')}]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("序号", style=get_color("index"))
    table.add_column("主命令", style=get_color("main_command"))
    table.add_column("中文名", style=get_color("command_name"))
    table.add_column("用法示例", style=get_color("usage"))
    table.add_column("备注说明", style=get_color("note"))
    table.add_column("标签", style=get_color("tags"))
    
    # 添加示例数据
    table.add_row("0", "git", "版本控制", "git commit -m 'message'", "提交更改", "dev,version")
    table.add_row("1", "docker", "容器管理", "docker run -it ubuntu", "运行容器", "container,deploy")
    table.add_row("2", "ls", "列出文件", "ls -la", "详细列表", "file,basic")
    
    console.print()
    console.print(table)
    
    # 显示面板效果
    console.print()
    show_success("这是成功消息的颜色效果")
    show_warning("这是警告消息的颜色效果")  
    show_error("这是错误消息的颜色效果")
    console.print()
