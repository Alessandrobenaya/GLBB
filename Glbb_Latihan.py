import pygame
import math
import sys
from pygame.locals import *
import pygame.gfxdraw
# Setting Screen atau Window
pygame.init()
screen = pygame.display.set_mode((1120,600))
pygame.display.set_caption("GLBB")
width_screen = screen.get_width()
height_screen = screen.get_height()
# Warna
Hitam = (0,0,0)
Putih = (255,255,255)
Merah = (255,0,0)
Cyan = (175, 238, 238)
Grey = (1,121,111)
# Inputan awal
time = 0
velocity = 0.5
g = 10/10000
vx = 0
vy = 0
dt = 0
radius = 50
v_input = ""
# Ball position atau Titik Center Bola
ball_x = 60
ball_y = 450
angle = 0
# Tambahkan Beberapa Kondisi
active = False
fall = True
rotation = True
gravity = True
paused = False
#slider horizonal
slider_pos = width_screen // 2
slider_pos_y = height_screen // 2


# Time
clock = pygame.time.Clock()
class Bola_Bergerak:

    def __init__(self):
        self.gravity = True

    def toggle_gravity(self):
        self.gravity = not self.gravity

    def rotated_right(self):
        global vx
        vx = int(v_input) / 90
        get_angle()
    def rotated_left(self):
        global vx
        vx = -int(v_input) / 90
        get_angle()
    def button_key(key):
        global zoom, time, vx
        if key[pygame.K_RIGHT] and side_R<= width_screen:
            vx = 0
            movement(velocity,0)
        if key[pygame.K_LEFT] and side_L >= 0:
            vx = 0
            movement(-velocity,0)
        if key[pygame.K_UP] and side_T >= 0:
            movement(0,-velocity)
            time = 0
        get_angle()

    def reset_position(self):
        global ball_x, ball_y, angle, vx, vy
        ball_x = 60
        ball_y = 450
        angle = 0
        vx = 0
        vy = 0


        
rotate = Bola_Bergerak()

def movement(ball_vx, ball_vy):
    global ball_x, ball_y, vx, vy, slider_pos , slider_pos_y
    if ball_vx != 0:
        ball_x += ball_vx * dt
        vx -= vx / 300
    if vx > -0.005 and vx < 0.005:
        vx = 0
    if side_L <= 0:
        ball_x = 60
        vx = -vx
    if side_R >= width_screen:
        ball_x = width_screen - 60
        vx = -vx
    if ball_vy != 0:
        if side_T >= 0:
            ball_y += ball_vy * 2 * dt
        if side_B >= height_screen:
            ball_y = latest_y - 10

    # Update slider position based on ball's x-coordinate
    slider_pos = int(ball_x)
    slider_pos_y = int(ball_y)


def get_angle():
    global ball_x, latest_x, angle
    if rotation:
        if latest_x < ball_x:
            angle -= ((abs(ball_x-latest_x)*360)/(3.14))/100
        if latest_x > ball_x:
            angle += ((abs(ball_x-latest_x)*360)/(3.14))/100

def scale():
    global radius
    posisi_bola = (abs(height_screen - 100 - ball_y)) / 20
    radius = 50 - posisi_bola

def get_grav():
    global time, ball_y, fall, vy, side_B, height_screen
    if gravity:
        if fall and side_B <= height_screen:
            ball_y += g * (time ** 2) * dt
            time += 1
        if side_B >= height_screen and vy >= 0:  # Menghentikan bola saat mencapai batas bawah dan bergerak ke bawah
            fall = False
            time = time / 1.2
        if not fall:
            ball_y -= g * (time ** 2) * dt
            time -= 1
        if time < 1:
            fall = True
            time = 0

def rotated_line(x, y):
    cos = math.cos(math.radians(angle)*-1)
    sin = math.sin(math.radians(angle)*-1)
    x_ya = (x*cos)-(y*sin)
    y_ya = (x*sin)+(y*cos)
    return x_ya,y_ya

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(teks, x, y, w, h, color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, color, (x, y, w, h))

    smallText = pygame.font.SysFont('Arial', 20)
    textSurf, textRect = text_objects(teks, smallText, Putih)
    textRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(textSurf, textRect)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()

def toggle_pause():
        global paused
        paused = not paused

