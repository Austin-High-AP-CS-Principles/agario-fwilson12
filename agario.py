import pygame, sys, random, math


pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("agar.io")



clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.radius = random.randint(35,85)
        self.color = (random.randint(0,240), random.randint(0,240), random.randint(0,240), 180)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.deltax = random.choice([-3,-2,-1,1,2,3])
        self.deltay = random.choice([-3,-2,-1,1,2,3])
        self.rect = self.image.get_rect(center = (x,y))

    def move(self):
        if self.rect.left <= -0 or self.rect.right >= 800:
            self.deltax *= -1
        if self.rect.top <= -100 or self.rect.bottom >= 600:
            self.deltay *= -1
        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay
    def collision_check(self, other):
        if math.dist(self.rect.center, other.rect.center) < (self.radius + other.radius)*.6:
            return True
        else: 
            return False
    def grow(self, other):
        self.radius += other.radius

class Player(Enemy):
    def __init__(self, x, y):
        super().__init__()
        self.color = (255, 255, 255)
        self.radius = 45
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (100,100))
    def move(self):
        mx, my = pygame.mouse.get_pos()


tangoes = pygame.sprite.Group()
for num in range(4):
    tangoes.add(Enemy(random.randint(100,700),random.randint(100,500)))

    

class Food(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Food, self).__init__()
        self.radius = 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(15,785),random.randint(15, 585)))


meals = pygame.sprite.Group()
for num in range(20):
    meals.add(Food("red"))
objects = pygame.sprite.Group()
objects.add(meals)
objects.add(tangoes)


running = True
while running:

    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

   

    meals.draw(screen)
   
    for tango in tangoes:
        tango.move()
    tangoes.draw(screen)
   
    for obj in objects:
            for other in objects:
                if other != obj and type(obj) != Food:
                    if math.dist(obj.rect.center, other.rect.center) < (obj.radius + other.radius)*.7 and obj.radius > other.radius:
                        obj.radius += other.radius
                        objects.remove(other)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
