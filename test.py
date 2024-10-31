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
PINK = (252, 142, 172)  # #FC8EAC
BLACK = (0, 0, 0)

# 폰트 설정
font = pygame.font.Font(None, 50)

# 숫자 배열
ROUND1 = [1, 2, 3, 4, 6, 8] # Round 1 숫자들
ROUND2 = [8, 9, 11, 13, 15, 16] # Round 2 숫자들
ROUND3 = [16, 17, 20, 22, 25, 26, 28, 30, 32] # Round 3 숫자들
ROUND4 = [32, 33, 35, 37, 40, 45, 50, 56, 60, 61, 64] # Round 4 숫자들
ROUND5 = [64, 70, 78, 81, 90, 95, 100, 115, 120, 124, 128] # Round 5 숫자들
ROUND6 = [128, 135, 150, 163, 172, 181, 198, 220, 233, 246, 251, 256] # Round 6 숫자들
ROUND7 = [256, 275, 289, 301, 344, 365, 390, 417, 446, 485, 500, 512] # Round 7 숫자들
ROUND8 = [512, 534, 572, 588, 613, 677, 718, 750, 821, 901, 967, 1004, 1024] # Round 8 숫자들

# 플레이어 클래스
class Player:
    def __init__(self):
        self.number = 1  # 시작 숫자
        self.rect = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 100, 80, 80)

    def draw(self):
        pygame.draw.rect(screen, PINK, self.rect, border_radius=10)
        self.draw_text_centered(str(self.number), self.rect)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 10

    def update_num(self, value):
        if value < self.number:
            self.number = 1  # 자신보다 작은 숫자 먹으면 1로 초기화
        elif value > self.number:
            self.gameover()  # 자신보다 큰 숫자 먹으면 게임 종료
        else:
            self.number += value  # 같은 숫자일 때 더하기

    def gameover(self):
        print("Game Over")
        pygame.quit()
        sys.exit()

    def draw_text_centered(self, text, rect):
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

# 떨어지는 숫자 클래스
class FallingNum:
    def __init__(self, num_list):
        self.value = random.choice(num_list)  # 지정된 수열에서 무작위 선택
        self.rect = pygame.Rect(random.randint(0, WIDTH - 80), -80, 80, 80)

    def fall(self, speed):
        self.rect.y += speed

    def draw(self):
        pygame.draw.rect(screen, PINK, self.rect, border_radius=10)
        self.draw_text_centered(str(self.value), self.rect)

    def draw_text_centered(self, text, rect):
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

# 게임 설정
player = Player()
falling_number = []
clock = pygame.time.Clock()
speed = 8

# 게임 루프
while True:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력 받아서 플레이어 이동
    keys = pygame.key.get_pressed()
    player.move(keys)

    # 라운드 전환: 플레이어 숫자에 따라 라운드 변경
    if 1 <= player.number < 8:
        round = 1
    elif 8 <= player.number < 16:
        round = 2
        speed = 10
    elif 16 <= player.number < 32:
        round = 3
        speed = 12
    elif 32 <= player.number < 64:
        round = 4
        speed = 15
    elif 64 <= player.number < 128:
        round = 5
        speed = 18
    elif 128 <= player.number < 256:
        round = 6
        speed = 21
    elif 256 <= player.number < 512:
        round = 7
        speed = 25
    elif 512 <= player.number < 1024:
        round = 8
        speed = 30

    # 라운드에 따라 적절한 숫자 리스트 선택
    if round == 1:
        number_list = ROUND1
    elif round == 2:
        number_list = ROUND2
    elif round == 3:
        number_list = ROUND3
    elif round == 4:
        number_list = ROUND4
    elif round == 5:
        number_list = ROUND5
    elif round == 6:
        number_list = ROUND6
    elif round == 7:
        number_list = ROUND7
    elif round == 8:
        number_list = ROUND8


    # 숫자 생성 (일정 확률로)
    if random.randint(1, 50) == 1:
        falling_number.append(FallingNum(number_list))

    # 떨어지는 숫자 처리
    for number in falling_number[:]:
        number.fall(speed)
        number.draw()

        # 충돌 체크 및 숫자 합산 (같은 숫자끼리만 합산 가능)
        if number.rect.colliderect(player.rect):
            player.update_num(number.value)
            falling_number.remove(number)

        # 화면 밖으로 나가면 제거
        elif number.rect.top > HEIGHT:
            falling_number.remove(number)

    # 플레이어 그리기
    player.draw()

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(30)
