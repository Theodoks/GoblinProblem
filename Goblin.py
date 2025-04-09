import sys, math, pygame
pygame.init()

class Button:
    text = "Default button"
    font = pygame.font.Font(None, 48)
    x = 0
    y = 0

    Btn = font.render(text, 1, (0, 255, 0))
    rect = Btn.get_rect()
    rect.centerx = x
    rect.centery = y

    def __init__(self, Text, X, Y):
        self.text = Text
        self.x = X
        self.y = Y
        self.Btn = self.font.render(Text, 1, (0, 255, 0))
        self.rect = self.Btn.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def render(self):
        window.blit(self.Btn, self.rect)

    def isClicked(self, mouseX, mouseY):
        if self.rect.centerx - self.rect.width/2 < mouseX < self.rect.centerx + self.rect.width/2 and self.rect.centery - self.rect.height/2 < mouseY < self.rect.centery + self.rect.height/2:
            return 1
        else:
            return 0

    def __del__(self):
        return 0


class MainMenu:
    def __init__(self):
        font = pygame.font.Font(None, 48)
        exitBtn = Button("EXIT", width / 2, height / 2 + 50)
        tryBtn = Button("TRY", width / 2, height / 2)
        while True:
            clicking = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                clicking = pygame.mouse.get_pressed()[0]

            if clicking:
                x, y = pygame.mouse.get_pos()
                if exitBtn.isClicked(x, y):
                    pygame.quit()
                    sys.exit(0)

                if tryBtn.isClicked(x, y):
                    exitBtn.__del__()
                    tryBtn.__del__()
                    window.fill((0,0,0))
                    pygame.display.flip()
                    game = Game(3, 0)

            tryBtn.render()
            exitBtn.render()

            pygame.display.flip()
            clock.tick(60)

class Player:
    x = 0
    y = 0
    speed = 1
    def __init__(self, X, Y, Speed):
        self.x = X
        self.y = Y
        self.speed = Speed

    def render(self):
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), 5)
    def update(self, mouseX, mouseY):

        distX = mouseX - self.x
        distY = mouseY - self.y
        if distY == 0:
            dx = 10
            dy = 0
        elif distX == 0:
            dx = 0
            dy = 10
        else:
            dx = math.sqrt(((distX**2 / distY**2) * self.speed**2) / (1 + distX**2 / distY**2))
            dy = math.sqrt(self.speed**2 - dx**2)
        if distX < 0:
            self.x -= dx
        else:
            self.x += dx
        if distY < 0:
            self.y -= dy
        else:
            self.y += dy

    def __del__(self):
        return 0
class Game:
    def __init__(self, goblinSpeed, assist):

        exitBtn = Button("EXIT", 50,  30)
        player = Player(width/2, height/2, 2.5)
        clicking = 0
        while True:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                clicking = pygame.mouse.get_pressed()[0]
                if pygame.mouse.get_pressed()[2]:
                    print("Right pressed")


            if clicking:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if exitBtn.isClicked(x, y):
                    exitBtn.__del__()
                    player.__del__()
                    window.fill((0, 0, 0))
                    pygame.display.flip()
                    game = MainMenu()
                player.update(x, y)

            pygame.draw.circle(window, (0, 64, 200), (width/2, height/2), 225)
            player.render()
            exitBtn.render()

            pygame.display.flip()
            window.fill((0, 0, 0))
            clock.tick(60)


width = 1024
height = 720


window = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

scene = MainMenu()
