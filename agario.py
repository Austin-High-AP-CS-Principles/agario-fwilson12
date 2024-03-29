import pygame, sys, random, math


pygame.init()

screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("agar.io")

def draw_grid(screen):
    for x in range(0, screen_width, 50):
        pygame.draw.line(screen, (230,230,230,230), (x, 0), (x, screen_height))

    for y in range(0, screen_height, 50):
        pygame.draw.line(screen, (230,230,230,230), (0, y), (screen_width, y))






clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.radius = random.randint(25,65)
        self.color = (random.randint(0,240), random.randint(0,240), random.randint(0,240), 180)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.deltax = random.choice([-2,2])
        self.deltay = random.choice([-2,2])
        self.rect = self.image.get_rect(center = (x,y))

    def move(self):
        if self.rect.left <= 2 or self.rect.right >= 1398:
            self.deltax *= -1
        if self.rect.top <= 2 or self.rect.bottom >= 798:
            self.deltay *= -1
        multi = 1
        if 0 <= self.radius <= 40:
            multi = 1.5
        elif 40 < self.radius <= 60:
            multi = .75
        elif 60 < self.radius <= 80:
            multi = .667
        elif 80 < self.radius <= 100:
            multi = .5
        elif 100 < self.radius:
            multi = .3

        self.rect.centerx += self.deltax *multi
        self.rect.centery += self.deltay *multi
    def collision_check(self, other):
        if math.dist(self.rect.center, other.rect.center) < (self.radius + other.radius)*.65 and self.radius > 1.1 * other.radius:
            return True
        else: 
            return False
    def grow(self, other):
        self.radius += other.radius
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=self.rect.center)

class Player(Enemy):
    def __init__(self, x, y):
        super(Player, self).__init__(x,y)
        self.color = (255, 255, 255)
        self.radius = 55
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (x,y))
    def move(self):
        mx, my = pygame.mouse.get_pos()
        distx = mx - self.rect.centerx
        disty = my - self.rect.centery
        hyp = math.sqrt(abs(distx**2 - disty**2))
        if hyp > 0:
            self.deltax = distx/hyp 
            self.deltay = disty/hyp 
        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay
    def loser(self):
        font = pygame.font.SysFont(None, 55)
        text = font.render("You died...", True, 'blue')
        screen.blit(text, (screen_width//2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
    
        
players = pygame.sprite.Group()
chris = Player(random.randint(600,800),random.randint(450,550))
players.add(chris)


tangoes = pygame.sprite.Group()
for num in range(5):
    tangoes.add(Enemy(random.randint(100,1300),random.randint(100,700)))

    

class Food(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Food, self).__init__()
        self.radius = 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(50,1350),random.randint(30, 770)))


meals = pygame.sprite.Group()
for num in range(10):
    meals.add(Food(random.choice(['red','yellow','green','blue'])))
objects = pygame.sprite.Group()
objects.add(meals)
objects.add(tangoes)
objects.add(players)




running = True
while running:

    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    draw_grid(screen)
   
    
    
    meals.draw(screen)
   
    for tango in tangoes:
        tango.move()
    tangoes.draw(screen)
    
    if chris in objects:
        chris.move()
    players.draw(screen)

    for obj in objects:
            for other in objects:
                if other != obj and type(obj) != Food:
                    if obj.collision_check(other):
                        obj.grow(other)
                        if type(other) != Food:
                            objects.remove(other)
                            other.kill()
                        elif type(other) == Food:
                            other.rect.x, other.rect.y = (random.randint(50,1350),random.randint(30, 770))
    if chris not in objects:
        chris.loser()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
