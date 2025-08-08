# src/cli.py
import sys
import argparse
import pyperclip # pip install pyperclip
from rich.prompt import Prompt, Confirm # From rich library
from rich.console import Console # For simple messages
from rich.panel import Panel # 新增这行


from src.db import load_db, save_db
from src.core import (
    add_command, update_command_name, update_command_tags, delete_usage, 
    find_commands, get_command_examples, get_usage_by_index, edit_usage,
    import_data, export_data
)
from src.display import (
    show_main_cmds, show_cmd_examples, show_add_result, show_find_results, 
    show_help, show_success, show_warning, show_error, console
)

def main():
    parser = argparse.ArgumentParser(
        description="KVS: A local command dictionary with rich terminal output.",
        formatter_class=argparse.RawTextHelpFormatter, # Preserve formatting for help
        add_help=False # We'll handle help manually
    )

    # Global options
    parser.add_argument('-h', '--help', action='store_true', 
                        help='Show this help message and exit.')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # --- list command ---
    list_parser = subparsers.add_parser('list', help='List commands or usages', add_help=False)
    list_parser.add_argument('cmd_name', nargs='?', help='Specific command to list examples for.')
    
    # --- add command ---
    add_parser = subparsers.add_parser('add', help='Add a new command or usage', add_help=False)
    add_parser.add_argument('cmd', nargs='?', help='Main command name (e.g., "git")')
    add_parser.add_argument('name', nargs='?', help='Chinese name/description (e.g., "版本管理")')
    add_parser.add_argument('usage', nargs='?', help='Usage example (e.g., "git commit -m")')
    add_parser.add_argument('note', nargs='?', help='Optional note/remark')
    add_parser.add_argument('--tags', type=str, help='Comma-separated tags (e.g., "dev,git,basic")')
    add_parser.add_argument('--interactive', '-i', action='store_true', 
                            help='Enter interactive mode for adding command.')

    # --- update command ---
    update_parser = subparsers.add_parser('update', help='Update command properties', add_help=False)
    update_subparsers = update_parser.add_subparsers(dest='update_type', required=True)

    # update name
    update_name_parser = update_subparsers.add_parser('name', help='Update Chinese name of a command')
    update_name_parser.add_argument('cmd', help='Main command name')
    update_name_parser.add_argument('new_name', help='New Chinese name')

    # update tags
    update_tags_parser = update_subparsers.add_parser('tag', help='Update tags of a command')
    update_tags_parser.add_argument('cmd', help='Main command name')
    update_tags_parser.add_argument('new_tags', type=str, help='New comma-separated tags (e.g., "dev,git")')

    # --- delete command ---
    delete_parser = subparsers.add_parser('delete', help='Delete a command usage or command', add_help=False)
    delete_parser.add_argument('cmd', nargs='?', help='Main command name')
    delete_parser.add_argument('identifier', nargs='?', 
                               help='Usage index (e.g., 0) or keyword (e.g., "checkout")')
    delete_parser.add_argument('--interactive', '-i', action='store_true', 
                               help='Enter interactive mode for deleting usage.')
    
    # --- edit command ---
    edit_parser = subparsers.add_parser('edit', help='Edit an existing command usage', add_help=False)
    edit_parser.add_argument('cmd', nargs='?', help='Main command name')
    edit_parser.add_argument('index', type=int, nargs='?', help='Index of the usage to edit')
    edit_parser.add_argument('--new-usage', help='New usage string')
    edit_parser.add_argument('--new-note', help='New note string')
    edit_parser.add_argument('--interactive', '-i', action='store_true', 
                             help='Enter interactive mode for editing usage.')

    # --- find command ---
    find_parser = subparsers.add_parser('find', help='Find commands by keyword', add_help=False)
    find_parser.add_argument('keywords', nargs='+', help='Keywords to search for')

    # --- copy command ---
    copy_parser = subparsers.add_parser('copy', help='Copy a command usage to clipboard', add_help=False)
    copy_parser.add_argument('cmd', help='Main command name')
    copy_parser.add_argument('index', type=int, nargs='?', default=0, 
                             help='Index of the usage to copy (default: 0)')

    # --- import command ---
    import_parser = subparsers.add_parser('import', help='Import commands from a JSON file', add_help=False)
    import_parser.add_argument('file_path', help='Path to the JSON file to import')
    import_parser.add_argument('--overwrite', action='store_true', 
                               help='Overwrite existing commands with imported ones (default: merge usages)')
    
    # --- export command ---
    export_parser = subparsers.add_parser('export', help='Export commands to a JSON file', add_help=False)
    export_parser.add_argument('file_path', help='Path to the JSON file to export to')


    args = parser.parse_args()
    
    if args.help or not sys.argv[1:]: # Show help if -h/--help or no arguments given
        show_help()
        return

    db = load_db()

    try:
        if args.command == 'list':
            if args.cmd_name:
                show_cmd_examples(db, args.cmd_name)
            else:
                show_main_cmds(db)

        elif args.command == 'add':
            cmd, name, usage, note, tags_list = None, None, None, None, None
            
            if args.interactive or not (args.cmd and args.name and args.usage):
                console.print(Panel("[bold yellow]进入交互式添加模式[/bold yellow]", border_style="yellow"))
                cmd = Prompt.ask("主命令 (例如: [green]git[/green])")
                if not cmd: raise ValueError("主命令不能为空。")
                name = Prompt.ask("中文名 (例如: [green]版本管理[/green])", default="")
                usage = Prompt.ask("用法示例 (例如: [green]git pull --rebase[/green])")
                if not usage: raise ValueError("用法示例不能为空。")
                note = Prompt.ask("备注说明 (可选)", default="")
                tags_str = Prompt.ask("标签 (逗号分隔, 例如: [green]dev,version[/green])", default="")
                if tags_str: tags_list = [t.strip() for t in tags_str.split(',') if t.strip()]
            else:
                cmd, name, usage, note = args.cmd, args.name, args.usage, args.note
                if args.tags:
                    tags_list = [t.strip() for t in args.tags.split(',') if t.strip()]

            cmd_data, index = add_command(db, cmd, name, usage, note, tags_list)
            save_db(db)
            show_success(f"已成功添加 '{cmd}' 的新用法！")
            show_add_result(cmd, cmd_data, usage, note, index)

        elif args.command == 'update':
            if args.update_type == 'name':
                if update_command_name(db, args.cmd, args.new_name):
                    save_db(db)
                    show_success(f"'{args.cmd}' 的中文名已更新为：[bold]{args.new_name}[/bold]")
                else:
                    show_error(f"未找到主命令：'{args.cmd}'")
            elif args.update_type == 'tag':
                tags_list = [t.strip() for t in args.new_tags.split(',') if t.strip()]
                if update_command_tags(db, args.cmd, tags_list):
                    save_db(db)
                    show_success(f"'{args.cmd}' 的标签已更新为：[bold]{', '.join(tags_list)}[/bold]")
                else:
                    show_error(f"未找到主命令：'{args.cmd}'")

        elif args.command == 'delete':
            cmd, identifier = args.cmd, args.identifier
            if args.interactive or not (cmd and identifier is not None):
                console.print(Panel("[bold yellow]进入交互式删除模式[/bold yellow]", border_style="yellow"))
                cmd = Prompt.ask("要删除用法的[green]主命令[/green]")
                if cmd not in db:
                    show_error(f"未找到主命令：'{cmd}'")
                    return
                show_cmd_examples(db, cmd) # Show current examples
                identifier = Prompt.ask("要删除的用法[green]序号[/green] (或[green]关键词[/green]模糊删除, 'q' 退出)", default="q")
                if identifier == 'q':
                    show_warning("已取消删除操作。")
                    return
                try:
                    identifier = int(identifier) # Try converting to int for index deletion
                except ValueError:
                    pass # Keep as string for keyword deletion
            
            if cmd not in db:
                show_error(f"未找到主命令：'{cmd}'")
                return

            # Confirm before deleting
            usage_to_delete = None
            if isinstance(identifier, int):
                usage_obj = get_usage_by_index(db, cmd, identifier)
                if usage_obj:
                    usage_to_delete = usage_obj.get('usage', '未知用法')
            elif isinstance(identifier, str):
                # For keyword, we need to find it first to show confirmation
                found_usages = [ex for ex in db[cmd].get('examples', []) 
                                if identifier.lower() in ex.get('usage', '').lower() or identifier.lower() in ex.get('note', '').lower()]
                if found_usages:
                    usage_to_delete = found_usages[0].get('usage', '未知用法') # Just show the first match for confirmation
            
            if usage_to_delete and not Confirm.ask(f"确认删除 '{cmd}' 的用法: [cyan]{usage_to_delete}[/cyan] 吗？", default=False):
                show_warning("已取消删除操作。")
                return

            removed_data, command_deleted = delete_usage(db, cmd, identifier)
            if removed_data:
                save_db(db)
                show_success(f"已删除 '{cmd}' 的用法: [cyan]{removed_data.get('usage','')}[/cyan] (备注: {removed_data.get('note','')})")
                if command_deleted:
                    show_warning(f"主命令 '{cmd}' 已无用法，已自动移除主命令。")
            else:
                show_error(f"删除失败。未找到主命令 '{cmd}' 或其用法 '{identifier}'。")

        elif args.command == 'edit':
            cmd, index, new_usage, new_note = args.cmd, args.index, args.new_usage, args.new_note

            if args.interactive or not (cmd and index is not None):
                console.print(Panel("[bold yellow]进入交互式编辑模式[/bold yellow]", border_style="yellow"))
                cmd = Prompt.ask("要编辑用法的[green]主命令[/green]")
                if cmd not in db:
                    show_error(f"未找到主命令：'{cmd}'")
                    return
                show_cmd_examples(db, cmd) # Show current examples
                index = Prompt.ask("要编辑的用法[green]序号[/green]", default=None)
                try:
                    index = int(index)
                except (ValueError, TypeError):
                    show_error("序号必须为数字。")
                    return
                
                current_usage_obj = get_usage_by_index(db, cmd, index)
                if not current_usage_obj:
                    show_error(f"未找到主命令 '{cmd}' 的序号为 {index} 的用法。")
                    return
                
                new_usage = Prompt.ask(f"新用法示例 (当前: [cyan]{current_usage_obj.get('usage','')}[/cyan])", 
                                       default=current_usage_obj.get('usage',''))
                new_note = Prompt.ask(f"新备注说明 (当前: [grey70]{current_usage_obj.get('note','')}[/grey70])", 
                                      default=current_usage_obj.get('note',''))
            
            if cmd not in db:
                show_error(f"未找到主命令：'{cmd}'")
                return
            
            if edit_usage(db, cmd, index, new_usage, new_note):
                save_db(db)
                show_success(f"已成功编辑 '{cmd}' 的第 {index} 条用法！")
                show_cmd_examples(db, cmd) # Show updated examples
            else:
                show_error(f"编辑失败。未找到主命令 '{cmd}' 或序号 {index}。")

        elif args.command == 'find':
            query = " ".join(args.keywords)
            results = find_commands(db, query)
            show_find_results(results, query)

        elif args.command == 'copy':
            cmd_data = db.get(args.cmd)
            if not cmd_data:
                show_error(f"未找到主命令：'{args.cmd}'")
                return
            
            examples = cmd_data.get('examples', [])
            if not examples:
                show_error(f"主命令 '{args.cmd}' 暂无用法示例。")
                return

            if not (0 <= args.index < len(examples)):
                show_error(f"用法序号 {args.index} 超出范围。'{args.cmd}' 共有 {len(examples)} 个用法 (0-{len(examples)-1})。")
                return
            
            usage_to_copy = examples[args.index]['usage']
            try:
                pyperclip.copy(usage_to_copy)
                show_success(f"用法 '[cyan]{usage_to_copy}[/cyan]' 已复制到剪贴板！")
            except pyperclip.PyperclipException as e:
                show_error(f"复制到剪贴板失败: {e}\n请确保您的系统安装了剪贴板工具（例如 Linux 上的 xclip 或 xsel）。")

        elif args.command == 'import':
            try:
                updated_db, new_cmd_count, merged_count = import_data(db, args.file_path, args.overwrite)
                save_db(updated_db)
                show_success(f"数据已从 '{args.file_path}' 成功导入！\n新增主命令: {new_cmd_count}，合并/更新用法: {merged_count}。")
                if not args.overwrite:
                    show_warning("注意：导入时未覆盖现有命令，而是合并了用法。")
            except FileNotFoundError as e:
                show_error(f"导入失败: {e}")
            except ValueError as e:
                show_error(f"导入失败: {e}")
            except Exception as e:
                show_error(f"导入过程中发生错误: {e}")

        elif args.command == 'export':
            try:
                if export_data(db, args.file_path):
                    show_success(f"数据已成功导出到 '{args.file_path}'！")
            except Exception as e:
                show_error(f"导出失败: {e}")

    except KeyboardInterrupt:
        console.print("\n[yellow]操作已取消。[/yellow]")
    except ValueError as e:
        show_error(f"参数错误: {e}")
    except Exception as e:
        show_error(f"发生未知错误: {e}")

if __name__ == "__main__":
    main()
