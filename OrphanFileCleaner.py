import os
from send2trash import send2trash
from collections import defaultdict

#功能 ：检测并清理孤立的 RAW/JPG 文件

def find_orphan_files(folder_path):
    """（此函数保持不变，同原始版本）"""
    file_dict = {
        'raw': defaultdict(list),
        'jpg': defaultdict(list)
    }

    for root, _, files in os.walk(folder_path):
        for file in files:
            base_name, ext = os.path.splitext(file)
            ext = ext.lower()
            full_path = os.path.join(root, file)
            key = base_name.lower()

            if ext in {'.cr2', '.nef', '.arw', '.dng', '.raf'}:
                file_dict['raw'][key].append(full_path)
            elif ext in {'.jpg', '.jpeg'}:
                file_dict['jpg'][key].append(full_path)

    orphans = {'raw': defaultdict(list), 'jpg': defaultdict(list)}

    for raw_name, paths in file_dict['raw'].items():
        if raw_name not in file_dict['jpg']:
            for path in paths:
                parent = os.path.dirname(path)
                orphans['raw'][parent].append(path)

    for jpg_name, paths in file_dict['jpg'].items():
        if jpg_name not in file_dict['raw']:
            for path in paths:
                parent = os.path.dirname(path)
                orphans['jpg'][parent].append(path)

    return orphans


def main():
    target_folder = input("请输入要检测的文件夹路径: ").strip()

    if not os.path.isdir(target_folder):
        print("错误：路径不存在或不是文件夹！")
        return

    # 获取孤儿文件数据
    orphans = find_orphan_files(target_folder)

    # 展平数据结构
    raw_files = [path for paths in orphans['raw'].values() for path in paths]
    jpg_files = [path for paths in orphans['jpg'].values() for path in paths]
    total_raw = len(raw_files)
    total_jpg = len(jpg_files)

    if total_raw + total_jpg == 0:
        print("未发现任何孤立文件")
        return

    # 统一显示统计信息
    print(f"\n【检测结果】")
    print(f"发现孤立RAW文件: {total_raw} 个")
    print(f"发现孤立JPG文件: {total_jpg} 个")

    # 统一展示文件列表
    if input("\n是否查看文件详情？(y/n): ").lower() == 'y':
        print("\n=== 孤立文件列表 ===")
        for path in raw_files:
            print(f"[RAW] {os.path.basename(path)}")
        for path in jpg_files:
            print(f"[JPG] {os.path.basename(path)}")

    # 统一删除操作
    if input("\n是否删除所有孤立文件？(y/n): ").lower() == 'y':
        deleted_count = 0
        # 合并所有待删除文件
        all_files = raw_files + jpg_files

        print("\n=== 删除进度 ===")
        for path in all_files:
            try:
                send2trash(path)
                file_type = "RAW" if path in raw_files else "JPG"
                print(f"已删除 [{file_type}]: {os.path.basename(path)}")
                deleted_count += 1
            except Exception as e:
                print(f"删除失败: {os.path.basename(path)} ({str(e)})")

        print(f"\n操作完成，成功删除 {deleted_count}/{len(all_files)} 个文件")


if __name__ == "__main__":
    main()