import pygame
from sys import exit
import random
#import

pygame.init()
#fps = 60


screen = pygame.display.set_mode((551, 720))
pygame.display.set_caption("Flapping Bird")

# images
bird_images = [pygame.image.load('bird_mid.png'), pygame.image.load('bird_up.png'),
               pygame.image.load('bird_down.png')]
bgImg = pygame.image.load('background.png')
groundImg = pygame.image.load('ground.png')  # it will be moving or scroling continuously
top_pipe_image = pygame.image.load('pipe_top.png')
bottom_pipe_image = pygame.image.load('pipe_bottom.png')
game_over = pygame.image.load('game_over.png')
game_start = pygame.image.load('start.png')

# game variables
scroll_speed = 1  # how fast the game runs and at speed ground img will move/scroll
bird_initial_pos = (100, 250)
Score = 0
# font
font = pygame.font.SysFont("monospace", 25)
game_stop = True


# game start menu


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_initial_pos
        self.image_index = 0  # img index to loop through the bird imgs and animates bird
        self.velo = 0
        self.jump = False
        # wil use to check bird dead or not
        self.alive = True

    def update(self, user_input):  # animate bird
        if self.alive:  # animate and flap bird only if its alive
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        # velocity with each flap
        self.velo += 0.5
        if self.velo > 8:
            self.velo = 8
        # prevent bird from falling down below ground level
        if self.rect.y < 500:
            self.rect.y += int(self.velo)
        # bird flap
        if self.velo == 0:
            self.jump = False

        # user input flap should be false and the y position of bird should be below the top of the screen
        if user_input[pygame.K_SPACE] and not self.jump and self.rect.y > 0 and self.alive:
            self.jump = True
            self.velo = -8

        # transform bird
        self.image = pygame.transform.rotate(self.image, self.velo * -5)


# ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # initialize the base class
        pygame.sprite.Sprite.__init__(self)
        self.image = groundImg  # specify img
        self.rect = self.image.get_rect()  # to manipulate positions of ground img
        self.rect.x = x  # cordinates of rect
        self.rect.y = y

    def update(self):
        self.rect.x = self.rect.x - scroll_speed  # create moving ground
        if self.rect.x <= -551:  # deleting the rect obj which moves out of screen/window
            self.kill()  # remove from group
             # delete obj

    # def __init__(self, x, y):
    # x,y cordinates at which ground will move
    # initialize the base class
    #   pygame.sprite.Sprite.__init__()
    #  self.image = groundImg  # specify img
    # self.rect = self.image.get_rect()  # to manipulate positions of ground img
    # self.rect.x = x  # cordinates of rect
    # self.rect.y = y

    # def update(self): #responsible for updation of ground pipes and bird
    #   self.rect.x = self.rect.x - scroll_speed  # create moving ground
    #  if self.rect.x <= -551:  # deleting the rect obj which moves out of screen/window
    #     self.kill()  # kill the rect obj


class Pipes(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.enter = False
        self.exit = False
        self.passed = False
        self.pipe_type = pipe_type

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -551:
            self.kill()

        # score basically setting enter exit passed variables
        global Score
        if self.pipe_type == 'bottom' or self.pipe_type == 'top':
            if bird_initial_pos[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_initial_pos[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                Score += 1

# quit game
def game_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # running = False


# game main func
def main():
    # score
    global Score
    fps = 60
    # pipe instance
    pipe_time = 0  # time interval at which pipes will spawn
    pipes = pygame.sprite.Group()
    # pipes.add(Pipes)

    # instantiate bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # instantiate initial ground/ground instance initialize
    ground_x = 0
    ground_y = 520
    ground = pygame.sprite.Group()
    ground.add(Ground(ground_x, ground_y))  # instance of ground

    #initialize clock
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)

        # call quit game
        game_quit()
        # frame
        screen.fill((0, 0, 0))
        # user input
        user_input = pygame.key.get_pressed()
        # draw bg
        screen.blit(bgImg, (0, 0))

        # to show score on scree
        score = font.render('SCORE: ' + str(Score), True, pygame.Color(255, 255, 255))
        screen.blit(score,(30,30))

        # spawn ground/add new ground instance
        if len(ground) <= 1:
            ground.add(Ground(551, ground_y))
            #print(type(ground))

        # spawn pipes
        # spawn pipes only if bird is alive
        if pipe_time <= 0 and bird.sprite.alive:
            x_pipe_top = 550
            x_pipe_bottom = 550
            y_pipe_top = random.randint(-600, -480)
            y_pipe_bottom = y_pipe_top + random.randint(90, 130) + bottom_pipe_image.get_height()

            # adding pipes images
            pipes.add(Pipes(x_pipe_top, y_pipe_top, top_pipe_image, 'top'))
            pipes.add(Pipes(x_pipe_bottom, y_pipe_bottom, bottom_pipe_image, 'bottom'))

            # pipe time
            pipe_time = random.randint(180, 250)
        pipe_time -= 1  # until it goes back to zero which is whne we re_spawn a pip at every while loop iteration w

        # draw all ground bird pipes
        # draw pipes and ground only if bird is alive
        if bird.sprite.alive:
            ground.draw(screen)
            pipes.draw(screen)
        bird.draw(screen)
        screen.blit(score, (30, 30))

        # check collisions
        collision_pipe = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False )
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipe or collision_ground:
            bird.sprite.alive = False

            # game over screen
            if collision_ground:
                screen.blit(game_over, (551 // 2 - 192 // 2, 720 // 2 - 71 // 2))
            elif collision_pipe:
                screen.blit(game_over, (551 // 2 - 192 // 2, 720 // 2 - 71 // 2))

                # restart gamne
                if user_input[pygame.K_r]:
                    Score = 0
                    main()

        #update score only if the bird is alive
        if bird.sprite.alive:
            # update of ground bird pipes
            ground.update()
            bird.update(user_input)
            pipes.update()
        #draw score after updating it
        score = font.render('SCORE: ' + str(Score), True, pygame.Color(255, 255, 255))
        screen.blit(score,(30, 30))


        pygame.display.update()


main()


# game start menu
def menu():
    global game_stop
    while game_stop:
        game_quit()

        # draw menu on screen
        screen.fill((0, 0, 0))
        screen.blit(bgImg, (0, 0))
        screen.blit(groundImg, (0, 520))
        screen.blit(bird_images[0], (100, 250))
        screen.blit(game_start, (551 // 2 - 192 // 2, 720 // 2 - 71 // 2))

        #user input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            game_stop = False
            main()


        pygame.display.update()


menu()

# running = True
# while running:
#   screen.fill((0, 0, 0))
#  screen.blit(bgImg, (0, 0))  # draw bg
# for event in pygame.event.get():
#    if event.type == pygame.QUIT:
#       running = False
