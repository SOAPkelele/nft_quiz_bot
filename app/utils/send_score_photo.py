from PIL import Image, ImageDraw, ImageFont

from app.settings import FILES_DIR


def score_photo(text: str, chat_id: int):
    background = FILES_DIR / "background.jpg"
    font_file = FILES_DIR / "RobotoMono-Regular.ttf"

    image = Image.open(background)
    w_image, h_image = image.size
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(str(font_file), size=95)
    w_text, h_text = font.getsize_multiline(text)

    if w_text > w_image:
        font = ImageFont.truetype(str(font_file), size=75)
        w_text, h_text = font.getsize_multiline(text)

    draw.multiline_text(xy=((w_image - w_text) / 2, (h_image - h_text) / 2),
                        text=text,
                        fill="black",
                        align="center",
                        font=font)
    filename = FILES_DIR / f"scores/{chat_id}.jpg"
    image.save(str(filename))
    return filename
