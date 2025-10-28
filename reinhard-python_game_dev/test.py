import pygame
from random import randint

pygame.init()
frame_size_x = 800 
frame_size_y = 400 

window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))

pygame.display.set_caption("Running Game")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font("gallery/fonts/CookieRun Black.ttf", 32)
start_time = 0

game_active = False   #This variable is used to check whether the game is active or not


player_walk_1 = pygame.image.load("gallery/sprites/sprite1.png").convert_alpha()
player_walk_1= pygame.transform.scale(player_walk_1,(int(player_walk_1.get_width()*0.3,),(int(player_walk_1.get_height()*0.3) )))
player_walk_2 = pygame.image.load("gallery/sprites/sprite1.png").convert_alpha()
player_walk_2= pygame.transform.scale(player_walk_2,(int(player_walk_2.get_width()*0.3,),(int(player_walk_2.get_height()*0.3) )))
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player = player_walk[player_index]
player_jump = pygame.image.load("gallery/sprites/sprite1.png").convert_alpha()
player_jump= pygame.transform.scale(player_walk_2,(int(player_jump.get_width()*0.3,),(int(player_jump.get_height()*0.3) )))
player_rect = player.get_rect(midbottom = (80, 320))
player_gravity = 0
score = 0 
high_score = 0

jump_sound = pygame.mixer.Sound('gallery/audio/jump.mp3')
game_over_sound = pygame.mixer.Sound('gallery/audio/death.mp3')
back_sound = pygame.mixer.Sound('gallery/audio/backsound.mp3')
back_sound.set_volume(0.5)
skybox = pygame.image.load('gallery/background.webp').convert()
ground = pygame.image.load('gallery/Ground.png').convert()

enemy_frame1 = pygame.image.load("gallery/sprites/Musuh.webp").convert_alpha()
enemy_frame2 = pygame.image.load("gallery/sprites/Musuh.webp").convert_alpha()
enemy_frame1 = pygame.transform.scale(enemy_frame1,(int(enemy_frame1.get_width()*0.4,),(int(enemy_frame1.get_height()*0.4) )))
enemy_frame2 = pygame.transform.scale(enemy_frame2,(int(enemy_frame2.get_width()*0.4,),(int(enemy_frame2.get_height()*0.4) )))
enemy_frames = [enemy_frame1, enemy_frame2]
enemy_frame_index = 0
enemy = enemy_frames[enemy_frame_index]

enemy2_frame1 = pygame.image.load("gallery/sprites/Musuh2.webp").convert_alpha()
enemy2_frame2 = pygame.image.load("gallery/sprites/Musuh2.webp").convert_alpha()
enemy2_frame1 = pygame.transform.scale(enemy2_frame1,(int(enemy2_frame1.get_width()*0.2,),(int(enemy2_frame1.get_height()*0.2) )))
enemy2_frame2 = pygame.transform.scale(enemy2_frame2,(int(enemy2_frame2.get_width()*0.2,),(int(enemy2_frame2.get_height()*0.2) )))
enemy2_frames = [enemy2_frame1, enemy2_frame2]
enemy2_frame_index = 0
enemy2 = enemy2_frames[enemy2_frame_index]

obstacle_rect_list = []

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

enemy_animition_timer = pygame.USEREVENT+2
pygame.time.set_timer(enemy_animition_timer, 200)

enemy2_animition_timer = pygame.USEREVENT+ 3
pygame.time.set_timer(enemy2_animition_timer, 500)   


def display_score():
    current_time = int(pygame.time.get_ticks() / 600) - start_time
    score = font.render(f"{current_time}", False, "white")
    score_rect = score.get_rect(center = (400, 50))
    window_screen.blit(score, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 
            if obstacle_rect.bottom == 320:
                window_screen.blit(enemy, obstacle_rect)
            else:
                window_screen.blit(enemy2, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return [] 


def collision(player, obstacles):
    global high_score
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                back_sound.stop()
                game_over_sound.play()
                if score > high_score:
                    high_score = score
                return False
    return True


def spawn_enemy():
    global enemy_frame_index, enemy2_frame_index, enemy, enemy2
    if event.type == obstacle_timer:
        if randint(0 , 2):
            print('enemy has spawned')
            obstacle_rect_list.append(enemy.get_rect(bottomright = (randint(900, 1100), 320)))
        else :
            obstacle_rect_list.append(enemy2.get_rect(bottomright = (randint(900, 1100), 120)))
    if event.type == enemy_animition_timer:
        if enemy_frame_index == 0:
            enemy_frame_index == 1
        else:
            enemy_frame_index = 0
        enemy = enemy_frames[enemy_frame_index]
    if event.type == enemy2_animition_timer:
        if enemy2_frame_index == 0:
            enemy2_frame_index == 1
        else:
            enemy2_frame_index = 0
        enemy2 = enemy2_frames[enemy2_frame_index]
def player_animation():
    global player, player_index
    if player_rect.bottom < 320 :
        player = player_jump
    else :  
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player = player_walk[int(player_index)]


def active_game():
    global player_gravity, obstacle_rect_list, game_active, score
    window_screen.blit(skybox, (0,0))    #Tampilkan background
    window_screen.blit(ground, (0, 320))    #Tampilkan tanah/ground
    score = display_score()
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 320:
        player_rect.bottom = 320
    player_animation()   #Jalankan animasi pemain
    window_screen.blit(player, player_rect)   #Tampilkan pemain di layar
    obstacle_rect_list = obstacle_movement(obstacle_rect_list)
    game_active = collision(player_rect, obstacle_rect_list)

def inactive_game():
    global score, high_score
    window_screen.fill((64,64,64))  #Set background color to gray
    window_screen.blit(player, player.get_rect(midbottom = (380, 280)))
    game_name = font.render("Runner Game", False, "white")
    game_name = pygame.transform.scale2x(game_name)
    game_name_rect = game_name.get_rect(center = (400, 80))
    game_message = font.render("Press Space to start", False, "white")
    game_message_rect = game_message.get_rect(center = (400, 300))
    score_message = font.render("Your Score :  {}".format(score), False, "white")
    score_message_rect = score_message.get_rect(center = (400, 320))
    high_score_message = font.render("Your High Score :{}". format(high_score), False, "white")
    high_score_message_rect = high_score_message.get_rect(center = (400,350))
    window_screen.blit(game_name, game_name_rect)
    if score == 0:
        window_screen.blit(game_message, game_message_rect)
    else:
        window_screen.blit(score_message, score_message_rect)
        window_screen.blit(high_score_message, high_score_message_rect)
    player_animation()
    obstacle_rect_list.clear()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            spawn_enemy()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 320:
                    jump_sound.play()
                    player_gravity = -30
                if event.key == pygame.K_s and player_rect.bottom == 320:
                    jump_sound.play()
                    player_gravity = +30
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:    
                start_time = int(pygame.time.get_ticks() / 600)
                game_active = True
                back_sound.play()

    if game_active:
        # print("Game Active")
        active_game()
    else:
        #print("Game Inactive")
        inactive_game()

    pygame.display.update()
    clock.tick(FPS)
