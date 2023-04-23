import pygame
import math

from quarto import Board, Piece, Game, Player, PIECES, HIGH, LOW, LIGHT, DARK, ROUND, SQUARE, SOLID, HOLLOW

class PygameVisualizer:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # set the size of the screen
        screen_size = (400, 400)
        self._screen = pygame.display.set_mode(screen_size)

        # constants/themes
        self._bg_color = (255, 255, 255) # white
        self._circle_size = 80
        self._margin = 10

        self._sprites = self._load_sprites()

    def _load_sprites(self):
        spritesheet = pygame.image.load("pieces.png").convert_alpha()
        sprite_width = sprite_height = 64
        sprites = []
        for i in range(4):
            for j in range(4):
                # calculate the x and y coordinates of the sprite on the spritesheet
                x = j * sprite_width
                y = i * sprite_height

                # clip the sprite from the spritesheet and add it to the list of sprites
                sprite_rect = pygame.Rect(x+1, y+1, sprite_width-2, sprite_height-2)
                sprite = spritesheet.subsurface(sprite_rect)
                sprites.append(sprite)
        return sprites

    def _draw_screen(self):
        self._screen.fill((255, 255, 255))
        for i in range(4):
            for j in range(4):
                # calculate the center of the circle
                x = (i + 0.5) * (self._circle_size + 2*self._margin) 
                y = (j + 0.5) * (self._circle_size + 2*self._margin)
                center = (int(x), int(y))
                # create the circle surface
                circle_surf = pygame.Surface((self._circle_size, self._circle_size))
                circle_surf.fill(self._bg_color)
                # draw the circle
                pygame.draw.circle(circle_surf, (0, 0, 0), (self._circle_size//2, self._circle_size//2), self._circle_size//2, 2)
                pygame.draw.circle(circle_surf, (255, 255, 255), (self._circle_size//2, self._circle_size//2), self._circle_size//2-2)
                self._screen.blit(circle_surf, circle_surf.get_rect(center=center))

    def piece_sprite_index(self, piece):
        index = 0
        if piece.has(HIGH):
            index += 8
            if piece.has(LIGHT):
                index += 4
        else:
            if piece.has(DARK):
                index += 4

        if piece.has(SQUARE):
            index += 2
            if piece.has(SOLID):
                index += 1
        else:
            if piece.has(HOLLOW):
                index += 1
        return index

    def update(self, board):
        self._draw_screen()
        for i in range(4):
            for j in range(4):
                p = board[(i,j)]
                if p:
                    x = (i + 0.5) * (self._circle_size + 2*self._margin) 
                    y = (j + 0.5) * (self._circle_size + 2*self._margin)
                    self._screen.blit(self._sprites[self.piece_sprite_index(p)], (x-31, y-31))
        pygame.display.update()


    def quit(self):
        # quit pygame
        pygame.quit()

    def wait_for_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    return "ok"

if __name__ == "__main__":
    game = PygameVisualizer()
    game.update(None)
    game.wait_for_input()
    game.quit()