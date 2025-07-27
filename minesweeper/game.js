const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const ROWS = 10;
const COLS = 10;
const CELL_SIZE = 40;
const MINES_COUNT = 15;

let board = [];
let revealed = [];
let flagged = [];
let gameOver = false;
let flagCount = 0;
let cellsToReveal = ROWS * COLS - MINES_COUNT;

// 初始化游戏板
function initBoard() {
    board = Array.from({length: ROWS}, () => Array(COLS).fill(0));
    revealed = Array.from({length: ROWS}, () => Array(COLS).fill(false));
    flagged = Array.from({length: ROWS}, () => Array(COLS).fill(false));
    gameOver = false;
    flagCount = 0;
    cellsToReveal = ROWS * COLS - MINES_COUNT;

    // 随机布雷
    let mines = 0;
    while (mines < MINES_COUNT) {
        const r = Math.floor(Math.random() * ROWS);
        const c = Math.floor(Math.random() * COLS);
        if (board[r][c] !== 'M') {
            board[r][c] = 'M';
            mines++;
        }
    }

    // 计算每个格子周围的地雷数
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            if (board[r][c] !== 'M') {
                let count = 0;
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        if (dr === 0 && dc === 0) continue;
                        const nr = r + dr;
                        const nc = c + dc;
                        if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && board[nr][nc] === 'M') {
                            count++;
                        }
                    }
                }
                board[r][c] = count;
            }
        }
    }
    updateInfo();
}

// 绘制游戏板
function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const x = c * CELL_SIZE;
            const y = r * CELL_SIZE;

            // 绘制格子背景
            ctx.fillStyle = revealed[r][c] ? '#e0ffe0' : '#b2d8b2';
            ctx.strokeStyle = '#2db400';
            ctx.lineWidth = 2;
            ctx.fillRect(x, y, CELL_SIZE, CELL_SIZE);
            ctx.strokeRect(x, y, CELL_SIZE, CELL_SIZE);

            // 绘制旗帜
            if (flagged[r][c]) {
                ctx.fillStyle = '#ff5252';
                ctx.beginPath();
                ctx.arc(x + CELL_SIZE / 2, y + CELL_SIZE / 2, 10, 0, 2 * Math.PI);
                ctx.fill();
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 16px 微软雅黑';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('旗', x + CELL_SIZE / 2, y + CELL_SIZE / 2);
            }

            // 显示数字或地雷
            if (revealed[r][c]) {
                if (board[r][c] === 'M') {
                    ctx.fillStyle = '#333';
                    ctx.font = 'bold 22px 微软雅黑';
                    ctx.fillText('💣', x + CELL_SIZE / 2, y + CELL_SIZE / 2 + 2);
                } else if (board[r][c] > 0) {
                    ctx.fillStyle = '#2db400';
                    ctx.font = 'bold 20px 微软雅黑';
                    ctx.fillText(board[r][c], x + CELL_SIZE / 2, y + CELL_SIZE / 2 + 2);
                }
            }
        }
    }
}

// 翻开格子
function revealCell(r, c) {
    if (revealed[r][c] || flagged[r][c] || gameOver) return;

    revealed[r][c] = true;
    cellsToReveal--;

    if (board[r][c] === 'M') {
        gameOver = true;
        revealAllMines();
        playSound('mineSound');
        setTimeout(() => alert('游戏失败！'), 100);
    } else if (board[r][c] === 0) {
        for (let dr = -1; dr <= 1; dr++) {
            for (let dc = -1; dc <= 1; dc++) {
                if (dr === 0 && dc === 0) continue;
                const nr = r + dr;
                const nc = c + dc;
                if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) {
                    revealCell(nr, nc);
                }
            }
        }
    }

    if (cellsToReveal === 0) {
        gameOver = true;
        playSound('winSound');
        setTimeout(() => alert('恭喜你，扫雷成功！'), 100);
    }

    playSound('openSound');
    drawBoard();
}

// 插旗
function flagCell(r, c) {
    if (revealed[r][c] || gameOver) return;

    flagged[r][c] = !flagged[r][c];
    flagCount += flagged[r][c] ? 1 : -1;
    playSound('flagSound');
    updateInfo();
    drawBoard();
}

// 显示所有地雷
function revealAllMines() {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            if (board[r][c] === 'M') {
                revealed[r][c] = true;
            }
        }
    }
}

// 播放音效
function playSound(id) {
    const sound = document.getElementById(id);
    if (sound) {
        sound.currentTime = 0;
        sound.play();
    }
}

// 更新信息
function updateInfo() {
    document.getElementById('mineCount').textContent = `地雷数: ${MINES_COUNT}`;
    document.getElementById('flagCount').textContent = `已插旗: ${flagCount}`;
}

// 重新开始游戏
function restartGame() {
    initBoard();
    drawBoard();
}

canvas.addEventListener('mousedown', function(e) {
    if (gameOver) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const c = Math.floor(x / CELL_SIZE);
    const r = Math.floor(y / CELL_SIZE);

    if (r < 0 || r >= ROWS || c < 0 || c >= COLS) return;

    if (e.button === 0) {
        // 左键开格
        revealCell(r, c);
    } else if (e.button === 2) {
        // 右键插旗
        flagCell(r, c);
    }
});

canvas.addEventListener('contextmenu', e => e.preventDefault());

// 初始化游戏
initBoard();
drawBoard();