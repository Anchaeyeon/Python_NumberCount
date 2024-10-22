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
PINK = (252, 142, 172)  # #FC8EAC 색상
BLACK = (0, 0, 0)

# 폰트 설정
font = pygame.font.Font(None, 50)

# 가능한 숫자 목록 (각 라운드별)
NUMBERS_ROUND1 = [1, 2, 3, 4, 6, 8] # Round 1 숫자들
NUMBERS_ROUND2 = [8, 9, 11, 13, 14, 15, 16] # Round 2 숫자들
NUMBERS_ROUND3 = [16, 17, 20, 21, 22, 25, 26, 28, 30, 32] # Round 3 숫자들
NUMBERS_ROUND4 = [32, 33, 35, 37, 40, 43, 45, 49, 50, 55, 56, 58, 60, 61, 64] # Round 4 숫자들

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

    def update_number(self, value):
        #같은 숫자끼리만 더할 수 있음
        if self.number == value:
            self.number += value  # 같은 숫자일 때만 합산

    def draw_text_centered(self, text, rect):
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

# 떨어지는 숫자 클래스
class FallingNumber:
    def __init__(self, number_list):
        self.value = random.choice(number_list)  # 지정된 수열에서 무작위 선택
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
falling_numbers = []
clock = pygame.time.Clock()
speed = 8
round_number = 1  # 현재 라운드

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
        round_number = 1
    elif 8 <= player.number < 16:
        round_number = 2
    elif 16 <= player.number < 32:
        round_number = 3
    elif 32 <= player.number < 64:
        round_number = 4

    # 라운드에 따라 적절한 숫자 리스트 선택
    if round_number == 1:
        number_list = NUMBERS_ROUND1
    elif round_number == 2:
        number_list = NUMBERS_ROUND2
    elif round_number == 3:
        number_list = NUMBERS_ROUND3
    elif round_number == 4:
        number_list = NUMBERS_ROUND4

    # 숫자 생성 (일정 확률로)
    if random.randint(1, 50) == 1:
        falling_numbers.append(FallingNumber(number_list))

    # 떨어지는 숫자 처리
    for number in falling_numbers[:]:
        number.fall(speed)
        number.draw()

        # 충돌 체크 및 숫자 합산 (같은 숫자끼리만 합산 가능)
        if number.rect.colliderect(player.rect):
            player.update_number(number.value)
            falling_numbers.remove(number)

        # 화면 밖으로 나가면 제거
        elif number.rect.top > HEIGHT:
            falling_numbers.remove(number)

    # 플레이어 그리기
    player.draw()

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(30)
