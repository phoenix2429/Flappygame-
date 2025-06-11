import pygame
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Futuristic Flappy Bird")

# Colors (neon style)
BLACK = (10, 10, 10)
NEON_BLUE = (50, 230, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (150, 50, 255)

# Fonts
FONT = pygame.font.SysFont("consolas", 40)
SMALL_FONT = pygame.font.SysFont("consolas", 30)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Bird class with glowing trail
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.radius = 20
        self.vel = 0
        self.gravity = 0.5
        self.lift = -10
        self.trail = []

    def update(self):
        self.vel += self.gravity
        self.y += self.vel
        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.vel = 0
        if self.y < self.radius:
            self.y = self.radius
            self.vel = 0
        self.trail.append((self.x, self.y))
        if len(self.trail) > 15:
            self.trail.pop(0)

    def flap(self):
        self.vel = self.lift

    def draw(self, win):
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            glow_surf = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (NEON_BLUE[0], NEON_BLUE[1], NEON_BLUE[2], alpha), (self.radius*2, self.radius*2), self.radius + 5)
            win.blit(glow_surf, (tx - self.radius*2, ty - self.radius*2))
        pygame.draw.circle(win, NEON_PINK, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(win, NEON_GREEN, (int(self.x + 7), int(self.y - 5)), 5)

# Obstacle class (energy walls)
class Obstacle:
    GAP = 180
    WIDTH = 80
    SPEED = 5

    def __init__(self):
        self.x = WIDTH + 50
        self.top = random.randint(100, HEIGHT - 300)
        self.passed = False

    def update(self):
        self.x -= self.SPEED

    def draw(self, win):
        top_rect = pygame.Rect(self.x, 0, self.WIDTH, self.top)
        bottom_rect = pygame.Rect(self.x, self.top + self.GAP, self.WIDTH, HEIGHT - (self.top + self.GAP))
        for i in range(5):
            alpha = 50 - i * 10
            glow_surf = pygame.Surface((self.WIDTH + i*10, self.top + i*10), pygame.SRCALPHA)
            glow_surf.fill((NEON_PURPLE[0], NEON_PURPLE[1], NEON_PURPLE[2], alpha))
            win.blit(glow_surf, (self.x - i*5, -i*5))
            glow_surf = pygame.Surface((self.WIDTH + i*10, HEIGHT - (self.top + self.GAP) + i*10), pygame.SRCALPHA)
            glow_surf.fill((NEON_PURPLE[0], NEON_PURPLE[1], NEON_PURPLE[2], alpha))
            win.blit(glow_surf, (self.x - i*5, self.top + self.GAP - i*5))
        pygame.draw.rect(win, NEON_PURPLE, top_rect)
        pygame.draw.rect(win, NEON_PURPLE, bottom_rect)

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius, bird.radius*2, bird.radius*2)
        top_rect = pygame.Rect(self.x, 0, self.WIDTH, self.top)
        bottom_rect = pygame.Rect(self.x, self.top + self.GAP, self.WIDTH, HEIGHT - (self.top + self.GAP))
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

# Background stars
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = self.size / 2

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)
            self.size = random.randint(1, 3)
            self.speed = self.size / 2

    def draw(self, win):
        pygame.draw.circle(win, NEON_BLUE, (int(self.x), int(self.y)), self.size)

def draw_window(win, bird, obstacles, stars, score, lives):
    win.fill(BLACK)
    for star in stars:
        star.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)
    bird.draw(win)
    score_text = FONT.render(f"Score: {score}", True, NEON_GREEN)
    win.blit(score_text, (10, 10))
    lives_text = SMALL_FONT.render(f"Lives: {'💖'*lives}", True, NEON_PINK)
    win.blit(lives_text, (10, 60))
    pygame.display.update()

def start_screen():
    WIN.fill(BLACK)
    title = FONT.render("Futuristic Flappy Bird", True, NEON_PINK)
    prompt = SMALL_FONT.render("Press SPACE to Start", True, NEON_GREEN)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    WIN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                waiting = False

def main():
    start_screen()

    bird = Bird()
    obstacles = []
    stars = [Star() for _ in range(60)]

    score = 0
    lives = 3
    run = True
    frame_count = 0

    while run:
        clock.tick(FPS)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.flap()

        bird.update()
        for star in stars:
            star.update()

        if frame_count % 90 == 0:
            obstacles.append(Obstacle())

        rem = []
        for obstacle in obstacles:
            obstacle.update()
            if obstacle.collide(bird):
                lives -= 1
                obstacles.remove(obstacle)
                if lives == 0:
                    run = False

            if obstacle.x + obstacle.WIDTH < 0:
                rem.append(obstacle)

            if not obstacle.passed and obstacle.x < bird.x:
                obstacle.passed = True
                score += 1

        for r in rem:
            obstacles.remove(r)

        if bird.y >= HEIGHT - bird.radius or bird.y <= bird.radius:
            lives -= 1
            if lives == 0:
                run = False
            bird.y = HEIGHT // 2
            bird.vel = 0

        draw_window(WIN, bird, obstacles, stars, score, lives)

    WIN.fill(BLACK)
    game_over_text = FONT.render("GAME OVER", True, NEON_PINK)
    final_score_text = FONT.render(f"Final Score: {score}", True, NEON_GREEN)
    WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    WIN.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
