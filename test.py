import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("넘버카운트")

# 색상
PINK = (252, 142, 172)  # #FC8EAC 색상
BLACK = (0, 0, 0)

# 폰트 설정
font = pygame.font.Font(None, 50)

# 플레이어 클래스
class Player:
    def __init__(self):
        self.number = 1  # 시작 숫자
        self.rect = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 100, 80, 80)  # 사각형

    def draw(self):
        pygame.draw.rect(screen, PINK, self.rect, border_radius=10)
        self.draw_text_centered(str(self.number), self.rect)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 10

    def update_number(self, value):
        self.number += value

    def draw_text_centered(self, text, rect):
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

# 떨어지는 숫자 클래스
class FallingNumber:
    def __init__(self, min_value, max_value):
        self.value = random.randint(min_value, max_value)  # 지정된 범위 내의 숫자 생성
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
speed = 10
round_number = 1  # 현재 라운드
min_value, max_value = 1, 8  # Round 1 숫자 범위

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

    # 라운드 전환: 플레이어 숫자가 8 이상이 되면 Round 2로 변경
    if player.number >= 8 and round_number == 1:
        round_number = 2
        min_value, max_value = 8, 32  # Round 2 숫자 범위 설정

    # 숫자 생성 (일정 확률로)
    if random.randint(1, 50) == 1:
        falling_numbers.append(FallingNumber(min_value, max_value))

    # 떨어지는 숫자 처리
    for number in falling_numbers[:]:
        number.fall(speed)
        number.draw()

        # 충돌 체크 및 숫자 합산
        if number.rect.colliderect(player.rect) and number.value == player.number:
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