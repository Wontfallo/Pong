#simple game of Pong. 
#By: Gerald Jackson  in Dec of 2013
#Left Player uses 'W' & 'S' keys 
#Right Player users 'Up Arrow' & 'Down Arrow' keys

import pygame
import sys
import textwrap
import time

time.sleep(3)

try:
    # Close the splash screen.
    import pyi_splash
    pyi_splash.close()
except ImportError:
    # Otherwise do nothing.
    pass

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
HALF_PADDLE_WIDTH = PADDLE_WIDTH // 2
FPS = 60

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Set up the font
FONT = pygame.font.SysFont('comicsans', 50)

# Set up the classes
class Paddle:
    def __init__(self, x, y, width, height, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.color = color

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    def __init__(self, x, y, radius, color, x_vel, y_vel):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# Set up the functions
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
       pygame.draw.rect(win, paddle.color, pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height))

    pygame.draw.circle(win, WHITE, (ball.x, ball.y), ball.radius)

    pygame.display.update()

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - 5 >= 0:
        left_paddle.y -= 5
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + 5 <= HEIGHT:
        left_paddle.y += 5

    if keys[pygame.K_UP] and right_paddle.y - 5 >= 0:
        right_paddle.y -= 5
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + 5 <= HEIGHT:
        right_paddle.y += 5

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, RED)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT, BLUE)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS, WHITE, 5, 5)

    left_score = 0
    right_score = 0

    game_over = False  # Define game_over here

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        if game_over:
            FONT_SIZE = 30  # Adjust this value to change the font size
            text = FONT.render(f"{winner} wins! Press Q to quit or Space to play again", True, WHITE)
            text = pygame.transform.scale(text, (text.get_width() * FONT_SIZE // text.get_height(), FONT_SIZE))
            
            # Adjust the y-coordinate to move the text up
            y_coordinate = HEIGHT//2 - text.get_height()//2 - 50  # Subtract 50 to move the text up           

            WIN.blit(text, (WIDTH//2 - text.get_width()//2, y_coordinate))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    run = False
                    break
                elif keys[pygame.K_SPACE]:
                    game_over = False
                    ball.reset()
                    left_paddle.reset()
                    right_paddle.reset()
                    left_score = 0
                    right_score = 0
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            handle_paddle_movement(keys, left_paddle, right_paddle)

            ball.x += ball.x_vel
            ball.y += ball.y_vel


            # Check for collision with paddles
            if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
                ball.y_vel *= -1

            if ball.x_vel < 0:
                if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                    if ball.x - ball.radius <= left_paddle.x + PADDLE_WIDTH:
                        ball.x_vel *= -1

                        middle_y = left_paddle.y + left_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (left_paddle.height / 2) / ball.x_vel
                        ball.y_vel = -1 * difference_in_y / reduction_factor

            else:
                if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                    if ball.x + ball.radius >= right_paddle.x:
                        ball.x_vel *= -1

                        middle_y = right_paddle.y + right_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (right_paddle.height / 2) / ball.x_vel
                        ball.y_vel = -1 * difference_in_y / reduction_factor

            # Check for point scored
            if ball.x < 0:
                right_score += 1
                ball.reset()
            elif ball.x > WIDTH:
                left_score += 1
                ball.reset()

            if left_score >= 5:
                game_over = True
                winner = "Left Player"
            elif right_score >= 5:
                game_over = True
                winner = "Right Player"

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()