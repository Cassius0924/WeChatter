from PIL import Image, ImageDraw, ImageFont


def text_to_image(data: str) -> str:
    image_width = 1000  # Width of the image
    line_height = 30  # Height of each line
    num_columns = 2  # Number of columns for text

    background_color = (255, 255, 255)  # White

    # 根据换行符(\n)将文本分成几行
    lines = data.split("\n")
    num_lines = len(lines)

    # 根据行数和行高计算图像高度
    max_lines_per_column = (num_lines + num_columns - 1) // num_columns
    image_height = max_lines_per_column * line_height
    image = Image.new("RGB", (image_width, image_height), background_color)

    # 选择字体和字体大小
    font_path = "../assets/fonts/SimHei.ttf"  # Replace with your font file path
    font_size = 25
    font = ImageFont.truetype(font_path, font_size)

    # 创建绘图上下文
    draw = ImageDraw.Draw(image)

    # 定义文本颜色
    text_color = (0, 0, 0)  # Black

    # 定义初始文本位置(左上角)
    x_position = 50
    y_position = 50

    lines_drawn = 0
    for i in range(num_columns):
        column_lines = lines[lines_drawn : lines_drawn + max_lines_per_column]
        if not column_lines:
            break

        text = "\n".join(column_lines)
        draw.text((x_position, y_position), text, fill=text_color, font=font)
        x_position += image_width // num_columns  # 移动到下一列
        lines_drawn += len(column_lines)
        y_position = 50  # 重置下一列的y_position

    # 保存图像
    output_image_path = "data/text_image/help.png"
    image.save(output_image_path)
    return output_image_path
