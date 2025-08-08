# src/core.py
from typing import List, Dict, Union
import json # 确保这行存在

from rich.prompt import Prompt, Confirm # 用于交互式输入

# 定义数据结构
# {
#   "cmd_name": {
#     "name": "中文名",
#     "tags": ["tag1", "tag2"],
#     "examples": [
#       {"usage": "usage string", "note": "note string"},
#       ...
#     ]
#   }
# }

def add_command(db: dict, cmd: str, name: str, usage: str, note: str, tags: List[str] = None) -> tuple[dict, int]:
    if cmd not in db:
        db[cmd] = {"name": name, "tags": [], "examples": []}
    
    # 如果提供了中文名且当前为空，则更新
    if name and not db[cmd]['name']:
        db[cmd]['name'] = name
    
    # 更新标签 (合并或覆盖，这里选择覆盖，如果需要合并可以再调整逻辑)
    if tags is not None:
        db[cmd]['tags'] = sorted(list(set(db[cmd].get('tags', []) + tags))) # 合并并去重排序
        
    db[cmd]["examples"].append({"usage": usage, "note": note})
    index = len(db[cmd]["examples"]) - 1
    return db[cmd], index

def update_command_name(db: dict, cmd: str, new_name: str) -> bool:
    if cmd not in db:
        return False
    db[cmd]['name'] = new_name
    return True

def update_command_tags(db: dict, cmd: str, new_tags: List[str]) -> bool:
    if cmd not in db:
        return False
    db[cmd]['tags'] = sorted(list(set(new_tags))) # 覆盖并去重排序
    return True

def delete_usage(db: dict, cmd: str, identifier: Union[int, str]) -> tuple[Union[dict, None], bool]:
    if cmd not in db or not db[cmd].get('examples'):
        return None # Command or examples not found

    exs = db[cmd]['examples']
    removed_usage = None

    if isinstance(identifier, int):
        idx = identifier
        if idx < 0 or idx >= len(exs):
            return None # Index out of bounds
        removed_usage = exs.pop(idx)
    else: # String (keyword)
        sub_l = identifier.lower()
        match_idx = -1
        for i, ex in enumerate(exs):
            if sub_l in ex.get('usage','').lower() or sub_l in ex.get('note','').lower():
                match_idx = i
                break
        if match_idx == -1:
            return None # Keyword not found
        removed_usage = exs.pop(match_idx)
    
    # 如果用法删完了，自动删除主命令
    if not exs:
        del db[cmd]
        return removed_usage, True # 返回删除的用法和主命令是否被删除的标志
    return removed_usage, False # 返回删除的用法和主命令未被删除的标志

def find_commands(db: dict, query: str) -> List[tuple]:
    query_l = query.lower()
    results = []

    for cmd, v in db.items():
        name = v.get('name', "")
        tags = v.get('tags', [])
        
        # 检查主命令名、中文名或标签是否匹配
        if (query_l in cmd.lower()) or (query_l in name.lower()) or any(query_l in tag.lower() for tag in tags):
            # 整条命令都算命中，展示所有用法
            for idx, ex in enumerate(v.get("examples", [])):
                results.append((cmd, name, idx, ex['usage'], ex['note']))
        else:
            # 检查用法示例或备注是否匹配
            for idx, ex in enumerate(v.get("examples", [])):
                if (query_l in ex.get("usage", "").lower()) or (query_l in ex.get("note", "").lower()):
                    results.append((cmd, name, idx, ex['usage'], ex['note']))
    
    # 可以选择在这里对 results 进行排序，例如按命令名或匹配度
    results.sort(key=lambda x: (x[0].lower(), x[2])) # 按命令名和序号排序
    return results

def get_command_examples(db: dict, cmd: str) -> List[Dict]:
    return db.get(cmd, {}).get("examples", [])

def get_usage_by_index(db: dict, cmd: str, index: int) -> Union[Dict, None]:
    exs = get_command_examples(db, cmd)
    if 0 <= index < len(exs):
        return exs[index]
    return None

def edit_usage(db: dict, cmd: str, index: int, new_usage: str = None, new_note: str = None) -> bool:
    if cmd not in db:
        return False
    
    exs = db[cmd].get("examples", [])
    if not (0 <= index < len(exs)):
        return False
    
    if new_usage is not None:
        exs[index]['usage'] = new_usage
    if new_note is not None:
        exs[index]['note'] = new_note
    
    return True

# 导入/导出逻辑
def import_data(db: dict, file_path: str, overwrite: bool = False) -> Dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            imported_data = json.load(f)
        
        if not isinstance(imported_data, dict):
            raise ValueError("Imported file is not a valid KVS database format (expected dictionary).")
            
        merged_count = 0
        new_cmd_count = 0

        for cmd_key, cmd_value in imported_data.items():
            if cmd_key in db:
                if overwrite:
                    db[cmd_key] = cmd_value
                    merged_count += 1
                else:
                    # 合并用法：保留现有用法，添加导入中不重复的用法
                    existing_examples = set(tuple(item.items()) for item in db[cmd_key].get('examples', []))
                    for new_ex in cmd_value.get('examples', []):
                        if tuple(new_ex.items()) not in existing_examples:
                            db[cmd_key].get('examples', []).append(new_ex)
                            merged_count += 1
                    # 更新名称和标签（可以根据需求调整合并策略）
                    if cmd_value.get('name'):
                        db[cmd_key]['name'] = cmd_value['name']
                    if cmd_value.get('tags'):
                        db[cmd_key]['tags'] = sorted(list(set(db[cmd_key].get('tags', []) + cmd_value['tags'])))
            else:
                db[cmd_key] = cmd_value
                new_cmd_count += 1
        return db, new_cmd_count, merged_count
    except FileNotFoundError:
        raise FileNotFoundError(f"Import file not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred during import: {e}")

def export_data(db: dict, file_path: str) -> bool:
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        raise Exception(f"An error occurred during export: {e}")

