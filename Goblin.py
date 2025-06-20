import sys, math, pygame
pygame.init()

class Slider:
    text = "Default slider"
    font = pygame.font.Font(None, 38)
    x = 0
    y = 0
    length = 180
    pos = 0
    color = (0, 255, 0)
    interacting = 0
    minVal = 0
    maxVal = 100

    def __init__(self, Text, X, Y, minVal = 0, maxVal = 100, color=(0, 255, 0)):
        self.text = Text
        self.x = X
        self.y = Y
        self.Btn = self.font.render(Text, 1, color)
        self.rect = self.Btn.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.minVal = minVal
        self.maxVal = maxVal

        self.Val = self.font.render(str(round(self.minVal + (self.maxVal - self.minVal) * self.pos, 2)), 1, self.color)
        self.valrect = self.Val.get_rect()
        self.valrect.centerx = self.x + self.length/2 + 30
        self.valrect.centery = self.y + 35

    def render(self):
        window.blit(self.Btn, self.rect)
        self.Val = self.font.render(str(round(self.minVal + (self.maxVal - self.minVal) * self.pos, 2)), 1, self.color)
        window.blit(self.Val, self.valrect)

        pygame.draw.line(window, self.color, (self.x - self.length / 2, self.y + 35), (self.x + self.length/2, self.y + 35), 10)
        pygame.draw.circle(window, self.color, (self.x - self.length/2 + self.length * self.pos, self.y + 35), 12)

    def isClicked(self, mouseX, mouseY):
        if self.x - self.length / 2 < mouseX < self.x + self.length/2 and self.y + 25 < mouseY < self.y + 45:
            return 1
        else:
            return 0

    def move(self, mouseX, mouseY):
        if mouseX > self.x + self.length/2:
            self.pos = 1.0
        elif mouseX < self.x - self.length/2:
            self.pos = 0
        else:
            self.pos = (mouseX - (self.x - self.length/2)) / self.length

class Button:
    text = "Default button"
    font = pygame.font.Font(None, 48)
    x = 0
    y = 0

    Btn = font.render(text, 1, (0, 255, 0))
    rect = Btn.get_rect()
    rect.centerx = x
    rect.centery = y

    def __init__(self, Text, X, Y, color=(0, 255, 0)):
        self.text = Text
        self.x = X
        self.y = Y
        self.Btn = self.font.render(Text, 1, color)
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
        exitBtn = Button("ВЫХОД", width / 2, height / 2 + 50)
        tryBtn = Button("НАЧАТЬ", width / 2, height / 2)
        speedSlider = Slider("СКОРОСТЬ ГОБЛИНА", width / 2, height / 2 - 100, 1, 5)
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
                        game = Game((speedSlider.minVal + speedSlider.pos * (speedSlider.maxVal - speedSlider.minVal)))

                    if speedSlider.isClicked(x, y):

                        speedSlider.interacting = 1


            tryBtn.render()
            exitBtn.render()


            if speedSlider.interacting:

                clicking = pygame.mouse.get_pressed()[0]
                if not clicking:
                    speedSlider.interacting = 0
                else:
                    x, y = pygame.mouse.get_pos()
                    speedSlider.move(x, y)
            speedSlider.render()


            pygame.display.flip()

            window.fill((0, 0, 0))
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

    def detectDeath(self, goblinAngle):
        x = self.x - width / 2
        y = self.y - height / 2
        if math.sqrt(x ** 2 + y ** 2) >= radius - 3 and abs(self.getAngle() - goblinAngle) < 0.05:
            return 1
        else:
            return 0

    def __del__(self):
        return 0


class Goblin:
    angle = 0
    goblinSpeed = 0

    def __init__(self, angle, goblinSpeed):
        self.angle = angle
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
    def __init__(self, goblinSpeed):

        exitBtn = Button("ВЫХОД", 70,  30)
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


            if clicking:
                x, y = pygame.mouse.get_pos()
                if abs(player.x - x) > 2 or abs(player.y - y) > 2:
                    player.update(x, y)

            if abs(goblin.angle % (math.pi * 2) - player.getAngle()) > 0.001:
                goblin.update(player.getAngle())

            if player.detectWin() or player.detectDeath(goblin.angle):
                win = Button("УСПЕХ!", width/2, height/2)
                death = Button("ВЫ БЫЛИ СЪЕДЕНЫ!", width/2, height/2, (200, 60, 0))
                while True:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit(0)
                        clicking = pygame.mouse.get_pressed()[0]

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            game = Game(goblinSpeed)



                    pygame.draw.circle(window, (0, 64, 200), (width / 2, height / 2), radius)
                    pygame.draw.circle(window, (255, 255, 255), (width / 2, height / 2), radius * (1 / goblinSpeed), 1)
                    player.render()
                    goblin.render()
                    if player.detectWin():
                        win.render()
                    else:
                        death.render()

                    pygame.display.flip()
                    window.fill((0, 0, 0))
                    clock.tick(60)

            pygame.draw.circle(window, (0, 64, 200), (width/2, height/2), radius)
            pygame.draw.circle(window, (255, 255, 255), (width / 2, height / 2), radius * (1 / goblinSpeed), 1)
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
