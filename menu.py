# import functions and librarys here
from text_on_image import text_on_image
from camera import photobooth
import cv2

print("Welcome to the photobooth")
print(
    "Choose one to start with:\n [1] Sunglasses 1 \n [2] Sunglasses 2 \n [3] Sunglasses 3 \n [4] Sunglasses 4 \n [5] Sunglasses 5 \n [6] Write Text \n Enter 7 to stat the photobooth! \n Enter 0 to quit"
)

props = [
    "props/black_glasses.png",
    "props/blue_glasses.png",
    "props/green_glasses.png",
    "props/red_glasses.png",
    "props/yellow_glasses.png",
    "props/speech2.png",
    "props/blue_mask.png",
    "props/red_mask.png",
    "props/yellow_mask.png",
]  # populate this with the image later
chosen_type = ""

while True:
    option = int(input("Enter your option here: "))
    print("Loading ... ")
    # update with function later
    if option == 10:
        if chosen_prop: break
        else: print("Please choose a prop first.")
    if option == 6:
        text = input("Enter the text you would like to show on the speech bubble: ")
        text_on_image(text)
        chosen_prop = "props/speech2.png"
        # path for the image is speech2.png, will create in the root of this folder
    elif option in [1, 2, 3, 4, 5, 7, 8, 9]:
        chosen_prop = props[option - 1]
        chosen_type = "glasses"
    elif option == 0: break

if option == 10:
    photobooth(chosen_prop, chosen_type)
