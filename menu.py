# import functions and librarys here
from text_on_image import text_on_image
from camera import photobooth_glasses
import cv2

print("Welcome to the photobooth")
print(
    "Choose one to start with:\n [1] Black Sunglasses  \n [2] Blue Sunglasses \n [3] Green Sunglasses  \n [4] Red Sunglasses \n [5] Yellow Sunglasses \n [6] Write Text \n [7] Transparent Blue \n [8] Transparent Red \n Enter 9 to start the photobooth! \n Enter 0 to quit"
)
props = [
    "props/black_glasses.png",
    "props/blue_glasses.png",
    "props/green_glasses.png",
    "props/red_glasses.png",
    "props/yellow_glasses.png",
    "props/speech2.png",
    "props/transparent_blue.png",
    "props/transparent_red.png",
]  # populate this with the image later
chosen_prop = ""

while True:
    option = int(input("Enter your option here: "))
    print("Loading ... ")
    # update with function later
    if option == 9:
        if chosen_prop:
            break
        else:
            print("Please choose a prop first.")
    if option == 6:
        text = input("Enter the text you would like to show on the speech bubble: ")
        text_on_image(text)
        chosen_prop = "props/speech2.png"
        # path for the image is speech2.png, will create in the root of this folder
    elif option in [1, 2, 3, 4, 5, 6, 7, 8]:
        chosen_prop = props[option - 1]
    elif option == 0:
        break

if option == 9:
    photobooth_glasses(chosen_prop)
