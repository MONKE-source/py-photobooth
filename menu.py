import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from text_on_image import text_on_image
from camera import photobooth

def start_photobooth():
    if chosen_prop:
        if chosen_type == "masks":
            messagebox.showinfo("Info", "Welcome to the masquerade!")
        else:
            messagebox.showinfo("Info", "Loading photobooth...")
        photobooth(chosen_prop, chosen_type, camera.get(), debug.get())
    else:
        messagebox.showwarning("Warning", "Please choose a prop first.")

def choose_prop(option):
    global chosen_prop, chosen_type
    if option == "6":
        text = text_entry.get()
        if text_on_image(text):
            chosen_prop = "props/speech2.png"
            chosen_type = "speech"
            messagebox.showinfo("Success", f"Your prop is now a speech bubble with {text} on it.")
        else:
            messagebox.showerror("Error", f"Your text is {len(text) - 170} characters too long! Please try again.")
    else:
        chosen_prop = props[int(option) - 1]
        chosen_type = types[int(option) - 1]
        messagebox.showinfo("Success", f"Success! Your prop is now a {chosen_type}!")
        messagebox.showinfo("Lore", lore[int(option) - 1])

def on_quit():
    root.destroy()

root = tk.Tk()
root.title("Photobooth Menu")
root.geometry("800x1000")
root.resizable(False, False)

camera = tk.IntVar(value=0)
debug = tk.IntVar(value=0)
chosen_prop = ""
chosen_type = ""

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
]
types = [
    "glasses", "glasses", "glasses", "glasses", "glasses",
    "speech", "masks", "masks", "masks", "masks", "masks",
    "masks", "princess", "prayer"
]
lore = [
    "A precious piece of art, glasses made by black house representatives of SSTudents to showcase their brilliance and bravery.",
    "A precious piece of art, glasses made by blue house representatives of SSTudents to showcase their valour and victories.",
    "A precious piece of art, glasses made by green house representatives of SSTudents to showcase their might and majesty.",
    "A precious piece of art, glasses made by red house representatives of SSTudents to showcase their fearlessness and firey heart.",
    "A precious piece of art, glasses made by yellow house representatives of SSTudents to showcase their strength and spirit.",
    "A right to speak.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the black house, a symbol of brilliance and bravery.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the blue house, a symbol of valour and victories.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the green house, a symbol of might and majesty.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the red house, a symbol of fearlessness and firey heart.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent the yellow house, a symbol of strength and spirit.",
    "The mysterious masquerade opens to SST! A masquerade mask to represent all those who visit the masquerade.",
    "The mysterious masquerade opens to SST! A masquerade mask only given to the most beautiful, the most noble, the most worthy of the masquerade's Lady.",
    "The mysterious masquerade opens to SST! A masquerade mask only given to the most forbearant, the most gentle, the most caring of the masquerade's cleric."
]

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=1)
style.configure("TLabel", font=("Helvetica", 14), padding=1)

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

ttk.Label(main_frame, text="Welcome to the Photobooth!", font=("Helvetica", 16, "bold")).pack(pady=10)

camera_frame = ttk.LabelFrame(main_frame, text="Camera Selection", padding="10")
camera_frame.pack(fill="both", expand=True, pady=5)
ttk.Radiobutton(camera_frame, text="Default", variable=camera, value=0).pack(anchor="w")
ttk.Radiobutton(camera_frame, text="External", variable=camera, value=1).pack(anchor="w")

debug_frame = ttk.LabelFrame(main_frame, text="Debug Mode", padding="10")
debug_frame.pack(fill="both", expand=True, pady=5)
ttk.Checkbutton(debug_frame, text="Enable Debug Mode", variable=debug).pack(anchor="w")

prop_frame = ttk.LabelFrame(main_frame, text="Choose a Prop", padding="10")
prop_frame.pack(fill="both", expand=True, pady=5)
options = [
    "Black Sunglasses", "Blue Sunglasses", "Green Sunglasses", "Red Sunglasses", "Yellow Sunglasses",
    "Write Text for Speech Bubble", "Black Mask", "Blue Mask", "Green Mask", "Red Mask", "Yellow Mask",
    "Visitor's Mask", "Princess, Complimentary Masquerade Mask 1", "Prayer, Complimentary Masquerade Mask 2"
]
for i, option in enumerate(options):
    ttk.Button(prop_frame, text=option, command=lambda i=i: choose_prop(str(i + 1))).pack(fill="x", pady=2)

speech_frame = ttk.LabelFrame(main_frame, text="Speech Bubble Text", padding="10")
speech_frame.pack(fill="both", expand=True, pady=5)
text_entry = ttk.Entry(speech_frame)
text_entry.pack(fill="x")

ttk.Button(main_frame, text="Start Photobooth", command=start_photobooth).pack(pady=10)
ttk.Button(main_frame, text="Quit", command=on_quit).pack(pady=5)

root.mainloop()