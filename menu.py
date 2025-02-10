# import functions and librarys here
from text_on_image import text_on_image

print("Welcome to the photobooth")
print(
    "Choose one to start with:\n [1] Sunglasses 1 \n [2] Sunglasses 2 \n [3] Sunglasses 3 \n [4] Sunglasses 4 \n [5] Sunglasses 5 \n [6] Write Text \n Enter 0 to quit"
)
props = []  # populate this with the image later

while True:
    option = int(input("Enter your option here: "))
    print("Loading ... ")
    # update with function later
    if option == 6:
        text = input("Enter the text you would like to show on the speech bubble: ")
        text_on_image(text)

    if option == 0:
        break
