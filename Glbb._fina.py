import pygame

pygame.init()

# Lebar dan tinggi layar
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Warna RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 50,
                        SCREEN_HEIGHT // 2 - 50, 100, 50)
input_text = ""

reset_button = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 100, 50)
pause_button = pygame.Rect(SCREEN_WIDTH - 230, SCREEN_HEIGHT - 70, 100, 50)

# Slider
slider = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 20)
slider_handle = pygame.Rect(x - 10, SCREEN_HEIGHT - 110, 20, 40)
slider_dragging = False

# Loop program
running = True
input_v = False
pause = False
while running:
    # Loop event pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Input teks
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    input_a = float(input_text)
                    a = input_a
                    input_v = True
                except ValueError:
                    pass
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if reset_button.collidepoint(event.pos):
                    x = 25
                    v = 0
                    a = 0
                    t = 0
                    ball_pos = (x, SCREEN_HEIGHT // 2)
                    input_v = False
                elif pause_button.collidepoint(event.pos):
                    pause = not pause
                elif slider_handle.collidepoint(event.pos):
                    slider_dragging = True
                    dx = event.pos[0] - slider_handle.x
                elif slider.collidepoint(event.pos):
                    slider_dragging = True
                    dx = event.pos[0] - slider_handle.centerx
            elif event.button == 4:  # Scroll up
                a -= 1
            elif event.button == 5:  # Scroll down
                a += 1

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if slider_dragging:
                slider_handle.x = event.pos[0] - dx
                if slider_handle.left < slider.left:
                    slider_handle.left = slider.left
                elif slider_handle.right > slider.right:
                    slider_handle.right = slider.right
                x = slider_handle.centerx
                v = 0  # Menghentikan bola saat menggeser slider

    # Menggambar latar belakang dengan warna putih
    screen.fill(WHITE)

    # Menggambar bola dengan warna merah
    pygame.draw.circle(screen, RED, ball_pos, BALL_RADIUS)

    # Menggambar slider dengan warna biru
    pygame.draw.rect(screen, BLUE, slider)
    pygame.draw.rect(screen, BLACK, slider_handle)

    # Menampilkan waktu pada layar
    time_text = font.render("Waktu: {:.2f} s".format(t), True, BLACK)
    screen.blit(time_text, (10, 10))

    # Menampilkan kecepatan
    vel_text = font.render("Kecepatan: {:.2f} m/s".format(v), True, BLACK)
    screen.blit(vel_text, (10, 40))

    accel_text = font.render("Percepatan: {:.2f} m/s^2".format(a), True, BLACK)
    screen.blit(accel_text, (10, 70))

    # Menampilkan input percepatan pada layar
    input_box_text = font.render("Input percepatan:", True, BLACK)
    screen.blit(input_box_text, (SCREEN_WIDTH // 70, SCREEN_HEIGHT // 2 - 200))
    input_text_surface = font.render(input_text, True, BLACK)
    screen.blit(input_text_surface, (230, 100))

    # Menampilkan tombol reset pada layar
    reset_text = font.render("Reset", True, BLACK)
    screen.blit(reset_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50))

    # Menampilkan tombol pause pada layar
    pause_text = font.render("Pause", True, BLACK)
    screen.blit(pause_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))

    # Memperbarui posisi bola dan waktu
    if not pause:
        if input_v:
            # Memperbarui kecepatan dan posisi bola
            v += a * delta_t
            x += v * delta_t

            # Memperbarui waktu
            t += delta_t

            # Mengatur batas posisi bola agar tidak keluar dari layar
            if x < BALL_RADIUS:
                x = BALL_RADIUS
                v = -v  # Memantulkan bola saat mencapai batas kiri layar
            elif x > SCREEN_WIDTH - BALL_RADIUS:
                x = SCREEN_WIDTH - BALL_RADIUS
                v = -v  # Memantulkan bola saat mencapai batas kanan layar

            ball_pos = (int(x), SCREEN_HEIGHT // 2)

            if v == 0:
                pause = True  # Menghentikan waktu jika kecepatan mencapai 0

    # Update layar
    pygame.display.flip()

pygame.quit()
