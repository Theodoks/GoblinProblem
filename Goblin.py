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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if exitBtn.isClicked(x, y):
                        pygame.quit()
                        sys.exit(0)

                    if tryBtn.isClicked(x, y):
                        exitBtn.__del__()
                        tryBtn.__del__()
                        window.fill((0, 0, 0))
                        pygame.display.flip()
                        game = Game(4, 0)




            tryBtn.render()
            exitBtn.render()

            pygame.display.flip()
            clock.tick(60)


class Player:
    x = 1
    y = 1
    speed = 1


    def __init__(self, X, Y, Speed):
        self.x = X
        self.y = Y
        self.speed = Speed

    def getAngle(self):
        if self.x != width/2:
            if self.x < width/2:
                return math.pi + math.atan(-(self.y - height/2) / (self.x - width/2))
            elif self.y > height/2:
                return 2 * math.pi + math.atan(-(self.y - height/2) / (self.x - width/2))
            else:
                return math.atan(-(self.y - height/2) / (self.x - width/2))
        else:
            if self.y > height/2:
                return 3 / 2 * math.pi
            else:
                return math.pi / 2

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

    def detectWin(self):
        x = self.x - width/2
        y = self.y - height/2
        if math.sqrt(x**2 + y**2) > radius:
            return 1
        else:
            return 0

    def __del__(self):
        return 0


class Goblin:
    angle = 0
    goblinSpeed = 0

    def __init__(self, angle, goblinSpeed):
        self.angle = 7 / 4 * math.pi
        self.goblinSpeed = goblinSpeed / radius

    def render(self):
        pygame.draw.circle(window, (60, 200, 0), (width/2 + radius * math.cos(self.angle), height/2 - radius * math.sin(self.angle)), 5)

    def update(self, target):

        if self.angle % (2*math.pi) > target:
            distLeft = target + (2*math.pi - (self.angle % (2*math.pi)))
        else:
            distLeft = target - (self.angle % (2*math.pi))

        distRight = 2*math.pi - distLeft


        if distLeft < distRight:
            if distLeft < self.goblinSpeed:

                self.angle = target
            else:
                self.angle += self.goblinSpeed
        else:
            if distRight < self.goblinSpeed:

                self.angle = target
            else:
                self.angle -= self.goblinSpeed

class Game:
    def __init__(self, goblinSpeed, assist):

        exitBtn = Button("EXIT", 50,  30)
        player = Player(width/2, height/2, speed)
        goblin = Goblin(0, goblinSpeed * speed)
        clicking = 0
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if exitBtn.isClicked(x, y):
                        exitBtn.__del__()
                        player.__del__()
                        window.fill((0, 0, 0))
                        pygame.display.flip()
                        game = MainMenu()
                clicking = pygame.mouse.get_pressed()[0]
                if pygame.mouse.get_pressed()[2]:
                    print("Right pressed")

            if clicking:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if abs(player.x - x) > 2 or abs(player.y - y) > 2:
                    player.update(x, y)

            if abs(goblin.angle % (math.pi * 2) - player.getAngle()) > 0.001:
                goblin.update(player.getAngle())

            if player.detectWin():
                win = Button("ESCAPED!", width/2, height/2)
                while True:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        clicking = pygame.mouse.get_pressed()[0]

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            game = Game(goblinSpeed, assist)

                    if clicking:
                        x, y = pygame.mouse.get_pos()
                        print(x, y)

                    pygame.draw.circle(window, (0, 64, 200), (width / 2, height / 2), radius)
                    pygame.draw.circle(window, (255, 0, 0), (width / 2, height / 2), radius * (1 / goblinSpeed))
                    player.render()
                    goblin.render()
                    win.render()

                    pygame.display.flip()
                    window.fill((0, 0, 0))
                    clock.tick(60)

            pygame.draw.circle(window, (0, 64, 200), (width/2, height/2), radius)
            pygame.draw.circle(window, (255, 0, 0), (width / 2, height / 2), radius * (1 / goblinSpeed))
            player.render()
            goblin.render()
            exitBtn.render()

            pygame.display.flip()
            window.fill((0, 0, 0))
            clock.tick(60)


width = 1024
height = 720
radius = 300
speed = 2.5
window = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

scene = MainMenu()
