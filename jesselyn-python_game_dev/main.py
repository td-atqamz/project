import pygame
import random

pygame.init()
pygame.font.init()
frame_size_x = 900
frame_size_y = 500
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption("Counter Attack")
clock = pygame.time.Clock()
FPS = 60
score = 0
high_score = 0

ship_width = 55  # Lebar pesawat (55 pixel)
ship_height = 40  # Tinggi pesawat (40 pixel)


player_aircraft = pygame.image.load("gallery/sprite/aircraft green.png").convert_alpha()
player_aircraft = pygame.transform.smoothscale(
    player_aircraft, (ship_width, ship_height)
)

enemy_aircraft = pygame.image.load("gallery/sprite/aircraft blue.png").convert_alpha()
enemy_aircraft = pygame.transform.smoothscale(enemy_aircraft, (ship_width, ship_height))
enemy_aircraft = pygame.transform.rotate(enemy_aircraft, 180)

active_screen_background = pygame.image.load("gallery/sprite/background.jpg").convert()
active_screen_background = pygame.transform.scale(
    active_screen_background, (frame_size_x, frame_size_y)
)

inactive_screen_background = pygame.image.load(
    "gallery/sprite/counter attack.jpg"
).convert()
inactive_screen_background = pygame.transform.scale(
    inactive_screen_background, (frame_size_x, frame_size_y)
)

bullet_fire_sound = pygame.mixer.Sound("gallery/audio/sfx_fire.wav")
bullet_hit_sound = pygame.mixer.Sound("gallery/audio/sfx_hit.wav")
game_over_sound = pygame.mixer.Sound("gallery/audio/sfx_game over.wav")


def active_screen():
    player_rect = player_aircraft.get_rect(center=(player_x, player_y))

    # tampilkan background
    window_screen.blit(active_screen_background, (0, 0))
    # tambah overlay hitam 85%
    overlay = pygame.Surface((frame_size_x, frame_size_y), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))  # RGBA
    window_screen.blit(overlay, (0, 0))

    score_font = pygame.font.Font("gallery/font/bebas.ttf", 32)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    window_screen.blit(
        score_text,
        (20, 10),
    )

    high_score_font = pygame.font.Font("gallery/font/bebas.ttf", 32)
    high_score_text = high_score_font.render(
        f"High Score: {high_score}", True, (255, 255, 255)
    )
    window_screen.blit(
        high_score_text,
        (20, 40),
    )

    # tampilkan pesawat player
    window_screen.blit(player_aircraft, player_rect.topleft)
    # tampilkan peluru
    for bullet in bullets_list:
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 5, 10)
        pygame.draw.rect(window_screen, (255, 0, 0), bullet_rect)
    # tampilkan musuh
    for enemy in enemies_list:
        enemy_rect = enemy_aircraft.get_rect(center=(enemy["x"], enemy["y"]))
        window_screen.blit(enemy_aircraft, enemy_rect.topleft)


def inactive_screen():
    window_screen.blit(inactive_screen_background, (0, 0))
    game_font = pygame.font.Font("gallery/font/bebas.ttf", 32)
    welcome_text = game_font.render("Press Any Key To Begin...", True, (219, 4, 4))
    window_screen.blit(
        welcome_text,
        (
            frame_size_x // 2 - welcome_text.get_width() // 2,
            frame_size_y // 2 - welcome_text.get_height() // 2,
        ),
    )


def spawn_enemy():
    # this function will handle enemy spwaning ligic
    if len(enemies_list) < 5:  # maksimal 5 musuh di layar
        enemy_x = random.randint(0, frame_size_x - ship_width)
        enemy_y = random.randint(-100, -40)  # spawn di atas layar
        enemies_list.append({"x": enemy_x, "y": enemy_y})


def update_enemies():
    for enemy in enemies_list:
        enemy["y"] += 2  # gerakan musuh ke bawah
        if enemy["y"] > frame_size_y:  # jika musuh keluar dari layar
            enemies_list.remove(enemy)


def spawn_bullet():
    global player_x, player_y, bullets_list
    bullet_x = player_x - 2.5
    bullet_y = player_y - 25
    bullets_list.append({"x": bullet_x, "y": bullet_y})


def update_bullet():
    global bullets_list
    for bullet in bullets_list:
        bullet["y"] -= 5  # gerakan peluru ke atas
        if bullet["y"] < 0:  # jika peluru keluar dari layar
            bullets_list.remove(bullet)  # hapus peluru yang sudah keluar


def check_collision():
    global bullets_list, enemies_list, score, high_score, player_x, player_y, game_active
    for bullet in bullets_list:
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 5, 10)
        for enemy in enemies_list:
            enemy_rect = enemy_aircraft.get_rect(center=(enemy["x"], enemy["y"]))
            if bullet_rect.colliderect(enemy_rect):
                bullets_list.remove(bullet)
                enemies_list.remove(enemy)
                bullet_hit_sound.play()
                score = score + 1
                if score >= high_score:
                    high_score = score
                break  # hentikan pengecekan setelah satu peluru mengenai musuh

    player_rect = player_aircraft.get_rect(center=(player_x, player_y))
    for enemy in enemies_list:
        enemy_rect = enemy_aircraft.get_rect(center=(enemy["x"], enemy["y"]))
        if enemy_rect.colliderect(player_rect):
            game_over_sound.play()
            game_active = False
            enemies_list.clear()
            break


game_active = False
player_x = frame_size_x // 2 - ship_width // 2
player_y = frame_size_y - ship_height - 10
fire_rate = 500
bullets_list = []
enemies_list = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            exit()

        if game_active is False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                score = 0

    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5  # move left continuosly
        if keys[pygame.K_RIGHT]:
            player_x += 5  # move right continuosly

        # keep player within screen
        player_x = max(0, min(player_x, frame_size_x))

        spawn_enemy()
        update_enemies()
        update_bullet()
        check_collision()

        if keys[pygame.K_SPACE]:
            spawn_bullet()
            pass
        active_screen()
    else:
        inactive_screen()

    pygame.display.update()
    clock.tick(FPS)
