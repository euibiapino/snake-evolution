import random
import pygame
from .config import GRID_COLS, GRID_ROWS, DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT
from .sprite_renderer import SnakeSpriteRenderer


DIRECTIONS = [DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT]


class MenuSnake:
    def __init__(self):
        self._renderer = SnakeSpriteRenderer()
        self.move_delay = 6
        self.timer = 0
        self._init_body()

    def _init_body(self):
        cx = GRID_COLS // 2
        cy = GRID_ROWS // 2
        self.direction = random.choice(DIRECTIONS)
        self.body = []
        for i in range(15):
            self.body.append((cx - self.direction[0] * i, cy - self.direction[1] * i))

    def _valid_directions(self):
        hx, hy = self.body[0]
        opposite = (-self.direction[0], -self.direction[1])
        valid = []
        for d in DIRECTIONS:
            if d == opposite:
                continue
            nx, ny = hx + d[0], hy + d[1]
            if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                valid.append(d)
        return valid

    def update(self):
        self.timer += 1
        if self.timer < self.move_delay:
            return
        self.timer = 0

        hx, hy = self.body[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]

        needs_turn = not (0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS)

        if not needs_turn and random.random() < 0.15:
            needs_turn = True

        if needs_turn:
            valid = self._valid_directions()
            if valid:
                self.direction = random.choice(valid)

        hx, hy = self.body[0]
        new_head = (hx + self.direction[0], hy + self.direction[1])

        if not (0 <= new_head[0] < GRID_COLS and 0 <= new_head[1] < GRID_ROWS):
            valid = self._valid_directions()
            if valid:
                self.direction = valid[0]
                new_head = (hx + self.direction[0], hy + self.direction[1])
            else:
                return

        self.body.insert(0, new_head)
        if len(self.body) > 15:
            self.body.pop()

    def draw(self, screen, alpha=80):
        surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self._renderer.draw(surface, self.body, self.direction, False)
        surface.set_alpha(alpha)
        screen.blit(surface, (0, 0))
