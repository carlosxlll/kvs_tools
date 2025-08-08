# 在 src/db.py 文件中添加主题保存功能

import json
import os
from pathlib import Path

def get_xdg_data_dir():
    """获取XDG数据目录"""
    xdg_data_home = os.environ.get('XDG_DATA_HOME')
    if xdg_data_home:
        return Path(xdg_data_home)
    else:
        return Path.home() / '.local' / 'share'

def get_db_path():
    """获取数据库文件路径"""
    data_dir = get_xdg_data_dir() / 'kvs'
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / 'commands.json'

def get_config_path():
    """获取配置文件路径"""
    config_dir = Path.home() / '.config' / 'kvs'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.json'

def load_db():
    """加载命令数据库"""
    db_path = get_db_path()
    if db_path.exists():
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_db(db):
    """保存命令数据库"""
    db_path = get_db_path()
    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

def load_config():
    """加载配置文件"""
    config_path = get_config_path()
    default_config = {
        "theme": "default"
    }
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 确保有默认值
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except (json.JSONDecodeError, IOError):
            return default_config
    return default_config

def save_config(config):
    """保存配置文件"""
    config_path = get_config_path()
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

def get_theme_setting():
    """获取主题设置"""
    config = load_config()
    return config.get("theme", "default")

def save_theme_setting(theme_name):
    """保存主题设置"""
    config = load_config()
    config["theme"] = theme_name
    return save_config(config)
