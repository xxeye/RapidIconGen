from modules.utils import wrap_text, adjust_text_size
from modules.image_processing import preprocess_images, adaptive_grid_layout, resize_with_aspect_ratio_fill
from modules.file_operations import move_gameicon_folder, compress_images, read_csv_data, list_available_datasets
from modules.config_loader import get_config, get_languages, get_language_settings
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

# 創建
def create_icon(assets_path, en_name, language, text, size, text_frame, text_frame_offset, img_path, imgA_path, iconX_path, mask_path, font_path, apply_mask, png_folder, suffix=""):
    
        # 獲取語言設置
    language_settings = get_language_settings()
    settings = language_settings.get(language, {
        "baseline_adjustment": 0,  # 預設基線調整
        "shadow_color": "#000000",  # 預設陰影顏色
        "gradient_colors": [
            (0.0, (255, 255, 255)),  # 預設文字漸層顏色
            (1.0, (0, 0, 0))
        ]
    })

    # 確認圖層資料夾存在
    if size == (146, 136) and suffix == "s":
        layer_folder = f"{assets_path}_layers/{size[0]}x{size[1]}s"
    else:
        layer_folder = f"{assets_path}_layers/{size[0]}x{size[1]}"
    
    language_folder = os.path.join(layer_folder, language)
    imgA_folder = os.path.join(layer_folder, '2imgA')
    img_iconX_folder = os.path.join(layer_folder, '1img_iconX')
    frame_folder = os.path.join(layer_folder, '0frame')
    
    os.makedirs(language_folder, exist_ok=True)
    os.makedirs(imgA_folder, exist_ok=True)
    os.makedirs(img_iconX_folder, exist_ok=True)
    os.makedirs(frame_folder, exist_ok=True)
    
    if size == (301, 300):
        gameicon_common_folder = os.path.join(layer_folder, '0gameicon/Common')
        gameicon_language_folder = os.path.join(layer_folder, f'0gameicon/Language/{language}')
        os.makedirs(gameicon_common_folder, exist_ok=True)
        os.makedirs(gameicon_language_folder, exist_ok=True)

    # 創建全黑圖片並儲存到 frame 資料夾
    black_frame = Image.new('RGB', size, (0, 0, 0))
    black_frame_path = os.path.join(frame_folder, 'black_frame.png')
    black_frame.save(black_frame_path)

    # 创建背景图像
    img_img = Image.open(img_path).convert("RGBA")
    iconX_img = Image.open(iconX_path).convert("RGBA")
    imgA_img = Image.open(imgA_path).convert("RGBA")

    # 調整iconX和imgA圖片大小以適應圖標大小，保持長寬比並填滿框架
    iconX_img = resize_with_aspect_ratio_fill(iconX_img, size)
    imgA_img = resize_with_aspect_ratio_fill(imgA_img, size)

    if apply_mask and mask_path:
        # 1. 載入蒙版並轉換為灰階模式
        mask_img = Image.open(mask_path).convert("L")  # 將蒙版加載為灰階模式
        mask_img = mask_img.resize(iconX_img.size, Image.LANCZOS)

        # 2. 確保 iconX 圖片具有 alpha 通道
        iconX_img = iconX_img.convert("RGBA")

        # 3. 分離 iconX 圖片的 RGBA 通道
        r, g, b, alpha_channel = iconX_img.split()

        # 4. 通過將 alpha 通道與蒙版相乘來結合透明度效果
        new_alpha = ImageChops.multiply(alpha_channel, mask_img)

        # 5. 將結合后的 alpha 通道應用回 iconX 圖片
        iconX_img.putalpha(new_alpha)

    # 調整背景圖像大小
    img_img = img_img.resize(size, Image.LANCZOS)

    # 合併圖像
    combined_img = img_img.copy()
    combined_img = Image.alpha_composite(combined_img.convert("RGBA"), iconX_img)
    combined_img = Image.alpha_composite(combined_img, imgA_img)

    # 保存每一層
    img_img_path = os.path.join(img_iconX_folder, "1background.png")
    iconX_img_path = os.path.join(img_iconX_folder, "2iconX.png")
    imgA_img_path = os.path.join(imgA_folder, "3imgAration.png")
    
    # 保存背景圖像
    img_img.save(img_img_path)

    # 保存符號圖像
    iconX_img.save(iconX_img_path)

    # 保存裝飾圖像
    imgA_img.save(imgA_img_path)

    if size == (301, 300):
        folder_name = os.path.basename(assets_path)
        common_img_path = os.path.join(gameicon_common_folder, f"{folder_name}.png")
        if not os.path.exists(common_img_path):
            iconX_img.save(common_img_path)

    icon_img = combined_img

    # 創建畫布
    draw = ImageDraw.Draw(icon_img)

    # 動態調整文字大小並包裝文字
    font, wrapped_text, line_spacing = adjust_text_size(text, font_path, text_frame)

    # 獲取字體的 ascent 和 descent
    ascent, descent = font.getmetrics() 
    
    # 計算每行文字的位置
    if len(wrapped_text) == 1:
        y_offset = (text_frame[1] - font.size) // 2  # 單行文字垂直居中
        text_y_start = size[1] - text_frame[1] + text_frame_offset + y_offset
        line_height = font.size
    else:
        y_offset = (text_frame[1] - font.size * len(wrapped_text)) // (len(wrapped_text) + 1)  # 多行文字垂直間距
        text_y_start = size[1] - text_frame[1] + text_frame_offset + y_offset
        line_height = font.size + y_offset

    # 文字漸層
    text_layer = Image.new('RGBA', size, (255, 255, 255, 0))
    shadow_layer = Image.new('RGBA', size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)
    shadow_draw = ImageDraw.Draw(shadow_layer)

    for i, line in enumerate(wrapped_text):
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = ascent + descent
        text_x = (size[0] - text_width) // 2
        text_y = text_y_start + i * line_height

        # 根據語言設置調整基線高度
        text_y += int(text_frame[1] * settings["baseline_adjustment"])

        # 繪製陰影文字
        shadow_offset_y = font.size // 8
        shadow_draw.text((text_x, text_y + shadow_offset_y), line, font=font, fill=settings["shadow_color"])

        # 創建文字漸層
        gradient_colors = settings["gradient_colors"]
        gradient_layer = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
        gradient_draw = ImageDraw.Draw(gradient_layer)

        for y in range(text_height):
            blend = y / text_height
            for j in range(len(gradient_colors) - 1):
                if gradient_colors[j][0] <= blend <= gradient_colors[j + 1][0]:
                    start_blend, start_color = gradient_colors[j]
                    end_blend, end_color = gradient_colors[j + 1]
                    local_blend = (blend - start_blend) / (end_blend - start_blend)
                    r = int(start_color[0] * (1 - local_blend) + end_color[0] * local_blend)
                    g = int(start_color[1] * (1 - local_blend) + end_color[1] * local_blend)
                    b = int(start_color[2] * (1 - local_blend) + end_color[2] * local_blend)
                    gradient_draw.line([(0, y), (text_width, y)], fill=(r, g, b))
                    break

        # 創建一個透明的文字蒙版層，大小與文字一致
        text_alpha_layer = Image.new('L', (text_width, text_height), 0)
        text_alpha_draw = ImageDraw.Draw(text_alpha_layer)

        # 繪製文字到文字蒙版層
        text_alpha_draw.text((0, 0), line, font=font, fill=255)

        # 使用文字蒙版作為 alpha 通道應用到漸層層上
        gradient_layer.putalpha(text_alpha_layer)

        # 將漸層文字圖層粘貼到圖標圖像上
        text_layer.paste(gradient_layer, (text_x, text_y), gradient_layer)


    # 保存文字圖層和陰影圖層
    text_layer_path = os.path.join(language_folder, "5text.png")
    shadow_layer_path = os.path.join(language_folder, "4text_shadow.png")
    text_layer.save(text_layer_path)
    shadow_layer.save(shadow_layer_path)

    # 合併文字和陰影圖層
    text_shadow_combined = Image.alpha_composite(shadow_layer, text_layer)

    if size == (301, 300):
        folder_name = os.path.basename(assets_path)
        merged_text_shadow_img_path = os.path.join(gameicon_language_folder, f"txt_{folder_name}_{language}.png")
        text_shadow_combined.save(merged_text_shadow_img_path, "PNG")
    
    # 保存最終圖像
    if suffix:
        output_path = os.path.join(png_folder, f"{en_name}_{size[0]}x{size[1]}{suffix}_{language}.png")
    else:
        output_path = os.path.join(png_folder, f"{en_name}_{size[0]}x{size[1]}_{language}.png")
    
    icon_img = Image.alpha_composite(icon_img, text_shadow_combined)
    icon_img.save(output_path, "PNG")
    print(f"Icon saved: {output_path}")

