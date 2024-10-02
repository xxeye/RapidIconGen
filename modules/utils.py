from PIL import ImageFont

# 文本換行函數
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    line = ''
    
    while words:
        while words and font.getlength(line + words[0]) <= max_width:
            line += (words.pop(0) + ' ')
        
        if not line:
            line = words.pop(0)

        lines.append(line.strip())
        line = ''

    return lines

# 字體縮小函數
def adjust_text_size(text, font_path, text_frame, allowed_exceed_ratio=0.1):
    max_font_size = text_frame[1] * 3 // 4
    font_size = max_font_size
    min_font_size = 10  # 最小字體大小
    font = ImageFont.truetype(font_path, font_size)
    
    line_spacing_factor = 1.2
    max_allowed_height = text_frame[1] * (1 + 0.4)
    
    while font_size >= min_font_size:
        ascent, descent = font.getmetrics()
        line_height = (ascent + descent) * line_spacing_factor
        wrapped_text = wrap_text(text, font, text_frame[0])
        total_height = line_height * len(wrapped_text)
        text_exceeds_width = any(font.getlength(line) > text_frame[0] for line in wrapped_text)
        
        if total_height <= max_allowed_height and not text_exceeds_width:
            return font, wrapped_text, line_height
        
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)

    return font, wrapped_text, (ascent + descent) * line_spacing_factor
