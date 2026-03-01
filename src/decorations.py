import pygame
import random
from .config import (
    CELL_SIZE, GRID_COLS, GRID_ROWS,
    BORDER_SIZE, BORDER_PX, GRID_OFFSET_X, GRID_OFFSET_Y,
    HEADER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    BORDER_COLOR, BORDER_DARK, BORDER_GRASS, BORDER_GRASS_ALT,
    DECO_SPRITE_PATH, SPRITE_CELL,
)

# Índices no sprite sheet de decorações
ROCK_1 = 0
ROCK_2 = 1
TREE = 2
BUSH = 3
FLOWERS = 4
GRASS = 5


class BorderDecorations:
    def __init__(self):
        self.sprites = self._load_sprites()
        self.layout = self._generate_layout()

    def _load_sprites(self):
        try:
            sheet = pygame.image.load(DECO_SPRITE_PATH).convert_alpha()
        except (pygame.error, FileNotFoundError):
            return []

        sprites = []
        cols = sheet.get_width() // SPRITE_CELL
        for i in range(cols):
            rect = pygame.Rect(i * SPRITE_CELL, 0, SPRITE_CELL, SPRITE_CELL)
            s = pygame.Surface((SPRITE_CELL, SPRITE_CELL), pygame.SRCALPHA)
            s.blit(sheet, (0, 0), rect)
            scaled = pygame.transform.scale(s, (CELL_SIZE, CELL_SIZE))
            sprites.append(scaled)
        return sprites

    def _generate_layout(self):
        """Distribui decorações aleatórias nas células da borda."""
        random.seed(42)  # Seed fixo para layout consistente
        layout = []

        total_cols = GRID_COLS + BORDER_SIZE * 2
        total_rows = GRID_ROWS + BORDER_SIZE * 2

        for row in range(total_rows):
            for col in range(total_cols):
                in_grid = (BORDER_SIZE <= col < BORDER_SIZE + GRID_COLS and
                           BORDER_SIZE <= row < BORDER_SIZE + GRID_ROWS)
                if in_grid:
                    continue

                # Posição em pixels
                px = col * CELL_SIZE
                py = HEADER_HEIGHT + row * CELL_SIZE

                # Cantos: pedras
                is_corner = ((col < BORDER_SIZE and row < BORDER_SIZE) or
                             (col >= total_cols - BORDER_SIZE and row < BORDER_SIZE) or
                             (col < BORDER_SIZE and row >= total_rows - BORDER_SIZE) or
                             (col >= total_cols - BORDER_SIZE and row >= total_rows - BORDER_SIZE))

                # Árvores/arbustos
                is_adjacent = (col == BORDER_SIZE - 1 or col == BORDER_SIZE + GRID_COLS or
                               row == BORDER_SIZE - 1 or row == BORDER_SIZE + GRID_ROWS)

                if is_corner:
                    deco = random.choice([ROCK_1, ROCK_2])
                elif is_adjacent:
                    deco = random.choice([TREE, BUSH, BUSH, FLOWERS, GRASS, GRASS])
                else:
                    deco = random.choice([GRASS, FLOWERS, BUSH, None, None])

                layout.append((px, py, deco))

        return layout

    def draw(self, screen):
        if not self.sprites:
            return

        total_cols = GRID_COLS + BORDER_SIZE * 2
        total_rows = GRID_ROWS + BORDER_SIZE * 2

        # Terreno base da borda
        for row in range(total_rows):
            for col in range(total_cols):
                in_grid = (BORDER_SIZE <= col < BORDER_SIZE + GRID_COLS and
                           BORDER_SIZE <= row < BORDER_SIZE + GRID_ROWS)
                if in_grid:
                    continue

                px = col * CELL_SIZE
                py = HEADER_HEIGHT + row * CELL_SIZE
                color = BORDER_COLOR if (row + col) % 2 == 0 else BORDER_DARK
                pygame.draw.rect(screen, color, (px, py, CELL_SIZE, CELL_SIZE))

        # Desenha as decorações por cima
        for px, py, deco_type in self.layout:
            if deco_type is not None and deco_type < len(self.sprites):
                screen.blit(self.sprites[deco_type], (px, py))
