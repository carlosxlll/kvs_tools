# KVS Tools - 本地命令词典 🛠️

KVS (Key-Value Store) 是一个功能强大的本地命令词典工具，帮助开发者管理和快速查找常用命令。支持丰富的终端输出效果、多种颜色主题，让命令管理变得高效且美观。

## ✨ 功能特性

- 📚 **本地存储** - 所有数据存储在本地，无需网络连接
- 🎨 **多主题支持** - 6种精美颜色主题（默认、深色、浅色、霓虹、海洋、彩虹）
- 🔍 **强大搜索** - 支持命令名、中文名、标签、用法示例的全文搜索
- 📋 **剪贴板集成** - 一键复制命令到剪贴板
- 🔄 **数据管理** - 支持 JSON 格式的数据导入/导出
- 💬 **交互模式** - 友好的交互式操作界面
- 🏷️ **标签系统** - 使用标签对命令进行分类管理
- ⚡ **快速访问** - 命令行工具，随时随地快速查询

## 📖 基本使用

### 添加命令

```bash
# 基础语法
kvs add <命令> <中文名> <用法示例> <备注说明> --tags <标签>

# 实际例子
kvs add git "版本控制" "git status" "查看仓库状态" --tags "dev,version"
kvs add docker "容器管理" "docker ps" "查看运行中的容器" --tags "container,deploy"

# 交互式添加（推荐新手使用）
kvs add --interactive
````

### 查看命令

```bash
# 查看所有命令
kvs list

# 查看特定命令的所有用法
kvs list git
kvs list docker
```

### 搜索命令

```bash
# 按关键词搜索
kvs find 版本
kvs find git
kvs find 状态
kvs find container
```

### 复制命令到剪贴板

```bash
# 复制指定命令的用法到剪贴板
kvs copy git 0      # 复制 git 的第0个用法
kvs copy docker 1   # 复制 docker 的第1个用法
```

## 🎯 高级功能

### 命令管理

#### 更新命令信息

```bash
# 更新中文名
kvs update name docker "Docker容器管理"

# 更新标签
kvs update tag docker "container,deploy,devops"
```

#### 编辑用法

```bash
# 编辑指定序号的用法
kvs edit docker 0 --new-usage "docker ps -a" --new-note "查看所有容器"

# 交互式编辑
kvs edit --interactive
```

#### 删除用法

```bash
# 按序号删除
kvs delete docker 0

# 按关键词删除
kvs delete docker "ps"

# 交互式删除
kvs delete --interactive
```

### 数据管理

#### 导出数据

```bash
# 导出所有命令到JSON文件
kvs export ~/my_commands.json
kvs export backup.json
```

#### 导入数据

```bash
# 合并导入（默认模式，不会覆盖已有命令）
kvs import ~/shared_commands.json

# 覆盖导入（会替换同名命令）
kvs import ~/backup.json --overwrite
```

### 主题管理

```bash
# 查看所有可用主题
kvs theme list

# 切换主题
kvs theme neon      # 霓虹主题
kvs theme dark      # 深色主题
kvs theme ocean     # 海洋主题
kvs theme rainbow   # 彩虹主题

# 查看当前主题演示效果
kvs theme demo
```

#### 可用主题预览

| 主题名       | 描述   | 特色              |
| --------- | ---- | --------------- |
| `default` | 默认主题 | 适合大多数终端，平衡的色彩搭配 |
| `dark`    | 深色主题 | 高亮颜色，适合深色背景终端   |
| `light`   | 浅色主题 | 深色字体，适合浅色背景终端   |
| `neon`    | 霓虹主题 | 超鲜艳颜色，科技感十足     |
| `ocean`   | 海洋主题 | 蓝绿色系，护眼舒适       |
| `rainbow` | 彩虹主题 | 多彩缤纷，每种元素不同颜色   |

### 获取帮助

```bash
# 查看基本帮助
kvs --help

# 查看详细使用示例
kvs examples

