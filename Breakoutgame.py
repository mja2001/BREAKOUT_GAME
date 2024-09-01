import pygame
import sys
import random

# Game settings
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

# Initialize Pygame
pygame.init()

class Paddle:
    def __init__(self, screen):
        self.screen = screen
        self.width = 100
        self.height = 10
        self.color = (0, 0, 255)  # Blue color for the paddle
        self.speed = 10
        self.rect = pygame.Rect((WIDTH - self.width) // 2, HEIGHT - 40, self.width, self.height)

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Ball:
    def __init__(self, screen):
        self.screen = screen
        self.size = 10
        self.color = (255, 255, 0)  # Yellow color for the ball
        self.speed = [5, -5]
        self.rect = pygame.Rect(WIDTH // 2 - self.size // 2, HEIGHT // 2 - self.size // 2, self.size, self.size)

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]

    def draw(self):
        pygame.draw.ellipse(self.screen, self.color, self.rect)

class Brick:
    def __init__(self, screen, x, y, width, height, strength):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.strength = strength
        self.color = self.calculate_color()  # Set the color based on strength

    def calculate_color(self):
        # "Men" colors: shades of blue, green, gray, and brown
        men_colors = [
            (70, 130, 180),  # Steel Blue
            (0, 128, 128),   # Teal
            (47, 79, 79),    # Dark Slate Gray
            (139, 69, 19),   # Saddle Brown
            (0, 0, 128),     # Navy
            (25, 25, 112),   # Midnight Blue
            (34, 139, 34),   # Forest Green
            (105, 105, 105)  # Dim Gray
        ]
        # Darken the color based on strength
        base_color = men_colors[self.strength % len(men_colors)]
        darkening_factor = 1 - 0.15 * (self.strength - 1)
        return (
            int(base_color[0] * darkening_factor),
            int(base_color[1] * darkening_factor),
            int(base_color[2] * darkening_factor)
        )

    def hit(self):
        self.strength -= 1
        if self.strength > 0:
            self.color = self.calculate_color()
        return self.strength == 0

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Breakout Game with Levels and Colors")
        self.clock = pygame.time.Clock()
        self.paddle = Paddle(self.screen)
        self.ball = Ball(self.screen)
        self.bricks = self.create_bricks(1)
        self.score = 0
        self.lives = 3
        self.level = 1
        self.font = pygame.font.SysFont(None, 36)

    def create_bricks(self, level):
        bricks = []
        brick_width = 70
        brick_height = 20
        brick_padding = 10
        for i in range(5):  # 5 rows of bricks
            for j in range(10):  # 10 columns of bricks
                brick_x = 35 + j * (brick_width + brick_padding)
                brick_y = 45 + i * (brick_height + brick_padding)
                strength = level  # Brick strength based on level
                bricks.append(Brick(self.screen, brick_x, brick_y, brick_width, brick_height, strength))
        return bricks

    def check_collisions(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed[1] = -self.ball.speed[1]

        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.ball.speed[1] = -self.ball.speed[1]
                if brick.hit():
                    self.bricks.remove(brick)
                    self.score += 10
                break

    def reset_ball(self):
        if self.ball.rect.top >= HEIGHT:
            self.lives -= 1
            self.ball.rect.x = WIDTH // 2 - self.ball.size // 2
            self.ball.rect.y = HEIGHT // 2 - self.ball.size // 2
            self.ball.speed = [5, -5]

    def draw(self):
        self.screen.fill(BLACK)
        self.paddle.draw()
        self.ball.draw()
        for brick in self.bricks:
            brick.draw()
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (20, 10))
        self.screen.blit(lives_text, (700, 10))
        self.screen.blit(level_text, (360, 10))

    def next_level(self):
        self.level += 1
        self.bricks = self.create_bricks(self.level)
        self.ball.rect.x = WIDTH // 2 - self.ball.size // 2
        self.ball.rect.y = HEIGHT // 2 - self.ball.size // 2
        self.ball.speed = [5, -5]
        self.paddle.rect.x = (WIDTH - self.paddle.width) // 2

    def run(self):
        while self.lives > 0:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

            self.ball.move()
            self.check_collisions()
            self.reset_ball()

            if not self.bricks:
                self.next_level()

            self.draw()

        self.game_over()

    def game_over(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("Game Over", True, WHITE)
        final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, 250))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 300))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        self.__init__()
                        self.run()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
