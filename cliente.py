import pygame
from network import Network

width = 700
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

clientNumber = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 4

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

def read_pos(tup):
    return tup[0], tup[1]

def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])

def check_collision(player1, player2):
    return player1.rect.colliderect(player2.rect)

def handle_collision(player1, player2):
    overlap_x = player1.rect.colliderect(player2.rect.move((player1.x - player2.x, 0)))
    overlap_y = player1.rect.colliderect(player2.rect.move((0, player1.y - player2.y)))

    if overlap_x < overlap_y:
        if player1.x < player2.x:
            player1.x -= overlap_x
            player2.x += overlap_x
        else:
            player1.x += overlap_x
            player2.x -= overlap_x
    else:
        if player1.y < player2.y:
            player1.y -= overlap_y
            player2.y += overlap_y
        else:
            player1.y += overlap_y
            player2.y -= overlap_y

def is_outside_screen(player, width, height):
    return player.x < 0 or player.y < 0 or player.x + player.width > width or player.y + player.height > height

def redrawWindow(win, player, player2):
    win.fill((0, 0, 0))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    startPos = n.getPos()
    p = Player(width // 2 - 50, height // 2 - 50, 100, 100, (0, 255, 0))  # Posicionando no centro
    p2 = Player(width // 2 - 50, height // 2 - 50, 100, 100, (255, 0, 0))  # Posicionando no centro
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send((p.x, p.y)))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()

        if check_collision(p, p2):
            handle_collision(p, p2)

        if is_outside_screen(p, width, height):
            print("Player 2 wins!")
            run = False

        if is_outside_screen(p2, width, height):
            print("Player 1 wins!")
            run = False

        redrawWindow(win, p, p2)

main()
