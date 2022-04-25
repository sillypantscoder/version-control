import pygame
import ver
import time

pygame.font.init()

WHITE = (255, 255, 255)

SCREENSIZE = [500, 500]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 20)
offset = [25, 25]

def MAIN():
	global screen
	global SCREENSIZE
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
					MENU(i.index)
		# Update button
		rendered = FONT.render("Update", True, (255, 255, 255))
		updaterect = pygame.Rect(0, SCREENSIZE[1] - rendered.get_height(), rendered.get_width(), rendered.get_height())
		if updaterect.collidepoint(pygame.mouse.get_pos()):
			renderedSolid = pygame.Surface(rendered.get_size())
			renderedSolid.fill((0, 255, 255))
			renderedSolid.blit(rendered, (0, 0))
			screen.blit(renderedSolid, updaterect.topleft)
			if pygame.mouse.get_pressed()[0]:
				ver.update()
		else:
			renderedSolid = pygame.Surface(rendered.get_size())
			renderedSolid.fill((0, 0, 255))
			renderedSolid.blit(rendered, (0, 0))
			screen.blit(renderedSolid, updaterect.topleft)
		# Send changes button
		rendered = FONT.render("Send changes", True, (255, 255, 255))
		updaterect = pygame.Rect(SCREENSIZE[0] - rendered.get_width(), SCREENSIZE[1] - rendered.get_height(), rendered.get_width(), rendered.get_height())
		if updaterect.collidepoint(pygame.mouse.get_pos()):
			renderedSolid = pygame.Surface(rendered.get_size())
			renderedSolid.fill((0, 255, 255))
			renderedSolid.blit(rendered, (0, 0))
			screen.blit(renderedSolid, updaterect.topleft)
			if pygame.mouse.get_pressed()[0]:
				ver.send()
		else:
			renderedSolid = pygame.Surface(rendered.get_size())
			renderedSolid.fill((0, 0, 255))
			renderedSolid.blit(rendered, (0, 0))
			screen.blit(renderedSolid, updaterect.topleft)
		pygame.display.flip()
		c.tick(10)

def MENU(index: int):
	global screen
	global SCREENSIZE
	commits = ver.getCommits()
	commitpos = ver.getCommits()[index].getPosition(offset)
	dialogrect = pygame.Rect(commitpos[0] - 25, commitpos[1] - 25, 60 + FONT.render(commits[index].name, True, (0, 0, 0)).get_width(), 50)
	c = pygame.time.Clock()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.VIDEORESIZE:
				SCREENSIZE = event.size
				screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
			elif event.type == pygame.MOUSEBUTTONUP:
				if dialogrect.collidepoint(pygame.mouse.get_pos()):
					pass
				else:
					return
		# Drawing
		commits = ver.getCommits()
		screen.fill(WHITE)
		for i in range(len(commits)):
			# Setup
			pos = commits[i].getPosition(offset)
			if commits[i].index == index: pygame.draw.rect(screen, (0, 0, 0), dialogrect, 1)
			# Draw the circle
			color = (255, 160, 0) if commits[i].type == "working" else (0, 0, 0) 
			pygame.draw.circle(screen, color, pos, (20 if index == i else 15))
			# Draw the green outline
			if commits[i].index == ver.getCurrentCommit().index:
				pygame.draw.circle(screen, (0, 255, 0), pos, (20 if index == i else 15), 2)
			# Draw the lines to the next commits
			for n in commits[i].getNextCommits():
				pygame.draw.line(screen, (0, 0, 0), pos, n.getPosition(offset), 5)
		# Hover effects
		for i in commits:
			pos = i.getPosition(offset)
			if index == i.index:
				# Draw the name
				rendered = FONT.render(i.name, True, (0, 0, 0))
				renderedSolid = pygame.Surface(rendered.get_size())
				renderedSolid.fill((255, 255, 255))
				renderedSolid.blit(rendered, (0, 0))
				screen.blit(renderedSolid, (pos[0] + 25, pos[1] - (rendered.get_height() / 2)))
				# Draw the buttons
				if i.type == "working":
					# Commit button
					rendered = FONT.render("Commit", True, (0, 0, 0))
					renderedSolid = pygame.Surface(rendered.get_size())
					renderedSolid.fill((0, 255, 0))
					renderedSolid.blit(rendered, (0, 0))
					pos = (dialogrect.right - rendered.get_width(), dialogrect.bottom - rendered.get_height())
					screen.blit(renderedSolid, pos)
					textrect = pygame.Rect(*pos, *rendered.get_size())
					if textrect.collidepoint(pygame.mouse.get_pos()):
						if pygame.mouse.get_pressed()[0]:
							ver.commit(i.index)
							screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
							#return
				# Revert button
				if len(ver.Commit(i.index).getNextCommits()) == 0:
					rendered = FONT.render("Revert", True, (255, 255, 255))
					renderedSolid = pygame.Surface(rendered.get_size())
					renderedSolid.fill((255, 0, 0))
					renderedSolid.blit(rendered, (0, 0))
					pos = (dialogrect.left, dialogrect.bottom - rendered.get_height())
					screen.blit(renderedSolid, pos)
					textrect = pygame.Rect(*pos, *rendered.get_size())
					if textrect.collidepoint(pygame.mouse.get_pos()):
						if pygame.mouse.get_pressed()[0]:
							ver.revert(i.index)
							screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
							time.sleep(0.5)
							#return
				# Go button
				rendered = FONT.render("Go here", True, (255, 255, 255))
				renderedSolid = pygame.Surface(rendered.get_size())
				renderedSolid.fill((0, 0, 255))
				renderedSolid.blit(rendered, (0, 0))
				pos = (dialogrect.right - rendered.get_width(), dialogrect.top)
				screen.blit(renderedSolid, pos)
				textrect = pygame.Rect(*pos, *rendered.get_size())
				if textrect.collidepoint(pygame.mouse.get_pos()):
					if pygame.mouse.get_pressed()[0]:
						i.apply()
						return
		pygame.display.flip()
		c.tick(10)

MAIN()