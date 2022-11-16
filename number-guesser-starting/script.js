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
* @param {Number} playerGuess - a number between 0-9
* @param {Number} computerGuess - a number between 0-9
* @param {Number} target - a random number between 0-9
* @return {Boolean} true means the player has won and false the computer wins
*/
function compareGuesses(playerGuess, computerGuess, target) {
  const playerDiff = Math.abs(playerGuess - target);
  const computerDiff = Math.abs(computerGuess - target);
  return playerDiff <= computerDiff ? true : false;
}

function main() {
  const target = generateTarget();
  console.log(target);
  const winner = compareGuesses(4, 6, target);
  console.log(winner);
}

main();
