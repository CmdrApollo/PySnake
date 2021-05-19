import pygame, random

SIZE = 600
TILECOUNT = 10
TILESIZE = SIZE//TILECOUNT
WIN = pygame.display.set_mode((SIZE, SIZE))
FPS = 60
GAMESPEED = 5

class Food:
    def __init__(self, color):
        self.pos = self.randomize_pos()
        self.col = color
        print(random.random()*20)
    
    def randomize_pos(self):
        return (random.randint(0, TILECOUNT-1), random.randint(0, TILECOUNT-1))

    def draw(self, win):
        pygame.draw.rect(win, self.col, (self.pos[0]*TILESIZE, self.pos[1]*TILESIZE, TILESIZE, TILESIZE))

class Snake:
    def __init__(self, pos, color):
        self.ogpos = pos
        self.poses = [pos]
        self.dir = (0, 0)
        self.col = color
    
    def handle_keys(self, press):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or press == pygame.K_LEFT:
            self.dir = (-1, 0)
            press = None
        elif keys[pygame.K_RIGHT] or press == pygame.K_RIGHT:
            self.dir = (1, 0)
            press = None
        if keys[pygame.K_UP] or press == pygame.K_UP:
            self.dir = (0, -1)
            press = None
        elif keys[pygame.K_DOWN] or press == pygame.K_DOWN:
            self.dir = (0, 1)
            press = None
        return press

    def update(self, food, press):
        self.poses.insert(0, (self.poses[0][0]+self.dir[0], self.poses[0][1]+self.dir[1]))
        self.poses.pop(-1)
        if self.poses[0][0] < 0: self.poses[0] = (TILECOUNT-1, self.poses[0][1])
        if self.poses[0][0] >= TILECOUNT: self.poses[0] = (0, self.poses[0][1])
        if self.poses[0][1] < 0: self.poses[0] = (self.poses[0][0], TILECOUNT-1)
        if self.poses[0][1] >= TILECOUNT: self.poses[0] = (self.poses[0][0], 0)
        for pos in self.poses[1:]:
            if self.poses[0] == pos:
                self.poses = [self.ogpos]
                self.dir = (0, 0)
                press = None
        if self.poses[0] == food.pos:
            self.poses.append(self.poses[0])
            food.pos = food.randomize_pos()

        self.handle_keys(press) 
        return press

    def draw(self, win):
        for pos in self.poses:
            if pos == self.poses[0]:
                pygame.draw.rect(win, (255, 150, 0), (pos[0]*TILESIZE, pos[1]*TILESIZE, TILESIZE, TILESIZE))
            else:
                pygame.draw.rect(win, self.col, (pos[0]*TILESIZE, pos[1]*TILESIZE, TILESIZE, TILESIZE))

def draw_win(win, snake, food):
    for i in range(TILECOUNT):
        for j in range(TILECOUNT):
            if (i+j) % 2 == 0:
                pygame.draw.rect(win, (90, 141, 191), (i*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))
            else:
                pygame.draw.rect(win, (40, 94, 148), (i*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))
    snake.draw(win)
    food.draw(win)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    s = Snake((TILECOUNT//2, TILECOUNT//2), (250, 184, 17))
    f = Food((227, 82, 45))
    timer = prevtime = 0
    queuedpress = None
    run = True

    while run:
        clock.tick(FPS)

        timer += 1/FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            queuedpress = pygame.K_LEFT
        elif keys[pygame.K_RIGHT]:
            queuedpress = pygame.K_RIGHT
        if keys[pygame.K_UP]:
            queuedpress = pygame.K_UP
        elif keys[pygame.K_DOWN]:
            queuedpress = pygame.K_DOWN
        
        if timer - prevtime >= 1/GAMESPEED:
            queuedpress = s.update(f, queuedpress)
            prevtime = timer
        draw_win(WIN, s, f)
    
    pygame.quit()

main()