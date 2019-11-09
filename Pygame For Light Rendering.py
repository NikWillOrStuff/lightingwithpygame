import sys, pygame
import math
from time import sleep

size = width, height = 800, 600
quality = 1

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill((0,0,0))
pygame.display.set_caption("2D shading renderer")

class colorLight:
	def __init__(self, coordinates, colors):
		self.place = (coordinates[0], coordinates[1])
		self.color = (colors[0], colors[1], colors[2])

colorLights = (colorLight((200,190), (500, 0, 1000)),colorLight((315,225), (0, 1000, 300)),colorLight((250,325), (1000, 500, 250)))

for light in colorLights:
	for shade in range(3):
		print(light.color[shade])

#loop through all pixels on screen to render image
for pixelY in range(math.floor(height/quality)):
	for pixelX in range(math.floor(width/quality)):
		#set brightness of current pixel according to distance from all lights
		color = [0,0,0]
		for light in colorLights:
			distance = math.dist((pixelX*quality,pixelY*quality),light.place)
			if distance > 1:
				for x in range(3):
					color[x] = color[x] + (light.color[x]/distance)
			else:
				for x in range(3):
					color[x] = color[x] + light.color[x]

		#cap colors at 255 before drawing
		for x in range(3):
			if color[x] > 255:
				color[x] = 255

		pygame.draw.rect(screen, color, (pixelX*quality,pixelY*quality, quality, quality))

	#once we're done with each X rows of pixels, perform updates
	x = 5
	if pixelY % x == x-1:
		pygame.display.update()
		print("Row", pixelY + 1)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
pygame.display.update()

#don't close automatically once render is complete
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	sleep(.1)
