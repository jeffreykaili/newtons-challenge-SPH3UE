import pygame 
import sys
import os 

''' 
Esc to exit the simluation at any time
P to drop ball and start the simulation 
Space to hit the ball with the putt 
Use the arrows beside the ball to change the mass of the ball 
Use the arrows beside the putt to change the force that it hits the ball
None of the values in this simluation are mathematically accurate, but do correctly demonstrate the concept of Newton's Three Laws of Motion
''' 

class Ball: 
	def __init__(self): 
		self.x = 1920//3
		self.y = 1080//2 
		self.xvelocity = 9
		self.gravity = 10
		self.size = 60
		self.original_image = pygame.image.load(os.path.join("ball.png")).convert_alpha()
		self.image = self.original_image

	def rect(self):
		ballRect = self.image.get_rect()
		ballRect.topleft = (self.x, self.y)
		return ballRect

	def forces(self, floor, putt=[]): 
		self.y += self.gravity 
		# normal force
		if(self.rect().colliderect(floor.rect())):
			self.y -= floor.normal

	def move(self, floor):
		self.x += self.xvelocity
		if(self.xvelocity >= 0.05): self.xvelocity -= floor.friction
		elif(self.xvelocity<=0.001 or abs(0.05-self.xvelocity)<=0.001): self.xvelocity = 0 

	def adjust(self, mass_level):
		mass = [0, 30, 60, 90]
		if(self.size != mass[mass_level]):
			self.size = mass[mass_level]
			self.image = pygame.transform.scale(self.original_image, (self.size, self.size))

class Floor: 
	def __init__(self):
		self.x = 0 
		self.y = 1080 - 207 
		self.normal = 10 
		self.friction = 0.05 
		self.image = pygame.image.load(os.path.join("floor.png")).convert_alpha()

	def rect(self): 
		floorRect = self.image.get_rect()
		floorRect.topleft = (self.x, self.y)
		return floorRect

class Putt: 
	def __init__(self, ball):
		self.x = ball.x - 45 
		self.y = 1080 - 360 - 210 
		self.original_image = pygame.image.load(os.path.join("putt.png")).convert_alpha()
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.midtop = (self.x, self.y)
		self.angle = 360

	def hit(self, c): 
		self.image = pygame.transform.rotate(self.original_image, self.angle)  
		if(c): self.angle = ((self.angle - 2)+360)%360
		else: self.angle = (self.angle + 4)%360
		x, y = self.rect.midtop 
		self.rect = self.image.get_rect()
		self.rect.midtop = (x, y)

pygame.init() 
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 120
force_level = 1 
mass_level = 2
continue_simulating = True 
recording = False

force_bar = [0]
for i in range(1,6): force_bar.append(pygame.image.load(os.path.join(str(i)+".png")).convert_alpha())
sizes = [0, (20, 50), (35, 30), (50, 30)]
game_floor = Floor()
game_ball = Ball()
floor_rect = game_floor.rect() 
game_putt = Putt(game_ball) 
hit_ball_1 = False 
hit_ball_2 = False 
ball_move = False

background = pygame.image.load(os.path.join("background.png")).convert_alpha()
plus_force = pygame.image.load(os.path.join("pforce.png")).convert_alpha()
minus_force = pygame.image.load(os.path.join("nforce.png")).convert_alpha()
plus_mass = pygame.image.load(os.path.join("pmass.png")).convert_alpha()
minus_mass = pygame.image.load(os.path.join("nmass.png")).convert_alpha()
plus_force_rect, minus_force_rect, plus_mass_rect, minus_mass_rect = plus_force.get_rect(), minus_force.get_rect(), plus_mass.get_rect(), minus_mass.get_rect() 
plus_force_rect.topleft = (game_putt.x - 120, game_putt.y + 20)
minus_force_rect.topleft = (game_putt.x - 120, game_putt.y + 160)
plus_mass_rect.topleft = (game_ball.x + game_ball.size, game_ball.y - 35)
minus_mass_rect.topleft = (game_ball.x + game_ball.size, game_ball.y + 30)

while continue_simulating:
	pygame.time.Clock().tick(FPS)

	for event in pygame.event.get(): 
		if(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_ESCAPE): 
				continue_simulating = False 
			if(event.key == pygame.K_SPACE and recording):
				if(not hit_ball_1 and not hit_ball_2): 
					game_ball.xvelocity = [0, 6, 7.5, 9, 10.5, 12][force_level]
					game_ball.xvelocity *= [0, 1.5, 1, 0.5][mass_level]
				hit_ball_1 = True 
			if(event.key == pygame.K_p):
				recording = True

		if event.type == pygame.MOUSEBUTTONUP:
			mpos = pygame.mouse.get_pos()
			if(plus_force_rect.collidepoint(mpos)):
				force_level = min(force_level + 1, 5)
			if(minus_force_rect.collidepoint(mpos)):
				force_level = max(force_level - 1, 1)
			if(plus_mass_rect.collidepoint(mpos)):
				mass_level = min(mass_level + 1, 3)
				game_ball.adjust(mass_level)
				plus_mass_rect.topleft = (game_ball.x + game_ball.size, game_ball.y - sizes[mass_level][1])
				minus_mass_rect.topleft = (game_ball.x + game_ball.size, game_ball.y + sizes[mass_level][0])
			if(minus_mass_rect.collidepoint(mpos)):
				mass_level = max(mass_level - 1, 1)
				game_ball.adjust(mass_level)
				plus_mass_rect.topleft = (game_ball.x + game_ball.size, game_ball.y - sizes[mass_level][1])
				minus_mass_rect.topleft = (game_ball.x + game_ball.size, game_ball.y + sizes[mass_level][0])

	# update forces check 
	if(recording): 
		game_ball.forces(game_floor)
	if(hit_ball_1):
		angles = [280, 296, 312, 328, 344, 0][::-1]
		if(game_putt.angle>angles[force_level]): # the range is from 360 --> 280
			game_putt.hit(1)
		else: 
			hit_ball_2 = True
			hit_ball_1 = False
	if(hit_ball_2): 
		if(game_putt.angle!=4):
			game_putt.hit(0)
		else: 
			# hit_ball_2 = False
			ball_move = True 
			game_putt.angle = 360
	if(ball_move): game_ball.move(game_floor) 

	screen.blit(background, (0, 0))
	screen.blit(game_floor.image, (game_floor.x, game_floor.y))
	screen.blit(game_ball.image, (game_ball.x, game_ball.y))
	screen.blit(game_putt.image, game_putt.rect)
	if(not recording):
		screen.blit(plus_mass, (game_ball.x + game_ball.size, game_ball.y - sizes[mass_level][1]))
		screen.blit(minus_mass, (game_ball.x + game_ball.size, game_ball.y + sizes[mass_level][0]))
	if(not hit_ball_1 and not hit_ball_2):
		screen.blit(plus_force, (game_putt.x - 120, game_putt.y + 20))
		screen.blit(minus_force, (game_putt.x - 120, game_putt.y + 160))
		screen.blit(force_bar[force_level], (game_putt.x - 220, game_putt.y + 35))
	pygame.display.update()