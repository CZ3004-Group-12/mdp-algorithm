import pygame


def draw_button(surface, color, length, height, x, y, width):
    for i in range(1, 3):
        s = pygame.Surface((length + (i * 2), height + (i * 2)))
        s.fill(color)
        alpha = (255 / (i + 2))
        if alpha <= 0:
            alpha = 1
        s.set_alpha(alpha)
        pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
        surface.blit(s, (x - i, y - i))
    pygame.draw.rect(surface, color, (x, y, length, height), 0)
    pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
    return surface


def write_text(surface, text, text_color, length, height, x, y):
    font_size = int(length // len(text) * 2)
    my_font = pygame.font.SysFont("Calibri", font_size)
    my_text = my_font.render(text, 1, text_color)
    surface.blit(my_text, ((x + length / 2) - my_text.get_width() / 2, (y + height / 2) - my_text.get_height() / 2))
    return surface


class Button:

    def __init__(self, surface, color, x, y, length, height, text, text_color):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.width = 0
        self.text = text
        self.text_color = text_color

        surface = draw_button(self.surface, self.color, self.length, self.height, self.x, self.y, self.width)
        surface = write_text(self.surface, self.text, self.text_color, self.length, self.height, self.x, self.y)
        self.rect = pygame.Rect(x, y, length, height)

    def pressed(self, mouse):
        if self.rect.bottomright[0] > mouse[0] > self.rect.topleft[0]:
            if self.rect.bottomright[1] > mouse[1] > self.rect.topleft[1]:
                print("Some button was pressed!")
                return True
            else:
                return False
        else:
            return False

    def get_xy_and_lh(self):
        return self.x, self.y, self.length, self.height