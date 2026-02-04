import pygame
import sys

from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    BG_COLOR, HEADER_COLOR, HEADER_HEIGHT, GRID_COLOR,
    CELL_SIZE, GRID_COLS, GRID_ROWS, SCREEN_WIDTH,
    SNAKE_SPEED
)
from src.entities import Snake


def draw_grid(screen):

    offset_y = HEADER_HEIGHT

    # Linhas verticais
    for x in range(0, SCREEN_WIDTH + 1, CELL_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, offset_y),
            (x, WINDOW_HEIGHT)
        )

    # Linhas horizontais
    for y in range(offset_y, WINDOW_HEIGHT + 1, CELL_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (SCREEN_WIDTH, y)
        )


def draw_header(screen, score):
    
    #Desenha o cabeçalho com a pontuação.
    
    pygame.draw.rect(screen, HEADER_COLOR, (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))

    pygame.draw.line(
        screen,
        GRID_COLOR,
        (0, HEADER_HEIGHT),
        (WINDOW_WIDTH, HEADER_HEIGHT),
        2
    )

    font = pygame.font.Font(None, 40)
    text = font.render(f"PONTOS: {score}", True, (0, 255, 128))

    text_rect = text.get_rect(midleft=(20, HEADER_HEIGHT // 2))
    screen.blit(text, text_rect)


def main():

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Evolution")

    clock = pygame.time.Clock()

    score = 0
    running = True

    # Cria a cobra
    snake = Snake()

    # Timer para controlar velocidade da cobra
    move_timer = 0
    move_interval = 1000 // SNAKE_SPEED  # milissegundos entre movimentos

    # GAME LOOP
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Atualiza timer e move a cobra
        move_timer += clock.get_time()
        if move_timer >= move_interval:
            move_timer = 0
            snake.move()

        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_header(screen, score)
        snake.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
