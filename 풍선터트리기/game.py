import pygame
import random

# 게임 초기화
pygame.init()

# 화면 크기 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("풍선 터뜨리기 게임")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 풍선 클래스
class Balloon:
    def __init__(self):
        self.image = pygame.image.load("balloon.png")  # 풍선 이미지 로드
        self.image = pygame.transform.scale(self.image, (40, 60))  # 이미지 크기 조절
        self.burst_image = pygame.image.load("burst.png")  # 터지는 이미지 로드
        self.burst_image = pygame.transform.scale(self.burst_image, (60, 60))  # 터지는 이미지 크기 조절
        self.x = random.randint(0, width - 40)
        self.y = random.randint(height // 3, height // 2)  # 주인공의 머리보다 조금 낮은 위치에서 생성
        self.speed = random.randint(1, 3)
        self.is_bursting = False
        self.burst_frame = 0

    def move(self):
        self.y -= self.speed

    def draw(self):
        if self.is_bursting:
            # 터지는 애니메이션
            if self.burst_frame < 10:  # 터지는 프레임 수
                screen.blit(self.burst_image, (self.x - 10, self.y - 10))  # 터지는 이미지 그리기
                self.burst_frame += 1
                return True
            return False  # 더 이상 그리지 않도록
        else:
            screen.blit(self.image, (self.x, self.y))  # 풍선 이미지 그리기
        return True

# 총알 클래스
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 18

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 5, 10))

# 게임 변수 초기화
score = 0
balloons = []
bullets = []
clock = pygame.time.Clock()
running = True

# 주인공 이미지 로드
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (100, 100))  # 이미지 크기 조절 (70x70)
player_x = width // 2
player_y = height - 107 # 주인공의 위치 조정

# 총알 쿨타임 변수
bullet_cooldown = 500  # 쿨타임 (밀리초)
last_shot_time = pygame.time.get_ticks()  # 마지막 발사 시간

# 제한 시간
start_time = pygame.time.get_ticks()
time_limit = 60 * 1000  # 60초

# 게임 루프
while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # 게임 종료 조건
    if elapsed_time > time_limit:
        running = False

    screen.fill(WHITE)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < width - 70:  # 플레이어 크기에 맞춰 조정
        player_x += 5

    # 총알 발사
    if keys[pygame.K_SPACE] and current_time - last_shot_time > bullet_cooldown:
        bullets.append(Bullet(player_x + 32.5, player_y))  # 중앙에서 총알 발사
        last_shot_time = current_time  # 발사 시간 업데이트

    # 풍선 생성
    if random.randint(1, 50) == 1:
        balloons.append(Balloon())

    # 총알 이동 및 그리기
    for bullet in bullets[:]:
        bullet.move()
        if bullet.y < 0:  # 화면 밖으로 나가면 제거
            bullets.remove(bullet)
        else:
            bullet.draw()

    # 풍선 이동 및 그리기
    for balloon in balloons[:]:
        if balloon.is_bursting:
            # 터진 풍선은 그리지 않음
            if not balloon.draw():
                balloons.remove(balloon)  # 애니메이션 완료 후 제거
        else:
            balloon.move()
            if balloon.y < 0:  # 화면 밖으로 나가면 제거
                balloons.remove(balloon)
            else:
                balloon.draw()

            # 충돌 체크
            for bullet in bullets[:]:
                if (bullet.x > balloon.x and 
                    bullet.x < balloon.x + 40 and 
                    bullet.y > balloon.y and 
                    bullet.y < balloon.y + 60):
                    balloon.is_bursting = True  # 풍선 터짐
                    bullets.remove(bullet)
                    score += 1

    # 주인공 이미지 그리기
    screen.blit(player_image, (player_x, player_y))

    # 점수 표시
    font = pygame.font.Font(None, 36)
    text = font.render(f"SCORE: {score}", True, RED)
    screen.blit(text, (10, 10))

    # 남은 시간 표시
    remaining_time = (time_limit - elapsed_time) // 1000
    time_text = font.render(f"REMANING TIME: {remaining_time}s", True, (0, 0, 255))
    screen.blit(time_text, (width - 320, 10))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 오버 화면
while True:
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER!", True, RED)
    score_text = font.render(f"FINAL SCORE: {score}", True, RED)
    
    screen.blit(game_over_text, (width // 2 - 150, height // 2 - 50))
    screen.blit(score_text, (width // 2 - 150, height // 2 + 10))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

pygame.quit()