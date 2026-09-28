import pygame
import random
import sys
import math

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar Utama
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Arcade Hub - Deluxe Edition")

# --- PALET WARNA (THEME SYSTEM) ---
DARK_COLORS = {
    "bg": (20, 20, 30),
    "panel": (35, 35, 48),
    "text": (255, 255, 255),
    "subtext": (200, 200, 200),
    "grid": (40, 40, 55),
    "accent": (26, 188, 156)
}

LIGHT_COLORS = {
    "bg": (240, 244, 248),
    "panel": (255, 255, 255),
    "text": (40, 40, 50),
    "subtext": (100, 110, 120),
    "grid": (220, 225, 235),
    "accent": (41, 128, 185)
}

CURRENT_THEME = "Dark"
THEME = DARK_COLORS

# Warna Permanen Game
RED = (231, 76, 60)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
CYAN = (26, 188, 156)
ORANGE = (230, 126, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font_large = pygame.font.SysFont(None, 48)
font_med = pygame.font.SysFont(None, 32)
font_small = pygame.font.SysFont(None, 22)

clock = pygame.time.Clock()

# Global Settings
GLOBAL_DIFFICULTY = "Sedang"
HIGH_SCORES = {
    "snake": 0,
    "flappy": 0,
    "catch": 0,
    "memory": 0
}

# Universal Back Button
def draw_back_button(text="BACK"):
    mouse_pos = pygame.mouse.get_pos()
    btn_rect = pygame.Rect(WIDTH - 110, 15, 95, 40)
    is_hover = btn_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, RED if not is_hover else (192, 57, 43), btn_rect, border_radius=8)
    txt = font_small.render(text, True, WHITE)
    screen.blit(txt, (btn_rect.x + (95 - txt.get_width())//2, btn_rect.y + 10))
    return btn_rect

# Result Screen dengan Opacity
def show_game_result_screen(title_text, details_text=""):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    dlg_rect = pygame.Rect(WIDTH//2 - 220, HEIGHT//2 - 140, 440, 280)
    pygame.draw.rect(screen, THEME["panel"], dlg_rect, border_radius=15)
    pygame.draw.rect(screen, THEME["accent"], dlg_rect, 3, border_radius=15)
    
    t_surf = font_large.render(title_text, True, YELLOW if "MENANG" in title_text.upper() or "SELESAI" in title_text.upper() else RED)
    screen.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, dlg_rect.y + 30))
    
    d_surf = font_med.render(details_text, True, THEME["text"])
    screen.blit(d_surf, (WIDTH//2 - d_surf.get_width()//2, dlg_rect.y + 100))
    
    btn_rect = pygame.Rect(WIDTH//2 - 100, dlg_rect.y + 180, 200, 45)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        is_hover = btn_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BLUE if not is_hover else (41, 128, 185), btn_rect, border_radius=10)
        b_txt = font_med.render("KEMBALI", True, WHITE)
        screen.blit(b_txt, (btn_rect.x + (200 - b_txt.get_width())//2, btn_rect.y + 12))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    return
        pygame.display.flip()
        clock.tick(30)


# ==========================================
# 1. GAME: SNAKE
# ==========================================
def run_snake():
    global HIGH_SCORES
    GRID_SIZE = 20
    COLS = WIDTH // GRID_SIZE
    ROWS = (HEIGHT - 60) // GRID_SIZE
    
    snake = [[10, 10], [9, 10], [8, 10]]
    direction = [1, 0]
    speed = 9 if GLOBAL_DIFFICULTY == "Mudah" else (13 if GLOBAL_DIFFICULTY == "Sedang" else 17)
    
    def spawn_food():
        while True:
            fx = random.randint(0, COLS - 1)
            fy = random.randint(0, ROWS - 1)
            if [fx, fy] not in snake:
                return [fx, fy]

    food = spawn_food()
    score = 0
    anim_counter = 0
    
    while True:
        screen.fill(THEME["bg"])
        anim_counter += 0.2
        
        for r in range(ROWS + 1):
            pygame.draw.line(screen, THEME["grid"], (0, 60 + r * GRID_SIZE), (WIDTH, 60 + r * GRID_SIZE))
        for c in range(COLS + 1):
            pygame.draw.line(screen, THEME["grid"], (c * GRID_SIZE, 60), (c * GRID_SIZE, HEIGHT))

        back_btn = draw_back_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != [0, 1]: direction = [0, -1]
                elif event.key == pygame.K_DOWN and direction != [0, -1]: direction = [0, 1]
                elif event.key == pygame.K_LEFT and direction != [1, 0]: direction = [-1, 0]
                elif event.key == pygame.K_RIGHT and direction != [-1, 0]: direction = [1, 0]
        
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        
        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS or new_head in snake:
            show_game_result_screen("GAME OVER", f"Skor Kamu: {score}")
            return
            
        snake.insert(0, new_head)
        
        if new_head == food:
            score += 1
            if score > HIGH_SCORES["snake"]:
                HIGH_SCORES["snake"] = score
            food = spawn_food()
        else:
            snake.pop()
            
        fx_px = food[0] * GRID_SIZE
        fy_px = 60 + food[1] * GRID_SIZE
        pulse_size = int(2 * math.sin(anim_counter * 2))
        pygame.draw.circle(screen, YELLOW, (fx_px + GRID_SIZE//2, fy_px + GRID_SIZE//2), (GRID_SIZE//2 - 3) + pulse_size)
        pygame.draw.circle(screen, WHITE, (fx_px + GRID_SIZE//2 - 3, fy_px + GRID_SIZE//2 - 3), 3)

        for i, segment in enumerate(snake):
            sx = segment[0] * GRID_SIZE
            sy = 60 + segment[1] * GRID_SIZE
            rect = pygame.Rect(sx + 2, sy + 2, GRID_SIZE - 4, GRID_SIZE - 4)
            if i == 0:
                pygame.draw.rect(screen, CYAN, rect, border_radius=8)
            else:
                pygame.draw.rect(screen, GREEN, rect, border_radius=6)
                
        sc_txt = font_med.render(f"Score: {score} | High: {HIGH_SCORES['snake']}", True, THEME["text"])
        screen.blit(sc_txt, (20, 20))
        
        pygame.display.flip()
        clock.tick(speed)


# ==========================================
# 2. GAME: TIC-TAC-TOE
# ==========================================
def run_tictactoe():
    board = [["" for _ in range(3)] for _ in range(3)]
    player_symbol = "X"
    bot_symbol = "O"
    turn = "X"
    winner = None

    def check_win(b):
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] != "": return b[r][0]
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] != "": return b[0][c]
        if b[0][0] == b[1][1] == b[2][2] != "": return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] != "": return b[0][2]
        if all(b[r][c] != "" for r in range(3) for c in range(3)): return "SERI"
        return None

    def bot_move():
        nonlocal board, turn, winner
        empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
        if not empty_cells: return

        chosen = None
        if GLOBAL_DIFFICULTY == "Mudah":
            chosen = random.choice(empty_cells)
        elif GLOBAL_DIFFICULTY == "Sedang":
            for sym in [bot_symbol, player_symbol]:
                for r, c in empty_cells:
                    board[r][c] = sym
                    if check_win(board) == sym:
                        board[r][c] = ""
                        chosen = (r, c)
                        break
                    board[r][c] = ""
                if chosen: break
            if not chosen: chosen = random.choice(empty_cells)
        else:
            for sym in [bot_symbol, player_symbol]:
                for r, c in empty_cells:
                    board[r][c] = sym
                    if check_win(board) == sym:
                        board[r][c] = ""
                        chosen = (r, c)
                        break
                    board[r][c] = ""
                if chosen: break
            if not chosen and (1, 1) in empty_cells: chosen = (1, 1)
            if not chosen: chosen = random.choice(empty_cells)

        board[chosen[0]][chosen[1]] = bot_symbol
        winner = check_win(board)
        turn = player_symbol

    while True:
        screen.fill(THEME["bg"])
        back_btn = draw_back_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return
                if turn == player_symbol and not winner:
                    mx, my = event.pos
                    if 250 <= mx <= 550 and 150 <= my <= 450:
                        r = (my - 150) // 100
                        c = (mx - 250) // 100
                        if board[r][c] == "":
                            board[r][c] = player_symbol
                            winner = check_win(board)
                            turn = bot_symbol

        if turn == bot_symbol and not winner:
            pygame.time.delay(400)
            bot_move()

        for r in range(3):
            for c in range(3):
                rect = pygame.Rect(250 + c * 100, 150 + r * 100, 95, 95)
                pygame.draw.rect(screen, THEME["panel"], rect, border_radius=12)
                pygame.draw.rect(screen, THEME["accent"], rect, 2, border_radius=12)
                if board[r][c] != "":
                    color = GREEN if board[r][c] == "X" else RED
                    txt = font_large.render(board[r][c], True, color)
                    screen.blit(txt, (rect.x + 33, rect.y + 22))

        status_text = f"Giliran: {turn}"
        if winner:
            if winner == "SERI": status_text = "Pertandingan Seri!"
            elif winner == player_symbol: status_text = "Selamat, Kamu Menang!"
            else: status_text = "Bot Menang!"
        
        st_surf = font_med.render(status_text, True, YELLOW)
        screen.blit(st_surf, (WIDTH//2 - st_surf.get_width()//2, 480))

        pygame.display.flip()
        clock.tick(30)

        if winner:
            pygame.time.delay(500)
            res_title = "MENANG!" if winner == player_symbol else ("SERI!" if winner == "SERI" else "KALAH!")
            show_game_result_screen(res_title, f"Tic-Tac-Toe vs Bot ({GLOBAL_DIFFICULTY})")
            return


# ==========================================
# 3. GAME: PONG
# ==========================================
def run_pong():
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    base_v = 5 if GLOBAL_DIFFICULTY == "Mudah" else (7 if GLOBAL_DIFFICULTY == "Sedang" else 9)
    ball_vel = [base_v, base_v]
    
    p1_y, p2_y = HEIGHT // 2 - 40, HEIGHT // 2 - 40
    p_width, p_height = 15, 90
    score1, score2 = 0, 0
    ball_history = []
    
    while True:
        screen.fill(THEME["bg"])
        back_btn = draw_back_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and p2_y > 60: p2_y -= 8
        if keys[pygame.K_DOWN] and p2_y < HEIGHT - p_height: p2_y += 8

        bot_speed = 3.5 if GLOBAL_DIFFICULTY == "Mudah" else (6 if GLOBAL_DIFFICULTY == "Sedang" else 8.5)
        target_y = ball_pos[1] - p_height // 2
        if p1_y < target_y and p1_y < HEIGHT - p_height: p1_y += bot_speed
        elif p1_y > target_y and p1_y > 60: p1_y -= bot_speed

        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        
        ball_history.append(list(ball_pos))
        if len(ball_history) > 6:
            ball_history.pop(0)
        
        if ball_pos[1] <= 60 or ball_pos[1] >= HEIGHT - 15:
            ball_vel[1] = -ball_vel[1]

        p1_rect = pygame.Rect(30, p1_y, p_width, p_height)
        p2_rect = pygame.Rect(WIDTH - 45, p2_y, p_width, p_height)
        ball_rect = pygame.Rect(ball_pos[0], ball_pos[1], 15, 15)

        if ball_rect.colliderect(p1_rect) or ball_rect.colliderect(p2_rect):
            ball_vel[0] = -ball_vel[0] * 1.05

        if ball_pos[0] < 0:
            score2 += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_vel = [base_v, base_v]
        elif ball_pos[0] > WIDTH:
            score1 += 1
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            ball_vel = [-base_v, base_v]

        if score2 >= 5 or score1 >= 5:
            pygame.display.flip()
            pygame.time.delay(500)
            is_win = score2 > score1
            show_game_result_screen("SELAMAT ANDA MENANG!" if is_win else "BOT MENANG!", f"Skor Kamu: {score2} - Bot: {score1}")
            return

        for pos in ball_history:
            pygame.draw.ellipse(screen, (100, 200, 255), (pos[0], pos[1], 15, 15))

        pygame.draw.rect(screen, THEME["text"], p1_rect, border_radius=6)
        pygame.draw.rect(screen, THEME["text"], p2_rect, border_radius=6)
        pygame.draw.ellipse(screen, YELLOW, ball_rect)
        pygame.draw.line(screen, THEME["grid"], (WIDTH // 2, 60), (WIDTH // 2, HEIGHT), 2)

        sc_txt = font_med.render(f"Bot: {score1}  |  Kamu: {score2}", True, THEME["text"])
        screen.blit(sc_txt, (WIDTH // 2 - 90, 20))

        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 4. GAME: FLAPPY BIRD
# ==========================================
def run_flappy():
    global HIGH_SCORES
    bird_y = HEIGHT // 2
    bird_vel = 0
    gravity = 0.45
    
    pipes = []
    pipe_timer = 0
    score = 0
    gap_size = 145 if GLOBAL_DIFFICULTY == "Mudah" else (125 if GLOBAL_DIFFICULTY == "Sedang" else 105)
    
    while True:
        screen.fill(THEME["bg"])
        back_btn = draw_back_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_vel = -7.5

        bird_vel += gravity
        bird_y += bird_vel

        pipe_timer += 1
        if pipe_timer >= 70:
            pipe_timer = 0
            p_height = random.randint(100, 340)
            pipes.append({"x": WIDTH, "top": p_height, "passed": False})

        for p in pipes:
            p["x"] -= 4.5

        pipes = [p for p in pipes if p["x"] > -70]
        bird_rect = pygame.Rect(120, int(bird_y), 34, 26)

        game_over = False
        if bird_y > HEIGHT - 30 or bird_y < 60:
            game_over = True

        for p in pipes:
            top_rect = pygame.Rect(p["x"], 60, 65, p["top"])
            bot_rect = pygame.Rect(p["x"], 60 + p["top"] + gap_size, 65, HEIGHT - (60 + p["top"] + gap_size))
            
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bot_rect):
                game_over = True
                
            if not p["passed"] and p["x"] < 120:
                score += 1
                p["passed"] = True
                if score > HIGH_SCORES["flappy"]:
                    HIGH_SCORES["flappy"] = score

        if game_over:
            show_game_result_screen("GAME OVER", f"Skor Kamu: {score} | High: {HIGH_SCORES['flappy']}")
            return

        for p in pipes:
            top_rect = pygame.Rect(p["x"], 60, 65, p["top"])
            bot_rect = pygame.Rect(p["x"], 60 + p["top"] + gap_size, 65, HEIGHT - (60 + p["top"] + gap_size))
            pygame.draw.rect(screen, (46, 204, 113), top_rect, border_radius=6)
            pygame.draw.rect(screen, (39, 174, 96), bot_rect, border_radius=6)

        pygame.draw.ellipse(screen, YELLOW, bird_rect)
        pygame.draw.circle(screen, BLACK, (138, int(bird_y) + 8), 4)
        pygame.draw.polygon(screen, ORANGE, [(150, int(bird_y) + 10), (162, int(bird_y) + 13), (150, int(bird_y) + 17)])

        sc_txt = font_med.render(f"Score: {score} | High: {HIGH_SCORES['flappy']}", True, THEME["text"])
        screen.blit(sc_txt, (20, 20))

        pygame.display.flip()
        clock.tick(50)


# ==========================================
# 5. GAME: CATCH THE COIN
# ==========================================
def run_catch():
    global HIGH_SCORES
    basket_x = WIDTH // 2 - 50
    basket_width = 100
    basket_speed = 7.5
    coins = [{"x": random.randint(30, WIDTH - 30), "y": 80, "speed": 4.5}]
    score = 0
    
    while True:
        screen.fill(THEME["bg"])
        back_btn = draw_back_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0: basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width: basket_x += basket_speed

        if score >= 40:
            target_coin_count = 4
            basket_width = 130
            basket_color = PURPLE
        elif score >= 25:
            target_coin_count = 3
            basket_width = 115
            basket_color = ORANGE
        elif score >= 10:
            target_coin_count = 2
            basket_width = 105
            basket_color = CYAN
        else:
            target_coin_count = 1
            basket_width = 100
            basket_color = BLUE

        while len(coins) < target_coin_count:
            coins.append({"x": random.randint(30, WIDTH - 30), "y": 70, "speed": random.randint(4, 8)})

        basket_rect = pygame.Rect(basket_x, HEIGHT - 55, basket_width, 22)

        for c in coins:
            c["y"] += c["speed"]
            coin_rect = pygame.Rect(c["x"], c["y"], 24, 24)
            
            if basket_rect.colliderect(coin_rect):
                score += 1
                if score > HIGH_SCORES["catch"]:
                    HIGH_SCORES["catch"] = score
                c["y"] = 70
                c["x"] = random.randint(30, WIDTH - 30)
                c["speed"] = random.randint(5, 9)
            elif c["y"] > HEIGHT:
                show_game_result_screen("GAME OVER", f"Skor Kamu: {score} | High: {HIGH_SCORES['catch']}")
                return

        pygame.draw.rect(screen, basket_color, basket_rect, border_radius=8)
        for c in coins:
            pygame.draw.circle(screen, YELLOW, (c["x"] + 12, int(c["y"]) + 12), 12)
            pygame.draw.circle(screen, WHITE, (c["x"] + 8, int(c["y"]) + 8), 4)

        sc_txt = font_med.render(f"Score: {score} | High: {HIGH_SCORES['catch']}", True, THEME["text"])
        screen.blit(sc_txt, (20, 20))

        pygame.display.flip()
        clock.tick(60)


# ==========================================
# 6. GAME: MEMORY MATCH
# ==========================================
def run_memory():
    cards_data = [1, 1, 2, 2, 3, 3, 4, 4]
    random.shuffle(cards_data)
    card_states = ["hidden"] * 8
    
    first_sel = None
    animating = False
    msg = "Temukan 4 pasang angka!"
    score = 0
    
    while True:
        screen.fill(THEME["bg"])
        back_btn = draw_back_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not animating:
                if back_btn.collidepoint(event.pos):
                    return
                mx, my = event.pos
                for i in range(8):
                    bx = 150 + (i % 4) * 130
                    by = 180 + (i // 4) * 130
                    card_rect = pygame.Rect(bx, by, 100, 100)
                    if card_rect.collidepoint((mx, my)) and card_states[i] == "hidden":
                        card_states[i] = "revealed"
                        if first_sel is None:
                            first_sel = i
                        else:
                            animating = True
                            if cards_data[first_sel] == cards_data[i]:
                                card_states[first_sel] = "matched"
                                card_states[i] = "matched"
                                first_sel = None
                                animating = False
                                score += 10
                                if all(st == "matched" for st in card_states):
                                    show_game_result_screen("SELESAI! MENANG!", f"Total Skor: {score}")
                                    return
                            else:
                                pygame.display.flip()
                                pygame.time.delay(500)
                                card_states[first_sel] = "hidden"
                                card_states[i] = "hidden"
                                first_sel = None
                                animating = False

        for i in range(8):
            bx = 150 + (i % 4) * 130
            by = 180 + (i // 4) * 130
            is_open = (card_states[i] == "revealed" or card_states[i] == "matched")
            
            card_rect = pygame.Rect(bx, by, 100, 100)
            if is_open:
                pygame.draw.rect(screen, PURPLE, card_rect, border_radius=12)
                txt = font_large.render(str(cards_data[i]), True, WHITE)
                screen.blit(txt, (bx + 38, by + 30))
            else:
                pygame.draw.rect(screen, THEME["panel"], card_rect, border_radius=12)
                pygame.draw.rect(screen, THEME["accent"], card_rect, 2, border_radius=12)

        m_txt = font_med.render(msg, True, YELLOW)
        screen.blit(m_txt, (WIDTH//2 - m_txt.get_width()//2, 100))

        pygame.display.flip()
        clock.tick(30)


# ==========================================
# SCREEN 2: ARCADE HUB (LIST 6 GAME)
# ==========================================
def game_arcade_screen():
    while True:
        screen.fill(THEME["bg"])
        
        title = font_large.render("PILIH GAME ARCADE", True, THEME["accent"])
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
        back_btn = draw_back_button("KELUAR")
        
        mouse_pos = pygame.mouse.get_pos()
        
        games_grid = [
            ("1. Snake", run_snake, WIDTH//2 - 270, 140),
            ("2. Tic-Tac-Toe", run_tictactoe, WIDTH//2 + 10, 140),
            ("3. Pong", run_pong, WIDTH//2 - 270, 230),
            ("4. Flappy Bird", run_flappy, WIDTH//2 + 10, 230),
            ("5. Catch Coin", run_catch, WIDTH//2 - 270, 320),
            ("6. Memory Match", run_memory, WIDTH//2 + 10, 320),
        ]
        
        game_btn_rects = []
        for name, func, gx, gy in games_grid:
            g_rect = pygame.Rect(gx, gy, 260, 60)
            is_hover = g_rect.collidepoint(mouse_pos)
            pygame.draw.rect(screen, BLUE if not is_hover else (41, 128, 185), g_rect, border_radius=10)
            gt = font_med.render(name, True, WHITE)
            screen.blit(gt, (g_rect.x + 25, g_rect.y + 15))
            game_btn_rects.append((g_rect, func))

        diff_info = font_med.render(f"Difficulty Aktif: {GLOBAL_DIFFICULTY}", True, YELLOW)
        screen.blit(diff_info, (WIDTH // 2 - diff_info.get_width()//2, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return
                for g_rect, func in game_btn_rects:
                    if g_rect.collidepoint(event.pos):
                        func()

        pygame.display.flip()
        clock.tick(30)


# ==========================================
# SCREEN 1: MAIN MENU
# ==========================================
def main_menu():
    global GLOBAL_DIFFICULTY, CURRENT_THEME, THEME
    while True:
        screen.fill(THEME["bg"])
        
        mouse_pos = pygame.mouse.get_pos()
        mode_btn = pygame.Rect(WIDTH - 130, 20, 110, 40)
        is_mode_hover = mode_btn.collidepoint(mouse_pos)
        pygame.draw.rect(screen, THEME["panel"], mode_btn, border_radius=8)
        pygame.draw.rect(screen, THEME["accent"], mode_btn, 2, border_radius=8)
        mode_txt = font_small.render(f"☀️ Light" if CURRENT_THEME == "Dark" else f"🌙 Dark", True, THEME["text"])
        screen.blit(mode_txt, (mode_btn.x + (110 - mode_txt.get_width())//2, mode_btn.y + 10))

        # Judul Utama
        title = font_large.render("GAME PYTHON ARCADE", True, THEME["accent"])
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        
        # Tombol MAIN
        main_btn = pygame.Rect(WIDTH // 2 - 140, 180, 280, 65)
        is_main_hover = main_btn.collidepoint(mouse_pos)
        pygame.draw.rect(screen, GREEN if not is_main_hover else (39, 174, 96), main_btn, border_radius=15)
        m_txt = font_large.render("MAIN", True, WHITE)
        screen.blit(m_txt, (main_btn.x + (280 - m_txt.get_width())//2, main_btn.y + 14))
        
        # Pilihan Difficulty
        diff_label = font_med.render("Pilih Tingkat Kesulitan:", True, THEME["subtext"])
        screen.blit(diff_label, (WIDTH // 2 - diff_label.get_width()//2, 285))
        
        diff_buttons = [
            ("Mudah", WIDTH // 2 - 210, 330),
            ("Sedang", WIDTH // 2 - 60, 330),
            ("Susah", WIDTH // 2 + 90, 330),
        ]
        
        diff_rects = []
        for name, dx, dy in diff_buttons:
            d_rect = pygame.Rect(dx, dy, 120, 45)
            is_active = (GLOBAL_DIFFICULTY == name)
            is_hover = d_rect.collidepoint(mouse_pos)
            
            bg_col = BLUE if is_active else (THEME["panel"] if not is_hover else THEME["accent"])
            pygame.draw.rect(screen, bg_col, d_rect, border_radius=10)
            
            dt = font_med.render(name, True, WHITE if is_active else THEME["text"])
            screen.blit(dt, (d_rect.x + (120 - dt.get_width())//2, d_rect.y + 10))
            diff_rects.append((d_rect, name))

        # --- COPYRIGHT TEXT BY PASCAL ---
        copy_txt = font_small.render("Copyright © 2026 Pascal. All Rights Reserved.", True, THEME["subtext"])
        screen.blit(copy_txt, (WIDTH // 2 - copy_txt.get_width() // 2, HEIGHT - 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode_btn.collidepoint(event.pos):
                    if CURRENT_THEME == "Dark":
                        CURRENT_THEME = "Light"
                        THEME = LIGHT_COLORS
                    else:
                        CURRENT_THEME = "Dark"
                        THEME = DARK_COLORS
                
                for d_rect, d_name in diff_rects:
                    if d_rect.collidepoint(event.pos):
                        GLOBAL_DIFFICULTY = d_name
                
                if main_btn.collidepoint(event.pos):
                    game_arcade_screen()

        pygame.display.flip()
        clock.tick(30)

# Jalankan Program Utama
if __name__ == "__main__":
    main_menu()