let humanScore = 0;
let computerScore = 0;
let currentRoundNumber = 1;

/**
 * Generates a random number between 0-9
 * @return {Number} a random number between 0-9
 */
function generateTarget() {
  return Math.floor(Math.random() * 9);
}

/**
 * Compares player and computer guesses to see what was closer to the target
 * @param {Number} humanGuess - a number between 0-9
 * @param {Number} computerGuess - a number between 0-9
 * @param {Number} target - a random number between 0-9
 * @return {Boolean} true means the player has won and false the computer wins
 */
function compareGuesses(humanGuess, computerGuess, target) {
  const playerDiff = Math.abs(humanGuess - target);
  const computerDiff = Math.abs(computerGuess - target);
  return playerDiff <= computerDiff ? true : false;
}

/**
 * Increments either the humanScore or computer score depending on the input
 * @param {String} winner - either 'human' or 'computer'
 */
function updateScore(winner) {
  if (winner === "human") {
    humanScore++;
  } else {
    computerScore++;
  }
}

/**
 * Advances the round by incrementing currentRoundNumber by 1
 */
function advanceRound() {
  currentRoundNumber++;
}
