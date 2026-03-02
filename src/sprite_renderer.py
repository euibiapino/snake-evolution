import pygame
from .config import (
    CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, SPRITE_CELL, SPRITE_PATH,
    SPR_HEAD_RIGHT, SPR_HEAD_LEFT, SPR_HEAD_UP, SPR_HEAD_DOWN,
    SPR_BODY_H, SPR_BODY_V,
    SPR_CORNER_BL, SPR_CORNER_BR, SPR_CORNER_TL, SPR_CORNER_TR,
    SPR_TAIL_RIGHT, SPR_TAIL_LEFT, SPR_TAIL_UP, SPR_TAIL_DOWN,
    DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN,
)

SHEET_COLS = 4


def _load_sprites():
    try:
        sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    except (pygame.error, FileNotFoundError):
        return None

    sprites = []
    rows = sheet.get_height() // SPRITE_CELL
    cols = sheet.get_width() // SPRITE_CELL

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * SPRITE_CELL, row * SPRITE_CELL, SPRITE_CELL, SPRITE_CELL)
            s = pygame.Surface((SPRITE_CELL, SPRITE_CELL), pygame.SRCALPHA)
            s.blit(sheet, (0, 0), rect)
            scaled = pygame.transform.scale(s, (CELL_SIZE, CELL_SIZE))
            sprites.append(scaled)

    return sprites


def _make_boost_sprites(sprites):
    result = []
    for sprite in sprites:
        tinted = sprite.copy()
        tinted.fill((80, 160, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
        result.append(tinted)
    return result


HEAD_MAP = {
    DIR_RIGHT: SPR_HEAD_RIGHT,
    DIR_LEFT:  SPR_HEAD_LEFT,
    DIR_UP:    SPR_HEAD_UP,
    DIR_DOWN:  SPR_HEAD_DOWN,
}

TAIL_MAP = {
    DIR_RIGHT: SPR_TAIL_LEFT,
    DIR_LEFT:  SPR_TAIL_RIGHT,
    DIR_UP:    SPR_TAIL_DOWN,
    DIR_DOWN:  SPR_TAIL_UP,
}


def _corner_index(prev_pos, curr_pos, next_pos):
    dx1 = prev_pos[0] - curr_pos[0]
    dy1 = prev_pos[1] - curr_pos[1]
    dx2 = next_pos[0] - curr_pos[0]
    dy2 = next_pos[1] - curr_pos[1]

    sx = dx1 + dx2
    sy = dy1 + dy2

    if sx > 0 and sy > 0:
        return SPR_CORNER_BR
    elif sx > 0 and sy < 0:
        return SPR_CORNER_TR
    elif sx < 0 and sy > 0:
        return SPR_CORNER_BL
    elif sx < 0 and sy < 0:
        return SPR_CORNER_TL

    return SPR_BODY_H


class SnakeSpriteRenderer:
    def __init__(self):
        self.sprites = _load_sprites()
        self.boost_sprites = _make_boost_sprites(self.sprites) if self.sprites else None

    def _get(self, index, boost=False):
        pool = self.boost_sprites if (boost and self.boost_sprites) else self.sprites
        if index >= len(pool):
            return pool[0]
        return pool[index]

    def _clip_excluding(self, screen, full_clip, seg_pos, corner_pos, cs):
        cx = corner_pos[0] * cs + GRID_OFFSET_X
        cy = corner_pos[1] * cs + GRID_OFFSET_Y
        if seg_pos[0] < corner_pos[0]:
            clip = pygame.Rect(full_clip.left, full_clip.top, cx, full_clip.height)
        elif seg_pos[0] > corner_pos[0]:
            clip = pygame.Rect(cx + cs, full_clip.top, full_clip.right - cx - cs, full_clip.height)
        elif seg_pos[1] < corner_pos[1]:
            clip = pygame.Rect(full_clip.left, full_clip.top, full_clip.width, cy)
        else:
            clip = pygame.Rect(full_clip.left, cy + cs, full_clip.width, full_clip.bottom - cy - cs)
        screen.set_clip(clip)

    def draw(self, screen, body, direction, speed_boost, lerp_t=1.0):
        if not self.sprites or len(body) == 0:
            return

        t = lerp_t
        back = 1.0 - t
        last = len(body) - 1
        cs = CELL_SIZE
        head_blit = None
        corner_blits = []

        corners = set()
        for i in range(1, last):
            prev = body[i - 1]
            pos = body[i]
            next_ = body[i + 1]
            if not ((prev[1] == pos[1] == next_[1]) or (prev[0] == pos[0] == next_[0])):
                corners.add(i)

        full_clip = screen.get_clip()

        for i in range(last, -1, -1):
            pos = body[i]
            px = pos[0] * cs + GRID_OFFSET_X
            py = pos[1] * cs + GRID_OFFSET_Y

            if i == 0:
                if last >= 1 and 1 not in corners:
                    px += (body[1][0] - pos[0]) * back * cs
                    py += (body[1][1] - pos[1]) * back * cs
                elif last >= 1:
                    px -= direction[0] * back * cs * 0.5
                    py -= direction[1] * back * cs * 0.5
                idx = HEAD_MAP[direction]
                head_blit = (self._get(idx, speed_boost), (int(px), int(py)))
                continue

            if i in corners:
                prev = body[i - 1]
                next_ = body[i + 1]
                idx = _corner_index(prev, pos, next_)
                corner_blits.append((self._get(idx, speed_boost), (int(px), int(py))))
                continue

            if i == last:
                px += (pos[0] - body[i - 1][0]) * back * cs
                py += (pos[1] - body[i - 1][1]) * back * cs
                dx = body[i - 1][0] - body[i][0]
                dy = body[i - 1][1] - body[i][1]
                idx = TAIL_MAP.get((dx, dy), SPR_TAIL_LEFT)
            else:
                next_ = body[i + 1]
                dy_prev = body[i - 1][1] - pos[1]
                if dy_prev == 0:
                    idx = SPR_BODY_H
                else:
                    idx = SPR_BODY_V
                px += (next_[0] - pos[0]) * back * cs
                py += (next_[1] - pos[1]) * back * cs

            need_clip = (i + 1) in corners or (i - 1) in corners
            if need_clip:
                clips = []
                if (i + 1) in corners:
                    clips.append(body[i + 1])
                if (i - 1) in corners:
                    clips.append(body[i - 1])
                if len(clips) == 1:
                    self._clip_excluding(screen, full_clip, pos, clips[0], cs)
                else:
                    self._clip_excluding(screen, full_clip, pos, clips[0], cs)
                    r1 = screen.get_clip()
                    self._clip_excluding(screen, full_clip, pos, clips[1], cs)
                    r2 = screen.get_clip()
                    screen.set_clip(r1.clip(r2))

            screen.blit(self._get(idx, speed_boost), (int(px), int(py)))

            if need_clip:
                screen.set_clip(full_clip)

        for j in corners:
            cpos = body[j]
            if j + 1 <= last and (j + 1) not in corners:
                tpos = body[j + 1]
                if tpos[1] == cpos[1]:
                    filler_idx = SPR_BODY_H
                else:
                    filler_idx = SPR_BODY_V
                fpx = tpos[0] * cs + GRID_OFFSET_X
                fpy = tpos[1] * cs + GRID_OFFSET_Y
                self._clip_excluding(screen, full_clip, tpos, cpos, cs)
                screen.blit(self._get(filler_idx, speed_boost), (int(fpx), int(fpy)))
                screen.set_clip(full_clip)

        for blit in corner_blits:
            screen.blit(*blit)
        if head_blit:
            screen.blit(*head_blit)
