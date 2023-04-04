from PIL import Image, ImageDraw, ImageFont
import numpy as np

def convert_code_to_image(code, font_path="arial.ttf", font_size=14, background_color=(29, 23, 23), text_color=(10, 250, 158), line_height=20, padding=10, border_width=5, border_color=(255, 255, 255), gradient_size=5, corner_radius=10, dpi_scale=1):
    
    Image.MAX_IMAGE_PIXELS = int(4096 * 4096 * 4096 // 4 // 3)

    font_size = int(font_size * dpi_scale)
    line_height = int(line_height * dpi_scale)
    padding = int(padding * dpi_scale)
    border_width = int(border_width * dpi_scale)
    gradient_size = int(gradient_size * dpi_scale)
    corner_radius = int(corner_radius * dpi_scale)

    font = ImageFont.truetype(font_path, font_size)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        raise ValueError(f"Font file not found or not supported: {font_path}")

    lines = code.split("\n")
    width = max([font.getsize(line)[0] for line in lines])
    height = len(lines) * line_height
    image_width = width + 2 * (padding + gradient_size + border_width)
    image_height = height + 2 * (padding + gradient_size + border_width)
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)
    y = border_width + gradient_size + padding
    for line in lines:
        draw.text((border_width + gradient_size + padding, y), line, text_color, font=font)
        y += line_height

    # Create gradient rectangles with rounded corners
    gradient_rect = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient_rect)

    for i in range(gradient_size):
        alpha = i / gradient_size
        color = tuple([int(alpha * c) for c in border_color]) + (int(255 * alpha),)
        gradient_draw.rounded_rectangle(
            (border_width + i, border_width + i, image_width - 1 - (border_width + i), image_height - 1 - (border_width + i)),
            outline=color, radius=corner_radius)

    # Apply corner radius
    gradient_rect = gradient_rect.resize((gradient_rect.width * 2, gradient_rect.height * 2), resample=Image.BOX)
    gradient_rect = gradient_rect.crop((corner_radius, corner_radius, gradient_rect.width - corner_radius, gradient_rect.height - corner_radius))
    gradient_rect = gradient_rect.resize((image_width, image_height), resample=Image.BOX)

    # Add padding
    padding_rect = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    padding_draw = ImageDraw.Draw(padding_rect)
    padding_color = tuple([int((1 - 1 / gradient_size) * c) for c in border_color]) + (255,)
    padding_draw.rounded_rectangle(
    (border_width + gradient_size, border_width + gradient_size, image_width - 1 - (border_width + gradient_size), image_height - 1 - (border_width + gradient_size)),
    outline=padding_color, radius=corner_radius)

    # Apply corner radius to gradient_rect
    gradient_rect = gradient_rect.resize((gradient_rect.width * 2, gradient_rect.height * 2), resample=Image.LANCZOS)
    gradient_rect = gradient_rect.crop((corner_radius, corner_radius, gradient_rect.width - corner_radius, gradient_rect.height - corner_radius))
    gradient_rect = gradient_rect.resize((image_width, image_height), resample=Image.LANCZOS)

    # Apply corner radius to padding_rect
    padding_rect = padding_rect.resize((padding_rect.width * 2, padding_rect.height * 2), resample=Image.LANCZOS)
    padding_rect = padding_rect.crop((corner_radius, corner_radius, padding_rect.width - corner_radius, padding_rect.height - corner_radius))
    padding_rect = padding_rect.resize((image_width, image_height), resample=Image.LANCZOS)

    # Combine image, gradient, and padding layers
    image = Image.alpha_composite(image.convert("RGBA"), gradient_rect)
    image = Image.alpha_composite(image, padding_rect)

    # Return final image
    return image.convert("RGB")
