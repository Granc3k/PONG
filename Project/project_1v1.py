"""
File: project.py
-----------------
This program is an empty program for your final project.  Update this comment
with a summary of your program!
"""

from graphics import Canvas
import time
import random

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
board_width = 100
board_height = 50
offset_paddle = 100
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 150
BALL_RADIUS = 15
DELAY = 1 / 60
paddle_speed = 10
NET_WIDTH = 1
NET_PART_HEIGHT = 70
NET_GAP = 2

def main():
    max_score = int(input("Enter the maximal score that could be reached: "))
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.set_canvas_title("Final Project")
    paddle_1 = create_paddle_1(canvas)
    paddle_2 = create_paddle_2(canvas)
    dx = 6
    dy = 6
    score_1 = 0
    score_2 = 0
    net = create_net(canvas)
    s_1_board = canvas.create_text(CANVAS_WIDTH/2-board_width/2, board_height, score_1)
    s_2_board = canvas.create_text(CANVAS_WIDTH/2+board_width/2, board_height, score_2)
    canvas.set_font(s_1_board, "Arial", 30)
    canvas.set_font(s_2_board, "Arial", 30)
    ball = create_ball(canvas)
    canvas.wait_for_click()
    while True:
        canvas.set_text(s_1_board, score_1)
        canvas.set_text(s_2_board, score_2)
        presses = canvas.get_new_key_presses()
        if collision(canvas, ball, paddle_1, paddle_2):
            dx *= -1
        dx, dy, ball, score_1, score_2 = move_ball(canvas, dx, dy, ball, score_1, score_2)
        move_paddle(canvas, paddle_1, "w", "s", presses)
        move_paddle(canvas, paddle_2, "Up", "Down", presses)
        canvas.move(ball, dx, dy)
        time.sleep(DELAY)
        canvas.update()
        if score_1 == max_score or score_2 == max_score:
            end_screen(canvas, score_1, score_2)
            canvas.update()
            canvas.wait_for_click()
            return False
        else:
            pass
    canvas.update()
    canvas.mainloop()


def create_paddle_1(canvas):
    y = CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2
    paddle_1 = canvas.create_rectangle(offset_paddle, y, offset_paddle + PADDLE_WIDTH, y + PADDLE_HEIGHT)
    canvas.set_color(paddle_1, "black")
    return paddle_1

def create_paddle_2(canvas):
    x = CANVAS_WIDTH - offset_paddle - PADDLE_WIDTH
    y = CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2
    paddle_2 = canvas.create_rectangle(x, y, x + PADDLE_WIDTH, y + PADDLE_HEIGHT)
    canvas.set_color(paddle_2, "black")
    return paddle_2

def create_ball(canvas):
    x = CANVAS_WIDTH / 2 - BALL_RADIUS
    y = CANVAS_HEIGHT / 2 - BALL_RADIUS
    ball = canvas.create_oval(x, y, x + 2 * BALL_RADIUS, y + 2 * BALL_RADIUS)
    canvas.set_color(ball, "black")
    return ball

def move_ball(canvas, dx, dy, ball, score_1, score_2):
    if canvas.get_left_x(ball) <= 1:
        canvas.delete(ball)
        ball = create_ball(canvas)
        score_2 += 1
        canvas.wait_for_click()
    elif canvas.get_left_x(ball) >= CANVAS_WIDTH - canvas.get_width(ball) - 1:
        canvas.delete(ball)
        ball = create_ball(canvas)
        score_1 += 1
        canvas.wait_for_click()
    if canvas.get_top_y(ball) <= 1:
        dy *= -1
    elif canvas.get_top_y(ball) >= CANVAS_HEIGHT - canvas.get_height(ball) - 1:
        dy *= -1
    return dx, dy, ball, score_1, score_2

def collision(canvas, ball, paddle_1, paddle_2):
    ball_coords = canvas.coords(ball)
    x1 = ball_coords[0]
    y1 = ball_coords[1]
    x2 = ball_coords[2]
    y2 = ball_coords[3]
    colliders = canvas.find_overlapping(x1, y1, x2, y2)
    for collider in colliders:
        if collider == ball:
            return False
        elif collider == paddle_1 or collider == paddle_2:
            return True

def move_paddle(canvas, paddle, up, down, presses):
    x = canvas.get_left_x(paddle)
    if canvas.get_top_y(paddle) <= 0:
        canvas.move_to(paddle, x, 1)
    elif canvas.get_top_y(paddle) >= CANVAS_HEIGHT-PADDLE_HEIGHT:
        canvas.move_to(paddle, x, CANVAS_HEIGHT-PADDLE_HEIGHT-1)
    else:
        for press in presses:
            if press.keysym == down:
                canvas.move(paddle, 0, paddle_speed)
            elif press.keysym == up:
                canvas.move(paddle, 0, -paddle_speed)

def create_net(canvas):
    x = CANVAS_WIDTH/2
    for i in range(10):
        net = canvas.create_rectangle(x-1, 10, x + 1, CANVAS_HEIGHT-10)
        canvas.set_color(net, "black")

def end_screen(canvas, score_1, score_2):
    screen = canvas.create_rectangle(0, 0, CANVAS_WIDTH,CANVAS_HEIGHT)
    canvas.set_color(screen, "black")
    if score_1 > score_2:
        text = canvas.create_text(CANVAS_WIDTH/2,CANVAS_HEIGHT/2, "Player 1 won the game!!!")
        canvas.set_fill_color(text, "white")
        canvas.set_font(text, "Arial", 60)
    else:
        text = canvas.create_text(CANVAS_WIDTH/2,CANVAS_HEIGHT/2, "Player 2 won the game!!!")
        canvas.set_fill_color(text, "white")
        canvas.set_font(text, "Arial", 60)

if __name__ == '__main__':
    main()
