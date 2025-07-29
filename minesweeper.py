import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 游戏参数
ROWS = 10
COLS = 10
CELL_SIZE = 40
MINES_COUNT = 15
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# 颜色定义
BACKGROUND = (240, 240, 240)
CELL_COLOR = (192, 192, 192)
REVEALED_COLOR = (160, 160, 160)
FLAG_COLOR = (255, 0, 0)
TEXT_COLORS = [
    (0, 0, 255),    # 1
    (0, 128, 0),    # 2
    (255, 0, 0),    # 3
    (0, 0, 128),    # 4
    (128, 0, 0),    # 5
    (0, 128, 128),  # 6
    (0, 0, 0),      # 7
    (128, 128, 128) # 8
]

# 初始化窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("扫雷")

# 字体设置
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Minesweeper:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        # 初始化游戏状态
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.game_over = False
        self.win = False
        self.flag_count = 0
        self.cells_to_reveal = ROWS * COLS - MINES_COUNT
        
        # 随机放置地雷
        self._place_mines()
        # 计算周围地雷数
        self._calculate_numbers()
        
    def _place_mines(self):
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if self.board[row][col] != 'M':
                self.board[row][col] = 'M'
                mines_placed += 1
                
    def _calculate_numbers(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 'M':
                    continue
                count = 0
                # 检查周围8个格子
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS:
                            if self.board[nr][nc] == 'M':
                                count += 1
                self.board[row][col] = count
                
    def reveal_cell(self, row, col):
        if (self.revealed[row][col] or self.flagged[row][col] or 
            self.game_over or self.win):
            return
            
        self.revealed[row][col] = True
        self.cells_to_reveal -= 1
        
        # 踩到地雷
        if self.board[row][col] == 'M':
            self.game_over = True
            return
            
        # 空白格子递归翻开周围
        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        self.reveal_cell(nr, nc)
                        
        # 检查胜利
        if self.cells_to_reveal == 0:
            self.win = True
            self.game_over = True
            
    def toggle_flag(self, row, col):
        if self.revealed[row][col] or self.game_over or self.win:
            return
        self.flagged[row][col] = not self.flagged[row][col]
        self.flag_count += 1 if self.flagged[row][col] else -1
        
    def draw(self):
        screen.fill(BACKGROUND)
        
        # 绘制格子
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # 绘制格子背景
                if self.revealed[row][col]:
                    pygame.draw.rect(screen, REVEALED_COLOR, rect)
                else:
                    pygame.draw.rect(screen, CELL_COLOR, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                
                # 绘制内容
                if self.revealed[row][col]:
                    if self.board[row][col] == 'M':
                        # 绘制地雷
                        pygame.draw.circle(screen, (0, 0, 0), 
                                          (x + CELL_SIZE//2, y + CELL_SIZE//2), 
                                          CELL_SIZE//4)
                    elif self.board[row][col] > 0:
                        # 绘制数字
                        color = TEXT_COLORS[self.board[row][col] - 1]
                        text = font.render(str(self.board[row][col]), True, color)
                        text_rect = text.get_rect(center=rect.center)
                        screen.blit(text, text_rect)
                elif self.flagged[row][col]:
                    # 绘制旗帜
                    pygame.draw.polygon(screen, FLAG_COLOR, [
                        (x + CELL_SIZE//2, y + CELL_SIZE//4),
                        (x + CELL_SIZE//4, y + 3*CELL_SIZE//4),
                        (x + 3*CELL_SIZE//4, y + 3*CELL_SIZE//4)
                    ])
        
        # 绘制游戏状态文字
        if self.game_over:
            text = small_font.render("游戏结束! 按R重新开始", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            pygame.draw.rect(screen, (255, 255, 255), 
                           (text_rect.x-10, text_rect.y-10, 
                            text_rect.width+20, text_rect.height+20))
            screen.blit(text, text_rect)
        elif self.win:
            text = small_font.render("恭喜胜利! 按R重新开始", True, (0, 255, 0))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            pygame.draw.rect(screen, (255, 255, 255), 
                           (text_rect.x-10, text_rect.y-10, 
                            text_rect.width+20, text_rect.height+20))
            screen.blit(text, text_rect)
            
        pygame.display.flip()

def main():
    game = Minesweeper()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if event.button == 1:  # 左键点击
                        game.reveal_cell(row, col)
                    elif event.button == 3:  # 右键点击
                        game.toggle_flag(row, col)
        
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
