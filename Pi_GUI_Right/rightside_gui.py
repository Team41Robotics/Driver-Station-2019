from tkinter import *
from PIL import Image as PILImage
from PIL import ImageTk
import math
import serial
#import serial_dummy as serial

# Define serial
ser = serial.Serial(port='/dev/ttyAMA0', baudrate=9600)

# Create window
root = Tk()
root.title("GUI")
width = 800
height = 480

# Full screen
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  #Move focus to this widget
root.bind("<Escape>", lambda e: root.quit())
root.config(cursor="none")
#root.geometry("{}x{}".format(width, height))

#Create canvas
ctx = Canvas(root, width=width, height = height, background="#222")
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
bg_bot = PILImage.open("background-bot.png")
bg_bot.convert("RGBA")
bg_bot = ImageTk.PhotoImage(bg_bot)
ctx.create_image(-230, 125, image=bg_bot, anchor=W)

claw_orig = PILImage.open("bot-arm.png")
claw_orig.convert("RGBA")
claw = claw_orig
claw_level = ImageTk.PhotoImage(claw)
claw_angles = [180, 45, 0]

#exitButton = PhotoImage(file="exitButton.gif")

#Resize buttons
extBtnWidth = 50
extBtnHeight = 50
#exitButton = resize(exitButton, extBtnWidth, extBtnHeight)

btnWidth = 250
btnHeight = int(height / 4)

claw_x = (width - btnWidth)/4 + 100 #(width - btnWidth)/2
claw_y = height/2 + 20

current_btn = -1

#Create buttons
claw = ctx.create_image(claw_x, claw_y, image=claw_level, tag="claw", anchor=CENTER)
#ctx.create_image(extBtnWidth/2, height - extBtnHeight/2, image=exitButton)
ctx.create_rectangle(0, height-extBtnHeight, extBtnWidth, height, fill="red", outline="white")
upRect = ctx.create_rectangle(800, btnHeight, 800 - btnWidth, btnHeight * 0, outline="white") #start
ballRect = ctx.create_rectangle(800, btnHeight * 2, 800 - btnWidth, btnHeight * 1, outline="white") #ball
levelRect = ctx.create_rectangle(800, btnHeight * 3, 800 - btnWidth, btnHeight * 2, outline="white") #level
customRect = ctx.create_rectangle(800, btnHeight * 4, 800 - btnWidth, btnHeight * 3, outline="white") #custom

buttons = [upRect, ballRect, levelRect, customRect]

#Create text
ctx.create_text((800 - btnWidth) + (btnWidth / 2), btnHeight / 2, text = "START", fill = "white", font = "helvetica 40")
ctx.create_text((800 - btnWidth) + (btnWidth / 2), (btnHeight + btnHeight / 2), text = "BALL", fill = "white", font = "helvetica 40")
ctx.create_text((800 - btnWidth) + (btnWidth / 2), (btnHeight * 2 + btnHeight / 2), text = "LEVEL", fill = "white", font = "helvetica 40")
ctx.create_text((800 - btnWidth) + (btnWidth / 2), (btnHeight * 3 + btnHeight / 2), text = "CUSTOM", fill = "white", font = "helvetica 40")

#Highlight when clicked
def handle_click(event):
	global current_btn
	if event.x <= extBtnWidth and event.y >= height - extBtnHeight:
		print("Exiting...")
		root.destroy()
		return
	button_num = current_btn
	if event.x >= 800 - btnWidth and event.y >= 0 and event.y < btnHeight: # START
		button_num = 0
	elif event.x >= 800 - btnWidth and event.y >= btnHeight and event.y < btnHeight * 2: # BALL
		button_num = 1
	elif event.x >= 800 - btnWidth and event.y >= btnHeight * 2 and event.y < btnHeight * 3: # LEVEL
		button_num = 2
	elif event.x >= 800 - btnWidth and event.y >= btnHeight * 3 and event.y < btnHeight * 4: # CUSTOM
		button_num = 3
	#else:
	#	button_num = -1
	
	render_claw(button_num)
	fill_rect(button_num)
	#ctx.create_image(extBtnWidth/2, height - extBtnHeight/2, image=exitButton)
	current_btn = button_num

def render_claw(button_num):
	if button_num == -1 or button_num == 3:
		return
	rotate_claw(claw_angles[button_num])

claw_temp = None

def rotate_claw(goal):
	global claw, claw_temp
	claw_temp = claw_orig.copy()
	claw_temp = claw_temp.rotate(goal)
	claw_temp = ImageTk.PhotoImage(claw_temp)
	ctx.delete("claw")
	claw = ctx.create_image(claw_x, claw_y, image=claw_temp, tag="claw", anchor=CENTER)

render_claw(0)

def fill_rect(button_num):
	if button_num == -1:
		return

	for button in buttons:
		ctx.itemconfig(button, fill = "#222")
	ctx.itemconfig(buttons[button_num], fill = "blue")

fill_rect(3)

ctx.bind("<Button-1>", handle_click)

# Debug tools
root.bind("<F1>", lambda evt: root.destroy())
root.bind("<F2>", lambda evt: root.config(cursor=""))

def publish():
	ser.write((3-current_btn).to_bytes(1,'big'))
	root.after(50, publish)

root.after(50, publish)
root.mainloop()
