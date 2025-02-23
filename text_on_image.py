# reference taken from https://www.geeksforgeeks.org/adding-text-on-image-using-python-pil/

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def text_on_image(text):
    if len(text) > 180: return False
    else:
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

        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img)

        # Define the initial font and size
        font_path = "others/Prototype.ttf"
        font_size = 300
        myFont = ImageFont.truetype(font_path, font_size)

        # Split the formatted text into lines
        lines = formatted_text.split("\n")

        # Adjust font size if any line overflows the image width
        for line in lines:
            text_bbox = I1.textbbox((0, 0), line, font=myFont)
            text_width = text_bbox[2] - text_bbox[0]
            content_window_width = 1600  # Adjust this value based on the width of the content window

            while text_width > content_window_width - 20:  # 20 pixels padding
                font_size -= 5
                myFont = ImageFont.truetype(font_path, font_size)
                text_bbox = I1.textbbox((0, 0), line, font=myFont)
                text_width = text_bbox[2] - text_bbox[0]

        # Calculate the total height of the text block
        total_text_height = sum([I1.textbbox((0, 0), line, font=myFont)[3] - I1.textbbox((0, 0), line, font=myFont)[1] for line in lines]) + (len(lines) - 1) * 10

        # Adjust the starting y-coordinate to center the text block vertically within the speech bubble
        content_window_top = 20
        content_window_height = 1450
        og_y = content_window_top + (content_window_height - total_text_height) // 2

        # Add each line of text to the image, centered
        for line in lines:
            text_bbox = I1.textbbox((0, 0), line, font=myFont)
            text_width = text_bbox[2] - text_bbox[0]
            content_window_left = 600  # Adjust this value based on the left position of the content window
            x_coordinate = content_window_left + (content_window_width - text_width) // 2

            I1.text(
                (x_coordinate, og_y),
                line,
                font=myFont,
                fill=(0, 0, 0),
            )
            og_y += font_size + 10  # Move to the next line

        # Save the edited image
        img.save("props/speech2.png")
        return True