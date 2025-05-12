import os
import shutil
import exifread

#自动获取图片拍摄日期，对照片按照日期进行打包分类

def get_shot_date(filepath):
    """获取图片的拍摄日期"""
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False)

        # 尝试多个可能的EXIF日期标签
        datetime_str = (
                tags.get('EXIF DateTimeOriginal') or
                tags.get('EXIF DateTimeDigitized') or
                tags.get('DateTime'))

        if not datetime_str:
            return None

        # 转换日期格式为YYYY-MM-DD
        return str(datetime_str).split()[0].replace(':', '-')

    except Exception as e:
        print(f"错误：无法读取 {filepath} 的Exif信息 ({e})")
        return None


def organize_photos(source_dir):
    """整理图片到日期目录"""
    # 支持的图片格式
    image_exts = ('.jpg', '.jpeg', '.png', '.tiff',
                  '.bmp', '.gif', '.arw', '.nef', '.cr2')

    # 创建计数器
    processed = 0
    errors = 0

    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)

        # 跳过目录和非图片文件
        if not os.path.isfile(filepath):
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext not in image_exts:
            continue

        # 获取拍摄日期
        date_str = get_shot_date(filepath)

        # 处理未知日期文件
        if not date_str:
            unknown_dir = os.path.join(source_dir, '未知日期')
            os.makedirs(unknown_dir, exist_ok=True)
            try:
                shutil.move(filepath, os.path.join(unknown_dir, filename))
                print(f"⚠️ 未识别 [{filename}] 已移至 {unknown_dir}")
                errors += 1
            except Exception as e:
                print(f"❌ 移动失败 [{filename}]: {e}")
            continue

        # 创建日期目录
        target_dir = os.path.join(source_dir, date_str)
        os.makedirs(target_dir, exist_ok=True)

        # 移动文件并处理冲突
        try:
            dest_path = os.path.join(target_dir, filename)
            if os.path.exists(dest_path):
                base, extension = os.path.splitext(filename)
                new_name = f"{base}_副本{extension}"
                dest_path = os.path.join(target_dir, new_name)
                print(f"⚠️ 发现重名文件，已创建副本 [{new_name}]")

            shutil.move(filepath, dest_path)
            print(f"✅ 已整理 [{filename}] → {date_str}")
            processed += 1

        except Exception as e:
            print(f"❌ 移动失败 [{filename}]: {e}")
            errors += 1

    # 输出统计信息
    print(f"\n整理完成！成功处理 {processed} 个文件，{errors} 个文件处理失败")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    else:
        source_dir = input("📁 请输入图片文件夹路径：")

    if not os.path.isdir(source_dir):
        print("❌ 错误：路径不存在或不是目录")
        sys.exit(1)

    print("\n开始整理图片...\n")
    organize_photos(source_dir)