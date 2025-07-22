import math
from typing import List, Tuple, Any, Optional

class MinimaxAlgorithm:
    def __init__(self, use_alpha_beta: bool = True):
        self.use_alpha_beta = use_alpha_beta
        self.nodes_evaluated = 0
    
    def minimax(self, state: Any, depth: int, maximizing_player: bool, 
                alpha: float = -math.inf, beta: float = math.inf) -> Tuple[float, Optional[Any]]:
        self.nodes_evaluated += 1
        
        if depth == 0 or self.is_terminal_state(state):
            return self.evaluate_state(state), None
        
        best_move = None
        
        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_possible_moves(state):
                new_state = self.make_move(state, move)
                eval_score, _ = self.minimax(new_state, depth - 1, False, alpha, beta)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                if self.use_alpha_beta:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            
            return max_eval, best_move
        
        else:
            min_eval = math.inf
            for move in self.get_possible_moves(state):
                new_state = self.make_move(state, move)
                eval_score, _ = self.minimax(new_state, depth - 1, True, alpha, beta)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                if self.use_alpha_beta:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            
            return min_eval, best_move
    
    def get_best_move(self, state: Any, depth: int = 6, maximizing_player: bool = True) -> Any:
        self.nodes_evaluated = 0
        _, best_move = self.minimax(state, depth, maximizing_player)
        return best_move
    
    def get_stats(self) -> dict:
        return {
            "nodes_evaluated": self.nodes_evaluated,
            "alpha_beta_enabled": self.use_alpha_beta
        }
    
    def is_terminal_state(self, state: Any) -> bool:
        raise NotImplementedError("Must implement is_terminal_state")
    
    def evaluate_state(self, state: Any) -> float:
        raise NotImplementedError("Must implement evaluate_state")
    
    def get_possible_moves(self, state: Any) -> List[Any]:
        raise NotImplementedError("Must implement get_possible_moves")
    
    def make_move(self, state: Any, move: Any) -> Any:
        raise NotImplementedError("Must implement make_move")

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.human_player = "O"
        self.ai_player = "X"
    
    def print_board(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("---------")
    
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]
    
    def make_move(self, index, player):
        if self.board[index] == " ":
            self.board[index] = player
            return True
        return False
    
    def undo_move(self, index):
        self.board[index] = " "
    
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] and 
                self.board[combo[0]] != " "):
                return self.board[combo[0]]
        
        if " " not in self.board:
            return "tie"
        
        return None
    
    def is_game_over(self):
        return self.check_winner() is not None
    
    def evaluate(self):
        winner = self.check_winner()
        if winner == self.ai_player:
            return 10
        elif winner == self.human_player:
            return -10
        else:
            return 0
    
    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        
        if winner == self.ai_player:
            return 10 - depth
        elif winner == self.human_player:
            return depth - 10
        elif winner == "tie":
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self.available_moves():
                self.make_move(move, self.ai_player)
                score = self.minimax(depth + 1, False)
                self.undo_move(move)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.make_move(move, self.human_player)
                score = self.minimax(depth + 1, True)
                self.undo_move(move)
                best_score = min(score, best_score)
            return best_score
    
    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        
        for move in self.available_moves():
            self.make_move(move, self.ai_player)
            score = self.minimax(0, False)
            self.undo_move(move)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
