import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NumberCount")

# 색상
PINK = (252, 142, 172) #FC8EAC
BLACK = (0, 0, 0)

# 폰트
font = pygame.font.Font(None, 50)
big_font = pygame.font.Font(None, 80)

# 처음 점수
score = 1

# 라운드별 숫자 배열
ROUND1 = [1, 1, 1, 2, 2, 2, 3, 4, 4, 6, 7, 8, 8, 8] # Round1 숫자 (1, 2, 4)
ROUND2 = [6, 7, 8, 8, 8, 9, 11, 13, 15, 16, 16] # Round2 숫자 (8)
ROUND3 = [11, 13, 15, 16, 16, 16, 17, 20, 22, 25, 28, 30, 32, 32, 32] # Round3 숫자 (16)
ROUND4 = [25, 28, 30, 32, 32, 32, 33, 37, 40, 45, 50, 56, 60, 64, 64] # Round4 숫자 (32)
ROUND5 = [45, 50, 56, 60, 64, 64, 64, 70, 78, 81, 90, 95, 100, 121, 128, 128, 128] # Round5 숫자 (64)
ROUND6 = [95, 100, 121, 128, 128, 150, 163, 172, 181, 220, 233, 246, 251, 256, 256, 256] # Round6 숫자 (128)
ROUND7 = [233, 246, 251, 256, 256, 256, 275, 289, 301, 365, 390, 417, 485, 490, 512, 512] # Round7 숫자 (256)
ROUND8 = [417, 485, 490, 512, 512, 512, 534, 588, 613, 677, 718, 821, 901, 1004, 1024, 1024, 1024] # Round8 숫자 (512)
ROUND9 = [718, 821, 901, 1004, 1024, 1024, 1024, 1223, 1340, 1501, 1687, 1700, 2024, 2048, 2048] # Round9 숫자 (1024)

# 플레이어 클래스
class Player:
    def __init__(self):
        self.number = 1  # 시작 숫자
        self.rect = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 100, 80, 80)

    def draw(self):
        pygame.draw.rect(screen, PINK, self.rect, border_radius=10)
        self.user_text(str(self.number), self.rect)

    def user_text(self, text, rect):
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 10

    def update_num(self, value):
        global score
        if value < self.number:
            self.number = 1  # 자신보다 작은 숫자 먹으면 1로 초기화
            score = 1
        elif value > self.number:
            self.draw_over()
            pygame.display.flip()
            pygame.time.delay(1500)
            self.GameOver()  # 자신보다 큰 숫자 먹으면 게임 종료
        elif score==2048:
            self.draw_clear() # 점수가 2048이 되면 점수 클리어
            pygame.display.flip()
            pygame.time.delay(1500)
            self.GameOver() # 게임 종료
        else:   # 같은 숫자일 때는 더하기
            self.number += value
            score += value

    def draw_score(self): # 현재 점수 표시
        text_score = font.render("Score : " + str(score), True, PINK)
        screen.blit(text_score, [380, 30])

    def draw_over(self):
        text_over = big_font.render("Game Over", True, PINK)
        screen.blit(text_over, [150, 350])
        yourScore = font.render("Your Score : " + str(score), True, PINK)
        screen.blit(yourScore, [195, 410])

    def draw_clear(self):
        text_clear = big_font.render("Game Clear", True, PINK)
        screen.blit(text_clear, [150, 350])
        clearScore = font.render("Clear Score : " + str(score), True, PINK)
        screen.blit(clearScore, [190, 410])

    def GameOver(self):
        print("Game Over")
        pygame.quit()
        sys.exit()

# 떨어지는 숫자 클래스
class FallingNum:
    def __init__(self, number_list):
        while True:
            self.value = random.choice(number_list)  # 랜덤으로 선택
            self.rect = pygame.Rect(random.randint(0, WIDTH - 80), -80, 80, 80)

            if not any(self.rect.colliderect(existing) for existing in existing_rects): #떨어지는 숫자 위치가 겹쳐서 내려오지 않도록
                break

    def fall(self, speed):
        self.rect.y += speed

    def draw(self):
        pygame.draw.rect(screen, PINK, self.rect, border_radius=10)
        self.fall_numTxt(str(self.value), self.rect)

    def fall_numTxt(self, text, rect): # 떨어지는 숫자 글씨
        fall_text = font.render(text, True, BLACK)
        fall_rect = fall_text.get_rect(center=rect.center)
        screen.blit(fall_text, fall_rect)

# 게임 시작을 할 수 있도록 버튼 추가
def game_start():
    title = big_font.render("NumberCount", True, PINK)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)

    startbtn = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 80)
    pygame.draw.rect(screen, PINK, startbtn, border_radius=10)
    start_text = font.render("Game Start", True, BLACK)
    rect = start_text.get_rect(center=startbtn.center)
    screen.blit(start_text, rect)

    pygame.display.flip()

    # 게임 시작 버튼 클릭
    click = True
    while click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if startbtn.collidepoint(mouse_pos):
                    click = False  # 게임 시작

# 게임 시작 화면 표시
game_start()

# 게임 화면 설정
player = Player()
falling_number = []
clock = pygame.time.Clock()
speed = 8

while True:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키를 눌러서 이동
    keys = pygame.key.get_pressed()
    player.move(keys)

    # 라운드 전환: 플레이어 숫자에 따라 라운드 변경
    if 1 <= player.number < 8:
        round = 1
        speed = 8
    elif 8 <= player.number < 16:
        round = 2
        speed = 10
    elif 16 <= player.number < 32:
        round = 3
        speed = 12
    elif 32 <= player.number < 64:
        round = 4
        speed = 14
    elif 64 <= player.number < 128:
        round = 5
        speed = 16
    elif 128 <= player.number < 256:
        round = 6
        speed = 18
    elif 256 <= player.number < 512:
        round = 7
        speed = 20
    elif 512 <= player.number < 1024:
        round = 8
        speed = 22
    elif 1024 <= player.number < 2048:
        round = 9
        speed = 24

    # 라운드에 따라 숫자 리스트 선택
    if round == 1:
        number_list = ROUND1
        speed = 8
    elif round == 2:
        number_list = ROUND2
        speed = 10
    elif round == 3:
        number_list = ROUND3
        speed = 12
    elif round == 4:
        number_list = ROUND4
        speed = 14
    elif round == 5:
        number_list = ROUND5
        speed = 16
    elif round == 6:
        number_list = ROUND6
        speed = 18
    elif round == 7:
        number_list = ROUND7
        speed = 20
    elif round == 8:
        number_list = ROUND8
        speed = 22
    elif round == 9:
        number_list = ROUND9
        speed = 24

    # 숫자 생성
    if random.randint(1, 25) == 1:
        existing_rects = [num.rect for num in falling_number]
        falling_number.append(FallingNum(number_list))

    # 떨어지는 숫자
    for number in falling_number[:]:
        number.fall(speed)
        number.draw()

        # 충돌 체크 & 숫자 더하기 (같은 숫자끼리만 더하기 가능)
        if number.rect.colliderect(player.rect):
            player.update_num(number.value)
            falling_number.remove(number)

        # 화면 밖으로 나가면 없애기
        elif number.rect.top > HEIGHT:
            falling_number.remove(number)

    # 플레이어 그리기
    player.draw()
    player.draw_score()

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(30)