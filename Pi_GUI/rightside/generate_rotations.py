from PIL import Image

claw = Image.open("grayclaw.png")
claw.convert("RGBA")
new_width = 512
wpercent = (new_width/float(claw.size[0]))
hsize = int(float(claw.size[1])*wpercent)
claw = claw.resize((new_width,hsize))
claw.save("claw.gif")
claw_down = claw.rotate(-30)
claw_down.save("claw_down.gif")
claw_ball = claw.rotate(30)
claw_ball.save("claw_ball.gif")
claw_up = claw.rotate(60)
claw_up.save("claw_up.gif")
