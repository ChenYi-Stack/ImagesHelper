# import os
# import sys
# from send2trash import send2trash
#
#
# def main():
#     # 获取用户输入的 RAW 文件夹路径
#     raw_folder = input("请输入 RAW 文件夹路径: ").strip()
#
#     # 验证路径有效性
#     if not os.path.isdir(raw_folder):
#         print("错误：输入的路径不存在或不是文件夹！")
#         sys.exit(1)
#
#     # 确定父文件夹和 JPG 文件夹路径
#     parent_folder = os.path.dirname(raw_folder)
#     jpg_folder = os.path.join(parent_folder, "JPG")
#
#     # 检查 JPG 文件夹是否存在
#     if not os.path.exists(jpg_folder):
#         print(f"错误：未找到对应的 JPG 文件夹 {jpg_folder}！")
#         sys.exit(1)
#
#     # 收集 RAW 文件的基本名（不含后缀）
#     raw_files = set()
#     for file in os.listdir(raw_folder):
#         file_path = os.path.join(raw_folder, file)
#         if os.path.isfile(file_path):
#             base_name = os.path.splitext(file)[0]
#             raw_files.add(base_name.lower())
#
#     # 如果没有 RAW 文件则直接退出
#     if not raw_files:
#         print("RAW 文件夹中没有文件，无需操作。")
#         sys.exit(0)
#
#     # === 第一部分：处理 JPG 冗余文件 ===
#     jpg_to_process = []
#     for file in os.listdir(jpg_folder):
#         file_path = os.path.join(jpg_folder, file)
#         if os.path.isfile(file_path):
#             base_name, ext = os.path.splitext(file)
#             if ext.lower() in ['.jpg', '.jpeg'] and base_name.lower() not in raw_files:
#                 jpg_to_process.append(file_path)
#
#     # === 第二部分：处理 RAW 文件夹中的 XMP 文件 ===
#     xmp_to_process = []
#     for file in os.listdir(raw_folder):
#         file_path = os.path.join(raw_folder, file)
#         if os.path.isfile(file_path) and file.lower().endswith('.xmp'):
#             xmp_to_process.append(file_path)
#
#     # 合并待处理文件列表
#     to_process = jpg_to_process + xmp_to_process
#     if not to_process:
#         print("没有需要处理的文件。")
#         sys.exit(0)
#
#     # 显示待处理文件分类信息
#     if jpg_to_process:
#         print("\n=== 以下 JPG 文件没有对应的 RAW 文件 ===")
#         for f in jpg_to_process:
#             print(f" - {os.path.basename(f)}")
#
#     if xmp_to_process:
#         print("\n=== 以下 XMP 文件将被删除 ===")
#         for f in xmp_to_process:
#             print(f" - {os.path.basename(f)}")
#
#     # 用户确认
#     confirm = input("\n是否将以上文件移至回收站？(y/n): ").strip().lower()
#     if confirm == 'y':
#         delete_files(to_process)
#     else:
#         print("操作已取消。")
#
#
# def delete_files(file_list):
#     """安全删除文件到回收站"""
#     success = 0
#     failed = 0
#
#     for file_path in file_list:
#         try:
#             send2trash(file_path)
#             print(f"已移至回收站: {os.path.basename(file_path)}")
#             success += 1
#         except Exception as e:
#             print(f"操作失败 [{os.path.basename(file_path)}]: {str(e)}")
#             failed += 1
#
#     print(f"\n操作完成: 成功移至回收站 {success} 个文件，失败 {failed} 个")
#
#
# if __name__ == "__main__":
#     main()