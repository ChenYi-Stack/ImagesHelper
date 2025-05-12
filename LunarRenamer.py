import os
from PIL import Image
from PIL.ExifTags import TAGS
from lunarcalendar import Converter, Solar, Lunar
from datetime import datetime

#功能：根据照片拍摄日期添加农历信息重命名
# 将农历月份数字转换为中文名称（含闰月处理）

def lunar_month_name(month_num, is_leap_month):
    """
    根据农历月份数字和 Lunar 对象，返回中文农历月份名称（含闰月）
    """
    month_names = ["正月", "二月", "三月", "四月", "五月", "六月",
                   "七月", "八月", "九月", "十月", "冬月", "腊月"]

    if 1 <= month_num <= 12:
        name = month_names[month_num - 1]
        if is_leap_month:
            return f"闰{name}"
        else:
            return name
    return ""

# 将农历日期数字转换为中文表达
def lunar_day_to_chinese(day_num):
    chinese_days = [
        "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
        "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
        "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
    ]
    if 1 <= day_num <= 30:
        return chinese_days[day_num - 1]
    return ""

# 从文件中提取 EXIF 的拍摄时间
def get_file_creation_date(file_path):
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "DateTimeOriginal":
                        # 格式：2025:05:09 12:34:56
                        date_str = value.split(" ")[0]
                        year, month, day = map(int, date_str.split(":"))
                        return year, month, day
    except Exception as e:
        print(f"读取 {file_path} 的 EXIF 出错: {e}")
    return None

# 主函数：遍历文件夹并重命名文件
def rename_files_in_folder(directory):
    date_counter = {}  # 用于记录相同日期的文件数量，避免重名

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue

        # 获取拍摄日期
        date_info = get_file_creation_date(file_path)
        if not date_info:
            print(f"跳过文件 {filename}：无法获取拍摄日期。")
            continue

        year, month, day = date_info
        solar = Solar(year, month, day)
        lunar = Converter.Solar2Lunar(solar)

        # 构建农历信息
        lunar_month = lunar.month
        lunar_day = lunar.day
        is_leap_month = lunar.isleap
        month_str = lunar_month_name(lunar_month, is_leap_month)
        day_str = lunar_day_to_chinese(lunar_day)

        # 构建新文件名
        base_name = f"{year}.{month}.{day} {month_str}{day_str}"
        ext = os.path.splitext(filename)[1]
        new_name = base_name + ext

        # 处理重名（添加序号）
        if base_name in date_counter:
            count = date_counter[base_name] + 1
            date_counter[base_name] = count
            new_name = f"{base_name}-{count}{ext}"
        else:
            date_counter[base_name] = 0

        # 构建新路径并重命名
        new_path = os.path.join(directory, new_name)
        try:
            os.rename(file_path, new_path)
            print(f"已重命名：{filename} -> {new_name}")
        except Exception as e:
            print(f"重命名失败：{filename} -> {new_name}，原因：{e}")

# 程序入口
if __name__ == "__main__":
    folder_path = input("请输入要处理的文件夹路径：")
    if os.path.isdir(folder_path):
        rename_files_in_folder(folder_path)
    else:
        print("输入的路径不是一个有效的文件夹。")