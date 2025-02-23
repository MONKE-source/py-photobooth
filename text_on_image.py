# reference taken from https://www.geeksforgeeks.org/adding-text-on-image-using-python-pil/

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def text_on_image(text):
    img = Image.open("props/bubble.png")
    text_arr = text.split(" ")

    # variables for the text splitting
    formatted_text = ""
    current_line = ""
    max_chars_per_line = 30

    # Adding line breaks to the text so that it stays inside the speech bubble
    for word in text_arr:
        if len(current_line) + len(word) + 1 > max_chars_per_line:
            formatted_text += current_line.strip() + "\n"
            current_line = word + " "
        else:
            current_line += word + " "
    # https://stackoverflow.com/questions/66721102/how-can-i-create-a-new-line-after-a-set-of-characters-in-python

    # Add the last line
    formatted_text += current_line.strip()

    # variables for ensuring the lining part is correct
    og_y = 750  # Adjusted to move the text up
    num_line_breaks = formatted_text.count("\n")

    # move the text accordingly
    if num_line_breaks > 3:
        for i in range(num_line_breaks - 3):
            if og_y == 500:
                break
            og_y -= 400

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)

    # Define the initial font and size
    font_path = "others/Prototype.ttf"
    font_size = 300
    myFont = ImageFont.truetype(font_path, font_size)

    # Calculate the width of the text and adjust the x-coordinate to center it
    text_bbox = I1.textbbox((0, 0), formatted_text, font=myFont)
    text_width = text_bbox[2] - text_bbox[0]
    img_width = img.width

    # Adjust font size if text overflows the image width
    while text_width > img_width - 20:  # 20 pixels padding
        font_size -= 55
        myFont = ImageFont.truetype(font_path, font_size)
        text_bbox = I1.textbbox((0, 0), formatted_text, font=myFont)
        text_width = text_bbox[2] - text_bbox[0]

    x_coordinate = (img_width - text_width) // 2

    # Add Text to an image
    I1.text(
        (x_coordinate, og_y),
        formatted_text,
        font=myFont,
        fill=(0, 0, 0),
    )

    # Save the edited image
    img.save("props/speech2.png")