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
    """Choose one to start with:
    [1] Black Sunglasses 
    [2] Blue Sunglasses 
    [3] Green Sunglasses 
    [4] Red Sunglasses 
    [5] Yellow Sunglasses 
    [6] Write Text for Speech Bubble
    [7] Black Mask 
    [8] Blue Mask 
    [9] Green Mask 
    [10] Red Mask 
    [11] Yellow Mask 
    [12] Visitor's Mask
    [13] Princess, Complimentary Masquerade Mask 1
    [14] Prayer, Complimentary Masquerade Mask 2
    Enter 0 to start the photobooth! 
    Enter QUIT to quit"""
)

props = [
    "props/black_glasses.png",
    "props/blue_glasses.png",
    "props/green_glasses.png",
    "props/red_glasses.png",
    "props/yellow_glasses.png",
    "props/speech2.png",
    "props/black_mask.png",
    "props/blue_mask.png",
    "props/green_mask.png",
    "props/red_mask.png",
    "props/yellow_mask.png",
    "props/visitor.png",
    "props/princess.png",
    "props/prayer.png",
]  # populate this with the image later
lore = [
    "A precious piece of art, glasses made by black house representatives of SSTudents to showcase their brilliance and bravery.",
    "A precious piece of art, glasses made by blue house representatives of SSTudents to showcase their valour and victories.",
    "A precious piece of art, glasses made by green house representatives of SSTudents to showcase their might and majesty.",
    "A precious piece of art, glasses made by red house representatives of SSTudents to showcase their fearlessness and firey heart.",
    "A precious piece of art, glasses made by yellow house representatives of SSTudents to showcase their strength and spirit.",
    "A right to speak.", # not shown
    "The mysterious masquerade opens to SST! A masquerade mask to represent the black house, a symbol of brilliance and bravery.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the blue house, a symbol of valour and victories.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the green house, a symbol of might and majesty.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the red house, a symbol of fearlessness and firey heart.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the yellow house, a symbol of strength and spirit.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent all those who visit the masquerade.",
    "The mysterious masquerade opens to SST! A masquerade mask only given to the most beautiful, the most noble, the most worthy of the masquerade's Lady.",
    "The mysterious masquerade opens to SST! A masquerade mask only given to the most forbearant, the most gentle, the most caring of the masquerade's cleric."
]
chosen_type = ""
chosen_prop = ""

while True:
    option = input("Enter your option here: ")
    print("Loading ... ")
    if option == "0": # option to activate photobooth()
        if chosen_prop: break
        else: print("Please choose a prop first.")
    if option == "6": # speec bubble function
        text = input("Enter the text you would like to show on the speech bubble: ")
        if text_on_image(text):
            chosen_prop = "props/speech2.png"
            chosen_type = "speech"
            print(f"Success! Your prop is now a speech bubble with {text} on it.")
        else: print(f"Your text is {len(text) - 170} characters too long! Please try again.")
    elif option in ["1", "2", "3", "4", "5"]: # glasses prop
        chosen_prop = props[int(option) - 1]
        chosen_type = "glasses"
        print(f"Success! Your prop is now a pair of glasses!")
        print(lore[int(option) - 1])
    elif option in ["7", "8", "9", "10", "11", "12"]: # glasses prop
        chosen_prop = props[int(option) - 1]
        chosen_type = "masks"
        print(f"Success! Welcome to the masquerade, enjoy your complimentry masquerade mask!")
        print(lore[int(option) - 1])
    elif option == "13":
        chosen_prop = props[int(option) - 1]
        chosen_type = "princess"
        print(f"Success! Welcome to the masquerade, enjoy your complimentry masquerade mask!")
        print(lore[int(option) - 1])
    elif option == "14":
        chosen_prop = props[int(option) - 1]
        chosen_type = "prayer"
        print(f"Success! Welcome to the masquerade, enjoy your complimentry masquerade mask!")
        print(lore[int(option) - 1])
    elif option == "QUIT": break
    else: print("Invalid input, please try again.")

if option == "0": 
    if chosen_type == "masks": print("Welcome to the masquerade!")
    else: print("Loading photobooth...")
    photobooth(chosen_prop, chosen_type, camera, debug)