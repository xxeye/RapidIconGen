import os
import shutil
import csv
import subprocess
from .config_loader import get_languages, compress_png

# 移動指定圖片到指定資料夾
def move_gameicon_folder(assets_path):
    source_folder = os.path.join(f"{assets_path}_layers", "301x300", "0gameicon")
    target_folder = os.path.join(os.path.dirname(assets_path), "0gameicon")
    if os.path.exists(source_folder):
        shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
        print(f"已將 {source_folder} 移動並覆蓋到 {target_folder}")
    else:
        print(f"源資料夾 {source_folder} 不存在，無法進行移動。")

# 使用subprocess壓縮圖片
def compress_images(png_folder, assets_path, en_name, config):
    icon_sizes = config['icon_sizes']
    languages = get_languages()  # 調用 get_languages 函數

    # 針對每個尺寸、語言的圖片進行壓縮
    for icon_config in icon_sizes:
        size = icon_config["size"]
        for language in languages:
            png_file = os.path.join(png_folder, f"{en_name}_{size[0]}x{size[1]}_{language}.png")
            if os.path.exists(png_file):
                compress_png(png_file)  # 調用 config_loader 中的壓縮函數

    # 壓縮 301x300 目錄下對應語言的所有圖片
    gameicon_folder = os.path.join(assets_path + "_layers", "301x300", "0gameicon")
    for language in languages:
        language_folder = os.path.join(gameicon_folder, "Language", language)
        if os.path.exists(language_folder):
            for root, dirs, files in os.walk(language_folder):
                for file in files:
                    if file.endswith(".png"):
                        png_file = os.path.join(root, file)
                        compress_png(png_file)  # 調用 config_loader 中的壓縮函數
    
    # 壓縮 301x300/0gameicon/Common/ 下的 assets_path.png
    folder_name = os.path.basename(assets_path)
    common_png_file = os.path.join(gameicon_folder, "Common", f"{folder_name}.png")
    if os.path.exists(common_png_file):
        subprocess.run(["pngquant", "--quality=40-60", "--speed=1", "--ext=.png", "--force", common_png_file])
        print(f"Compressed: {common_png_file}")

# 獲取文件夾中的所有圖片
def get_images_from_folder(folder):
    images = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                images.append(Image.open(image_path))
    return images

def read_csv_data(assets_path, file_name, mode):
    file_path = os.path.join(assets_path, file_name)
    
    if mode == "text_data":  # 讀取語言和文本的情況
        text_data = {}
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                text_data[row['language']] = row['text']
        return text_data
    
    elif mode == "prefix_mask_data":  # 讀取前綴和套用遮罩的情況
        nas_data_list, apply_masks = [], []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nas_data_list.append(row['nas_data_list'])
                apply_masks.append(row['apply_masks'].strip())  # 保留原始大小寫
        return nas_data_list, apply_masks

def list_available_datasets(base_path):
    datasets = []
    index = 1

    # 遍歷 base_path 的第一層資料夾
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)

        # 檢查該路徑是否是資料夾，並且該資料夾下是否存在 text_data.csv 文件
        if os.path.isdir(folder_path) and os.path.exists(os.path.join(folder_path, 'text_data.csv')):
            datasets.append(folder)  # 只加入資料夾名稱
            print(f"{index}. {folder}")
            index += 1

    # 讓用戶輸入要選擇的資料夾編號
    selected_indexes = input("請輸入要使用的資料集編號（用逗號分隔）: ").split(',')
    selected_folders = [datasets[int(i) - 1] for i in selected_indexes if i.isdigit()]
    
    return selected_folders