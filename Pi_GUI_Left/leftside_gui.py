test = True

from tkinter import *
import math
if not test:
    import serial
else:
    import serial_dummy as serial

# Define Serial
ser = serial.Serial(
    port='/dev/ttyAMA0', # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 9600
)

# Create window
root = Tk()
root.title("GUI")
width = 800
height = 480
# Full screen
if not test:
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  #Move focus to this widget
    root.bind("<Escape>", lambda e: root.quit())
    root.config(cursor="none")
    #root.geometry("{}x{}".format(width, height))

# Create canvas
ctx = Canvas(root, width=width,
             height=height, background="black")
ctx.pack()

bg = PhotoImage(file="left_bg.gif")
ctx.create_image(0, 0, image=bg, tag="bg", anchor=NW)

# "It's circle time!" - James Narayanan
circle_coords = [(369,396), (129,395), (129, 272), (129, 150)]
radius = 50
padding = 5
current_btn = -1

# Exit button
exit_button_width = 50
exit_button_height = 50
ctx.create_rectangle(width - exit_button_width, height - exit_button_height, width, height, fill='red')

# Create hab buttons
btn_height = height/2 - exit_button_height/2 - 5
btn_width = 300

def draw_habs(hab12='#111', hab23='#111', cargo_ship='#111', load_hatch='#111'):
    # Rectangles
    ctx.delete('hab12')
    ctx.create_rectangle(width-btn_width, 0, width, btn_height, fill=hab12, outline='white',tag='hab12')
    ctx.delete('hab23')
    ctx.create_rectangle(width-btn_width, btn_height, width, btn_height*2, fill=hab23, outline='white',tag='hab23')
    # Text boxes
    ctx.delete('hab12txt')
    ctx.create_text(width-btn_width/2, btn_height/2, text="HAB 1 → 2", fill="white", font="helvetica 40", tag='hab12txt')
    ctx.delete('hab23txt')
    ctx.create_text(width-btn_width/2, btn_height*3/2, text="HAB 2 → 3", fill="white", font="helvetica 40", tag='hab23txt')

draw_habs()


def handle_click(event):
    global current_btn
    if event.x >= width - exit_button_width and event.y >= height - exit_button_height:
        print("Exiting...")
        root.destroy()
        return
    
    # Figure out what the user picked
    picked_btn = -1
    for i in range(len(circle_coords)):
        coord = circle_coords[i]
        if (event.x >= coord[0] - radius - padding and event.x <= coord[0] + radius + padding and
            event.y >= coord[1] - radius - padding and event.y <= coord[1] + radius + padding): # Bounding box
            picked_btn = i
    
    # Check hab buttons
    if event.x >= width - btn_width and event.y <= btn_height*2:
        picked_btn = -1
        if event.y <= btn_height: # Hab 1 to 2
            picked_btn = 4
        elif event.y <= btn_height * 2: # Hab 2 to 3
            picked_btn = 5
    
    if current_btn == picked_btn:
        current_btn = -1
    else:
        current_btn = picked_btn

    # Draw ball or hatch
    ctx.delete('hatch0')
    ctx.delete('hatch1')
    if current_btn >= 0 and current_btn <= 3:
        draw_habs()
        coord = circle_coords[current_btn]
        r = 37
        x0 = coord[0] - r
        x1 = coord[0] + r
        y0 = coord[1] - r
        y1 = coord[1] + r
        ctx.create_oval(x0, y0, x1, y1, outline='yellow', width=10, tag='hatch0')
        ctx.create_oval(x0-3, y0-3, x1+3, y1+3, outline='#DDD', width=2, tag='hatch1')
    elif current_btn == 4: draw_habs(hab12='blue')
    elif current_btn == 5: draw_habs(hab23='blue')
    else: draw_habs()

delay = 50

def publish():
    #print(get_height(current_btn))
    ser.write((current_btn+1).to_bytes(1,'big'))
    root.after(delay, publish)

ctx.bind("<Button-1>", handle_click)
ctx.pack()    

# Debug tools
root.bind("<F1>", lambda evt: root.destroy())
root.bind("<F2>", lambda evt: root.config(cursor=""))

root.after(delay, publish)
root.mainloop()