def draw_slider():
    pygame.draw.rect(screen, Putih, (50, height_screen - 30, width_screen - 100, 20))
    pygame.draw.rect(screen, Hitam, (slider_pos - 10, height_screen - 30, 20, 20))
    slider_rect = pygame.Rect(50, height_screen - 30, width_screen - 100, 20)
    pygame.draw.line(screen, Putih, (slider_rect.left, slider_rect.centery), (slider_rect.right, slider_rect.centery), 2)
    pygame.draw.circle(screen, Putih, (slider_pos, slider_rect.centery), 10)

def draw_vertical_slider():
    pygame.draw.rect(screen, Putih, (width_screen - 30, 50, 20, height_screen - 190))
    pygame.draw.rect(screen, Hitam, (width_screen - 30, slider_pos_y - 10, 20, 20))
    slider_rect = pygame.Rect(width_screen - 30, 50, 20, height_screen - 190)
    pygame.draw.line(screen, Putih, (slider_rect.centerx, slider_rect.top), (slider_rect.centerx, slider_rect.bottom), 2)
    pygame.draw.circle(screen, Putih, (slider_rect.centerx, slider_pos_y), 10)

pygame.display.update()

# Membuat Rectangle Input Box
input_rect = pygame.Rect(550, 525, 140, 32)
color_active = pygame.Color(Grey)
color_passive = pygame.Color(Hitam)
color = color_passive

pause = False
while True:
    dt = clock.tick_busy_loop(120)
    # Background warna window
    screen.fill(Cyan)
    # Garis Lintasan
    pygame.draw.line(screen, Hitam, (0, 497), (1120, 497),3)
    # Membuat Lingkaran
    radius_x = radius
    radius_y = radius
    ball_pos = (int(ball_x), int(ball_y))
    pygame.gfxdraw.aaellipse(screen, ball_pos[0], ball_pos[1], int(radius), int(radius), Hitam)
    # Batas tiap tepi
    side_T = ball_y-40
    side_B = ball_y+150
    side_L = ball_x-50
    side_R = ball_x+50
    # Posisi Bola
    latest_x = ball_x
    latest_y = ball_y
    # Garis Diamater Bola
    x1,x2 = rotated_line(-radius,0),rotated_line(radius,0)
    x1 = ball_x+x1[0],x1[1]+ball_y
    x2 = ball_x+x2[0],x2[1]+ball_y
    line_rad = pygame.draw.aaline(screen, Merah, x2, x1, 4)
    events = pygame.event.get()

    draw_vertical_slider()

    button("Reset", 20, 525, 80, 30, Hitam, Grey, rotate.reset_position)
    button("Pause", 120, 525, 80, 30, Hitam, Grey, toggle_pause)

    for event in events:
    # kondisi jika inputan kosong
        if v_input == "":
            v_input = ""
    # untuk keluar program dengan x
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:  # Pause dengan menekan tombol "p"
                    toggle_pause()

                if rotate.gravity:
                    get_grav()

                if event.key == pygame.K_BACKSPACE:
                    v_input = v_input[:-1]
                else:
                    if len(v_input) < 4: 
                        v_input += event.unicode
                    try:
                        cek = int()
                        if v_input == "0":
                            v_input = ""
                    except:
                        pass
    if active:
        color = color_active
    else:
        color = color_passive

    # menampilkan input box
    base_font_input = pygame.font.Font(None,35)
    pygame.draw.rect(screen, color, input_rect, width=3)
    text_surface = base_font_input.render(v_input, True, Hitam)
    screen.blit(text_surface,(input_rect.x + 25, input_rect.y +6))
    input_rect.w = max(100, text_surface.get_width() + 10)
    if not paused:
        movement(vx, vy)
        Bola_Bergerak.button_key(pygame.key.get_pressed())
        get_grav()
        scale()

    vel_text_surface = base_font_input.render("Kecepatan: {:.2f} m/s".format(vx), True, Hitam)
    screen.blit(vel_text_surface, (10, 40))

    draw_slider()

    # Membuat Tombol Kanan dan Kiri
    button("Rotasi Kanan", 660, 525, 100, 30, Hitam, Grey,rotate.rotated_right)
    button("Rotasi Kiri", 440, 525, 100, 30, Hitam, Grey,rotate.rotated_left)

    pygame.display.update()
