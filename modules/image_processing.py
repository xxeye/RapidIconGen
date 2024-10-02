from PIL import Image, ImageDraw, ImageFont, ImageChops
import os

# 等比例填滿並裁剪函數
def resize_with_aspect_ratio_fill(image, target_size):
    original_width, original_height = image.size
    target_width, target_height = target_size
    
    # 計算填滿框架所需的比例
    ratio = max(target_width / original_width, target_height / original_height)
    
    # 按照比例縮放圖片
    new_size = (int(original_width * ratio), int(original_height * ratio))
    resized_image = image.resize(new_size, Image.LANCZOS)
    
    # 裁剪圖片以適應框架
    left = (resized_image.width - target_width) / 2
    top = (resized_image.height - target_height) / 2
    right = (resized_image.width + target_width) / 2
    bottom = (resized_image.height + target_height) / 2
    
    return resized_image.crop((left, top, right, bottom))

#等比例縮放（Aspect Ratio Preserve Fit）
#計算圖片的縮放比例，使圖片的寬度或高度完全適應目標框架的一邊，另一邊會留有空白,圖片縮放後居中放置。
def resize_with_aspect_ratio_fit(image, target_size):
    original_width, original_height = image.size
    target_width, target_height = target_size

    ratio = min(target_width / original_width, target_height / original_height)
    new_size = (int(original_width * ratio), int(original_height * ratio))
    resized_image = image.resize(new_size, Image.LANCZOS)

    # 創建一個空白的目標尺寸圖像並居中放置縮放後的圖片
    new_image = Image.new('RGBA', target_size, (255, 255, 255, 0))  # 背景透明
    offset = ((target_width - new_size[0]) // 2, (target_height - new_size[1]) // 2)
    new_image.paste(resized_image, offset)
    return new_image

#中心裁切（Center Crop）將圖片居中並裁剪掉多餘的部分
def center_crop(image, target_size):
    original_width, original_height = image.size
    target_width, target_height = target_size

    left = (original_width - target_width) / 2
    top = (original_height - target_height) / 2
    right = (original_width + target_width) / 2
    bottom = (original_height + target_height) / 2

    return image.crop((left, top, right, bottom))

#填充（Padding）等比例縮放圖片後，在目標框架內加上填充區域
def resize_with_padding(image, target_size, padding_color=(255, 255, 255, 0)):
    original_width, original_height = image.size
    target_width, target_height = target_size

    ratio = min(target_width / original_width, target_height / original_height)
    new_size = (int(original_width * ratio), int(original_height * ratio))
    resized_image = image.resize(new_size, Image.LANCZOS)

    # 創建填充背景
    new_image = Image.new('RGBA', target_size, padding_color)
    offset = ((target_width - new_size[0]) // 2, (target_height - new_size[1]) // 2)
    new_image.paste(resized_image, offset)
    return new_image

#拉伸（Stretch Crop）
def stretch_resize(image, target_size):
    return image.resize(target_size, Image.LANCZOS)

#自由裁切（Free Crop）
def free_crop(image, crop_box):
    # crop_box = (left, top, right, bottom)
    return image.crop(crop_box)


# 預處理相同尺寸的圖片
def preprocess_images(icon_sizes, languages, png_folder, en_name):
    size_groups = {}
    
    for icon_config in icon_sizes:
        size = icon_config["size"]
        for language in languages:
            icon_paths = []
            if "suffix" in icon_config:
                icon_paths.append(os.path.join(png_folder, f"{en_name}_{size[0]}x{size[1]}{icon_config['suffix']}_{language}.png"))
            icon_paths.append(os.path.join(png_folder, f"{en_name}_{size[0]}x{size[1]}_{language}.png"))
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    img = Image.open(icon_path).convert('RGBA')
                    if size not in size_groups:
                        size_groups[size] = []
                    size_groups[size].append(img)
                    break

    preprocessed_images = []
    for size, imgs in size_groups.items():
        total_width = sum(img.width for img in imgs)
        max_height = max(img.height for img in imgs)

        new_image = Image.new('RGBA', (total_width, max_height), (0, 0, 0, 0))
        x_offset = 0
        for img in imgs:
            temp_image = Image.new('RGBA', new_image.size, (0, 0, 0, 0))
            temp_image.paste(img, (x_offset, 0))
            new_image = Image.alpha_composite(new_image, temp_image)
            x_offset += img.width
        
        preprocessed_images.append(new_image)

    return preprocessed_images

# 自適應的網格佈局
def adaptive_grid_layout(images, output_path):
    max_width = max(img.width for img in images)
    
    current_width = 0
    current_row_images = []
    rows = []
    row_heights = []

    for img in images:
        if current_width + img.width > max_width:
            rows.append(current_row_images)
            row_heights.append(max(img.height for img in current_row_images))
            current_row_images = []
            current_width = 0

        current_row_images.append(img)
        current_width += img.width

    if current_row_images:
        rows.append(current_row_images)
        row_heights.append(max(img.height for img in current_row_images))

    total_height = sum(row_heights)
    new_image = Image.new('RGBA', (max_width, total_height), color=(0, 0, 0, 0))

    y_offset = 0
    for i, row in enumerate(rows):
        x_offset = 0
        row_height = row_heights[i]
        for img in row:
            temp_image = Image.new('RGBA', new_image.size, (0, 0, 0, 0))
            temp_image.paste(img, (x_offset, y_offset + (row_height - img.height)))
            new_image = Image.alpha_composite(new_image, temp_image)
            x_offset += img.width
        y_offset += row_height

    new_image.save(output_path, format='PNG')

