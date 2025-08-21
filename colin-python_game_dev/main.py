import pygame
import random

pygame.init()
frame_size_x = 800
frame_size_y = 500
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption("Spell B")
clock = pygame.time.Clock()
FPS = 60

game_active = False

## siapkan aset yang kita butuhkan
# font
title_font = pygame.font.Font("assets/fonts/jersey.ttf", 64)
word_font = pygame.font.Font("assets/fonts/jersey.ttf", 32)


# sound
correct_sound = pygame.mixer.Sound("assets/sounds/correct.mp3")
game_over_sound = pygame.mixer.Sound("assets/sounds/gameover.mp3")
game_start_sound = pygame.mixer.Sound("assets/sounds/gamestart.mp3")
key_typing_sound = pygame.mixer.Sound("assets/sounds/keytyping.wav")
menu_screen_sound = pygame.mixer.Sound("assets/sounds/menuscreen.mp3")
wrong_sound = pygame.mixer.Sound("assets/sounds/wrong.mp3")


# background sprite
background = pygame.image.load("assets/background.webp").convert()
background = pygame.transform.scale(background, (1400, 850))

bee_background = pygame.image.load("assets/Beebackground.webp").convert()
bee_background = pygame.transform.scale(bee_background, (800, 650))


## siapkan list soal
word_list = [
    "Accurate",
    "Eager",
    "Recognize",
    "Extraordinary",
    "Weary",
    "Proceed",
    "Outstanding",
    "Industrialism",
    "Sturdy",
    "Recall",
    "Graveyard",
    "Disaster",
    "disclose",
    "Demonstrate",
    "descend",
    "Understandable",
    "Paranoid",
    "Euthanized",
    "Constitutionalizing",
    "Misinterpretations",
    "Photosynthesizing",
    "Nonrepresentational",
    "Disproportionableness",
    "Inconsequentialities",
    "Lymphangioleiomyomatosis",
    "Uncontradictorily",
    "Overcapitalization",
    "Thermochromatography",
    "Magniloquent",
    "ymphangioleiomyomatosis",
    "Perspicaciousness",
    "Antitransubstantiationalist",
    "Hexakosioihexekontahexaphobia",
    "Tetrakishexahexaheptane",
    "Dichlorodifluoromethane",
    "Dimethylaminophenyltrimethylpyrazoline",
    "Pneumonoultramicroscopicsilicovolcanoconiosis",
    "Methionylthreonylthreonylglutaminylarginyl",
    "Gargoyleosaurus",
    "Podokesaurus",
    "Rhinorex",
    "Segnosaurus",
    "Triceratops",
    "Veterupristisaurus",
    "Xuanhanosaurus",
    "Dictionary",
    "Camera",
    "Hydra," 
    "Trombone",
    "Piano",
    "Inferno",
    "Quill",
    "Null",
    "Dollar",
    "Cent",
    "Castle",
    "Stock",
    "Apple",
    "Orange",
    "Banana",
    "Cryo",
    "Freezing",
    "Trail",
    "Armor",
    "Camel",
    "Hydrogent",
    "Underground",
    "War",
    "Flag",
    "Country",
    "Bread",
    "Chant",
    "Chart",
    "Lag",
    "Game",
    "Over",
    "Obvious",
    "Hard",
    "Equator",
    "Gas",
    "Fate",
    "Plate",
    "Blame",
    "Train",
    "Counter",
    "Goal",
    "Dog",
    "Cat",
    "Dry",
    "Devious",
    "Polish",
    "Class",
    "Worn",
    "Horn",
    "Vector",
    "Velocity",
    "Same",
    "Soon",
    "Lame",
    "Heaven",
    "Beta",
]


#### siapkan fungsi fungsi yang dibutuhkan
### inactive_screen
def inactive_screen():
    # tampilkan background ke window_screen
    window_screen.blit(background, (-300, -125))

    # buat text "Spell Bee" warna hitam
    game_name_surface = title_font.render("Spell     Bee", True, (0, 0, 0))
    # buat rect untuk text
    game_name_rect = game_name_surface.get_rect()
    # atur posisi rect supaya berada di tengah atas
    game_name_rect.midtop = (frame_size_x / 2, -7)
    # tampilkan text di window_screen
    window_screen.blit(game_name_surface, game_name_rect)

    # buat text "Press Space to Play" warna merah
    play_text = title_font.render("Press Space to Play", True, (255, 0, 0))
    # buat rect untuk text
    play_rect = play_text.get_rect()
    # atur posisi rect supaya berada di tengah bawah
    play_rect.midbottom = (frame_size_x / 2, frame_size_y - 20)
    # tampilkan text di window_screen
    window_screen.blit(play_text, play_rect)


### active_screen
def active_screen():
    # tampilkan warna hitam sebagai background
    window_screen.fill((0, 0, 0))
    window_screen.blit(bee_background, (-0, -20))

    show_words()
    show_score()
    show_timer()


