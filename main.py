import pygame
import ver

WHITE = (255, 255, 255)

SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE)

commits = ver.getCommits()

c = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Drawing
    screen.fill(WHITE)
    for i in range(len(commits)):
        r = 15
        if pygame.Rect(0, i * 50, 50, 50).collidepoint(pygame.mouse.get_pos()): r = 20
        pygame.draw.circle(screen, (0, 0, 0), (25, (i * 50) + 25), r)
        for n in commits[i].getNextCommits():
            pygame.draw.line(screen, (0, 0, 0), (25, (i * 50) + 25), (25, (n.index * 50) + 25), 5)
    pygame.display.flip()
    c.tick(60)