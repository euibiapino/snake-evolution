import pygame
import random
import math
from .config import CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, PARTICLE_COUNT, PARTICLE_SPEED, PARTICLE_LIFETIME, PARTICLE_SIZE


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, PARTICLE_SPEED)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = PARTICLE_LIFETIME
        self.max_life = PARTICLE_LIFETIME
        self.size = random.randint(2, PARTICLE_SIZE)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1

    @property
    def alive(self):
        return self.life > 0

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        r, g, b = self.color
        size = max(1, int(self.size * (self.life / self.max_life)))
        surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (r, g, b, alpha), (size, size), size)
        screen.blit(surface, (int(self.x) - size, int(self.y) - size))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, grid_x, grid_y, color, count=PARTICLE_COUNT):
        px = grid_x * CELL_SIZE + GRID_OFFSET_X + CELL_SIZE // 2
        py = grid_y * CELL_SIZE + GRID_OFFSET_Y + CELL_SIZE // 2
        for _ in range(count):
            self.particles.append(Particle(px, py, color))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

    def clear(self):
        self.particles.clear()
