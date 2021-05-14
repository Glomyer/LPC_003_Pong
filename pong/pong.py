import turtle
import os
import platform
import threading

if platform.system() == "Linux":
    import playsound as ps
if platform.system() == "Windows":
    import winsound
    # needs testing
if platform.system() == "Darwin":
    pass
    # test afplay


def play_sound(filename):
    if platform.system() == "Linux":
        ps.playsound(filename)
    if platform.system() == "Windows":
        winsound.PlaySound(filename)
        # needs testing
    if platform.system() == "Darwin":
        os.system(f"afplay {filename}&")
        # does this work? got no mac lol


def loop_bgm():
    while True:
        play_sound('cheetahmen.wav')


def update_hud():
    hud.clear()
    font_settings = ("Press Start 2P", 24, "normal")
    hud.write("{} : {}".format(score_1, score_2), align="center", font=font_settings)


def on_close():
    global running
    running = False


# draw screen
screen = turtle.Screen()
screen.title("My Pong")
screen.bgcolor("black")
screen.bgpic("ff6ocean.png")
screen.setup(width=800, height=600)
screen.tracer(0)

# draw paddle 1
paddle_1 = turtle.Turtle()
paddle_1.speed(0)
paddle_1.shape("square")
paddle_1.color("white")
paddle_1.shapesize(stretch_wid=5, stretch_len=1)
paddle_1.penup()
paddle_1.goto(-350, 0)

# draw paddle 2
paddle_2 = turtle.Turtle()
paddle_2.speed(0)
paddle_2.shape("square")
paddle_2.color("white")
paddle_2.shapesize(stretch_wid=5, stretch_len=1)
paddle_2.penup()
paddle_2.goto(350, 0)

# draw ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("black",  "yellow")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.3
ball.dy = 0.3

# score
score_1 = 0
score_2 = 0

# head-up display
hud = turtle.Turtle()
hud.speed(0)
hud.shape("square")
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 260)
update_hud()

# function for catching the act of closing the window
screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)


def paddle_1_up():
    y = paddle_1.ycor()
    if y < 250:
        y += 30
    else:
        y = 250
    paddle_1.sety(y)


def paddle_1_down():
    y = paddle_1.ycor()
    if y > -250:
        y += -30
    else:
        y = -250
    paddle_1.sety(y)


def paddle_2_up():
    y = paddle_2.ycor()
    if y < 250:
        y += 30
    else:
        y = 250
    paddle_2.sety(y)


def paddle_2_down():
    y = paddle_2.ycor()
    if y > -250:
        y += -30
    else:
        y = -250
    paddle_2.sety(y)


# keyboard
screen.listen()
screen.onkeypress(paddle_1_up, "w")
screen.onkeypress(paddle_1_down, "s")
screen.onkeypress(paddle_2_up, "Up")
screen.onkeypress(paddle_2_down, "Down")

musicLoop = threading.Thread(target=loop_bgm, name='backgroundMusicThread')
# shut down music thread when the rest of the program exits
musicLoop.daemon = True
musicLoop.start()

# condition for the main loop of the game
running = True

while running:
    screen.update()

    # ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # collision with the upper wall
    if ball.ycor() > 290:
        play_sound("bounce.wav")
        ball.sety(290)
        ball.dy *= -1

    # collision with lower wall
    if ball.ycor() < -290:
        play_sound("bounce.wav")
        ball.sety(-290)
        ball.dy *= -1

    # collision with left wall
    if ball.xcor() < -390:
        score_2 += 1
        update_hud()
        play_sound("258020__kodack__arcade-bleep-sound.wav")
        ball.goto(0, 0)
        ball.dx *= -1

    # collision with right wall
    if ball.xcor() > 390:
        score_1 += 1
        update_hud()
        play_sound("258020__kodack__arcade-bleep-sound.wav")
        ball.goto(0, 0)
        ball.dx *= -1

    # collision with the paddle 1
    if ball.xcor() < -330 and paddle_1.ycor() + 50 > ball.ycor() > paddle_1.ycor() - 50:
        ball.dx *= -1
        play_sound("bounce.wav")

    # collision with the paddle 2
    if ball.xcor() > 330 and paddle_2.ycor() + 50 > ball.ycor() > paddle_2.ycor() - 50:
        ball.dx *= -1
        play_sound("bounce.wav")
