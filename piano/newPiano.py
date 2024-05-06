import pygame
import os

pygame.init()

SCREEN_WIDTH = 792  # 别问 问就是刚好放得下
SCREEN_HEIGHT = 150
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("臭鸭鸭的钢琴2.0")

# 音频文件
audios = {}
for i in range(0, 23):
    audios[i] = pygame.mixer.Sound(os.path.join("audio", f"tone ({i}).wav"))

# 布局
keyLay = [
    "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
    "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4"
]

# 键盘尺寸和位置
keyWidth = SCREEN_WIDTH // len(keyLay)
wkeyHeight = SCREEN_HEIGHT // 1
bkeyHeight = wkeyHeight // 1.3
keyHeight = [wkeyHeight, bkeyHeight] * 12
keyXY = [(i * keyWidth, 0) for i in range(len(keyLay))]

# 一些初始定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
KEY_DOWN_COLOR = (100, 100, 100)
KEY_UP_COLOR = (200, 200, 200)
font_size = 15  # 设置字体大小
font = pygame.font.Font(None, font_size)


# 绘制键盘
def sakiko():  # 致敬传奇键盘手丰川祥子
    for i, (x, y) in enumerate(keyXY):
        if i % 12 in [1, 3, 6, 8, 10]:  # 黑键位置
            pygame.draw.rect(screen, BLACK, (x, y, keyWidth, bkeyHeight))
            text = font.render(keyLay[i], True, WHITE)
            screen.blit(text, (x + keyWidth // 2 - text.get_width() // 2, y + 5))
        else:  # 白键位置
            pygame.draw.rect(screen, BLACK, (x, y, keyWidth, wkeyHeight), 1)
            pygame.draw.rect(screen, WHITE, (x + 1, y + 1, keyWidth - 2, wkeyHeight - 2))
            text = font.render(keyLay[i], True, BLACK)
            screen.blit(text, (x + keyWidth // 2 - text.get_width() // 2, y + 5))


def playSound(index):
    audios[index].play()


while True:
    screen.fill((211, 211, 211))
    sakiko()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            key_index = x // keyWidth
            if y < wkeyHeight:  # 点击在白键上
                playSound(key_index)
                pygame.draw.rect(screen, KEY_DOWN_COLOR,
                                 (keyXY[key_index][0], keyXY[key_index][1], keyWidth, wkeyHeight))
            else:  # 点击在黑键上
                playSound(key_index)
                pygame.draw.rect(screen, KEY_DOWN_COLOR, (
                    keyXY[key_index][0], keyXY[key_index][1] + wkeyHeight, keyWidth, bkeyHeight))
            pygame.display.flip()
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            key_index = x // keyWidth
            if y < wkeyHeight:  # 释放在白键上
                pygame.draw.rect(screen, WHITE,
                                 (keyXY[key_index][0], keyXY[key_index][1], keyWidth, wkeyHeight))
            else:  # 释放在黑键上
                pygame.draw.rect(screen, BLACK, (
                    keyXY[key_index][0], keyXY[key_index][1] + wkeyHeight, keyWidth, bkeyHeight))
            pygame.display.flip()

pygame.quit()
