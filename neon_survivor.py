import tkinter as tk
import random
import math
import time

# =========================================================
# NEON SURVIVOR
# Game 2D sederhana menggunakan Tkinter
# Tidak membutuhkan pygame atau modul tambahan
# =========================================================

WIDTH = 1000
HEIGHT = 650

root = tk.Tk()
root.title("NEON SURVIVOR")
root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="#080b16",
    highlightthickness=0
)
canvas.pack()

# =========================================================
# GAME STATE
# =========================================================

game_running = False
game_over = False

score = 0
high_score = 0
wave = 1

player_hp = 100
player_max_hp = 100

xp = 0
xp_needed = 100
level = 1

kills = 0

keys = set()

mouse_x = WIDTH // 2
mouse_y = HEIGHT // 2
mouse_down = False

last_time = time.time()

dash_ready = True
dash_cooldown = 0

spawn_timer = 0
spawn_interval = 0.8

enemy_list = []
bullet_list = []
particle_list = []
xp_list = []

# =========================================================
# PLAYER
# =========================================================

player = {
    "x": WIDTH / 2,
    "y": HEIGHT / 2,
    "radius": 15,
    "speed": 5,
    "shoot_timer": 0,
    "shoot_delay": 0.15
}

# =========================================================
# UTILITY
# =========================================================

def distance(x1, y1, x2, y2):
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )


def create_particles(x, y, color, amount=8):

    for _ in range(amount):

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 5)

        particle_list.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.uniform(0.3, 0.8),
            "color": color
        })


# =========================================================
# STAR BACKGROUND
# =========================================================

stars = []

for _ in range(100):

    stars.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.uniform(0.2, 1.5),
        "size": random.choice([1, 1, 1, 2])
    })


def draw_background():

    canvas.create_rectangle(
        0,
        0,
        WIDTH,
        HEIGHT,
        fill="#080b16",
        outline=""
    )

    for star in stars:

        canvas.create_oval(
            star["x"],
            star["y"],
            star["x"] + star["size"],
            star["y"] + star["size"],
            fill="#5c6bc0",
            outline=""
        )

        star["y"] += star["speed"]

        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)


# =========================================================
# PLAYER DRAW
# =========================================================

def draw_player():

    x = player["x"]
    y = player["y"]
    r = player["radius"]

    # Glow
    canvas.create_oval(
        x-r-7,
        y-r-7,
        x+r+7,
        y+r+7,
        outline="#2457ff",
        width=2
    )

    # Body
    canvas.create_oval(
        x-r,
        y-r,
        x+r,
        y+r,
        fill="#27d7ff",
        outline="#ffffff",
        width=2
    )

    # Aim direction
    dx = mouse_x - x
    dy = mouse_y - y

    length = math.sqrt(dx*dx + dy*dy)

    if length != 0:

        dx /= length
        dy /= length

        canvas.create_line(
            x,
            y,
            x + dx * 28,
            y + dy * 28,
            fill="white",
            width=4
        )


# =========================================================
# SHOOTING
# =========================================================

def shoot():

    if player["shoot_timer"] > 0:
        return

    dx = mouse_x - player["x"]
    dy = mouse_y - player["y"]

    length = math.sqrt(dx*dx + dy*dy)

    if length == 0:
        return

    dx /= length
    dy /= length

    bullet_list.append({
        "x": player["x"],
        "y": player["y"],
        "vx": dx * 13,
        "vy": dy * 13,
        "life": 1.5
    })

    create_particles(
        player["x"] + dx * 20,
        player["y"] + dy * 20,
        "#ffff66",
        3
    )

    player["shoot_timer"] = player["shoot_delay"]


# =========================================================
# ENEMY
# =========================================================

def spawn_enemy():

    side = random.randint(0, 3)

    if side == 0:
        x = random.randint(0, WIDTH)
        y = -30

    elif side == 1:
        x = WIDTH + 30
        y = random.randint(0, HEIGHT)

    elif side == 2:
        x = random.randint(0, WIDTH)
        y = HEIGHT + 30

    else:
        x = -30
        y = random.randint(0, HEIGHT)

    enemy_type = random.random()

    if enemy_type < 0.75:

        enemy = {
            "x": x,
            "y": y,
            "radius": 14,
            "speed": random.uniform(1.2, 2.3) + wave * 0.05,
            "hp": 1 + wave // 4,
            "max_hp": 1 + wave // 4,
            "color": "#ff3b6b"
        }

    elif enemy_type < 0.95:

        enemy = {
            "x": x,
            "y": y,
            "radius": 21,
            "speed": random.uniform(0.7, 1.2),
            "hp": 4 + wave // 2,
            "max_hp": 4 + wave // 2,
            "color": "#b83bff"
        }

    else:

        enemy = {
            "x": x,
            "y": y,
            "radius": 10,
            "speed": random.uniform(2.8, 3.8),
            "hp": 1,
            "max_hp": 1,
            "color": "#ff9d00"
        }

    enemy_list.append(enemy)


