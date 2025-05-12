import os
import re
from datetime import datetime

#用于修改240320格式的日期到20240320格式

def is_valid_date(yymmdd):
    """验证前6位是否为有效日期（YYMMDD格式）"""
    try:
        # 将YY转换为YYYY（假设是2000-2099年）
        datetime.strptime(f"20{yymmdd}", "%Y%m%d")
        return True
    except ValueError:
        return False


def rename_folders(target_dir):
    # 验证目录有效性
    if not os.path.exists(target_dir):
        raise FileNotFoundError(f"目录不存在: {target_dir}")
    if not os.path.isdir(target_dir):
        raise NotADirectoryError(f"路径不是目录: {target_dir}")

    # 遍历目录
    for name in os.listdir(target_dir):
        old_path = os.path.join(target_dir, name)

        # 只处理文件夹
        if os.path.isdir(old_path):
            # 匹配前6位数字的结构
            match = re.match(r"^(\d{6})(\D.*)?$", name)  # 分离数字部分和后续内容
            if match:
                yymmdd, suffix = match.groups()
                suffix = suffix or ""  # 处理空后缀

                # 日期有效性验证
                if is_valid_date(yymmdd):
                    # 构建新名称
                    new_name = f"20{yymmdd}{suffix}"
                    new_path = os.path.join(target_dir, new_name)

                    # 避免重复和覆盖
                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        print(f"成功转换: {name: <20} -> {new_name}")
                    else:
                        print(f"跳过重复: {new_name} 已存在")
                else:
                    print(f"无效日期: {yymmdd}（文件夹 {name}）")
            else:
                print(f"格式不符: {name}")


if __name__ == "__main__":
    # 用户交互
    target_dir = input("请输入要处理的目录路径（直接回车使用当前目录）: ").strip()
    if not target_dir:
        target_dir = os.getcwd()

    # 执行重命名
    print("\n" + "=" * 60)
    try:
        rename_folders(target_dir)
    except Exception as e:
        print(f"发生错误: {str(e)}")
    print("=" * 60 + "\n")

    # 完成提示
    input("操作执行完毕，按回车键退出...")