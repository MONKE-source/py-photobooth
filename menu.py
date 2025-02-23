# import functions and librarys here
from text_on_image import text_on_image
from camera import photobooth

print("Welcome to the Photobooth!")

# camera for cv2.VideoCapture bc i have obs on my macbook sorry gang
while True:
    try:
        camera = int(input("Which camera would you like to use? 0 for default, 1 for external: "))
        if camera not in [0, 1]: raise ValueError
        else: break
    except ValueError:
        print("Invalid input. Please input 0 or 1.") 
# a debug mode that will show FPS counter and landmarks
debug = input("Do you wish to turn on debug mode? 1 for Yes, any other input else for No: ") 
if debug != "1": debug = 0
else: debug = 1

print(
    "Choose one to start with:\n [1] Black Sunglasses \n [2] Blue Sunglasses \n [3] Green Sunglasses \n [4] Red Sunglasses \n [5] Yellow Sunglasses \n [6] Write Text \n [7] Blue Mask \n [8] Red Mask \n [9] Yellow Mask \n Enter 10 to start the photobooth! \n Enter 0 to quit"
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
chosen_prop = ""

while True:
    option = int(input("Enter your option here: "))
    print("Loading ... ")
    if option == 10: # option to activate photobooth()
        if chosen_prop: break
        else: print("Please choose a prop first.")
    if option == 6: # speec bubble function
        text = input("Enter the text you would like to show on the speech bubble: ")
        text_on_image(text)
        chosen_prop = "props/speech2.png"
        chosen_type = "speech"
    elif option in [1, 2, 3, 4, 5]: # glasses prop
        chosen_prop = props[option - 1]
        chosen_type = "glasses"
    elif option in [7, 8, 9]: # glasses prop
        chosen_prop = props[option - 1]
        chosen_type = "masks"
    elif option == 0: break

if option == 10: photobooth(chosen_prop, chosen_type, camera, debug)