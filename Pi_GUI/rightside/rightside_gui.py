from tkinter import *
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

#Load buttons
claw_down = PhotoImage(file="claw_down.gif")
claw_level = PhotoImage(file="claw.gif")
claw_ball = PhotoImage(file="claw_ball.gif")
claw_up = PhotoImage(file="claw_up.gif")
exitButton = PhotoImage(file="exitButton.gif")


#Resize buttons
exitButton = resize(exitButton, 75, 75)

btnWidth = 250
btnHeight = 120

#Create buttons
claw = ctx.create_image(200, 240, image=claw_level, tag="claw")
ctx.create_image(20, 400, image=exitButton)
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
	if event.x >= 800 - btnWidth and event.y >= 0 and event.y < btnHeight: 
		button_num = 0
		ctx.delete("claw")
		claw = ctx.create_image(200, 240, image=claw_up, tag="claw")
	elif event.x >= 800 - btnWidth and event.y >= btnHeight and event.y < btnHeight * 2: 
		button_num = 1
		ctx.delete("claw")
		claw = ctx.create_image(200, 240, image=claw_ball, tag="claw")
	elif event.x >= 800 - btnWidth and event.y >= btnHeight * 2 and event.y < btnHeight * 3: 
		button_num = 2
		ctx.delete("claw")
		claw = ctx.create_image(200, 240, image=claw_level, tag="claw")
	elif event.x >= 800 - btnWidth and event.y >= btnHeight * 3 and event.y < btnHeight * 4: 
		button_num = 3
		ctx.delete("claw")
		claw = ctx.create_image(200, 240, image=claw_down, tag="claw")
	else:
		button_num = -1
		ctx.delete("claw")
		claw = ctx.create_image(200, 240, image=claw_level, tag="claw")
	fill_rect(button_num)
	
	
def fill_rect(button_num):
	for button in buttons:
		ctx.itemconfig(button, fill = "black")
	if button_num == -1:
		return
	ctx.itemconfig(buttons[button_num], fill = "blue")

ctx.bind("<Button-1>", handle_click)

root.mainloop()
