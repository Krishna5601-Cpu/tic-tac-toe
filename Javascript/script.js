const cells = document.querySelectorAll(".cell");

const statusText = document.getElementById("status");

const xScoreEl = document.getElementById("xScore");
const oScoreEl = document.getElementById("oScore");
const drawScoreEl = document.getElementById("drawScore");

const startBtn = document.getElementById("startBtn");
const restartBtn = document.getElementById("restartBtn");
const resetScoreBtn = document.getElementById("resetScoreBtn");
const statsBtn = document.getElementById("statsBtn");

let board = Array(9).fill("");

let currentPlayer = "X";

let gameOver = false;

let playerX = "Player X";
let playerO = "Player O";

let xScore = Number(localStorage.getItem("xScore")) || 0;
let oScore = Number(localStorage.getItem("oScore")) || 0;
let drawScore = Number(localStorage.getItem("drawScore")) || 0;
let gamesPlayed = Number(localStorage.getItem("gamesPlayed")) || 0;

const winningCombinations = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],

  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],

  [0, 4, 8],
  [2, 4, 6],
];

updateScores();

startBtn.addEventListener("click", () => {
  playerX = document.getElementById("player1").value.trim() || "Player X";

  playerO = document.getElementById("player2").value.trim() || "Player O";

  updateStatus();
});

cells.forEach((cell) => {
  cell.addEventListener("click", handleCellClick);
});

restartBtn.addEventListener("click", restartGame);

resetScoreBtn.addEventListener("click", () => {
  if (!confirm("Reset all scores?")) return;

  xScore = 0;
  oScore = 0;
  drawScore = 0;
  gamesPlayed = 0;

  saveScores();
  updateScores();
});

statsBtn.addEventListener("click", () => {
  alert(`
Games Played: ${gamesPlayed}

${playerX} Wins: ${xScore}
${playerO} Wins: ${oScore}
Draws: ${drawScore}
`);
});

function handleCellClick(e) {
  const index = e.target.dataset.index;

  if (board[index] !== "" || gameOver) {
    return;
  }

  board[index] = currentPlayer;

  e.target.textContent = currentPlayer;

  e.target.classList.add(currentPlayer.toLowerCase());

  const result = checkWinner();

  if (result) {
    gameOver = true;

    result.forEach((index) => {
      cells[index].classList.add("winner");
    });

    gamesPlayed++;

    if (currentPlayer === "X") {
      xScore++;
    } else {
      oScore++;
    }

    saveScores();
    updateScores();

    const winner = currentPlayer === "X" ? playerX : playerO;

    statusText.textContent = `🏆 ${winner} Wins!`;

    return;
  }

  if (!board.includes("")) {
    gameOver = true;

    drawScore++;
    gamesPlayed++;

    saveScores();
    updateScores();

    statusText.textContent = "🤝 Match Drawn!";

    return;
  }

  currentPlayer = currentPlayer === "X" ? "O" : "X";

  updateStatus();
}

function checkWinner() {
  for (const combo of winningCombinations) {
    const [a, b, c] = combo;

    if (board[a] && board[a] === board[b] && board[b] === board[c]) {
      return combo;
    }
  }

  return null;
}

function restartGame() {
  if (!confirm("Restart current game?")) {
    return;
  }

  board = Array(9).fill("");

  gameOver = false;

  currentPlayer = "X";

  cells.forEach((cell) => {
    cell.textContent = "";

    cell.classList.remove("x", "o", "winner");
  });

  updateStatus();
}

function updateStatus() {
  const currentName = currentPlayer === "X" ? playerX : playerO;

  statusText.textContent = `🎯 ${currentName}'s Turn (${currentPlayer})`;
}

function updateScores() {
  xScoreEl.textContent = `X: ${xScore}`;

  oScoreEl.textContent = `O: ${oScore}`;

  drawScoreEl.textContent = `Draws: ${drawScore}`;
}

function saveScores() {
  localStorage.setItem("xScore", xScore);

  localStorage.setItem("oScore", oScore);

  localStorage.setItem("drawScore", drawScore);

  localStorage.setItem("gamesPlayed", gamesPlayed);
}
