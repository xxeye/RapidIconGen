import os
import subprocess

def get_languages():
    # 返回所有支持的語言代碼
    return ["CNY", "CHT", "ENU", "ESP", "PTE", "THB", "VND"]

    """
    壓縮 PNG 文件的函數
    :param png_file: PNG 文件的路徑
    :param quality: 壓縮質量範圍，默認 "40-60"
    :param speed: 壓縮速度，默認 1（最慢）
    """
def compress_png(png_file, quality="40-60", speed=1):
    subprocess.run([
        "pngquant", f"--quality={quality}", f"--speed={speed}", "--ext=.png", "--force", "--floyd=0.4", png_file
    ])
    print(f"Compressed: {png_file}")

# 讀取配置文件
def get_config(assets_path):
    # 定義圖標尺寸和配置
    icon_sizes = [
        {"size": (128, 128), "text_frame": (100, 22), "text_frame_offset": -13, "img": os.path.join(assets_path, 'img/128x128.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_128x128.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_500x500.png'), "mask": os.path.join(assets_path, 'mask/mask_128x128.png')},
        {"size": (146, 136), "text_frame": (120, 30), "text_frame_offset": -7, "img": os.path.join(assets_path, 'img/146x136.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_146x136.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_500x500.png'), "mask": os.path.join(assets_path, 'mask/mask_146x136.png')},
        {"size": (200, 200), "text_frame": (160, 37), "text_frame_offset": -19, "img": os.path.join(assets_path, 'img/200x200.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_200x200.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_500x500.png'), "mask": os.path.join(assets_path, 'mask/mask_200x200.png')},
        {"size": (220, 162), "text_frame": (200, 39), "text_frame_offset": -12, "img": os.path.join(assets_path, 'img/220x162.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_220x162.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_500x300.png'), "mask": os.path.join(assets_path, 'mask/mask_220x162.png')},
        {"size": (301, 300), "text_frame": (220, 49), "text_frame_offset": -32, "img": os.path.join(assets_path, 'img/301x300.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_301x300.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_500x500.png'), "mask": os.path.join(assets_path, 'mask/mask_301x300.png')},
        {"size": (500, 300), "text_frame": (475, 55), "text_frame_offset": -25, "img": os.path.join(assets_path, 'img/500x300.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_500x300.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_500x300.png'), "mask": os.path.join(assets_path, 'mask/mask_500x300.png')},
        {"size": (400, 581), "text_frame": (360, 61), "text_frame_offset": -41, "img": os.path.join(assets_path, 'img/400x581.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_400x581.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_400x581.png'), "mask": os.path.join(assets_path, 'mask/mask_400x581.png')},
        {"size": (500, 500), "text_frame": (362, 64), "text_frame_offset": -51, "img": os.path.join(assets_path, 'img/500x500.png'), "imgA": os.path.join(assets_path, 'imgA/imgA_500x500.png'), "iconX": os.path.join(assets_path, 'iconX/iconX_500x500.png'), "mask": os.path.join(assets_path, 'mask/mask_500x500.png')},
    ]

    # 定義字體
    fonts = {
        "CNY": os.path.join(assets_path, 'fonts/HarmonyOS_Sans_TC_Black.ttf'),
        "ENU": os.path.join(assets_path, 'fonts/HarmonyOS_Sans_TC_Black.ttf'),
        "ESP": os.path.join(assets_path, 'fonts/HarmonyOS_Sans_TC_Black.ttf'),
        "PTE": os.path.join(assets_path, 'fonts/HarmonyOS_Sans_TC_Black.ttf'),
        "THB": os.path.join(assets_path, 'fonts/tahomabd.ttf'),
        "VND": os.path.join(assets_path, 'fonts/HarmonyOS_Sans_TC_Black.ttf'),
        "CHT": os.path.join(assets_path, 'fonts/HarmonyOS_Sans_TC_Black.ttf'),
    }

    return {
        "icon_sizes": icon_sizes,
        "fonts": fonts
    }

#get_language_settings函數_文字漸層顏色
DEFAULT_GRADIENT_COLORS = [
    (0.0, (239, 215, 255)),  # 起始顏色
    (0.3, (239, 215, 255)),  # 中間顏色
    (1.0, (177, 177, 241))    # 結束顏色
]
#get_language_settings函數_文字陰影顏色
DEFAULT_SHADOW_COLOR = "#352043"  # 統一的陰影顏色

def get_language_settings():
    return {
        "CNY": {
            "baseline_adjustment": -0,
            "shadow_color": DEFAULT_SHADOW_COLOR,  # 使用統一的陰影顏色
            "gradient_colors": DEFAULT_GRADIENT_COLORS  # 使用統一的漸層顏色
        },
        "CHT": {
            "baseline_adjustment": -0,
            "shadow_color": DEFAULT_SHADOW_COLOR,  # 使用統一的陰影顏色
            "gradient_colors": DEFAULT_GRADIENT_COLORS  # 使用統一的漸層顏色
        },
        "ENU": {
            "baseline_adjustment": 0,
            "shadow_color": DEFAULT_SHADOW_COLOR,  # 使用統一的陰影顏色
            "gradient_colors": DEFAULT_GRADIENT_COLORS  # 使用統一的漸層顏色
        },
        "ESP": {
            "baseline_adjustment": 0,
            "shadow_color": DEFAULT_SHADOW_COLOR,  # 使用統一的陰影顏色
            "gradient_colors": DEFAULT_GRADIENT_COLORS  # 使用統一的漸層顏色
        },
        "PTE": {
            "baseline_adjustment": 0,
            "shadow_color": DEFAULT_SHADOW_COLOR,  # 使用統一的陰影顏色
            "gradient_colors": DEFAULT_GRADIENT_COLORS  # 使用統一的漸層顏色
        },
        "THB": {
            "baseline_adjustment": -0,
            "shadow_color": DEFAULT_SHADOW_COLOR,  # 使用統一的陰影顏色
            "gradient_colors": DEFAULT_GRADIENT_COLORS  # 使用統一的漸層顏色
        },
        "VND": {
            "baseline_adjustment": 0,
            "shadow_color": DEFAULT_SHADOW_COLOR,  # 使用統一的陰影顏色
            "gradient_colors": DEFAULT_GRADIENT_COLORS  # 使用統一的漸層顏色
        }
    }