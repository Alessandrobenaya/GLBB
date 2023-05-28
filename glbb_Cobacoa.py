import pygame
import math

pygame.init()

# Lebar dan tinggi layar
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Warna RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Judul layar
pygame.display.set_caption("Simulasi Gerak Lurus Berubah Beraturan")

# Inisialisasi posisi, kecepatan, dan percepatan bola
x = 50
y = SCREEN_HEIGHT // 2
v = 0
a = 0

# Inisialisasi waktu
t = 0
delta_t = 0.01

# Ukuran dan posisi bola
BALL_RADIUS = 35

# Font teks
font = pygame.font.Font(None, 36)

# Input box
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50, 100, 50)
input_text = ""

reset_button = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 100, 50)
pause_button = pygame.Rect(SCREEN_WIDTH - 230, SCREEN_HEIGHT - 70, 100, 50)
drop_button = pygame.Rect(SCREEN_WIDTH - 340, SCREEN_HEIGHT - 70, 100, 50)

# Slider horizontal
slider = pygame.Rect(50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100, 20)
slider_handle = pygame.Rect(x - 10, SCREEN_HEIGHT - 110, 20, 40)
slider_dragging = False

# Slider vertikal
y_slider = pygame.Rect(750, 175, 20, SCREEN_HEIGHT - 320)
y_slider_handle = pygame.Rect(740, y - 40, 40, 20)
y_slider_dragging = False

# Fungsi untuk mengubah ukuran objek berdasarkan posisi x
def scale_object_based_on_position(radius_x, radius_y, scale_factor, position):
    scaled_radius_x = radius_x * scale_factor
    scaled_radius_y = radius_y * scale_factor
    if position > SCREEN_WIDTH / 2:
        scaled_radius_x *= 1 + (position - SCREEN_WIDTH / 2) / (SCREEN_WIDTH / 2)
        scaled_radius_y *= 1 + (position - SCREEN_WIDTH / 2) / (SCREEN_WIDTH / 2)
    return scaled_radius_x, scaled_radius_y

# Fungsi untuk menjatuhkan bola
def drop_ball():
    global x, y, v, a, t
    x = slider_handle.centerx
    y = y_slider_handle.centery
    v = 0
    a = 0
    t = 0

# Fungsi untuk mengubah ukuran bola berdasarkan posisi slider vertikal
def scale_ball_size(position):
    scale_factor = (SCREEN_HEIGHT - position) / (SCREEN_HEIGHT - y_slider.y)
    return scale_factor

# Loop program
running = True
input_v = False
pause = False
scale = 1.0  # Faktor skala awal
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
                    x = 50
                    y = SCREEN_HEIGHT // 2
                    v = 0
                    a = 0
                    t = 0
                    input_v = False
                elif pause_button.collidepoint(event.pos):
                    pause = not pause
                elif drop_button.collidepoint(event.pos):
                    drop_ball()
                elif slider_handle.collidepoint(event.pos):
                    slider_dragging = True
                    dx = event.pos[0] - slider_handle.x
                elif y_slider_handle.collidepoint(event.pos):
                    y_slider_dragging = True
                    dy = event.pos[1] - y_slider_handle.y
                elif slider.collidepoint(event.pos):
                    slider_dragging = True
                    dx = event.pos[0] - slider_handle.centerx
                elif y_slider.collidepoint(event.pos):
                    y_slider_dragging = True
                    dy = event.pos[1] - y_slider_handle.centery
            elif event.button == 4:  # Scroll up
                a += 1
            elif event.button == 5:  # Scroll down
                a -= 1

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                slider_dragging = False
                y_slider_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if slider_dragging:
                slider_handle.x = event.pos[0] - dx
                if slider_handle.left < slider.left:
                    slider_handle.left = slider.left
                elif slider_handle.right > slider.right:
                    slider_handle.right = slider.right
                x = slider_handle.centerx
            elif y_slider_dragging:
                y_slider_handle.y = event.pos[1] - dy
                if y_slider_handle.top < y_slider.top:
                    y_slider_handle.top = y_slider.top
                elif y_slider_handle.bottom > y_slider.bottom:
                    y_slider_handle.bottom = y_slider.bottom
                y = y_slider_handle.centery
                scale = scale_ball_size(y)

    # Menggambar latar belakang dengan warna putih
    screen.fill(WHITE)

    # Menggambar bola dengan warna merah
    radius_x = BALL_RADIUS
    radius_y = BALL_RADIUS
    scaled_radius_x, scaled_radius_y = scale_object_based_on_position(radius_x, radius_y, scale, x)
    ball_pos = (int(x), int(y))
    pygame.draw.ellipse(screen, RED, (ball_pos[0] - scaled_radius_x, ball_pos[1] - scaled_radius_y, scaled_radius_x * 2, scaled_radius_y * 2))

    # Menggambar garis berputar pada bola
    line_length = scaled_radius_x * 1  # Menggandakan panjang garis
    angle = math.radians(a * t)  # Menghitung sudut rotasi berdasarkan percepatan dan waktu
    line_pos = (
        ball_pos[0] + line_length * math.cos(angle), ball_pos[1] + line_length * math.sin(angle),
    )
    pygame.draw.line(screen, BLACK, ball_pos, line_pos, 3)

    # Menggambar slider horizontal dengan warna biru
    pygame.draw.rect(screen, BLUE, slider)
    pygame.draw.rect(screen, BLACK, slider_handle)

    # Menggambar slider vertikal dengan warna hijau
    pygame.draw.rect(screen, GREEN, y_slider)
    pygame.draw.rect(screen, BLACK, y_slider_handle)

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

    # Menampilkan tombol drop pada layar
    drop_text = font.render("Drop", True, BLACK)
    screen.blit(drop_text, (SCREEN_WIDTH - 310, SCREEN_HEIGHT - 50))

    # Memperbarui posisi bola dan waktu
    if not pause:
        if input_v:
            # Memperbarui kecepatan dan posisi bola
            v += a * delta_t
            x += v * delta_t

            # Memperbarui waktu
            t += delta_t

            # Mengatur batas posisi bola agar tidak keluar dari layar
            if x < scaled_radius_x:
                x = scaled_radius_x
                v = -v  # Memantulkan bola saat mencapai batas kiri layar
            elif x > SCREEN_WIDTH - scaled_radius_x:
                x = SCREEN_WIDTH - scaled_radius_x
                v = -v  # Memantulkan bola saat mencapai batas kanan layar

    # Jika tombol drop ditekan dan posisi vertikal sudah ditentukan
    if drop_button.collidepoint(pygame.mouse.get_pos()) and y_slider_dragging:
        drop_ball()

    # Update layar
    pygame.display.flip()

pygame.quit()

