from Tkinter import *
import math
import serial

# Define Serial
ser = serial.Serial(
    port='/dev/ttyAMA0', # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

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
#root.geometry("{}x{}".format(width, height))

# Create canvas
ctx = Canvas(root, width=width,
             height=height, background="black")
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
ctx.pack()

rect_width = 250
rect_height = 440
side_rect_width = 180
theta = 8 # Degrees
# Center side
ctx.create_rectangle(width/2 - rect_width/2, height/2 - rect_height/2, width/2 + rect_width/2, height/2 + rect_height/2, fill='white', outline='black')
# Left side
ctx.create_polygon(
    width/2 - rect_width/2 - side_rect_width,   height/2 - rect_height/2 - side_rect_width*math.tan(math.radians(theta)), # Top left
    width/2 - rect_width/2,     height/2 - rect_height/2, # Top right
    width/2 - rect_width/2,     height/2 + rect_height/2, # Bottom right
    width/2 - rect_width/2 - side_rect_width,   height/2 + rect_height/2 - side_rect_width*math.tan(math.radians(theta)), # Bottom left
    fill='#eee',outline='black'
)
# Right side
ctx.create_polygon(
    width/2 + rect_width/2,     height/2 - rect_height/2, # Top right
    width/2 + rect_width/2 + side_rect_width,   height/2 - rect_height/2 - side_rect_width*math.tan(math.radians(theta)), # Top left
    width/2 + rect_width/2 + side_rect_width,   height/2 + rect_height/2 - side_rect_width*math.tan(math.radians(theta)), # Bottom left
    width/2 + rect_width/2,     height/2 + rect_height/2, # Bottom right
    fill='#eee',outline='black'
)
# "It's circle time!" - James Narayanan
radius = 55
h1 = height/2 + rect_height/2 - radius - rect_height/8
margin = 20
# heights = [h1, h1 - 2*radius - margin, h1 - 4*radius - 2*margin]
heights = [h1 - 4*radius - 2*margin, h1 - 2*radius - margin, h1]
side_height_offset = 10
side_circle_width = radius - 10

circles = [[0,0,0],[0,0,0], [0,0,0]]
current_circle = [-1,-1]

for spot, h in enumerate(heights):
    # Center side
    circles[1][spot] = ctx.create_oval(
        width/2 - radius,   h - radius,
        width/2 + radius,   h + radius,
        fill='red',outline='black'
    )
    # Left side
    circles[0][spot] = ctx.create_oval(
        width/2 - rect_width/2 - side_rect_width/2 - side_circle_width,    h - radius + side_height_offset,
        width/2 - rect_width/2 - side_rect_width/2 + side_circle_width,    h + radius + side_height_offset,
        fill='red',outline='black'
    )
    # Right side
    circles[2][spot] = ctx.create_oval(
        width/2 + rect_width/2 + side_rect_width/2 - side_circle_width,    h - radius + side_height_offset,
        width/2 + rect_width/2 + side_rect_width/2 + side_circle_width,    h + radius + side_height_offset,
        fill='red',outline='black'
    )


exit_button_width = 50
exit_button_height = 50
ctx.create_rectangle(width - exit_button_width, height - exit_button_height, width, height, fill='red')

def handle_click(event):
    global current_circle
    print ("clicked at", event.x, event.y)

    if event.x >= width - exit_button_width and event.y >= height - exit_button_height:
    #if event.x >= 0 and event.y >= 0:
        print("Exiting...")
        root.destroy()
        return
    
    picked_circle = [-1, -1] # x, y
    if event.x < width/2 - rect_width/2: # Left side
        picked_circle[0] = 0
    elif event.x > width/2 + rect_width/2: # Right side
        picked_circle[0] = 2
    else: # Center
        picked_circle[0] = 1
        for spot, h in enumerate(heights): # Reverses height array to go top to bottom
            if event.y < h + radius + margin/2 and event.y > h - radius - margin/2:
                picked_circle[1] = spot
                break

    if picked_circle[0] % 2 == 0: # If it's on the side
         for spot, h in enumerate(heights): # Reverses height array to go top to bottom
            if event.y < h + radius + side_height_offset + margin/2 and event.y > h - radius + side_height_offset - margin/2:
                picked_circle[1] = spot
                break

    if picked_circle[0] == -1 or picked_circle[1] == -1:
        return

    for col in circles:
        for c in col:
            ctx.itemconfig(c, fill= "red")
    
    if current_circle != picked_circle:
        ctx.itemconfig(circles[picked_circle[0]][picked_circle[1]], fill= "green")
        current_circle = picked_circle
    else:
        current_circle = [-1,-1]

    print ("clicked ",picked_circle)
    print("--------------")

def get_height(circle):
    if circle[0] == -1:
        return 0
    if circle[0] % 2 == 0:
        return 6 - (circle[1]*2 + 1)
    else:
        return 6 - (circle[1]*2)

delay = 50

def publish():
    #print(get_height(current_circle))
    ser.write(bytes(get_height(current_circle)))
    root.after(delay, publish)

ctx.bind("<Button-1>", handle_click)
ctx.pack()    

root.after(delay, publish)
root.mainloop()