### get_random_word
# pilih random word dari list soal yang ada
def get_random_word():
    global word_list
    if len(word_list) > 0:
        return random.choice(word_list)
    else:
        return None


### show_words
# putih kalau belum di-type
# hijau kalau benar di-type
def show_words():
    global word, current_word
    word_position = (frame_size_x / 2, frame_size_y / 2 - 50)

    # buat tiga bagian: yang sudah benar (hijau), yang belum diketik (putih)
    typed_part = current_word  # bagian yang sudah diketik (hijau)
    remaining_part = word[len(current_word) :]  # bagian yang belum diketik (putih)

    # render bagian yang sudah diketik (hijau)
    if typed_part:
        typed_surface = word_font.render(typed_part, True, (0, 255, 0))
    else:
        typed_surface = word_font.render("", True, (0, 255, 0))

    # render bagian yang belum diketik (putih)
    remaining_surface = word_font.render(remaining_part, True, (255, 255, 255))

    # hitung total lebar dari seluruh kata
    total_surface = word_font.render(word, True, (255, 255, 255))
    total_width = total_surface.get_width()

    # hitung posisi mulai agar centered
    start_x = word_position[0] - total_width // 2

    # tampilkan bagian yang sudah diketik (hijau)
    if typed_part:
        typed_rect = typed_surface.get_rect()
        typed_rect.topleft = (start_x, word_position[1])
        window_screen.blit(typed_surface, typed_rect)
        # update posisi untuk bagian selanjutnya
        start_x += typed_surface.get_width()

    # tampilkan bagian yang belum diketik (putih)
    if remaining_part:
        remaining_rect = remaining_surface.get_rect()
        remaining_rect.topleft = (start_x, word_position[1])
        window_screen.blit(remaining_surface, remaining_rect)


### show_score
# score ditampilkan di pojok kiri atas
# high_score ditampilkan di bawah score
def show_score():
    global score, high_score
    # render score
    score_surface = word_font.render(f"Score: {score}", True, (255, 255, 255))
    # buat rect untuk score
    score_rect = score_surface.get_rect()
    # atur posisi rect supaya berada di pojok kiri atas
    score_rect.topleft = (10, 10)
    # tampilkan score di window_screen
    window_screen.blit(score_surface, score_rect)

    # render high_score
    high_score_surface = word_font.render(
        f"High Score: {high_score}", True, (255, 255, 255)
    )
    # buat rect untuk high_score
    high_score_rect = high_score_surface.get_rect()
    # atur posisi rect supaya berada di bawah score
    high_score_rect.topleft = (10, 40)
    # tampilkan high_score di window_screen
    window_screen.blit(high_score_surface, high_score_rect)


### show_timer
# timer ditampilkan di pojok kanan atas
def show_timer():
    global timer
    # render timer (2 digit)
    timer_surface = word_font.render(f"Timer: {int(timer):02}", True, (255, 255, 255))
    # buat rect untuk timer
    timer_rect = timer_surface.get_rect()
    # atur posisi rect supaya berada di pojok kanan atas
    timer_rect.topright = (frame_size_x - 10, 10)
    # tampilkan timer di window_screen
    window_screen.blit(timer_surface, timer_rect)


## variabel untuk game-nya
# score
score = 0
# high_score
high_score = 0
# timer
timer = 15  # in seconds

# question word 
word = get_random_word()
# current word
current_word = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            exit()

        # event saat game_active False
        if game_active is False and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_active = True

        # event saat game_active True
        if game_active is True and event.type == pygame.KEYDOWN:
            # deteksi semua input dari keyboard, tapi hanya yang huruf abjad
            print(event.key)

            # kalau huruf yang ditekan adalah huruf abjad
            if pygame.K_a <= event.key <= pygame.K_z:
                key_typing_sound.play()

                # ubah pygame key ke karakter
                # misalnya pygame.K_a menjadi 'a'
                pressed_char = chr(event.key)
                expected_char = word[len(current_word)].lower()

                if pressed_char == expected_char:
                    # jika huruf yang ditekan sesuai dengan huruf di word
                    current_word += word[len(current_word)]

                    # jika current_word sudah sama dengan word
                    if current_word == word:
                        correct_sound.play()
                        score += 1  # tambah score 1
                        timer += 3  # tambah timer 5 detik
                        # cek apakah score lebih besar dari high_score
                        if score > high_score:
                            high_score = score
                        # reset current_word
                        current_word = ""
                        # ambil word baru
                        word = get_random_word()
                else:
                    # jika huruf yang ditekan tidak sesuai dengan huruf di word
                    wrong_sound.play()
                    # reset current_word
                    current_word = ""
                    # ambil word baru
                    word = get_random_word()

    if game_active:
        active_screen()

        # update timer
        if timer > 0:
            timer -= 1 / FPS
            if timer <= 0:
                game_active = False
                game_over_sound.play()
                # reset score and timer
                score = 0
                timer = 15

    else:
        inactive_screen()

    pygame.display.update()
    clock.tick(FPS)
