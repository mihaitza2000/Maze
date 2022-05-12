import pygame, time, threading, random
from time import sleep
from datetime import datetime
from pygame import *
from win32api import GetSystemMetrics 

width, height = 1280, 720
sign = 1

pygame.init()
screen = pygame.display.set_mode([width, height])
radius = 1

side, t = 40, 200
timeout, sec = t, t
dir = [(-1,0),(-1,-1),(-1,1),(1,0),(1,-1),(1,1),(0,1),(0,-1)]

W, G = [], []

pickaxes = pygame.image.load('./images/pickaxes.png')
pickaxes = pygame.transform.scale(pickaxes, (side, side))

dinamite = pygame.image.load('./images/dinamite.png')
dinamite = pygame.transform.scale(dinamite, (side, side))

portal = pygame.image.load('./images/portal.png')
portal = pygame.transform.scale(portal, (side, side))

hourglass = pygame.image.load('./images/hourglass.png')
hourglass = pygame.transform.scale(hourglass, (side, side))

shield = pygame.image.load('./images/shield.png')
shield = pygame.transform.scale(shield, (side, side))

ghost = pygame.image.load('./images/ghost.png')
ghost = pygame.transform.scale(ghost, (side, side))

border = pygame.image.load('./images/border.jpg')
border = pygame.transform.scale(border, (side, side))

borderClock = pygame.image.load('./images/border.jpg')
borderClock = pygame.transform.scale(borderClock, (4*side, side))

character = pygame.image.load('./images/character.jpg')
character = pygame.transform.scale(character, (side, side))

flash = pygame.image.load('./images/flash.png')
flash = pygame.transform.scale(flash, (side, side))

xTool, yTool, dark1, dark2 = 0, 0, 0, 255
listTools = [flash, pickaxes, hourglass, shield, ghost, portal, dinamite]
availableTools = []
randomTool = listTools[random.randint(0, len(listTools)-1)]
randomTool = listTools[6]
myfont = pygame.font.SysFont('Comic Sans MS', side)
activeTool, clock = -1, '0'

wall, cell, unvisited, h, w, maze, board = 'w', 'c', 'u', 17, 32, [], []

def get_board(maze):
    m = ""
    for i in range(h):
        maze[i][0] = 'w'
        maze[i][w-1] = 'w'
    for j in range(w):
        maze[0][j] = 'w'
        maze[h-1][j] = 'w'
    maze[0][1] = 'c'
    maze[h-1][w-2] = 'c'
    for i in range(h):
        for j in range(w):
            if (maze[i][j] == 'c'):
                m = m + '0'
            else:
                m = m + '1'
        if i != h-1:
            m = m + '\n'
    return m

