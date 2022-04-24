import pygame
import ver

pygame.font.init()

WHITE = (255, 255, 255)

SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 20)
offset = [25, 25]

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.VIDEORESIZE:
			SCREENSIZE = event.size
			screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
		elif event.type == pygame.MOUSEMOTION:
			if event.buttons[0]:
				offset[0] += event.rel[0]
				offset[1] += event.rel[1]
	# Drawing
	ver.updateFiles()
	commits = ver.getCommits()
	screen.fill(WHITE)
	for i in range(len(commits)):
		# Setup
		pos = commits[i].getPosition(offset)
		hovered = pygame.Rect(pos[0] - 25, pos[1] - 25, 50, 50).collidepoint(pygame.mouse.get_pos())
		# Draw the circle
		color = (255, 160, 0) if commits[i].type == "working" else (0, 0, 0) 
		pygame.draw.circle(screen, color, pos, (20 if hovered else 15))
		# Draw the green outline
		if commits[i].index == ver.getCurrentCommit().index:
			pygame.draw.circle(screen, (0, 255, 0), pos, (20 if hovered else 15), 2)
		# Draw the lines to the next commits
		for n in commits[i].getNextCommits():
			pygame.draw.line(screen, (0, 0, 0), pos, n.getPosition(offset), 5)
	# Hover effects
	for i in commits:
		pos = i.getPosition(offset)
		if pygame.Rect(pos[0] - 25, pos[1] - 25, 50, 50).collidepoint(pygame.mouse.get_pos()):
			rendered = FONT.render(i.name, True, (0, 0, 0))
			renderedSolid = pygame.Surface(rendered.get_size())
			renderedSolid.fill((255, 255, 255))
			renderedSolid.blit(rendered, (0, 0))
			screen.blit(renderedSolid, (pos[0] + 25, pos[1] - (rendered.get_height() / 2)))
			if pygame.mouse.get_pressed()[0]:
				i.apply()
	pygame.display.flip()
	c.tick(10)