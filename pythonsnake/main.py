import pygame
import random

def drawblock(color:str, location:tuple[int, int]):
    rect = pygame.Rect(location[0] + blockmargin, location[1] + blockmargin, blocksize - blockmargin,
                       blocksize - blockmargin)
    pygame.draw.rect(screen, color, rect)

pygame.init()
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True
display = pygame.display

pygame.font.init()

blocksize = 40
blockmargin = 2

snake = [[400, 400], [360, 400], [320,400]]

locatieXY = [0,0]
direction = [0,0]
lastdirection = [0,0]
speed = 5
gameover = False
snakecolor = "blue"

lastMs = 0
apple:tuple[int, int] = (-1, -1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                direction = direction if lastdirection[0] == 1 else [-1, 0]
            if event.key == pygame.K_d:
                direction = direction if lastdirection[0] == -1 else [1, 0]
            if event.key == pygame.K_w:
                direction = direction if lastdirection[1] == 1 else [0, -1]
            if event.key == pygame.K_s:
                direction = direction if lastdirection[1] == -1 else [0, 1]

    screen.fill("purple")

    passedMs = pygame.time.get_ticks() % (1000 / speed)

    if not gameover:
        while apple == (-1, -1):
            x = random.randint(0, int(screenWidth / blocksize) - 1) * blocksize
            y = random.randint(0, int(screenHeight / blocksize) - 1) * blocksize

            for block in snake:
                if block[0] == x or block[1] == y:
                    break

            apple = (x, y)

        if apple[0] == snake[0][0] and apple[1] == snake[0][1]:
            snake.append(list(apple))
            apple = (-1, -1)
            speed += 0.1

        if passedMs < lastMs and direction != [0,0]:
            frontBlock = [0,0]
            frontBlock[0] = snake[0][0] + direction[0] * blocksize
            frontBlock[1] = snake[0][1] + direction[1] * blocksize

            if frontBlock[0] >= screenWidth:
                frontBlock[0] = 0

            if frontBlock[0] < 0:
                frontBlock[0] = screenWidth - blocksize

            if frontBlock[1] >= screenHeight:
                frontBlock[1] = 0

            if frontBlock[1] < 0:
                frontBlock[1] = screenHeight - blocksize

            snakenotail = snake[:-1]

            for block in snakenotail:
                if frontBlock == block:
                    gameover = True

            if not gameover:
                snake = [frontBlock] + snakenotail
                lastdirection = direction

        for block in snake:
            drawblock("blue", block)
            drawblock("red", apple)

    if gameover:
        color = "blue" if snakecolor == "darkgreen" else "darkgreen"
        for block in snake:
            drawblock(color, block)
        snakecolor = color

        my_font = pygame.font.SysFont('Comic Sans MS', 60)
        gameover = my_font.render("Game Over", False, (255, 255, 255))
        highscore = my_font.render("Je score = " + str(int(speed * len(snake))), False, (255, 255, 255))

        screen.blit(gameover, (screenWidth / 2 - gameover.get_size()[0] / 2, screenHeight / 2 - gameover.get_size()[1]))
        screen.blit(highscore, (screenWidth / 2 - highscore.get_size()[0] / 2, screenHeight / 2 + gameover.get_size()[1] / 2))

    display.flip()
    #clock.tick(60)

    lastMs = passedMs

pygame.quit()

