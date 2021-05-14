import turtle
import os
import platform
import threading

if platform.system() == "Linux" or platform.system() == "Windows":
    import playsound as ps


def play_sound(filename):
    if platform.system() == "Linux" or platform.system() == "Windows":
        ps.playsound(filename)
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


# game values
SQUARE_SIDE = 20

WINDOW_TITLE = "My Pong"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WINDOW_BACKGROUND = "black"

PADDLE_COLOR = "white"
PADDLE_SHAPE = "square"
PADDLE_WIDTH, PADDLE_HEIGHT = 1, 5
PADDLE_OFFSET_X, PADDLE_OFFSET_Y = 50, 50
PADDLE_WALK_SIZE = 30

PADDLE_1_UP_KEY = "w"
PADDLE_1_DOWN_KEY = "s"
PADDLE_2_UP_KEY = "Up"
PADDLE_2_DOWN_KEY = "Down"

BALL_SHAPE = "square"
BALL_COLOR = "white"

HUD_SHAPE = "square"
HUD_COLOR = "white"
HUD_X, HUD_Y = 0, 260
HUD_FONT = "Press Start 2P", 24, "normal"

BOUNCE_SOUND = "bounce.wav"
SCORE_RAISING_SOUND = "258020__kodack__arcade-bleep-sound.wav"

WALL_COLLISION_MARGIN = 10
PADDLE_COLLISION_AREA_X = WINDOW_WIDTH // 2 - (PADDLE_OFFSET_X + PADDLE_WIDTH * SQUARE_SIDE)
PADDLE_REAL_WIDTH, PADDLE_REAL_HEIGHT = PADDLE_WIDTH * SQUARE_SIDE, PADDLE_HEIGHT * SQUARE_SIDE

# draw screen
screen = turtle.Screen()
screen.title(WINDOW_TITLE)
screen.bgcolor(WINDOW_BACKGROUND)
screen.bgpic("ff6ocean.png")
screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
screen.tracer(0)

# draw paddle 1
paddle_1 = turtle.Turtle()
paddle_1.speed(0)
paddle_1.shape(PADDLE_SHAPE)
paddle_1.color(PADDLE_COLOR)
paddle_1.shapesize(stretch_wid=PADDLE_HEIGHT, stretch_len=PADDLE_WIDTH)
paddle_1.penup()
paddle_1.goto(-(WINDOW_WIDTH // 2 - PADDLE_OFFSET_X), 0)

# draw paddle 2
paddle_2 = turtle.Turtle()
paddle_2.speed(0)
paddle_2.shape(PADDLE_SHAPE)
paddle_2.color(PADDLE_COLOR)
paddle_2.shapesize(stretch_wid=PADDLE_HEIGHT, stretch_len=PADDLE_WIDTH)
paddle_2.penup()
paddle_2.goto(WINDOW_WIDTH // 2 - PADDLE_OFFSET_X, 0)

# draw ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape(BALL_SHAPE)
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
hud.shape(HUD_SHAPE)
hud.color(HUD_COLOR)
hud.penup()
hud.hideturtle()
hud.goto(0, 260)
update_hud()

# function for catching the act of closing the window
screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)


def paddle_1_up():
    y = paddle_1.ycor()
    if y < WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y:
        y += PADDLE_WALK_SIZE
    else:
        y = WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y
    paddle_1.sety(y)


def paddle_1_down():
    y = paddle_1.ycor()
    if y > -(WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y):
        y += -PADDLE_WALK_SIZE
    else:
        y = -(WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y)
    paddle_1.sety(y)


def paddle_2_up():
    y = paddle_2.ycor()
    if y < WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y:
        y += PADDLE_WALK_SIZE
    else:
        y = WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y
    paddle_2.sety(y)


def paddle_2_down():
    y = paddle_2.ycor()
    if y > -(WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y):
        y += -PADDLE_WALK_SIZE
    else:
        y = -(WINDOW_HEIGHT // 2 - PADDLE_OFFSET_Y)
    paddle_2.sety(y)


# keyboard
screen.listen()
screen.onkeypress(paddle_1_up, PADDLE_1_UP_KEY)
screen.onkeypress(paddle_1_down, PADDLE_1_DOWN_KEY)
screen.onkeypress(paddle_2_up, PADDLE_2_UP_KEY)
screen.onkeypress(paddle_2_down, PADDLE_2_DOWN_KEY)

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
    if ball.ycor() > WINDOW_HEIGHT // 2 - WALL_COLLISION_MARGIN:
        play_sound(BOUNCE_SOUND)
        ball.sety(WINDOW_HEIGHT // 2 - WALL_COLLISION_MARGIN)
        ball.dy *= -1

    # collision with lower wall
    if ball.ycor() < -(WINDOW_HEIGHT // 2 - WALL_COLLISION_MARGIN):
        play_sound(BOUNCE_SOUND)
        ball.sety(-(WINDOW_HEIGHT // 2 - WALL_COLLISION_MARGIN))
        ball.dy *= -1

    # collision with left wall
    if ball.xcor() < -(WINDOW_WIDTH // 2 - WALL_COLLISION_MARGIN):
        score_2 += 1
        update_hud()
        play_sound(SCORE_RAISING_SOUND)
        ball.goto(0, 0)
        ball.dx *= -1

    # collision with right wall
    if ball.xcor() > WINDOW_WIDTH // 2 - WALL_COLLISION_MARGIN:
        score_1 += 1
        update_hud()
        play_sound(SCORE_RAISING_SOUND)
        ball.goto(0, 0)
        ball.dx *= -1

    # collision with the paddle 1
    if ball.xcor() < -PADDLE_COLLISION_AREA_X and \
            (paddle_1.ycor() + PADDLE_REAL_HEIGHT // 2) > ball.ycor() > (paddle_1.ycor() - PADDLE_REAL_HEIGHT // 2):
        ball.dx *= -1
        play_sound(BOUNCE_SOUND)

    # collision with the paddle 2
    if ball.xcor() > PADDLE_COLLISION_AREA_X and \
            (paddle_2.ycor() + PADDLE_REAL_HEIGHT // 2) > ball.ycor() > (paddle_2.ycor() - PADDLE_REAL_HEIGHT // 2):
        ball.dx *= -1
        play_sound(BOUNCE_SOUND)
