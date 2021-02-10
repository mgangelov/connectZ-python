import sys, re
import errorCodes

cmdLineArguments = sys.argv[1:]

boardWidth=0
boardHeight=0
boardWinCondition=0
board=[]
boardColumnsCurrentHeight=[]

isFirstPlayerTurn=True

overallMoveCount=0
currentMoveCount=0

def formatPlayerWinningCondition(playerId):
  return str([playerId for _ in range(boardWinCondition)])

def isValidWinCondition():
  '''Determines whether the winning condition is valid
  by comparing it to the board diagonal - the largest
  possible line within the dimensions
  '''
  maxBoardDiagonalLength = max(boardWidth, boardHeight)
  return boardWinCondition <= maxBoardDiagonalLength


def initBoardDimensions(boardDimensionRow):
  global boardWidth
  global boardHeight
  global boardWinCondition
  global board
  global boardColumnsCurrentHeight
  if not re.match(r'\d+ \d+ \d+', boardDimensionRow):
    print(errorCodes.FILE_INVALID)
    sys.exit()
  [
    boardWidth,
    boardHeight,
    boardWinCondition
  ] = list(map(int, boardDimensionRow.split(' ')))
  board = [
    [0 for _ in range(boardWidth)] for _ in range(boardHeight)
  ]
  boardColumnsCurrentHeight = [0 for _ in range(boardWidth)]
  if not isValidWinCondition():
    print(errorCodes.GAME_ILLEGAL)
    sys.exit()


def printBoard(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
  table = [fmt.format(*row) for row in s]
  print('\n'.join(table))

def checkVertical(column, playerId):
  # Using strings for easy check of winning sequences 
  playerWinningCondition = formatPlayerWinningCondition((playerId)) 
  columnElements = str([board[x][column] for x in range(boardHeight)])
  return playerWinningCondition in columnElements

def checkHorizontal(column, playerId):
  # Using strings for easy check of winning sequences
  row = boardColumnsCurrentHeight[column]
  playerWinningCondition = formatPlayerWinningCondition((playerId)) 
  rowElements = str(
    [board[row-1][x] for x in range(boardWidth)]
  )
  return playerWinningCondition in rowElements


def checkDiagonals(column, playerId):
  row = boardColumnsCurrentHeight[column] - 1
  playerWinningCondition = formatPlayerWinningCondition((playerId))
  maxdiagonalSize = max(boardHeight, boardWidth)
  diagonal1 = str([board[i][i-column+row] for i in range(maxdiagonalSize) if i-column+row in range(boardHeight)])
  diagonal2 = str([board[i][column+row-i] for i in range(maxdiagonalSize) if column+row-i in range(boardWidth)])
  
  return playerWinningCondition in diagonal1 or playerWinningCondition in diagonal2

def checkIfBoardWin(lastMove, playerId):
  return (
    checkVertical(lastMove, playerId) or
    checkHorizontal(lastMove, playerId) or
    checkDiagonals(lastMove, playerId)
  )

def runMove(move):
  global board
  global isFirstPlayerTurn
  global currentMoveCount
  normalisedMove = move - 1
  if normalisedMove >= boardWidth:
    print(errorCodes.GAME_ILLEGAL_COLUMN)
    sys.exit()
  currentPlayerId = 1 if isFirstPlayerTurn else 2
  if boardColumnsCurrentHeight[normalisedMove] + 1 > boardHeight:
    print(errorCodes.GAME_ILLEGAL_ROW)
    sys.exit()
  board[boardColumnsCurrentHeight[normalisedMove]][normalisedMove] = (
    currentPlayerId # Setting playerId on location played)
  )
  currentMoveCount += 1
  boardColumnsCurrentHeight[normalisedMove] += 1
  if checkIfBoardWin(normalisedMove, currentPlayerId):
    if currentMoveCount < overallMoveCount:
      print(errorCodes.GAME_ILLEGAL_CONTINUE)
      sys.exit()
    elif currentMoveCount == overallMoveCount: # Winning condition
      print(currentPlayerId)
      # printBoard(board)
      sys.exit()
  isFirstPlayerTurn = not isFirstPlayerTurn

def countLinesInFile(file):
  with open(file) as f:
      for i, _ in enumerate(f):
          pass
  return i + 1

def main():
  global overallMoveCount
  if len(cmdLineArguments) <= 0:
    print('connectz.py: Provide one input file')
    sys.exit()


  gameSpecFilename = cmdLineArguments[0]
  
  try:
    overallMoveCount = countLinesInFile(gameSpecFilename) - 1
    with open(gameSpecFilename) as gameSpecFile:
      initBoardDimensions(gameSpecFile.readline())
      for move in gameSpecFile:
        if not re.match(r'\d+', move):
          print(errorCodes.FILE_INVALID)
          sys.exit()
        runMove(int(move))
    boardSize = boardWidth * boardHeight
    if overallMoveCount == boardSize: # Board is full after all moves
      print(errorCodes.GAME_DRAW)
      sys.exit()
    elif overallMoveCount < boardSize:
      print(errorCodes.GAME_INCOMPLETE)
      sys.exit()
  except FileNotFoundError:
    print('File does not exist')
    print(errorCodes.FILE_ERROR)
    sys.exit()

if __name__ == "__main__":
    main()