def draw_enemies():

    for enemy in enemy_list:

        x = enemy["x"]
        y = enemy["y"]
        r = enemy["radius"]

        # Glow
        canvas.create_oval(
            x-r-4,
            y-r-4,
            x+r+4,
            y+r+4,
            outline=enemy["color"],
            width=2
        )

        # Enemy
        canvas.create_oval(
            x-r,
            y-r,
            x+r,
            y+r,
            fill=enemy["color"],
            outline="white"
        )

        # HP bar
        hp_percent = enemy["hp"] / enemy["max_hp"]

        canvas.create_rectangle(
            x-r,
            y-r-8,
            x+r,
            y-r-4,
            fill="#300000",
            outline=""
        )

        canvas.create_rectangle(
            x-r,
            y-r-8,
            x-r + (2*r * hp_percent),
            y-r-4,
            fill="#00ff88",
            outline=""
        )


# =========================================================
# BULLETS
# =========================================================

def update_bullets(dt):

    global score
    global kills

    for bullet in bullet_list[:]:

        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]

        bullet["life"] -= dt

        if (
            bullet["life"] <= 0
            or bullet["x"] < 0
            or bullet["x"] > WIDTH
            or bullet["y"] < 0
            or bullet["y"] > HEIGHT
        ):

            if bullet in bullet_list:
                bullet_list.remove(bullet)

            continue

        # Collision with enemies
        for enemy in enemy_list[:]:

            if distance(
                bullet["x"],
                bullet["y"],
                enemy["x"],
                enemy["y"]
            ) < enemy["radius"] + 4:

                enemy["hp"] -= 1

                create_particles(
                    bullet["x"],
                    bullet["y"],
                    enemy["color"],
                    5
                )

                if bullet in bullet_list:
                    bullet_list.remove(bullet)

                if enemy["hp"] <= 0:

                    create_particles(
                        enemy["x"],
                        enemy["y"],
                        enemy["color"],
                        18
                    )

                    score += 10
                    kills += 1

                    xp_list.append({
                        "x": enemy["x"],
                        "y": enemy["y"],
                        "value": 20
                    })

                    if enemy in enemy_list:
                        enemy_list.remove(enemy)

                break


def draw_bullets():

    for bullet in bullet_list:

        x = bullet["x"]
        y = bullet["y"]

        canvas.create_oval(
            x-4,
            y-4,
            x+4,
            y+4,
            fill="#fff36b",
            outline=""
        )


# =========================================================
# XP
# =========================================================

def update_xp():

    global xp
    global level
    global xp_needed
    global player_max_hp
    global player_hp

    for orb in xp_list[:]:

        if distance(
            player["x"],
            player["y"],
            orb["x"],
            orb["y"]
        ) < 100:

            dx = player["x"] - orb["x"]
            dy = player["y"] - orb["y"]

            length = math.sqrt(dx*dx + dy*dy)

            if length != 0:

                orb["x"] += dx / length * 5
                orb["y"] += dy / length * 5

        if distance(
            player["x"],
            player["y"],
            orb["x"],
            orb["y"]
        ) < 22:

            xp += orb["value"]

            if orb in xp_list:
                xp_list.remove(orb)

            while xp >= xp_needed:

                xp -= xp_needed

                level += 1

                xp_needed = int(xp_needed * 1.25)

                player_max_hp += 10
                player_hp = player_max_hp

                player["speed"] += 0.25
                player["shoot_delay"] *= 0.94

                create_particles(
                    player["x"],
                    player["y"],
                    "#00ffff",
                    35
                )


def draw_xp():

    for orb in xp_list:

        x = orb["x"]
        y = orb["y"]

        canvas.create_oval(
            x-7,
            y-7,
            x+7,
            y+7,
            fill="#00ffcc",
            outline="#ffffff"
        )


# =========================================================
# ENEMY MOVEMENT
# =========================================================

def update_enemies():

    global player_hp

    for enemy in enemy_list[:]:

        dx = player["x"] - enemy["x"]
        dy = player["y"] - enemy["y"]

        length = math.sqrt(dx*dx + dy*dy)

        if length != 0:

            enemy["x"] += dx / length * enemy["speed"]
            enemy["y"] += dy / length * enemy["speed"]

        if distance(
            player["x"],
            player["y"],
            enemy["x"],
            enemy["y"]
        ) < player["radius"] + enemy["radius"]:

            player_hp -= 0.5

            enemy["x"] -= dx / length * 10
            enemy["y"] -= dy / length * 10

            if player_hp <= 0:

                end_game()


