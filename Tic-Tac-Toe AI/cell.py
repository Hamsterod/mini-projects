import pygame

width = 30

class Cell:
    def __init__(self, position, cell_type):
        self.position = position
        self.cell_type = cell_type

    def draw_cell(self, screen):
        pygame.draw.rect(screen, "white", [self.position.x * screen.get_width() / 3, self.position.y * screen.get_height() / 3, screen.get_width() / 3, screen.get_height() / 3], 5)
        if  self.cell_type == 2:
            pygame.draw.circle(screen, "#f58973", [ self.position.x * screen.get_width() / 3 + screen.get_width() / 6,
                                                                self.position.y * screen.get_width() / 3 + screen.get_width() / 6],
                                                                screen.get_width() / 6 - 20, 10)
        if self.cell_type == 1:
            pygame.draw.line(screen, "#73a7f5", [self.position.x * screen.get_width() / 3 + width, self.position.y * screen.get_height() / 3 + width],
                                                    [self.position.x * screen.get_width() / 3 + screen.get_width() / 3 - width, self.position.y * screen.get_height() / 3 + screen.get_height() / 3 - width],15)
            pygame.draw.line(screen, "#73a7f5",[self.position.x * screen.get_width() / 3 + screen.get_width() / 3 - width, self.position.y * screen.get_height() / 3 + width],
                                                   [self.position.x * screen.get_width() / 3 + width, self.position.y * screen.get_height() / 3 + screen.get_height() / 3 - width], 15)