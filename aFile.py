import os
import sys
import shutil
from send2trash import send2trash

# 定义支持的 RAW 格式（可扩展）
RAW_EXTENSIONS = {'.cr2', '.nef', '.arw', '.dng', '.raf'}


def organize_files(target_folder):
    """整理文件到子文件夹，返回 (jpg_folder, raw_folder)"""
    jpg_folder = os.path.join(target_folder, "JPG")
    raw_folder = os.path.join(target_folder, "RAW")

    # 创建子文件夹
    os.makedirs(jpg_folder, exist_ok=True)
    os.makedirs(raw_folder, exist_ok=True)

    moved_files = {'jpg': 0, 'raw': 0, 'skip': 0}

    # 遍历整理文件
    for filename in os.listdir(target_folder):
        src_path = os.path.join(target_folder, filename)
        if os.path.isfile(src_path):
            base, ext = os.path.splitext(filename)
            ext = ext.lower()

            # 确定目标路径
            dest_path = None
            if ext in ('.jpg', '.jpeg'):
                dest_path = os.path.join(jpg_folder, filename)
                key = 'jpg'
            elif ext in RAW_EXTENSIONS:
                dest_path = os.path.join(raw_folder, filename)
                key = 'raw'

            # 执行移动
            if dest_path:
                try:
                    if not os.path.exists(dest_path):
                        shutil.move(src_path, dest_path)
                        moved_files[key] += 1
                    else:
                        moved_files['skip'] += 1
                        print(f"跳过已存在文件: {filename}")
                except Exception as e:
                    print(f"移动失败 [{filename}]: {str(e)}")

    # 输出统计
    print(f"\n整理完成:")
    print(f" - 移动 JPG 文件: {moved_files['jpg']} 个")
    print(f" - 移动 RAW 文件: {moved_files['raw']} 个")
    print(f" - 跳过重复文件: {moved_files['skip']} 个")

    return jpg_folder, raw_folder


def main():
    # 获取目标文件夹
    target_folder = input("请输入照片文件夹路径: ").strip()
    if not os.path.isdir(target_folder):
        print("错误：路径不存在或不是文件夹！")
        sys.exit(1)

    # jpg_folder, raw_folder = target_folder, target_folder  # 默认不整理
    # ========== 步骤 1：文件整理 ==========
    # 自动检测是否已存在 JPG/RAW 子文件夹
    auto_jpg = os.path.join(target_folder, "JPG")
    auto_raw = os.path.join(target_folder, "RAW")
    # 初始化文件夹路径（如果用户手动创建了则优先使用）
    jpg_folder = auto_jpg if os.path.exists(auto_jpg) else target_folder
    raw_folder = auto_raw if os.path.exists(auto_raw) else target_folder

    # 询问是否需要整理
    organize_confirm = input("\n是否要将文件整理到 JPG/RAW 子文件夹？(y/n): ").lower().strip()
    if organize_confirm == 'y':
        print("\n正在整理文件...")
        jpg_folder, raw_folder = organize_files(target_folder)
        print(f"\n整理后路径:")
        print(f" - JPG 文件夹: {jpg_folder}")
        print(f" - RAW 文件夹: {raw_folder}")
    else:
        # 用户选择不整理时，检测是否已有手动创建的文件夹
        if os.path.exists(auto_jpg) or os.path.exists(auto_raw):
            print(f"检测到手动创建的 JPG/RAW 子文件夹，将基于此整理")
            jpg_folder = auto_jpg if os.path.exists(auto_jpg) else target_folder
            raw_folder = auto_raw if os.path.exists(auto_raw) else target_folder
        else:
            print("保持原文件夹结构。")
        print(f"当前路径:")
        print(f" - JPG 文件夹: {jpg_folder}")
        print(f" - RAW 文件夹: {raw_folder}")


    # ========== 步骤 2：清理文件 ==========
    # 收集 RAW 文件基本名
    raw_bases = set()
    for file in os.listdir(raw_folder):
        file_path = os.path.join(raw_folder, file)
        if os.path.isfile(file_path):
            base, ext = os.path.splitext(file)
            if ext.lower() in RAW_EXTENSIONS:
                raw_bases.add(base.lower())

    # 识别待删除文件
    to_delete = []
    stats = {'jpg': 0, 'xmp': 0}

    # 检查 JPG 冗余
    for file in os.listdir(jpg_folder):
        file_path = os.path.join(jpg_folder, file)
        if os.path.isfile(file_path):
            base, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext in ('.jpg', '.jpeg') and base.lower() not in raw_bases:
                to_delete.append(file_path)
                stats['jpg'] += 1

    # 检查 XMP 文件（修改后检测父文件夹）
    xmp_confirm = input("\n是否要删除.xmp文件？(y/n): ").lower().strip()
    if xmp_confirm == 'y':
        for file in os.listdir(target_folder):  # 关键修改点
            file_path = os.path.join(target_folder, file)
            if os.path.isfile(file_path) and file.lower().endswith('.xmp'):
                to_delete.append(file_path)
                stats['xmp'] += 1
    else:
        print(".xmp文件将不会被删除。")

    if not to_delete:
        print("\n没有需要清理的文件。")
        sys.exit(0)

    # 显示待删除列表
    print("\n=== 待删除文件列表 ===")
    for f in to_delete:
        print(f" - {os.path.basename(f)}")
    # 显示统计
    print("\n=== 清理统计 ===")
    print(f"检测到 RAW 文件: {len(raw_bases)} 个")
    print(f"需删除的冗余 JPG: {stats['jpg']} 个")
    print(f"需删除的 XMP 文件: {stats['xmp']} 个")
    print(f"\n共计 {len(to_delete)} 个文件")

    # 最终确认
    confirm = input("\n是否确认移至回收站？(y/n): ").lower().strip()
    if confirm == 'y':
        delete_files(to_delete,stats)
    else:
        print("操作已取消。")

def delete_files(file_list,stats):
    """安全删除到回收站"""
    success, failed = 0, 0
    for path in file_list:
        try:
            send2trash(path)
            print(f"已删除: {os.path.basename(path)}  --共 {stats['jpg'] + stats['xmp']} 个，目前为第{success+1}个")
            success += 1
        except Exception as e:
            print(f"失败: {os.path.basename(path)} ({str(e)})")
            failed += 1
    print(f"\n操作结果: 成功 {success} 个, 失败 {failed} 个")


if __name__ == "__main__":
    main()