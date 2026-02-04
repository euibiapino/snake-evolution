import pygame
from ..config import (
    GRID_COLS, GRID_ROWS, CELL_SIZE, HEADER_HEIGHT,
    SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, SNAKE_BODY_ALT,
    DIR_RIGHT
)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        
        #Posição inicial: centro do grid
        center_x = GRID_COLS // 2
        center_y = GRID_ROWS // 2

        self.body = [
            (center_x, center_y),      #Cabeça
            (center_x - 1, center_y),  #Corpo
            (center_x - 2, center_y),  #Cauda
        ]

        self.direction = DIR_RIGHT
        self.growing = 0

    @property
    def head(self):
        return self.body[0]

    def set_direction(self, new_direction):
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self):
        head_x, head_y = self.head
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        self.body.insert(0, new_head)

        if self.growing > 0:
            self.growing -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.growing += amount

    def draw(self, screen):

        for i, (x, y) in enumerate(self.body):
            pixel_x = x * CELL_SIZE
            pixel_y = y * CELL_SIZE + HEADER_HEIGHT

            margin = 2
            rect = pygame.Rect(
                pixel_x + margin,
                pixel_y + margin,
                CELL_SIZE - margin * 2,
                CELL_SIZE - margin * 2
            )

            if i == 0:
                #CABEÇA
                pygame.draw.rect(screen, SNAKE_HEAD_COLOR, rect, border_radius=8)

                #Desenha os olhos
                self._draw_eyes(screen, pixel_x, pixel_y)
            else:
                #CORPO
                color = SNAKE_BODY_COLOR if i % 2 == 0 else SNAKE_BODY_ALT
                pygame.draw.rect(screen, color, rect, border_radius=5)

    def _draw_eyes(self, screen, pixel_x, pixel_y):
        eye_radius = 3
        dx, dy = self.direction

        if dx == 1:     #Direita
            eye1 = (pixel_x + CELL_SIZE - 8, pixel_y + 8)
            eye2 = (pixel_x + CELL_SIZE - 8, pixel_y + CELL_SIZE - 8)
        elif dx == -1:  #Esquerda
            eye1 = (pixel_x + 8, pixel_y + 8)
            eye2 = (pixel_x + 8, pixel_y + CELL_SIZE - 8)
        elif dy == -1:  #Cima
            eye1 = (pixel_x + 8, pixel_y + 8)
            eye2 = (pixel_x + CELL_SIZE - 8, pixel_y + 8)
        else:           #Baixo
            eye1 = (pixel_x + 8, pixel_y + CELL_SIZE - 8)
            eye2 = (pixel_x + CELL_SIZE - 8, pixel_y + CELL_SIZE - 8)

        pygame.draw.circle(screen, (0, 0, 0), eye1, eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), eye2, eye_radius)

    def __len__(self):
        return len(self.body)
