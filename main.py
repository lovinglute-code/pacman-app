import pygame
import math
import numpy as np
import random

# --- 설정 (Constants) ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800  # [수정] 버튼 공간 확보를 위해 세로 길이 늘림
FPS = 60
BLOCK_SIZE = 24

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 0, 139)
GRAY = (100, 100, 100)

# 맵 레이아웃
MAP_LAYOUT = [
    "1111111111111111111",
    "1222222221222222221",
    "1211211121211121121",
    "1211211121211121121",
    "1222222222222222221",
    "1211212111112121121",
    "1222212221222122221",
    "1111211133311121111",
    "3331213339333121333",
    "1111213119113121111",
    "3333233199913323333",
    "1111213111113121111",
    "3331213333333121333",
    "1111212111112121111",
    "1222222221222222221",
    "1211211121211121121",
    "1221222233322221221",
    "1121212111112121211",
    "1222212221222122221",
    "1111111111111111111"
]

MAP_ROWS = len(MAP_LAYOUT)
MAP_COLS = len(MAP_LAYOUT[0])
MAP_WIDTH_PX = MAP_COLS * BLOCK_SIZE
MAP_HEIGHT_PX = MAP_ROWS * BLOCK_SIZE
OFFSET_X = (SCREEN_WIDTH - MAP_WIDTH_PX) // 2
OFFSET_Y = 50 # 상단 여백

