"""
Implementación del algoritmo Minimax para juegos de dos jugadores.
Este algoritmo es utilizado para tomar decisiones óptimas en juegos de suma cero.
"""

import math
from typing import List, Tuple, Any, Optional

class MinimaxAlgorithm:
    """
    Clase que implementa el algoritmo Minimax con poda alfa-beta opcional.
    """
    
    def __init__(self, use_alpha_beta: bool = True):
        """
        Inicializa el algoritmo Minimax.
        
        Args:
            use_alpha_beta (bool): Si usar poda alfa-beta para optimizar el algoritmo
        """
        self.use_alpha_beta = use_alpha_beta
        self.nodes_evaluated = 0
    
    def minimax(self, state: Any, depth: int, maximizing_player: bool, 
                alpha: float = -math.inf, beta: float = math.inf) -> Tuple[float, Optional[Any]]:
        """
        Implementa el algoritmo Minimax con poda alfa-beta opcional.
        
        Args:
            state: Estado actual del juego
            depth: Profundidad máxima de búsqueda
            maximizing_player: True si es el turno del jugador maximizador
            alpha: Valor alfa para poda alfa-beta
            beta: Valor beta para poda alfa-beta
            
        Returns:
            Tupla con (valor_evaluado, mejor_movimiento)
        """
        self.nodes_evaluated += 1
        
        # Caso base: profundidad 0 o estado terminal
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
                
                # Poda alfa-beta
                if self.use_alpha_beta:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break  # Poda beta
            
            return max_eval, best_move
        
        else:
            min_eval = math.inf
            for move in self.get_possible_moves(state):
                new_state = self.make_move(state, move)
                eval_score, _ = self.minimax(new_state, depth - 1, True, alpha, beta)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                # Poda alfa-beta
                if self.use_alpha_beta:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Poda alfa
            
            return min_eval, best_move
    
    def get_best_move(self, state: Any, depth: int = 6, maximizing_player: bool = True) -> Any:
        """
        Obtiene el mejor movimiento para el estado actual.
        
        Args:
            state: Estado actual del juego
            depth: Profundidad de búsqueda
            maximizing_player: Si es el turno del jugador maximizador
            
        Returns:
            El mejor movimiento encontrado
        """
        self.nodes_evaluated = 0
        _, best_move = self.minimax(state, depth, maximizing_player)
        return best_move
    
    def get_stats(self) -> dict:
        """
        Obtiene estadísticas del último cálculo.
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            "nodes_evaluated": self.nodes_evaluated,
            "alpha_beta_enabled": self.use_alpha_beta
        }
