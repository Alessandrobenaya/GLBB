import pygame

pygame.init()

# Lebar dan tinggi layar
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Warna RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Judul layar
pygame.display.set_caption("Simulasi Gerak Lurus Berubah Beraturan")

# Inisialisasi posisi, kecepatan, dan percepatan bola
x = 25
v = 0
a = 0

# Inisialisasi waktu
t = 0
delta_t = 0.01

# Ukuran dan posisi bola
BALL_RADIUS = 20
ball_pos = (x, SCREEN_HEIGHT // 2)

# Font teks
font = pygame.font.Font(None, 36)

# Input box
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 100, 50)
input_text = ""

reset_button = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 100, 50)

# Loop program
running = True
while running:
    # Loop event pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Input teks
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    a = float(input_text)
                except ValueError:
                    pass
                input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if reset_button.collidepoint(event.pos):
                x = 25
                v = 0
                a = 0
                t = 0
                ball_pos = (x, SCREEN_HEIGHT // 2)
    

    # Menggambar latar belakang dengan warna putih
    screen.fill(WHITE)

    # Menggambar bola dengan warna merah
    pygame.draw.circle(screen, RED, ball_pos, BALL_RADIUS)

    # Memperbarui posisi bola dan waktu
    x = x + v * delta_t + 0.5 * a * delta_t ** 2
    v = v + a * delta_t
    ball_pos = (int(x), SCREEN_HEIGHT // 2)

    # Jika bola mencapai batas layar, balik arah
    if ball_pos[0] + BALL_RADIUS >= SCREEN_WIDTH or ball_pos[0] - BALL_RADIUS <= 0:
        v = -v

    # Menampilkan waktu pada layar
    time_text = font.render("Waktu: {:.2f} s".format(t), True, BLACK)
    screen.blit(time_text, (10, 10))

    # Menampilkan kecepatan pada layar
    speed_text = font.render("Kecepatan: {:.2f} m/s".format(v), True, BLACK)
    screen.blit(speed_text, (10, 50))

    # Menampilkan input percepatan pada layar
    input_text_surface = font.render(input_text, True, BLACK)
    screen.blit(input_text_surface, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 40))
    input_box.w = max(100, input_text_surface.get_width() + 10)
    pygame.draw.rect(screen, BLACK, input_box, 2)

    # Menampilkan Input Reset
    reset_text = font.render("Reset", True, BLACK)
    pygame.draw.rect(screen, BLACK, reset_button, 2)
    screen.blit(reset_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 55))

    # Menampilkan percepatan pada layar
    acceleration_text = font.render("Percepatan: {:.2f} m/s^2".format(a), True, BLACK)
    screen.blit(acceleration_text, (10, 90))

    # Memperbarui waktu
    t += delta_t

    # Update tampilan layar
    pygame.display.flip()

# Quit pygame
pygame.quit()