# =========================================================
# PARTICLES
# =========================================================

def update_particles(dt):

    for particle in particle_list[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["life"] -= dt

        if particle["life"] <= 0:

            if particle in particle_list:
                particle_list.remove(particle)


def draw_particles():

    for particle in particle_list:

        size = max(1, int(particle["life"] * 5))

        canvas.create_oval(
            particle["x"] - size,
            particle["y"] - size,
            particle["x"] + size,
            particle["y"] + size,
            fill=particle["color"],
            outline=""
        )


# =========================================================
# PLAYER MOVEMENT
# =========================================================

def move_player():

    dx = 0
    dy = 0

    if "w" in keys:
        dy -= 1

    if "s" in keys:
        dy += 1

    if "a" in keys:
        dx -= 1

    if "d" in keys:
        dx += 1

    if dx != 0 or dy != 0:

        length = math.sqrt(dx*dx + dy*dy)

        dx /= length
        dy /= length

        player["x"] += dx * player["speed"]
        player["y"] += dy * player["speed"]

    # Batasi dalam arena
    player["x"] = max(
        20,
        min(WIDTH - 20, player["x"])
    )

    player["y"] = max(
        20,
        min(HEIGHT - 20, player["y"])
    )


# =========================================================
# DASH
# =========================================================

def dash():

    global dash_ready
    global dash_cooldown

    if not dash_ready:
        return

    dx = mouse_x - player["x"]
    dy = mouse_y - player["y"]

    length = math.sqrt(dx*dx + dy*dy)

    if length == 0:
        return

    dx /= length
    dy /= length

    for _ in range(12):

        player["x"] += dx * 8
        player["y"] += dy * 8

        player["x"] = max(
            20,
            min(WIDTH - 20, player["x"])
        )

        player["y"] = max(
            20,
            min(HEIGHT - 20, player["y"])
        )

    create_particles(
        player["x"],
        player["y"],
        "#27d7ff",
        20
    )

    dash_ready = False
    dash_cooldown = 2.0


# =========================================================
# HUD
# =========================================================

def draw_hud():

    # HP
    canvas.create_text(
        20,
        20,
        anchor="nw",
        text=f"HP: {int(player_hp)}/{player_max_hp}",
        fill="white",
        font=("Arial", 16, "bold")
    )

    # Level
    canvas.create_text(
        20,
        50,
        anchor="nw",
        text=f"LEVEL: {level}",
        fill="#00ffff",
        font=("Arial", 16, "bold")
    )

    # Score
    canvas.create_text(
        WIDTH - 20,
        20,
        anchor="ne",
        text=f"SCORE: {score}",
        fill="white",
        font=("Arial", 16, "bold")
    )

    # Wave
    canvas.create_text(
        WIDTH - 20,
        50,
        anchor="ne",
        text=f"WAVE: {wave}",
        fill="#ff66aa",
        font=("Arial", 16, "bold")
    )

    # HP bar
    canvas.create_rectangle(
        20,
        82,
        220,
        98,
        fill="#26070e",
        outline="#ff3b6b"
    )

    hp_percent = player_hp / player_max_hp

    canvas.create_rectangle(
        20,
        82,
        20 + 200 * hp_percent,
        98,
        fill="#ff3b6b",
        outline=""
    )

    # XP bar
    canvas.create_rectangle(
        20,
        HEIGHT - 28,
        WIDTH - 20,
        HEIGHT - 15,
        fill="#061f24",
        outline="#00ffff"
    )

    xp_percent = xp / xp_needed

    canvas.create_rectangle(
        20,
        HEIGHT - 28,
        20 + (WIDTH - 40) * xp_percent,
        HEIGHT - 15,
        fill="#00ffff",
        outline=""
    )

    # Dash status
    dash_text = "DASH READY [SHIFT]" if dash_ready else f"DASH: {dash_cooldown:.1f}"

    canvas.create_text(
        WIDTH / 2,
        25,
        text=dash_text,
        fill="#ffff66",
        font=("Arial", 13, "bold")
    )


# =========================================================
# WAVE
# =========================================================

def update_wave():

    global wave
    global spawn_interval

    new_wave = 1 + kills // 15

    if new_wave != wave:

        wave = new_wave

        spawn_interval = max(
            0.25,
            0.8 - wave * 0.035
        )

        create_particles(
            player["x"],
            player["y"],
            "#ff66ff",
            30
        )


# =========================================================
# GAME OVER
# =========================================================

def end_game():

    global game_running
    global game_over
    global high_score

    game_running = False
    game_over = True

    if score > high_score:
        high_score = score

    canvas.create_rectangle(
        0,
        0,
        WIDTH,
        HEIGHT,
        fill="#05050a"
    )

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2 - 80,
        text="GAME OVER",
        fill="#ff3366",
        font=("Arial", 48, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2,
        text=f"SCORE  {score}",
        fill="white",
        font=("Arial", 25, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2 + 40,
        text=f"HIGH SCORE  {high_score}",
        fill="#00ffff",
        font=("Arial", 18)
    )

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2 + 100,
        text="Press R to play again",
        fill="#ffff66",
        font=("Arial", 18, "bold")
    )


# =========================================================
# RESET
# =========================================================

def reset_game():

    global game_running
    global game_over

    global score
    global wave
    global player_hp
    global xp
    global xp_needed
    global level
    global kills

    global dash_ready
    global dash_cooldown

    global spawn_timer
    global spawn_interval

    enemy_list.clear()
    bullet_list.clear()
    particle_list.clear()
    xp_list.clear()

    player["x"] = WIDTH / 2
    player["y"] = HEIGHT / 2

    player["speed"] = 5
    player["shoot_delay"] = 0.15
    player["shoot_timer"] = 0

    score = 0
    wave = 1
    player_hp = 100
    xp = 0
    xp_needed = 100
    level = 1
    kills = 0

    dash_ready = True
    dash_cooldown = 0

    spawn_timer = 0
    spawn_interval = 0.8

    game_over = False
    game_running = True


# =========================================================
# GAME UPDATE
# =========================================================

def game_loop():

    global last_time
    global spawn_timer
    global dash_cooldown
    global dash_ready

    now = time.time()

    dt = now - last_time
    last_time = now

    if dt > 0.1:
        dt = 0.1

    if game_running:

        move_player()

        if mouse_down:
            shoot()

        if player["shoot_timer"] > 0:
            player["shoot_timer"] -= dt

        # Spawn enemy
        spawn_timer += dt

        if spawn_timer >= spawn_interval:

            spawn_timer = 0

            spawn_enemy()

        update_bullets(dt)
        update_enemies()
        update_xp()
        update_particles(dt)
        update_wave()

        # Dash cooldown
        if not dash_ready:

            dash_cooldown -= dt

            if dash_cooldown <= 0:

                dash_ready = True
                dash_cooldown = 0

        # Draw everything
        draw_background()
        draw_xp()
        draw_bullets()
        draw_enemies()
        draw_particles()
        draw_player()
        draw_hud()

    elif not game_over:

        draw_menu()

    root.after(16, game_loop)


# =========================================================
# MENU
# =========================================================

def draw_menu():

    canvas.delete("all")

    draw_background()

    canvas.create_text(
        WIDTH / 2,
        180,
        text="NEON SURVIVOR",
        fill="#00ffff",
        font=("Arial", 52, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        250,
        text="SURVIVE • SHOOT • LEVEL UP",
        fill="#ff66cc",
        font=("Arial", 18, "bold")
    )

    canvas.create_text(
        WIDTH / 2,
        340,
        text="W A S D  =  MOVE",
        fill="white",
        font=("Arial", 16)
    )

    canvas.create_text(
        WIDTH / 2,
        375,
        text="LEFT CLICK  =  SHOOT",
        fill="white",
        font=("Arial", 16)
    )

    canvas.create_text(
        WIDTH / 2,
        410,
        text="SHIFT  =  DASH",
        fill="#ffff66",
        font=("Arial", 16)
    )

    canvas.create_text(
        WIDTH / 2,
        490,
        text="PRESS ENTER TO START",
        fill="#00ff88",
        font=("Arial", 22, "bold")
    )


# =========================================================
# INPUT
# =========================================================

def key_down(event):

    key = event.keysym.lower()

    keys.add(key)

    if key == "shift":

        dash()

    if key == "return" and not game_running:

        reset_game()

    if key == "r" and game_over:

        reset_game()


def key_up(event):

    key = event.keysym.lower()

    if key in keys:
        keys.remove(key)


def mouse_move(event):

    global mouse_x
    global mouse_y

    mouse_x = event.x
    mouse_y = event.y


def mouse_press(event):

    global mouse_down
    mouse_down = True


def mouse_release(event):

    global mouse_down
    mouse_down = False


# =========================================================
# BIND EVENTS
# =========================================================

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

canvas.bind("<Motion>", mouse_move)
canvas.bind("<Button-1>", mouse_press)
canvas.bind("<ButtonRelease-1>", mouse_release)

# Fokus keyboard
canvas.focus_set()

# Mulai
draw_menu()
game_loop()

root.mainloop()