def surroundingCells(rand_wall):
	s_cells = 0
	if (maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
		s_cells += 1
	if (maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
		s_cells += 1
	if (maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
		s_cells +=1
	if (maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
		s_cells += 1
	return s_cells

def get_maze():
    for i in range(0, h):
        line = []
        for j in range(0, w):
            line.append(unvisited)
        maze.append(line)

    starting_h = int(random.random()*h)
    starting_w = int(random.random()*w)
    if (starting_h == 0):
        starting_h += 1
    if (starting_h == h-1):
        starting_h -= 1
    if (starting_w == 0):
        starting_w += 1
    if (starting_w == w-1):
        starting_w -= 1

    maze[starting_h][starting_w] = cell
    walls = []
    walls.append([starting_h - 1, starting_w])
    walls.append([starting_h, starting_w - 1])
    walls.append([starting_h, starting_w + 1])
    walls.append([starting_h + 1, starting_w])

    maze[starting_h-1][starting_w] = 'w'
    maze[starting_h][starting_w - 1] = 'w'
    maze[starting_h][starting_w + 1] = 'w'
    maze[starting_h + 1][starting_w] = 'w'

    while (walls):
        rand_wall = walls[int(random.random()*len(walls))-1]
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1]-1] == 'u' and maze[rand_wall[0]][rand_wall[1]+1] == 'c'):
                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = 'c'
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])
                    if (rand_wall[0] != h-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[1] != 0):	
                        if (maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0]-1][rand_wall[1]] == 'u' and maze[rand_wall[0]+1][rand_wall[1]] == 'c'):
                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = 'c'
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                    if (rand_wall[1] != w-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue
        if (rand_wall[0] != h-1):
            if (maze[rand_wall[0]+1][rand_wall[1]] == 'u' and maze[rand_wall[0]-1][rand_wall[1]] == 'c'):
                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = 'c'
                    if (rand_wall[0] != h-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                    if (rand_wall[1] != w-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue
        if (rand_wall[1] != w-1):
            if (maze[rand_wall[0]][rand_wall[1]+1] == 'u' and maze[rand_wall[0]][rand_wall[1]-1] == 'c'):
                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    maze[rand_wall[0]][rand_wall[1]] = 'c'
                    if (rand_wall[1] != w-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != 'c'):
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                    if (rand_wall[0] != h-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[0] != 0):	
                        if (maze[rand_wall[0]-1][rand_wall[1]] != 'c'):
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)
                continue
        for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                walls.remove(wall)

    for i in range(0, h):
        for j in range(0, w):
            if (maze[i][j] == 'u'):
                maze[i][j] = 'w'

    for i in range(0, w):
        if (maze[1][i] == 'c'):
            maze[0][i] = 'c'
            break

    for i in range(w-1, 0, -1):
        if (maze[h-2][i] == 'c'):
            maze[h-1][i] = 'c'
            break
    return maze

def countdown():
    global t, sec, clock, dark1, dark2, sign
    now = datetime.now()
    T = now.strftime("%S")
    if int(T) % 2 == 0 and sec == t and t > 0:
        t -= 1
        if dark1 > 255 or dark1 < 0:
            sign *= -1
        dark1 += 25*sign
        #dark2 += 5*sign
    elif int(T) % 2 == 1:
        sec = t
    if sec//60 < 10:
        clock = '0' + clock
    if sec%60 < 10:
        newClock = clock[:-1] + '0' + clock[-1]
        clock = newClock
    timeDisplay = myfont.render(clock, False, (255, 0, 0))
    screen.blit(borderClock, (14*side, 0))
    screen.blit(timeDisplay, (14.7*side,-side/4))
    clock = str(sec//60) + ':' + str(sec%60)

class Character:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.g = False
        self.tool = ''
    def show(self):
        screen.blit(character,(self.x*side, self.y*side)) 
    def move(self, dirX, dirY):
        if (self.x+dirX >= 0 and self.x+dirX < width//side) and  (self.y+dirY > 0 and self.y+dirY < height//side) and (not W[self.x+dirX][self.y+dirY].choose == 1 or self.g):
            self.x += dirX
            self.y += dirY
    def test(self, G):
        global xTool, yTool, randomTool, timeout
        if (xTool == self.x and yTool == self.y) or (timeout-t) > 10:
            timeout = t
            if xTool == self.x and yTool == self.y:
                availableTools.append([randomTool, 1, 220])
            while True:
                xTool, yTool = random.randint(0,width//side-1), random.randint(0,height//side-1)
                randomTool = listTools[random.randint(0, len(listTools)-1)]
                if G[xTool][yTool].choose == 1:
                    break

class Selection:
    def __init__(self, pos):
        self.selected = False
        self.position = pos
    def show(self):
        if self.selected:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.position*side, 0, side, side),  2)
    def move(self, step):
        if (self.position > 0 and step < 0) or (self.position < len(availableTools)-1 and step > 0):
            self.position += step
            
class Wall:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.choose = 0
        self.darkness = 220
        self.wall = pygame.image.load('./images/wall.jpg')
        self.wall = pygame.transform.scale(self.wall, (side, side))
    def show(self):
        if self.y != 0:
            screen.blit(self.wall,(self.x*side, self.y*side))  
            rect = pygame.Surface((side, side))
            rect.set_alpha(self.darkness)
            rect.fill((0,0,0))
            screen.blit(rect,(self.x*side, self.y*side))

class Grass:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.choose = 0
        self.darkness = dark1
        self.grass = pygame.image.load('./images/grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (side, side))
    def show(self):
        if self.choose == 1:
            screen.blit(self.grass,(self.x*side, self.y*side)) 
            rect = pygame.Surface((side, side))
            rect.set_alpha(self.darkness)
            rect.fill((0,0,0))
            screen.blit(rect,(self.x*side, self.y*side))

def boardSelection():
    for i in range(14):
        screen.blit(border, (i*side, 0))
    for i in range(18, 32):
        screen.blit(border, (i*side, 0))

def init():
    global W, board, G, xTool, yTool
    for i in range(width//side):
        l1 = []
        l2 = []
        for j in range(height//side):
            w = Wall(i, j)
            g = Grass(i, j)
            l1.append(w)
            l2.append(g)
        W.append(l1)
        G.append(l2)
    l = []
    map = []
    
    for elem in board:
        if elem != '\n':
            l.append(elem)
        else:
            map.append(l)
            l = []
    map.append(l)
    for i in range(len(map[0])):
        for j in range(len(map)):
            if map[j][i] == '1':
                W[i][j+1].choose = 1
            else:
                G[i][j+1].choose = 1
    while True:
        xTool, yTool = random.randint(1,width//side-1), random.randint(1,height//side-1)
        if G[xTool][yTool].choose == 1:
            break
def show(c):
    global dark1, dark2, radius
    for i in range(len(availableTools)):
        if availableTools[i][1] == 1:
            screen.blit(availableTools[i][0], (i*side, 0))
    for i in range(width//side):
        for j in range(height//side):
            if abs(c.x - i) <= radius and abs(c.y - j) <= radius and c.tool == 'f':
                W[i][j].darkness = dark2
                G[i][j].darkness = dark2
            else:
                W[i][j].darkness = dark1
                G[i][j].darkness = dark1
            W[i][j].show()
            G[i][j].show()
                
def play(endGame):
    global t, activeTool, xTool, yTool, radius
    init()
    c = Character(1,1)
    s = Selection(0)
    while not endGame:
        screen.fill((0,0,0))
        boardSelection()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    endGame = True
                    break
                elif event.key == K_a or event.key == K_LEFT:
                    c.move(-1,0)
                elif event.key == K_s or event.key == K_DOWN:
                    c.move(0,1)
                elif event.key == K_d or event.key == K_RIGHT:
                    c.move(1,0)
                elif event.key == K_w or event.key == K_UP:
                    c.move(0,-1)
                elif event.key == K_u and not len(availableTools) == 0:
                    if not s.selected :
                        activeTool = 0
                        s.selected = True
                    else:
                        activeTool = -1
                        s.selected = False
                if s.selected and not len(availableTools) == 0:
                    if event.key == K_LEFT:
                        s.move(-1)
                        activeTool -= 1
                    elif event.key == K_RIGHT:
                        s.move(1)
                        activeTool += 1
                    elif event.key == K_RETURN and activeTool > -1:
                        if availableTools[activeTool][0] == listTools[0]:
                            c.tool = 'f'
                            radius += 1
                        elif availableTools[activeTool][0] == listTools[2]:
                            t += 10
                        elif availableTools[activeTool][0] == listTools[4]:
                            c.g = True
                        elif availableTools[activeTool][0] == listTools[6]:
                            for d in dir:
                                if c.x+d[0] >= 0 and c.x+d[0] <= width-1 and c.y+d[1] >= 0 and c.y+d[1] <= height-1:
                                    W[c.x+d[0]][c.y+d[1]].choose = 0
                                    W[c.x+d[0]][c.y+d[1]].wall = pygame.image.load('./images/grass.jpg')
                                    W[c.x+d[0]][c.y+d[1]].wall = pygame.transform.scale(W[c.x+d[0]][c.y+d[1]].wall, (side, side))
                        availableTools.remove(availableTools[s.position])
                        activeTool -= 1
        rect = pygame.Surface((width, height))
        show(c)
        screen.blit(randomTool, (xTool*side, yTool*side))
        rect = pygame.Surface((side, side))
        rect.set_alpha(0)
        rect.fill((0,0,0))
        screen.blit(rect,(xTool*side, yTool*side))
        
        c.show()
        c.test(G)
        
        if s.selected:
            s.show()
        countdown()
            
        pygame.display.flip() 
    pygame.quit()

if __name__ == "__main__":
    get_maze()
    board = get_board(maze)
    play(False)
    
    
    
    
    
    
    
    
    