# reference taken from https://www.geeksforgeeks.org/adding-text-on-image-using-python-pil/

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

img = Image.open("props/bubble.png")
text = "They have shown that when Pt-WO3 film is ex- posed to H2 gas,They have shown that when Pt-WO3 film is ex- posed to H2 gas,They have shown that when Pt-WO3 film is ex- posed to H2 gas,"
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
og_y = 1300
num_line_breaks = formatted_text.count("\n")

# move the text accordingly
if num_line_breaks > 3:
    for i in range(num_line_breaks - 3):
        if og_y == 500:
            break
        og_y -= 400

# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)

# Define the font and size
myFont = ImageFont.truetype("others/Prototype.ttf", 300)

# Add Text to an image
I1.text(
    (1900, og_y),
    formatted_text,
    font=myFont,
    fill=(0, 0, 0),
)

# Display edited image
img.show()

# Save the edited image