# --- 사운드 생성 클래스 ---
class SoundGenerator:
    def __init__(self):
        try:
            if pygame.mixer.get_init():
                pygame.mixer.quit()
            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.mixer.init()
            self.sample_rate = 44100
            self.enabled = True
        except:
            print("Sound init failed")
            self.enabled = False
    
    def generate_wave(self, freq, duration, vol=0.5, wave_type='sine'):
        if not self.enabled: return None
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        if wave_type == 'sine': wave = np.sin(2 * np.pi * freq * t)
        elif wave_type == 'square': wave = np.sign(np.sin(2 * np.pi * freq * t))
        elif wave_type == 'sawtooth': wave = 2 * (t * freq - np.floor(t * freq + 0.5))
        else: wave = np.sin(2 * np.pi * freq * t)

        fade_len = int(n_samples * 0.1)
        if fade_len > 0:
            fade = np.linspace(1, 0, fade_len)
            wave[-fade_len:] *= fade
            
        audio = (wave * vol * 32767).astype(np.int16)
        if pygame.mixer.get_init():
            ch = pygame.mixer.get_init()[2]
            if ch == 2: audio = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(audio)

    def make_intro_music(self):
        if not self.enabled: return []
        notes = [261, 329, 392, 523, 392, 329, 261, 0] 
        sounds = []
        for note in notes:
            if note == 0: sounds.append(self.generate_wave(1, 0.1, 0)) 
            else: sounds.append(self.generate_wave(note, 0.1, 0.3, 'square'))
        return sounds

    def make_waka_sound(self):
        if not self.enabled: return None, None
        return self.generate_wave(150, 0.15, 0.3, 'sawtooth'), self.generate_wave(300, 0.15, 0.3, 'sawtooth')

    def make_eat_ghost_sound(self):
        if not self.enabled: return None
        return self.generate_wave(800, 0.1, 0.4, 'square')

    def make_die_sound(self):
        if not self.enabled: return None
        duration = 1.0
        n_samples = int(self.sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        freqs = np.linspace(800, 50, n_samples)
        wave = np.sin(2 * np.pi * freqs * t)
        audio = (wave * 0.5 * 32767).astype(np.int16)
        if pygame.mixer.get_init():
            ch = pygame.mixer.get_init()[2]
            if ch == 2: audio = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(audio)

# --- 터치 컨트롤러 클래스 ---
class TouchController:
    def __init__(self):
        self.btn_size = 80
        center_x = SCREEN_WIDTH // 2
        base_y = SCREEN_HEIGHT - 150
        
        # 상하좌우 버튼 Rect 정의
        self.up_rect = pygame.Rect(center_x - self.btn_size//2, base_y - self.btn_size, self.btn_size, self.btn_size)
        self.down_rect = pygame.Rect(center_x - self.btn_size//2, base_y + self.btn_size, self.btn_size, self.btn_size)
        self.left_rect = pygame.Rect(center_x - self.btn_size*1.5, base_y, self.btn_size, self.btn_size)
        self.right_rect = pygame.Rect(center_x + self.btn_size*0.5, base_y, self.btn_size, self.btn_size)
        
    def draw(self, screen):
        # 버튼 그리기
        for rect, label in [(self.up_rect, "^"), (self.down_rect, "v"), (self.left_rect, "<"), (self.right_rect, ">")]:
            pygame.draw.rect(screen, GRAY, rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
            # 화살표 텍스트는 생략하고 도형으로 표시해도 됨

    def get_input(self, pos):
        if self.up_rect.collidepoint(pos): return (0, -1)
        if self.down_rect.collidepoint(pos): return (0, 1)
        if self.left_rect.collidepoint(pos): return (-1, 0)
        if self.right_rect.collidepoint(pos): return (1, 0)
        return None

# --- 게임 클래스 ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Mobile")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 20, True)
        self.big_font = pygame.font.SysFont('arial', 40, True)
        
        self.synth = SoundGenerator()
        self.snd_intro = self.synth.make_intro_music()
        self.snd_waka1, self.snd_waka2 = self.synth.make_waka_sound()
        self.snd_eat_ghost = self.synth.make_eat_ghost_sound()
        self.snd_die = self.synth.make_die_sound()
        
        self.controller = TouchController()
        self.reset_game()

    def reset_game(self):
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.lives = 3
        self.state = "INTRO"
        self.reset_level()
        
    def reset_level(self):
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        self.ghost_house = []
        ghost_spawn = []
        
        for r, row in enumerate(MAP_LAYOUT):
            for c, char in enumerate(row):
                x = OFFSET_X + c * BLOCK_SIZE
                y = OFFSET_Y + r * BLOCK_SIZE
                if char == '1': self.walls.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                elif char == '9':
                    self.ghost_house.append(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                    ghost_spawn.append((x, y))

        self.player = Player(OFFSET_X + 9 * BLOCK_SIZE, OFFSET_Y + 16 * BLOCK_SIZE)
        
        if len(ghost_spawn) >= 2:
            self.ghosts = [
                Ghost(ghost_spawn[0][0], ghost_spawn[0][1], RED, "blinky"),
                Ghost(ghost_spawn[0][0], ghost_spawn[0][1], PINK, "pinky"),
                Ghost(ghost_spawn[1][0], ghost_spawn[1][1], CYAN, "inky"),
                Ghost(ghost_spawn[1][0], ghost_spawn[1][1], ORANGE, "clyde")
            ]
        else: self.ghosts = [Ghost(OFFSET_X + 9*BLOCK_SIZE, OFFSET_Y + 9*BLOCK_SIZE, RED, "blinky")]
        
        self.pellets = []
        self.power_pellets = []
        for r, row in enumerate(MAP_LAYOUT):
            for c, char in enumerate(row):
                x = OFFSET_X + c * BLOCK_SIZE
                y = OFFSET_Y + r * BLOCK_SIZE
                if (r==1 and c==1) or (r==1 and c==17) or (r==18 and c==1) or (r==18 and c==17):
                    self.power_pellets.append(pygame.Rect(x+6, y+6, 12, 12))
                elif char not in ['1', '9', '3']:
                    self.pellets.append(pygame.Rect(x+10, y+10, 4, 4))

    def play_intro(self):
        for sound in self.snd_intro:
            if sound: sound.play()
            pygame.time.delay(150)
        self.state = "PLAYING"

    def update(self):
        if self.state != "PLAYING": return

        self.player.update(self.walls)
        
        # 펠릿 충돌 처리
        p_hit_list = self.player.rect.collidelistall(self.pellets)
        if p_hit_list:
            for i in sorted(p_hit_list, reverse=True):
                del self.pellets[i]
                self.score += 10
                if self.score % 20 == 0 and self.snd_waka1: self.snd_waka1.play()
                elif self.score % 10 == 0 and self.snd_waka2: self.snd_waka2.play()

        pp_hit_list = self.player.rect.collidelistall(self.power_pellets)
        if pp_hit_list:
            for i in sorted(pp_hit_list, reverse=True):
                del self.power_pellets[i]
                self.score += 50
                if self.snd_eat_ghost: self.snd_eat_ghost.play()
                for g in self.ghosts:
                    g.frightened = True
                    g.frightened_timer = 600

        if not self.pellets and not self.power_pellets:
            self.state = "WON"
            if self.snd_intro: self.snd_intro[0].play()

        for ghost in self.ghosts:
            ghost.update(self.walls, self.player.rect.center)
            if self.player.rect.colliderect(ghost.rect):
                if ghost.frightened:
                    ghost.reset_pos()
                    self.score += 200
                    if self.snd_eat_ghost: self.snd_eat_ghost.play()
                else:
                    self.lives -= 1
                    if self.snd_die: self.snd_die.play()
                    if self.lives == 0: self.state = "GAMEOVER"
                    else:
                        pygame.time.delay(1000)
                        self.player.reset_pos()
                        for g in self.ghosts: g.reset_pos()

    def draw(self):
        self.screen.fill(BLACK)
        
        score_text = self.font.render(f"SCORE: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        for wall in self.walls:
            pygame.draw.rect(self.screen, DARK_BLUE, wall)
            pygame.draw.rect(self.screen, BLUE, wall, 1)
        for p in self.pellets: pygame.draw.rect(self.screen, (255, 180, 180), p)
        for pp in self.power_pellets: pygame.draw.circle(self.screen, WHITE, pp.center, 8)

        self.player.draw(self.screen)
        for ghost in self.ghosts: ghost.draw(self.screen)
        
        # [모바일] 컨트롤러 그리기
        self.controller.draw(self.screen)

        if self.state == "INTRO":
            txt = self.big_font.render("TOUCH TO START", True, YELLOW)
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
        elif self.state == "GAMEOVER":
            txt = self.big_font.render("GAME OVER", True, RED)
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
        elif self.state == "WON":
            txt = self.big_font.render("YOU WIN!", True, YELLOW)
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))

        pygame.display.flip()

    def run(self):
        self.play_intro()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                
                # [모바일] 터치 입력 처리
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.state == "PLAYING":
                        direction = self.controller.get_input(pos)
                        if direction:
                            self.player.set_dir(direction[0], direction[1])
                    elif self.state in ["INTRO", "GAMEOVER", "WON"]:
                         self.reset_game()
                         self.play_intro()

            self.update()
            self.draw()
            self.clock.tick(FPS)

# --- Player & Ghost (기존 동일) ---
class Player:
    def __init__(self, x, y):
        self.start_pos = (x, y)
        self.reset_pos()
        self.speed = 3
        self.anim_counter = 0
    def reset_pos(self):
        self.x, self.y = self.start_pos
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE-2, BLOCK_SIZE-2)
        self.dx, self.dy = 0, 0
        self.next_dx, self.next_dy = 0, 0
    def set_dir(self, dx, dy): self.next_dx, self.next_dy = dx, dy
    def update(self, walls):
        new_rect = self.rect.copy()
        new_rect.x += self.next_dx * self.speed
        new_rect.y += self.next_dy * self.speed
        collision = False
        for wall in walls:
            if new_rect.colliderect(wall): collision = True; break
        if not collision: self.dx, self.dy = self.next_dx, self.next_dy
        self.rect.x += self.dx * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.dx > 0: self.rect.right = wall.left
                if self.dx < 0: self.rect.left = wall.right
        self.rect.y += self.dy * self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.dy > 0: self.rect.bottom = wall.top
                if self.dy < 0: self.rect.top = wall.bottom
        map_left_limit = OFFSET_X
        map_right_limit = OFFSET_X + MAP_WIDTH_PX
        if self.rect.left > map_right_limit: self.rect.right = map_left_limit
        elif self.rect.right < map_left_limit: self.rect.left = map_right_limit
        self.anim_counter += 0.2
    def draw(self, screen):
        center = self.rect.center
        radius = BLOCK_SIZE // 2
        mouth_open = int(abs(math.sin(self.anim_counter)) * 30)
        angle = 0
        if self.dx == 1: angle = 0
        elif self.dx == -1: angle = 180
        elif self.dy == -1: angle = 90
        elif self.dy == 1: angle = 270
        pygame.draw.circle(screen, YELLOW, center, radius)
        if mouth_open > 0:
            p1 = center
            p2 = (center[0] + radius * math.cos(math.radians(angle + mouth_open)), center[1] - radius * math.sin(math.radians(angle + mouth_open)))
            p3 = (center[0] + radius * math.cos(math.radians(angle - mouth_open)), center[1] - radius * math.sin(math.radians(angle - mouth_open)))
            pygame.draw.polygon(screen, BLACK, [p1, p2, p3])

class Ghost:
    def __init__(self, x, y, color, name):
        self.start_pos = (x, y)
        self.color = color
        self.name = name
        self.reset_pos()
        self.speed = 2
    def reset_pos(self):
        self.x, self.y = self.start_pos
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE-2, BLOCK_SIZE-2)
        self.dx, self.dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.frightened = False
        self.frightened_timer = 0
    def update(self, walls, target_pos):
        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0: self.frightened = False
            curr_speed = 1
        else: curr_speed = self.speed
        self.rect.x += self.dx * curr_speed
        self.rect.y += self.dy * curr_speed
        hit_wall = False
        for wall in walls:
            if self.rect.colliderect(wall):
                hit_wall = True
                self.rect.x -= self.dx * curr_speed
                self.rect.y -= self.dy * curr_speed
                break
        if hit_wall or random.randint(0, 50) == 0:
            options = [(1,0), (-1,0), (0,1), (0,-1)]
            random.shuffle(options)
            best_dir = options[0]
            if not self.frightened and random.randint(0, 3) > 0:
                min_dist = 99999
                for dx, dy in options:
                    test_rect = self.rect.copy()
                    test_rect.x += dx * BLOCK_SIZE
                    test_rect.y += dy * BLOCK_SIZE
                    if test_rect.collidelist(walls) == -1:
                        dist = math.hypot(test_rect.centerx - target_pos[0], test_rect.centery - target_pos[1])
                        if dist < min_dist: min_dist = dist; best_dir = (dx, dy)
            else:
                for dx, dy in options:
                    test_rect = self.rect.copy()
                    test_rect.x += dx * 10
                    test_rect.y += dy * 10
                    if test_rect.collidelist(walls) == -1: best_dir = (dx, dy); break
            self.dx, self.dy = best_dir
        map_left_limit = OFFSET_X
        map_right_limit = OFFSET_X + MAP_WIDTH_PX
        if self.rect.left > map_right_limit: self.rect.right = map_left_limit
        elif self.rect.right < map_left_limit: self.rect.left = map_right_limit
    def draw(self, screen):
        color = BLUE if self.frightened else self.color
        rect = self.rect
        pygame.draw.circle(screen, color, (rect.centerx, rect.top + BLOCK_SIZE//2), BLOCK_SIZE//2)
        pygame.draw.rect(screen, color, (rect.left, rect.centery, BLOCK_SIZE, BLOCK_SIZE//2))
        eye_color = WHITE
        pygame.draw.circle(screen, eye_color, (rect.centerx - 4, rect.centery - 2), 4)
        pygame.draw.circle(screen, eye_color, (rect.centerx + 4, rect.centery - 2), 4)
        pygame.draw.circle(screen, BLACK, (rect.centerx - 4 + self.dx*2, rect.centery - 2 + self.dy*2), 2)
        pygame.draw.circle(screen, BLACK, (rect.centerx + 4 + self.dx*2, rect.centery - 2 + self.dy*2), 2)

if __name__ == "__main__":
    game = Game()
    game.run()