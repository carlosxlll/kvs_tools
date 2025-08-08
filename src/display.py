# src/display.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def show_main_cmds(db: dict):
    if not db:
        console.print()
        console.print(Panel("[grey70]暂无收录任何主命令，可以用 'kvs add' 新增。[/grey70]", border_style="yellow"))
        console.print()
        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        row_styles=["none","#232323"],
        box=box.SIMPLE,
        title="[bold]命令主目录[/bold]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("命令", style="bold green", no_wrap=False)
    table.add_column("中文名", style="white")
    table.add_column("用法数量", style="grey70", justify="right")
    table.add_column("标签", style="blue") # 新增标签列

    for cmd, v in db.items():
        name = v.get('name', "")
        usage_len = len(v.get("examples", []))
        tags = ", ".join(v.get("tags", [])) # 获取并格式化标签
        table.add_row(cmd, name or "-", str(usage_len), tags or "-")

    console.print()
    console.print(table)
    console.print()

def show_cmd_examples(db: dict, cmd: str):
    if cmd not in db:
        console.print()
        console.print(Panel(f"[red]未找到主命令：'{cmd}'[/red]\n请检查拼写，或用 'kvs add' 添加新命令。", border_style="red"))
        console.print()
        return

    v = db[cmd]
    name = v.get("name", "")
    exs = v.get("examples", [])
    if not exs:
        console.print()
        console.print(Panel(f"[yellow]主命令 '{cmd}'（{name or '无中文名'}）暂无用法示例。[/yellow]\n可用 'kvs add' 补充。", border_style="yellow"))
        console.print()
        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        row_styles=["none","#202020"],
        box=box.SIMPLE,
        title=f"[bold]{cmd} 用法列表 ({name or '无中文名'})[/bold]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("序号", style="grey42", justify="left", no_wrap=False)
    table.add_column("用法示例", style="white", no_wrap=False)
    table.add_column("备注说明", style="grey70", no_wrap=False)

    for idx, ex in enumerate(exs):
        table.add_row(str(idx), ex.get("usage",""), ex.get("note",""))

    console.print()
    console.print(table)
    console.print()

def show_add_result(cmd: str, cmd_data: dict, usage: str, note: str, index: int):
    table = Table(
        show_header=True,
        header_style="bold cyan",
        row_styles=["none","#232323"],
        box=box.SIMPLE,
        title=f"[bold]已添加的命令用法[/bold]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("主命令", style="bold green", no_wrap=False)
    table.add_column("中文名", style="white")
    table.add_column("用法示例", style="cyan")
    table.add_column("备注说明", style="grey70")
    table.add_column("序号", style="grey42", justify="right")

    table.add_row(cmd, cmd_data.get('name', ''), usage, note, str(index))
    console.print()
    console.print(table)
    console.print()

def show_find_results(results: list, query: str):
    if not results:
        console.print()
        console.print(Panel(f"[yellow]未找到包含关键词 '{query}' 的任何主命令或用法。[/yellow]", border_style="yellow"))
        console.print()
        return

    table = Table(
        show_header=True,
        header_style="bold cyan",
        row_styles=["none","#191919"],
        box=box.SIMPLE,
        title=f"[bold]关键词“{query}”查找结果[/bold]",
        pad_edge=True,
        expand=True,
        padding=(0,2),
    )
    table.add_column("主命令", style="bold green")
    table.add_column("中文名", style="white")
    table.add_column("序号", style="grey42", justify="left")
    table.add_column("用法示例", style="cyan")
    table.add_column("备注说明", style="grey70")

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
    title = "[bold deep_sky_blue1]kvs 本地命令词典（多用法彩色显示）[/bold deep_sky_blue1]"
    console.print(Panel(title, expand=False, border_style="deep_sky_blue1"))
    console.print("[bold yellow]常用操作：[/bold yellow]")
    console.print("[bold green]  kvs list[/bold green][white]            查看全部主命令及说明[/white]")
    console.print("[bold green]  kvs list <命令>[/bold green][white]     查看某主命令的全部用法示例[/white]")
    console.print("[bold green]  kvs add ...[/bold green][white]         新增主命令和用法（或为已有命令新增用法）[/white]")
    console.print("[bold green]  kvs update ...[/bold green][white]      修改主命令的中文说明[/white]")
    console.print("[bold green]  kvs update-tag ...[/bold green][white]  修改主命令的标签[/white]")
    console.print("[bold green]  kvs delete ...[/bold green][white]      删除某命令下指定用法（根据序号或关键词）[/white]")
    console.print("[bold green]  kvs edit ...[/bold green][white]        编辑某命令下指定用法[/white]")
    console.print("[bold green]  kvs find ...[/bold green][white]        关键词模糊查找命令与用法（支持中英文）[/white]")
    console.print("[bold green]  kvs copy ...[/bold green][white]        复制用法到剪贴板[/white]")
    console.print("[bold green]  kvs import/export ...[/bold green][white] 导入/导出命令数据[/white]")
    console.print("")
    console.print("[bold yellow]示例：[/bold yellow]")
    eg = Text()
    eg.append("  kvs add ls \"列文件\" \"ls -l\" \"详细显示\" --tags file,basic\n", "cyan")
    eg.append("  kvs add git --interactive\n", "cyan") # 交互式示例
    eg.append("  kvs list\n", "cyan")
    eg.append("  kvs list git\n", "cyan")
    eg.append("  kvs update ls \"文件列表\"\n", "cyan")
    eg.append("  kvs update-tag git dev,version\n", "cyan")
    eg.append("  kvs delete git 0\n", "cyan")
    eg.append("  kvs delete git --interactive\n", "cyan") # 交互式删除示例
    eg.append("  kvs edit git 1 --new-usage \"git branch -a\"\n", "cyan")
    eg.append("  kvs find 分支\n", "cyan")
    eg.append("  kvs copy git 0\n", "cyan")
    eg.append("  kvs export ~/kvs_backup.json\n", "cyan")
    console.print(eg)
    console.print("[bold magenta]Tip：[/bold magenta][grey50]命令词典保存在符合XDG规范的目录下，请注意备份。[/grey50]")
    console.print("\n[grey70]支持中文、模糊查找；适合个人高效管理常用命令。[/grey70]\n")

def show_success(message: str):
    console.print(Panel(f"[green]{message}[/green]", border_style="green"))

def show_warning(message: str):
    console.print(Panel(f"[yellow]{message}[/yellow]", border_style="yellow"))

def show_error(message: str):
    console.print(Panel(f"[red]{message}[/red]", border_style="red"))