def main():
    # 獲取腳本執行位置（當前目錄）
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # 列出符合條件的資料夾，並讓用戶選擇
    selected_folders = list_available_datasets(base_path)

    # 獲取語言列表
    languages = get_languages()

    # 遍歷所有的資料集
    for folder in selected_folders:
        assets_path = os.path.join(base_path, folder)  # 將資料夾名稱與 base_path 組合成完整路徑

        # 調用 read_csv_data 函數來讀取當前資料集的 CSV 文件
        nas_data_list, apply_masks = read_csv_data(assets_path, 'prefix_mask_data.csv', 'prefix_mask_data')
        
        for index, nas_data in enumerate(nas_data_list):
            nas_data = nas_data.strip()

            # Apply masks if the value is 'Y' or 'y' (case-insensitive)
            apply_mask = apply_masks[index].strip().lower() == 'y'

            # 讀取文本數據
            text_data = read_csv_data(assets_path, 'text_data.csv', 'text_data')

            # 單獨創建 ENU 變數
            en_name = text_data.get("ENU", "")

            icon_output_folder = f"{nas_data}_{en_name}"
            os.makedirs(icon_output_folder, exist_ok=True)

            # 在 icon_output_folder 下創建 "icon" 資料夾
            icon_folder = os.path.join(icon_output_folder, "ICON")
            os.makedirs(icon_folder, exist_ok=True)

            # 在 "icon" 資料夾下創建 "PNG" 資料夾
            png_folder = os.path.join(icon_folder, "PNG")
            os.makedirs(png_folder, exist_ok=True)

            # 配置設置
            config = get_config(assets_path)
            icon_sizes = config['icon_sizes']
            fonts = config['fonts']

            for icon_config in config['icon_sizes']:
                for language in languages:
                    text = text_data.get(language, "")  # 從 text_data 中獲取對應語言的文本
                    create_icon(
                        assets_path,
                        en_name,
                        language,
                        text,
                        icon_config["size"],
                        icon_config["text_frame"],
                        icon_config["text_frame_offset"],
                        icon_config["img"],
                        icon_config["imgA"],
                        icon_config["iconX"],
                        icon_config["mask"],
                        config['fonts'][language],
                        apply_mask,
                        png_folder,  # 傳遞 png_folder 作為圖標存放目錄
                        icon_config.get("suffix", "")
                    )

            # 生成預覽圖
            preprocessed_images = preprocess_images(config['icon_sizes'], languages, png_folder, en_name)
            preview_path = f"{assets_path}_Preview.png"
            adaptive_grid_layout(preprocessed_images, preview_path)

            print(f"Preview saved: {preview_path}")

            # 調用壓縮函數壓縮圖標
            #compress_images(png_folder, assets_path, en_name, config)

            # 移動 gameicon 資料夾
            #move_gameicon_folder(assets_path)

if __name__ == "__main__":
    main()