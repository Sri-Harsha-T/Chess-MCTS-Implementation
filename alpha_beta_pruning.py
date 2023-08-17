import chess
import chess.pgn
import chess.engine
from sympy import evaluate

eval_dict = {'p' : -1, 'kn' : -3, 'b' : -3, 'r' : -5, 'q' : -9, 'ki' : -10**5, 'KI' : 10**5, 'Q' : 9, 'R' : 5, 'B' : 3, 'KN' : 3, 'P' : 1}

def eval(pos):
    global eval_dict
    score = 0
    for i in pos:
        if (i not in eval_dict):
            continue
        score+=eval_dict[i]
    return score

def mini_max(temp_board, all_moves, white, over, depth, alpha = -10**5-5, beta = 10**5+5):
    posi = temp_board.fen()

    if (over or depth == 0):
        if(over):
            if(temp_board.result()[0]=='1'):
                return (temp_board, 10**5+1, '')
            elif(temp_board.result()[-1]=='1'):
                return (temp_board, -10**5-1, '')
            else :
                return (temp_board, 0, '')
        
        if(white):
            mx = -10**5
            move = ''
            for i in all_moves:
                temp_board.push_san(i)

                all_moves = [temp_board.san(i) for i in list(temp_board.legal_moves)]
                val = eval(temp_board.fen().split()[0])

                if(mx<val):
                    mx = val
                    move = i
                alpha = max(alpha, mx)
                if(beta<=alpha):
                    temp_board = chess.Board(fen=posi)
                    break
                temp_board = chess.Board(posi)
            return (temp_board, mx, move)
        else:
            mn = 10**5
            move = ''
            for i in all_moves:
                temp_board.push_san(i)
                all_moves = [temp_board.san(i) for i in list(temp_board.legal_moves)]
                val = eval(temp_board.fen().split()[0])

                if(mn>val):
                    mn = val
                    move = i
                beta = min(beta, mn)
                if(beta <= alpha):
                    temp_board = chess.Board(posi)
                    break
                temp_board = chess.Board(posi)
            return (temp_board, mn, move)
        
    if (white):
        mx = -10**6
        move = ''
        for i in all_moves:
            temp_board.push_san(i)

            temp_all_moves = [temp_board.san(i) for i in list(temp_board.legal_moves)]
            val = mini_max(temp_board, temp_all_moves, 0, temp_board.is_game_over(), depth-1, alpha, beta)
            if(mx<val[1]):
                mx = val[1]
                move = i
            temp_board = chess.Board(posi)
            alpha = max(alpha, mx)
            if(beta <= alpha):
                temp_board = chess.Board(posi)
                break
            temp_board = chess.Board(posi)
        return (temp_board, mx, move)
    else:
        mn = 10**6
        move = ''
        for i in all_moves:
            temp_board.push_san(i)
            temp_all_moves = [temp_board.san(i) for i in list(temp_board.legal_moves)]
            val = mini_max(temp_board, temp_all_moves,1,temp_board, temp_board.is_game_over(), depth-1, alpha, beta)
            if(mn>val[1]):
                mn = val[1]
                move = i
            temp_board = chess.Board(posi)
            beta = min(beta, mn)
            if(beta<=alpha):
                temp_board = chess.Board(posi)
                break
            temp_board = chess.Board(posi)
            return (temp_board, mn, move)

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(r'C:\Sri Harsha\\IITB\\Projects\\Chess-Engine\stockfish_15_win_x64')

white = 1
moves = 0
pgn = []
game = chess.pgn.Game()
evaluations = []

while((not board.is_game_over())):
    all_moves = [board.san(i) for i in list(board.legal_moves)]
    if(white):
        result = mini_max(board, all_moves, 1, board.is_game_over(), 1)
        board = result[0]
        pgn.append(result[2])
        board.push_san(result[2])
        white ^= 1
    else : 
        result = engine.play(board, chess.engine.Limit(time=0.1))
        pgn.append(board.san(result.move))
        board.push_san(board.san(result.move))
        white ^= 1
    moves+=1
    board_eval = evaluate(board.fen().split()[0])
    evaluations.append(board_eval)
print(board)
print("".join(pgn))
print()
print(evaluations)
print(board.result())
game.headers["Result"] = board.result()

engine.quit()

