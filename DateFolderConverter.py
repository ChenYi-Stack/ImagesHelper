import os
import re
from datetime import datetime

# 功能 ：将包含日期信息的文件夹名称转换为标准格式
# 示例：将 "2025年1月1日" 转换为 "2025-01-01"

def parse_folder_name(folder_name):
    """尝试解析文件夹名称中的日期信息"""
    match = re.match(
        r'^(\d{4})[^\d]*(\d{1,2})[^\d]*(\d{1,2})[^\d]*$',
        folder_name
    )
    if not match:
        return None
    try:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        return datetime(year, month, day)
    except (ValueError, TypeError):
        return None


# 获取目标路径
target_dir = input("请输入要处理的文件夹路径：").strip()
if not os.path.isdir(target_dir):
    print("路径不存在或不是文件夹")
    exit()

# 递归收集所有子文件夹
date_folders = []
for root, dirs, _ in os.walk(target_dir):
    for name in dirs:
        dt = parse_folder_name(name)
        if dt:
            full_path = os.path.join(root, name)
            date_folders.append((full_path, name, dt))

if not date_folders:
    print("没有找到符合日期格式的文件夹")
    exit()

# 按路径深度排序（先处理深层文件夹）
date_folders.sort(key=lambda x: x[0].count(os.sep), reverse=True)

# 显示可转换的文件夹
print("\n检测到以下日期文件夹：")
for idx, (path, old_name, dt) in enumerate(date_folders):
    print(f"{idx + 1}. [路径] {path} → 日期：{dt.date()}")

# 选择目标格式
print("\n请选择目标日期格式：")
print("1. YYYYMMDD（例如：20250101）")
print("2. YYYY-MM-DD（例如：2025-01-01）")
print("3. YYYY年M月D日（例如：2025年1月1日）")
print("4. YYYY.MM.DD（例如：2025.01.01）")

choice = input("请输入选项数字（1-4）：")
if not choice.isdigit() or (choice := int(choice)) not in [1, 2, 3, 4]:
    print("无效的选项")
    exit()

# 定义格式转换函数
format_funcs = {
    1: lambda dt: dt.strftime("%Y%m%d"),
    2: lambda dt: dt.strftime("%Y-%m-%d"),
    3: lambda dt: f"{dt.year}年{dt.month}月{dt.day}日",
    4: lambda dt: dt.strftime("%Y.%m.%d"),
}
format_func = format_funcs[choice]

# 显示转换预览
print("\n以下文件夹将被重命名：")
for path, old_name, dt in date_folders:
    parent_dir = os.path.dirname(path)
    new_name = format_func(dt)
    print(f"{path} → {os.path.join(parent_dir, new_name)}")

# 确认执行
if input("\n是否确认重命名？(y/n)：").lower() != 'y':
    print("操作已取消")
    exit()

# 执行重命名
for path, old_name, dt in date_folders:
    parent_dir = os.path.dirname(path)
    new_name = format_func(dt)
    new_path = os.path.join(parent_dir, new_name)

    if path == new_path:
        continue

    # 处理名称冲突
    final_path = new_path
    counter = 1
    while os.path.exists(final_path):
        final_path = f"{new_path}_{counter}"
        counter += 1

    try:
        os.rename(path, final_path)
        print(f"成功: {path} → {final_path}")
    except Exception as e:
        print(f"失败: {path} → {final_path}，错误：{str(e)}")