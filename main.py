import pygame
import ver

pygame.font.init()

WHITE = (255, 255, 255)

SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE)
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 20)

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	# Drawing
	ver.updateFiles()
	commits = ver.getCommits()
	screen.fill(WHITE)
	for i in range(len(commits)):
		r = 15
		if pygame.Rect(0, i * 50, 50, 50).collidepoint(pygame.mouse.get_pos()):
			# Hovered
			r = 20
			rendered = FONT.render(commits[i].name, True, (0, 0, 0))
			screen.blit(rendered, (50, ((i + 1) * 50) - ((rendered.get_height() / 2) + 25)))
			if pygame.mouse.get_pressed()[0]:
				commits[i].apply()
		color = (0, 0, 0)
		if commits[i].type == "working": color = (255, 160, 0)
		pygame.draw.circle(screen, color, (25, (i * 50) + 25), r)
		if commits[i].index == ver.getCurrentCommit().index:
			pygame.draw.circle(screen, (0, 255, 0), (25, (i * 50) + 25), r, 2)
		for n in commits[i].getNextCommits():
			pygame.draw.line(screen, (0, 0, 0), (25, (i * 50) + 25), (25, (n.index * 50) + 25), 5)
	pygame.display.flip()
	c.tick(10)