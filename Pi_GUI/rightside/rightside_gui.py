from tkinter import *
from PIL import Image as PILImage
from PIL import ImageTk
import math

# Create window
root = Tk()
root.title("GUI")
width = 800
height = 480

# Full screen
'''root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  #Move focus to this widget
root.bind("<Escape>", lambda e: root.quit())'''
root.geometry("{}x{}".format(width, height))

#Create canvas
ctx = Canvas(root, width=width, height = height, background="black")
ctx.pack()

def resize(photo, w, h):
    scale = (min(w / photo.width(), h / photo.height()))
    if scale > 1:
        scale = math.floor(scale)
        #print("Zoom in " + str(scale) + "x")
        photo = photo.zoom(scale)
    elif scale < 1:
        scale = math.ceil(1 / scale)
        #print("Zoom out " + str(scale) + "x")
        photo = photo.subsample(scale)
    return photo

def rotate(photo, deg):
	photo2 = PILImage
	return photo


# Create images
claw_orig = PILImage.open("claw.png")
claw_orig.convert("RGBA")
claw = claw_orig
claw_level = ImageTk.PhotoImage(claw)
claw_angles = [60, 30, 0, -30]

exitButton = PhotoImage(file="exitButton.gif")

#Resize buttons
extBtnWidth = 50
extBtnHeight = 50
exitButton = resize(exitButton, extBtnWidth, extBtnHeight)

btnWidth = 250
btnHeight = 120

claw_x = (width - btnWidth)/4 + 20 #(width - btnWidth)/2
claw_y = height/2 - 20

current_btn = -1

#Create buttons
claw = ctx.create_image(claw_x, claw_y, image=claw_level, tag="claw", anchor=CENTER)
ctx.create_image(extBtnWidth/2, height - extBtnHeight/2, image=exitButton)
upRect = ctx.create_rectangle(800, btnHeight, 800 - btnWidth, btnHeight * 0, outline="white") #up
ballRect = ctx.create_rectangle(800, btnHeight * 2, 800 - btnWidth, btnHeight * 1, outline="white") #ball
levelRect = ctx.create_rectangle(800, btnHeight * 3, 800 - btnWidth, btnHeight * 2, outline="white") #level
downRect = ctx.create_rectangle(800, btnHeight * 4, 800 - btnWidth, btnHeight * 3, outline="white") #down

buttons = [upRect, ballRect, levelRect, downRect]

#Create text
ctx.create_text((800 - btnWidth) + (btnWidth / 2), btnHeight / 2, text = "UP", fill = "white", font = "helvetica 40")
ctx.create_text((800 - btnWidth) + (btnWidth / 2), (btnHeight + btnHeight / 2), text = "BALL", fill = "white", font = "helvetica 40")
ctx.create_text((800 - btnWidth) + (btnWidth / 2), (btnHeight * 2 + btnHeight / 2), text = "LEVEL", fill = "white", font = "helvetica 40")
ctx.create_text((800 - btnWidth) + (btnWidth / 2), (btnHeight * 3 + btnHeight / 2), text = "DOWN", fill = "white", font = "helvetica 40")

#Highlight when clicked
def handle_click(event):
	if event.x <= extBtnWidth and event.y >= height - extBtnHeight:
		print("Exiting...")
		root.destroy()
		return

	if event.x >= 800 - btnWidth and event.y >= 0 and event.y < btnHeight: # UP
		button_num = 0
	elif event.x >= 800 - btnWidth and event.y >= btnHeight and event.y < btnHeight * 2: # BALL
		button_num = 1
	elif event.x >= 800 - btnWidth and event.y >= btnHeight * 2 and event.y < btnHeight * 3: # LEVEL
		button_num = 2
	elif event.x >= 800 - btnWidth and event.y >= btnHeight * 3 and event.y < btnHeight * 4: # DOWN
		button_num = 3
	else:
		button_num = -1
	
	render_claw(button_num)
	fill_rect(button_num)
	ctx.create_image(extBtnWidth/2, height - extBtnHeight/2, image=exitButton)
	current_btn = button_num
	
claw_temp = None
current_angle = 0
goal = 0

def render_claw(button_num):
	global goal
	if button_num == -1:
		return
	#claw = ctx.create_image(claw_x, claw_y, image=claws[button_num][0], tag="claw", anchor=CENTER)
	print("Gonna like rotate to {} degrees, man".format(claw_angles[button_num]))
	goal = claw_angles[button_num]

def rotate_claw():
	global claw, claw_temp, claw_orig, current_angle, goal
	if not goal == current_angle:
		if (abs(goal - current_angle) <= 0.5):
			current_angle = goal
		err = goal - current_angle
		kP = 0.25
		current_angle += err * kP
		claw_temp = claw_orig.copy()
		claw_temp = claw_temp.rotate(current_angle)
		claw_temp = ImageTk.PhotoImage(claw_temp)
		ctx.delete("claw")
		claw = ctx.create_image(claw_x, claw_y, image=claw_temp, tag="claw", anchor=CENTER)
	root.after(int(1000/60), rotate_claw)

rotate_claw()

def fill_rect(button_num):
	if button_num == -1:
		return

	for button in buttons:
		ctx.itemconfig(button, fill = "black")
	ctx.itemconfig(buttons[button_num], fill = "blue")

ctx.bind("<Button-1>", handle_click)

root.mainloop()
