import pygame
from math import floor
from Simulator import Simulator

# COLOURS
white = (255, 255, 255)
black = (0, 0, 0)
orange = (240, 120, 0)
rainbow = [
    white,
    (240, 0, 0),
    (180, 60, 0),
    (120, 120, 0),
    (60, 180, 0),
    (0, 240, 0),
    (0, 180, 60),
    (0, 120, 120),
    (0, 60, 180),
    (0, 0, 240)
]
margin = 20
panelWidth = 200
buttonHeight = 50


class Visualisation:
    """
    Visualiser for Game of Life ``World``s.
    """

    def __init__(self, simulator: Simulator, size: (int, int) = (800, 600), scale: float = 1) -> None:
        """
        Constructor to initiate the visualistion. Visualisor requires focus, meaning that it connects to ``Simulator`` object to call ``update()``.

        :param simulator: ``Simulator``-object used to evolve the state of the world.
        :param size: tuple to indicate the desired screen size. Typical values are (800, 600), (1024, 768), (1280, 1024), etc.
        :param scale: float to indicate the draw-scale: 1 = 100%, 0.5 = 50%, etc.
        """
        pygame.init()
        pygame.font.init()
        self.simulator = simulator
        self.size = size
        self.org_scale = scale
        self.scale = scale
        self.__determineScale__()
        self.scaled_margin = margin * self.scale
        self.paused = True
        self.font = pygame.font.SysFont("Arial", 16)
        self.surface = pygame.display.set_mode((self.size[0], self.size[1]))
        pygame.display.set_caption("BS - Game of Life")
        self.surface.fill(white)
        pygame.display.flip()
        self.done = False
        self.editable = True
        self.clock = pygame.time.Clock()

        while not self.done:
            self.__handle_events__()

            if not self.editable and not self.paused:
                self.simulator.update()

            self.__redraw__()

            if self.editable:
                self.clock.tick(10) # 10 fps when editing (for responsiveness)
            else:
                self.clock.tick(2) # 2 fps otherwise (to slow down simulation)

    def __handle_events__(self) -> None:
        """
        Internal method to handle interaction with the UI.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                if mouseX > self.scaled_margin and mouseX < self.scaled_margin + self.simulator.get_world().width * self.scaled_margin:
                    if mouseY > self.scaled_margin and mouseY < self.scaled_margin + self.simulator.get_world().height * self.scaled_margin:
                        x = floor((mouseX - self.scaled_margin) / self.scaled_margin)
                        y = floor((mouseY - self.scaled_margin) / self.scaled_margin)
                        oldValue = self.simulator.get_world().get(x, y)
                        newValue = (oldValue + 1) % 9
                        if self.editable:
                            self.simulator.get_world().set(x, y, newValue)
                if mouseX > self.size[0] - panelWidth + margin and mouseX < self.size[0] - margin:
                    if mouseY > margin*3 and mouseY < margin*3+buttonHeight:
                        self.editable = False
                        self.paused = not self.paused

    def __determineScale__(self) -> None:
        """
        Determine and adapts the scale factor of the display to fit the requested world.
        """
        # scale too big:
        while self.scale*(self.simulator.get_world().height+2)*margin > self.size[1] and self.scale*(self.simulator.get_world().width+2)*margin > self.size[0] - panelWidth:
            self.scale = round(self.scale*0.9, 2)

        # scale too small:
        if floor(self.scale * margin) < 5:
            self.scale = 5/margin


    def __redraw__(self) -> None:
        """
        Internal method to redraw the elements of the visualisation.
        """
        # Clean the canvas
        self.surface.fill(white)

        # Draw the cells
        for y in range(self.simulator.get_world().height):
            for x in range(self.simulator.get_world().width):
                pygame.draw.rect(self.surface, rainbow[self.simulator.get_world().get(x,y)], ((x+1) * self.scaled_margin, (y + 1) * self.scaled_margin, self.scaled_margin, self.scaled_margin))
        # Draw vertical lines
        for y in range(self.simulator.get_world().height+1):
            pygame.draw.line(self.surface, black, (self.scaled_margin, (y + 1) * self.scaled_margin), ((self.simulator.get_world().width + 1) * self.scaled_margin, (y + 1) * self.scaled_margin))
        # Draw horizontal lines
        for x in range(self.simulator.get_world().width+1):
            pygame.draw.line(self.surface, black, ((x+1) * self.scaled_margin, self.scaled_margin), ((x + 1) * self.scaled_margin, (self.simulator.get_world().height + 1) * self.scaled_margin))

        panelX = self.size[0] - panelWidth + margin
        panelY = margin

        # Generation text
        pygame.draw.rect(self.surface, white, (panelX, panelY, panelWidth-2*margin, buttonHeight))
        genText = "Generation: "+str(self.simulator.generation)
        gt = self.font.render(genText, 0, black)
        self.surface.blit(gt, (panelX, panelY))

        buttonWidth = panelWidth-2*margin
        panelY += 2 * margin
        # Pause button
        pygame.draw.rect(self.surface, orange,
                         (panelX, panelY, buttonWidth, buttonHeight))
        ppText = "Play" if self.paused else "Pause"
        playPausedText = self.font.render(ppText, 0, white)
        (w,h) = self.font.size(ppText)
        self.surface.blit(playPausedText, (panelX+(buttonWidth-w)/2, panelY+(buttonHeight-h)/2))

        # Write to screen
        pygame.display.update()
