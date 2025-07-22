import copy
from typing import List, Tuple, Optional
from .minimax import MinimaxAlgorithm

class TresEnRaya(MinimaxAlgorithm):
    def __init__(self, use_alpha_beta: bool = True):
        super().__init__(use_alpha_beta)
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human_player = 'X'
        self.ai_player = 'O'
        self.current_player = self.human_player
    
    def print_board(self):
        print("\n   0   1   2")
        for i in range(3):
            print(f"{i}  {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}")
            if i < 2:
                print("  -----------")
    
    def is_valid_move(self, row: int, col: int) -> bool:
        return (0 <= row < 3 and 0 <= col < 3 and 
                self.board[row][col] == ' ')
    
    def make_move_on_board(self, row: int, col: int, player: str) -> bool:
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self, board: List[List[str]]) -> Optional[str]:
        for row in board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != ' ':
                return board[0][col]
        
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        
        if all(cell != ' ' for row in board for cell in row):
            return 'T'
        
        return None
    
    def is_terminal_state(self, state: List[List[str]]) -> bool:
        return self.check_winner(state) is not None
    
    def evaluate_state(self, state: List[List[str]]) -> float:
        winner = self.check_winner(state)
        if winner == self.ai_player:
            return 1.0
        elif winner == self.human_player:
            return -1.0
        elif winner == 'T':
            return 0.0
        else:
            return 0.0
    
    def get_possible_moves(self, state: List[List[str]]) -> List[Tuple[int, int]]:
        moves = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def make_move(self, state: List[List[str]], move: Tuple[int, int]) -> List[List[str]]:
        new_state = copy.deepcopy(state)
        row, col = move
        
        moves_count = sum(1 for i in range(3) for j in range(3) if state[i][j] != ' ')
        current_player = self.human_player if moves_count % 2 == 0 else self.ai_player
        
        new_state[row][col] = current_player
        return new_state
    
    def get_ai_move(self) -> Tuple[int, int]:
        best_move = self.get_best_move(self.board, depth=9, maximizing_player=True)
        return best_move
    
    def get_human_move(self) -> Tuple[int, int]:
        while True:
            try:
                row = int(input("Ingresa la fila (0-2): "))
                col = int(input("Ingresa la columna (0-2): "))
                
                if self.is_valid_move(row, col):
                    return (row, col)
                else:
                    print("Movimiento inválido. Intenta de nuevo.")
            except ValueError:
                print("Por favor, ingresa números válidos.")
    
    def reset_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = self.human_player
    
    def play_game(self):
        print("¡Bienvenido al juego de Tres en Raya!")
        print("Tú eres 'X' y la IA es 'O'")
        print("Las coordenadas van de 0 a 2")
        
        while True:
            self.print_board()
            
            winner = self.check_winner(self.board)
            if winner:
                if winner == 'T':
                    print("\n¡Empate!")
                elif winner == self.human_player:
                    print("\n¡Felicitaciones! ¡Has ganado!")
                else:
                    print("\n¡La IA ha ganado!")
                break
            
            if self.current_player == self.human_player:
                print(f"\nTurno del jugador ({self.human_player})")
                row, col = self.get_human_move()
                self.make_move_on_board(row, col, self.human_player)
                self.current_player = self.ai_player
                
            else:
                print(f"\nTurno de la IA ({self.ai_player})")
                print("La IA está pensando...")
                row, col = self.get_ai_move()
                self.make_move_on_board(row, col, self.ai_player)
                print(f"La IA jugó en ({row}, {col})")
                
                # Mostrar estadísticas
                stats = self.get_stats()
                print(f"Nodos evaluados: {stats['nodes_evaluated']}")
                
                self.current_player = self.human_player
        
        play_again = input("\n¿Quieres jugar de nuevo? (s/n): ").lower().strip()
        if play_again == 's' or play_again == 'sí':
            self.reset_game()
            self.play_game()


def main():
    game = TresEnRaya(use_alpha_beta=True)
    game.play_game()


if __name__ == "__main__":
    main()
