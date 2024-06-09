import pygame, random
from random import randint

WIDTH = 800
HEIGHT = 550
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bruce")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_hp_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/player.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.hp = 100
		self.jumping = False
		self.Y_GRAVITY = 1
		self.JUMP_HEIGHT = 20
		self.Y_VELOCITY = self.JUMP_HEIGHT

	def update(self):
		self.hp += 1/24
		self.speed_x = 0
		if self.hp > 100:
			self.hp = 100
		if self.hp < 0:
			self.hp = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speed_x = -10
		if keystate[pygame.K_d]:
			self.speed_x = 10
		if keystate[pygame.K_f]:
			self.jumping = True
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

class Candy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(candy_images)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = 0

	def update(self):
		self.rect.y += self.speedy
		#self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-150, - 100)
			self.speedy = random.randrange(1, 10)

class Choco(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(choco_images)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = 0

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-150, - 100)
			self.speedy = random.randrange(1, 10)

class Snake(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("img/snake.png"),(100,50)).convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH
		self.rect.y = random.randrange(500,520)
		self.speedx = random.randrange(-5, -3)
		self.speedy = 0

	def update(self):
		self.rect.x += self.speedx
		if self.rect.right < 0:
			self.rect.x = WIDTH
			self.rect.y = random.randrange(500,520)
			self.speedx = random.randrange(-5,-3)

### high score
with open("data.txt", mode="r") as file:
	high_score = int(file.read())

def show_go_screen():
	screen.blit(background, [0,0])
	draw_text(screen, "Bruce", 65, WIDTH // 2, HEIGHT // 4)
	draw_text(screen, "Come las golosinas", 20, WIDTH // 2, HEIGHT //2)
	draw_text(screen, "high score: "+str(high_score), 30, WIDTH // 2, HEIGHT* 3//5)
	draw_text(screen, "Press Q", 20, WIDTH // 2, HEIGHT* 3//4)
	draw_text(screen, "Created by: Francisco Carvajal", 10,  60, 500)
	
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

candy_images = []
candy_list = ["img/candy1.png", "img/candy2.png", "img/candy3.png"]
for img in candy_list:
	candy_images.append(pygame.image.load(img).convert())

choco_images = []
choco_list = ["img/choco.png", "img/choco2.png","img/choco4.png"]
for img in choco_list:
	choco_images.append(pygame.image.load(img).convert())

def show_game_over_screen():
	screen.blit(background, [0,0])
	if high_score < score:
		draw_text(screen, "¡high score!", 60, WIDTH  // 2, HEIGHT * 1/4)
		draw_text(screen, "score: "+str(score), 30, WIDTH // 2, HEIGHT // 2)
		draw_text(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 4/5)
	else:
		draw_text(screen, "score: "+str(score), 60, WIDTH // 2, HEIGHT * 1/3)
		draw_text(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 2/3)

	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

# Cargar imagen de fondo
background = pygame.transform.scale(pygame.image.load("img/fond.png").convert(),(800,550))

game_over = False
running = True
start = True
while running:
	if game_over:
		show_game_over_screen()
		if score > high_score:
			high_score = score
			with open("data.txt", mode="w") as file:
				file.write(str(high_score))
		game_over = False
		all_sprites = pygame.sprite.Group()
		candy_list = pygame.sprite.Group()
		choco_list = pygame.sprite.Group()
		snake_list = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		for i in range(8):
			candy = Candy()
			all_sprites.add(candy)
			candy_list.add(candy)
			
		for i in range(4):
			choco = Choco()
			all_sprites.add(choco)
			choco_list.add(choco)

		snake = Snake()
		all_sprites.add(snake)
		snake_list.add(snake)
			
		score = 0

	if start:
		show_go_screen()
		start = False
		all_sprites = pygame.sprite.Group()
		candy_list = pygame.sprite.Group()
		choco_list = pygame.sprite.Group()
		snake_list = pygame.sprite.Group()
		player = Player()
		all_sprites.add(player)
		for i in range(8):
			candy = Candy()
			all_sprites.add(candy)
			candy_list.add(candy)
			
		for i in range(4):
			choco = Choco()
			all_sprites.add(choco)
			choco_list.add(choco)

		snake = Snake()
		all_sprites.add(snake)
		snake_list.add(snake)
			
		score = 0

	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
			sys.exit()

	if player.jumping:
		player.rect.bottom -= player.Y_VELOCITY
		player.Y_VELOCITY -= player.Y_GRAVITY
		if player.Y_VELOCITY < - player.JUMP_HEIGHT:
			player.jumping = False
			player.Y_VELOCITY = player.JUMP_HEIGHT
		
	all_sprites.update()

	if player.hp == 0:
		game_over = True
	
	if candy.rect.top > HEIGHT:
		score -= 10
	if choco.rect.top > HEIGHT:
		score -= 100

	#colisiones - candy - player
	hits = pygame.sprite.spritecollide(player, candy_list, True)
	for hit in hits:
		player.hp += 1
		score += 10
		candy = Candy()
		all_sprites.add(candy)
		candy_list.add(candy)

	#colisiones - choco - player
	hits2 = pygame.sprite.spritecollide(player, choco_list, True )
	for hit in hits2:
		player.hp += 2
		score += 100
		choco = Choco()
		all_sprites.add(choco)
		choco_list.add(choco)
	
	#colisiones - snake - player
	hits2 = pygame.sprite.spritecollide(player, snake_list, True )
	for hit in hits2:
		player.hp -= randint(10,30)
		snake = Snake()
		all_sprites.add(snake)
		snake_list.add(snake)

	screen.blit(background, [0, 0])

	all_sprites.draw(screen)

	#Marcador
	draw_text(screen, str(score), 25, WIDTH // 2, 10)
	draw_text(screen, str(high_score), 25, WIDTH*8//10, 10)

	# Escudo.
	draw_hp_bar(screen, 5, 5, player.hp)
	draw_hp_bar(screen, player.rect.x, player.rect.y - 10, player.hp)

	pygame.display.flip()