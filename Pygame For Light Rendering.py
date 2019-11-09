import sys, pygame
import math
from time import sleep

size = width, height = 600, 400
quality = 1
lightTravel = 12

pygame.init()
screen = pygame.display.set_mode(size)
screen.fill((0,0,0))
pygame.display.set_caption("2D shading renderer")

class colorLight:
	def __init__(self, coordinates, colors):
		self.place = (coordinates[0], coordinates[1])
		self.color = (colors[0], colors[1], colors[2])

colorLights = (colorLight((200,190), (256, 24, 512)),colorLight((315,225), (24, 512, 154)),colorLight((250,325), (512, 256, 128)))
walls = {1:(300,200,300,250),2:(300,200,400,200),3:(215,310,275,310), 4:(500,200,500,250),5:(100,200,100,250)}

for light in colorLights:
	for shade in range(3):
		print(light.color[shade])

def ccw(A,B,C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

#loop through all pixels on screen to render image
for pixelY in range(math.floor(height/quality)):
	for pixelX in range(math.floor(width/quality)):
		#set brightness of current pixel according to distance from all lights
		color = [0,0,0]
		for light in colorLights:

			lineofsight = True
			for wall in walls:
				if intersect((walls[wall][0], walls[wall][1]) , (walls[wall][2], walls[wall][3]), (light.place[0], light.place[1]), (pixelX*quality,pixelY*quality)) == True:
					lineofsight = False					

			if lineofsight:
				distance = math.dist((pixelX*quality,pixelY*quality),light.place)
				distance = distance / lightTravel
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
		
		for x in walls:
			pygame.draw.line(screen,(255,255,255),(walls[x][0],walls[x][1]),(walls[x][2],walls[x][3]))
		pygame.display.update()
		print("Row", pixelY + 1)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

print("done!")
pygame.display.update()

#don't close automatically once render is complete
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	sleep(.1)
