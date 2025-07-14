"""
Juego de Tres en Raya (Tic-Tac-Toe) gráfico con pygame usando el algoritmo Minimax.
"""

import pygame
import sys
import copy
import math
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import time
from typing import List, Tuple, Optional
from .minimax import MinimaxAlgorithm

# Configuración de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
VIOLETA = (128, 0, 128)

class TresEnRayaPygame(MinimaxAlgorithm):
    """
    Implementación gráfica del juego Tres en Raya usando pygame y Minimax.
    """
    
    def __init__(self, use_alpha_beta: bool = True):
        """
        Inicializa el juego de Tres en Raya gráfico.
        
        Args:
            use_alpha_beta (bool): Si usar poda alfa-beta
        """
        super().__init__(use_alpha_beta)
        
        # Configuración del juego
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human_player = 'X'
        self.ai_player = 'O'
        self.current_player = self.human_player
        self.game_over = False
        self.winner = None
        
        # Configuración de pygame
        pygame.init()
        self.VENTANA_TAMAÑO = 600
        self.CELDA_TAMAÑO = self.VENTANA_TAMAÑO // 3
        self.LINEA_GROSOR = 3
        
        # Ventana y fuente
        self.pantalla = pygame.display.set_mode((self.VENTANA_TAMAÑO, self.VENTANA_TAMAÑO + 100))
        pygame.display.set_caption("Tres en Raya - IA con Minimax")
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_grande = pygame.font.Font(None, 72)
        
        # Control de tiempo
        self.reloj = pygame.time.Clock()
        
        # Estados del juego
        self.ai_thinking = False
        self.nodes_evaluated = 0
        
        # Sistema de análisis matemático
        self.game_history = []
        self.analysis_data = {
            'moves': [],
            'nodes_evaluated': [],
            'depth_used': [],
            'time_taken': [],
            'difficulty': []
        }
        self.showing_analysis = False
        self.analysis_button_rect = None
        
        # Sistema de dificultades
        self.difficulty_levels = {
            'Fácil': {'depth': 1, 'random_chance': 0.4, 'color': VERDE},
            'Normal': {'depth': 3, 'random_chance': 0.2, 'color': AMARILLO},
            'Difícil': {'depth': 6, 'random_chance': 0.1, 'color': NARANJA},
            'Imposible': {'depth': 9, 'random_chance': 0.0, 'color': ROJO}
        }
        self.current_difficulty = 'Normal'
        self.showing_difficulty_menu = True
        
    def dibujar_tablero(self):
        """Dibuja el tablero de juego."""
        self.pantalla.fill(BLANCO)
        
        # Dibujar líneas del tablero
        for i in range(1, 3):
            # Líneas verticales
            pygame.draw.line(self.pantalla, NEGRO, 
                           (i * self.CELDA_TAMAÑO, 0), 
                           (i * self.CELDA_TAMAÑO, self.VENTANA_TAMAÑO), 
                           self.LINEA_GROSOR)
            # Líneas horizontales
            pygame.draw.line(self.pantalla, NEGRO, 
                           (0, i * self.CELDA_TAMAÑO), 
                           (self.VENTANA_TAMAÑO, i * self.CELDA_TAMAÑO), 
                           self.LINEA_GROSOR)
        
        # Dibujar X y O
        for fila in range(3):
            for col in range(3):
                if self.board[fila][col] == 'X':
                    self.dibujar_x(fila, col)
                elif self.board[fila][col] == 'O':
                    self.dibujar_o(fila, col)
    
    def dibujar_x(self, fila: int, col: int):
        """Dibuja una X en la posición especificada."""
        margen = 20
        x = col * self.CELDA_TAMAÑO + margen
        y = fila * self.CELDA_TAMAÑO + margen
        x_fin = (col + 1) * self.CELDA_TAMAÑO - margen
        y_fin = (fila + 1) * self.CELDA_TAMAÑO - margen
        
        pygame.draw.line(self.pantalla, AZUL, (x, y), (x_fin, y_fin), 8)
        pygame.draw.line(self.pantalla, AZUL, (x, y_fin), (x_fin, y), 8)
    
    def dibujar_o(self, fila: int, col: int):
        """Dibuja una O en la posición especificada."""
        centro_x = col * self.CELDA_TAMAÑO + self.CELDA_TAMAÑO // 2
        centro_y = fila * self.CELDA_TAMAÑO + self.CELDA_TAMAÑO // 2
        radio = self.CELDA_TAMAÑO // 2 - 20
        
        pygame.draw.circle(self.pantalla, ROJO, (centro_x, centro_y), radio, 8)
    
    def dibujar_menu_dificultad(self):
        """Dibuja el menú de selección de dificultad."""
        self.pantalla.fill(BLANCO)
        
        # Título
        titulo = self.fuente_grande.render("Selecciona la Dificultad", True, NEGRO)
        titulo_rect = titulo.get_rect(center=(self.VENTANA_TAMAÑO//2, 100))
        self.pantalla.blit(titulo, titulo_rect)
        
        # Opciones de dificultad
        y_start = 200
        button_height = 80
        button_width = 400
        
        for i, (difficulty, config) in enumerate(self.difficulty_levels.items()):
            y = y_start + i * (button_height + 20)
            
            # Botón
            button_rect = pygame.Rect(
                (self.VENTANA_TAMAÑO - button_width) // 2,
                y,
                button_width,
                button_height
            )
            
            # Color del botón
            if difficulty == self.current_difficulty:
                pygame.draw.rect(self.pantalla, config['color'], button_rect)
                pygame.draw.rect(self.pantalla, NEGRO, button_rect, 3)
            else:
                pygame.draw.rect(self.pantalla, GRIS_CLARO, button_rect)
                pygame.draw.rect(self.pantalla, NEGRO, button_rect, 2)
            
            # Texto del botón
            text_color = BLANCO if difficulty == self.current_difficulty else NEGRO
            text = self.fuente.render(difficulty, True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.pantalla.blit(text, text_rect)
            
            # Descripción
            descriptions = {
                'Fácil': 'La IA comete errores frecuentes',
                'Normal': 'La IA juega bien pero no perfecta',
                'Difícil': 'La IA juega muy bien',
                'Imposible': 'La IA nunca pierde'
            }
            
            desc_text = self.fuente.render(descriptions[difficulty], True, GRIS)
            desc_rect = desc_text.get_rect(center=(self.VENTANA_TAMAÑO//2, y + button_height + 10))
            self.pantalla.blit(desc_text, desc_rect)
        
        # Instrucciones
        instrucciones = self.fuente.render("Haz clic en una dificultad para jugar", True, NEGRO)
        instrucciones_rect = instrucciones.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 50))
        self.pantalla.blit(instrucciones, instrucciones_rect)
    
    def obtener_click_dificultad(self, pos_mouse: Tuple[int, int]) -> Optional[str]:
        """
        Verifica si se hizo clic en algún botón de dificultad.
        
        Args:
            pos_mouse: Posición del mouse (x, y)
            
        Returns:
            Nombre de la dificultad seleccionada o None
        """
        x, y = pos_mouse
        
        y_start = 200
        button_height = 80
        button_width = 400
        
        for i, difficulty in enumerate(self.difficulty_levels.keys()):
            button_y = y_start + i * (button_height + 20)
            
            button_rect = pygame.Rect(
                (self.VENTANA_TAMAÑO - button_width) // 2,
                button_y,
                button_width,
                button_height
            )
            
            if button_rect.collidepoint(x, y):
                return difficulty
        
        return None
    
    def dibujar_interfaz(self):
        """Dibuja la interfaz del juego."""
        # Área de información
        info_rect = pygame.Rect(0, self.VENTANA_TAMAÑO, self.VENTANA_TAMAÑO, 100)
        pygame.draw.rect(self.pantalla, GRIS_CLARO, info_rect)
        
        # Texto del estado del juego
        if self.game_over:
            if self.winner == 'T':
                texto = "¡Empate!"
                color = GRIS
            elif self.winner == self.human_player:
                texto = "¡Has ganado!"
                color = VERDE
            else:
                texto = "¡La IA ha ganado!"
                color = ROJO
            
            texto_superficie = self.fuente_grande.render(texto, True, color)
            texto_rect = texto_superficie.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 30))
            self.pantalla.blit(texto_superficie, texto_rect)
            
            # Botón para reiniciar
            reiniciar_texto = self.fuente.render("Presiona R para reiniciar o M para el menú", True, NEGRO)
            reiniciar_rect = reiniciar_texto.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 70))
            self.pantalla.blit(reiniciar_texto, reiniciar_rect)
            
        elif self.ai_thinking:
            pensando_texto = self.fuente.render("La IA está pensando...", True, NEGRO)
            pensando_rect = pensando_texto.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 30))
            self.pantalla.blit(pensando_texto, pensando_rect)
            
            # Mostrar estadísticas
            if self.nodes_evaluated > 0:
                stats_texto = self.fuente.render(f"Nodos evaluados: {self.nodes_evaluated}", True, NEGRO)
                stats_rect = stats_texto.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 60))
                self.pantalla.blit(stats_texto, stats_rect)
        
        else:
            if self.current_player == self.human_player:
                turno_texto = self.fuente.render("Tu turno - Haz clic en una celda", True, NEGRO)
            else:
                turno_texto = self.fuente.render("Turno de la IA", True, NEGRO)
            
            turno_rect = turno_texto.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 30))
            self.pantalla.blit(turno_texto, turno_rect)
            
            # Mostrar quién es quién y dificultad
            info_texto = self.fuente.render("Tú: X (Azul) - IA: O (Rojo)", True, NEGRO)
            info_rect = info_texto.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 50))
            self.pantalla.blit(info_texto, info_rect)
            
            # Mostrar dificultad actual
            difficulty_color = self.difficulty_levels[self.current_difficulty]['color']
            dificultad_texto = self.fuente.render(f"Dificultad: {self.current_difficulty}", True, difficulty_color)
            dificultad_rect = dificultad_texto.get_rect(center=(self.VENTANA_TAMAÑO//2, self.VENTANA_TAMAÑO + 80))
            self.pantalla.blit(dificultad_texto, dificultad_rect)
        
        # Mostrar costo de la última jugada si existe
        if len(self.analysis_data['moves']) > 0:
            last_nodes = self.analysis_data['nodes_evaluated'][-1]
            last_time = self.analysis_data['time_taken'][-1] * 1000  # convertir a ms
            self.mostrar_costo_jugada(last_nodes, last_time)
        
        # Dibujar botón de análisis matemático
        self.dibujar_boton_analisis()
    
    def obtener_posicion_clic(self, pos_mouse: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Convierte la posición del mouse en coordenadas del tablero.
        
        Args:
            pos_mouse: Posición del mouse (x, y)
            
        Returns:
            Tupla con (fila, columna) o None si está fuera del tablero
        """
        x, y = pos_mouse
        
        # Verificar si el clic está dentro del tablero
        if x < 0 or x >= self.VENTANA_TAMAÑO or y < 0 or y >= self.VENTANA_TAMAÑO:
            return None
        
        fila = y // self.CELDA_TAMAÑO
        col = x // self.CELDA_TAMAÑO
        
        return (fila, col)
    
    def es_movimiento_valido(self, fila: int, col: int) -> bool:
        """
        Verifica si un movimiento es válido.
        
        Args:
            fila: Fila del movimiento
            col: Columna del movimiento
            
        Returns:
            True si el movimiento es válido
        """
        return (0 <= fila < 3 and 0 <= col < 3 and 
                self.board[fila][col] == ' ')
    
    def realizar_movimiento(self, fila: int, col: int, jugador: str) -> bool:
        """
        Realiza un movimiento en el tablero.
        
        Args:
            fila: Fila del movimiento
            col: Columna del movimiento
            jugador: Jugador que realiza el movimiento
            
        Returns:
            True si el movimiento fue exitoso
        """
        if self.es_movimiento_valido(fila, col):
            self.board[fila][col] = jugador
            return True
        return False
    
    def verificar_ganador(self, board: List[List[str]]) -> Optional[str]:
        """
        Verifica si hay un ganador en el tablero.
        
        Args:
            board: Estado del tablero
            
        Returns:
            'X', 'O' si hay ganador, 'T' si hay empate, None si el juego continúa
        """
        # Verificar filas
        for fila in board:
            if fila[0] == fila[1] == fila[2] != ' ':
                return fila[0]
        
        # Verificar columnas
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != ' ':
                return board[0][col]
        
        # Verificar diagonales
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        
        # Verificar empate
        if all(cell != ' ' for row in board for cell in row):
            return 'T'
        
        return None
    
    # Métodos heredados de MinimaxAlgorithm
    def is_terminal_state(self, state: List[List[str]]) -> bool:
        """Implementa el método abstracto de MinimaxAlgorithm."""
        return self.verificar_ganador(state) is not None
    
    def evaluate_state(self, state: List[List[str]]) -> float:
        """Implementa el método abstracto de MinimaxAlgorithm."""
        winner = self.verificar_ganador(state)
        if winner == self.ai_player:
            return 1.0
        elif winner == self.human_player:
            return -1.0
        elif winner == 'T':
            return 0.0
        else:
            return 0.0
    
    def get_possible_moves(self, state: List[List[str]]) -> List[Tuple[int, int]]:
        """Implementa el método abstracto de MinimaxAlgorithm."""
        moves = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    moves.append((i, j))
        return moves
    
    def make_move(self, state: List[List[str]], move: Tuple[int, int]) -> List[List[str]]:
        """Implementa el método abstracto de MinimaxAlgorithm."""
        new_state = copy.deepcopy(state)
        row, col = move
        
        # Determinar qué jugador hace el movimiento
        moves_count = sum(1 for i in range(3) for j in range(3) if state[i][j] != ' ')
        current_player = self.human_player if moves_count % 2 == 0 else self.ai_player
        
        new_state[row][col] = current_player
        return new_state
    
    def obtener_movimiento_ia(self) -> Tuple[int, int]:
        """
        Obtiene el mejor movimiento para la IA según la dificultad.
        
        Returns:
            Tupla con (fila, columna) del mejor movimiento
        """
        difficulty_config = self.difficulty_levels[self.current_difficulty]
        
        # Medir tiempo de ejecución
        start_time = time.time()
        
        # Probabilidad de hacer un movimiento aleatorio (para reducir dificultad)
        if random.random() < difficulty_config['random_chance']:
            # Hacer un movimiento aleatorio
            possible_moves = self.get_possible_moves(self.board)
            if possible_moves:
                move = random.choice(possible_moves)
                end_time = time.time()
                
                # Registrar datos para análisis
                move_number = len(self.analysis_data['moves']) + 1
                self.analysis_data['moves'].append(move_number)
                self.analysis_data['nodes_evaluated'].append(1)  # Movimiento aleatorio
                self.analysis_data['depth_used'].append(1)
                self.analysis_data['time_taken'].append(end_time - start_time)
                self.analysis_data['difficulty'].append(self.current_difficulty)
                
                return move
        
        # Usar minimax con la profundidad según dificultad
        self.nodes_evaluated = 0
        best_move = self.get_best_move(
            self.board, 
            depth=difficulty_config['depth'], 
            maximizing_player=True
        )
        stats = self.get_stats()
        self.nodes_evaluated = stats['nodes_evaluated']
        
        end_time = time.time()
        
        # Registrar datos para análisis
        move_number = len(self.analysis_data['moves']) + 1
        self.analysis_data['moves'].append(move_number)
        self.analysis_data['nodes_evaluated'].append(self.nodes_evaluated)
        self.analysis_data['depth_used'].append(difficulty_config['depth'])
        self.analysis_data['time_taken'].append(end_time - start_time)
        self.analysis_data['difficulty'].append(self.current_difficulty)
        
        return best_move
    
    def reiniciar_juego(self):
        """Reinicia el juego."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = self.human_player
        self.game_over = False
        self.winner = None
        self.ai_thinking = False
        self.nodes_evaluated = 0
    
    def volver_al_menu(self):
        """Vuelve al menú de dificultad."""
        self.reiniciar_juego()
        self.showing_difficulty_menu = True
    
    def mostrar_analisis_matematico(self):
        """Muestra el análisis matemático del algoritmo Minimax usando matplotlib."""
        if not self.analysis_data['moves']:
            print("No hay datos para mostrar")
            return
        
        # Crear figura con subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análisis Matemático del Algoritmo Minimax', fontsize=16, fontweight='bold')
        
        # Gráfico 1: Nodos evaluados por movimiento
        ax1.bar(self.analysis_data['moves'], self.analysis_data['nodes_evaluated'], 
                color='skyblue', edgecolor='navy', alpha=0.7)
        ax1.set_title('Nodos Evaluados por Movimiento')
        ax1.set_xlabel('Número de Movimiento')
        ax1.set_ylabel('Nodos Evaluados')
        ax1.grid(True, alpha=0.3)
        
        # Agregar texto con estadísticas
        total_nodes = sum(self.analysis_data['nodes_evaluated'])
        avg_nodes = total_nodes / len(self.analysis_data['nodes_evaluated'])
        ax1.text(0.02, 0.98, f'Total: {total_nodes}\nPromedio: {avg_nodes:.1f}', 
                transform=ax1.transAxes, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Gráfico 2: Tiempo de ejecución por movimiento
        ax2.plot(self.analysis_data['moves'], 
                [t * 1000 for t in self.analysis_data['time_taken']], 
                marker='o', linewidth=2, markersize=6, color='red')
        ax2.set_title('Tiempo de Ejecución por Movimiento')
        ax2.set_xlabel('Número de Movimiento')
        ax2.set_ylabel('Tiempo (ms)')
        ax2.grid(True, alpha=0.3)
        
        # Agregar estadísticas de tiempo
        total_time = sum(self.analysis_data['time_taken']) * 1000
        avg_time = total_time / len(self.analysis_data['time_taken'])
        ax2.text(0.02, 0.98, f'Total: {total_time:.1f}ms\nPromedio: {avg_time:.1f}ms', 
                transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Gráfico 3: Profundidad utilizada
        ax3.scatter(self.analysis_data['moves'], self.analysis_data['depth_used'], 
                   c=self.analysis_data['nodes_evaluated'], cmap='viridis', 
                   s=100, alpha=0.7, edgecolors='black')
        ax3.set_title('Profundidad vs Nodos Evaluados')
        ax3.set_xlabel('Número de Movimiento')
        ax3.set_ylabel('Profundidad Utilizada')
        ax3.grid(True, alpha=0.3)
        
        # Agregar colorbar
        cbar = plt.colorbar(ax3.collections[0], ax=ax3)
        cbar.set_label('Nodos Evaluados')
        
        # Gráfico 4: Análisis de complejidad
        moves_array = np.array(self.analysis_data['moves'])
        nodes_array = np.array(self.analysis_data['nodes_evaluated'])
        
        ax4.semilogy(moves_array, nodes_array, 'bo-', label='Nodos Evaluados')
        
        # Agregar líneas de referencia de complejidad
        if len(moves_array) > 1:
            # Complejidad exponencial teórica
            theoretical_exp = [3 ** (9 - i) for i in moves_array]
            ax4.semilogy(moves_array, theoretical_exp, 'r--', alpha=0.5, label='O(3^n) Teórico')
            
            # Complejidad con poda alfa-beta
            theoretical_pruned = [3 ** ((9 - i) * 0.5) for i in moves_array]
            ax4.semilogy(moves_array, theoretical_pruned, 'g--', alpha=0.5, label='O(3^(n/2)) con poda')
        
        ax4.set_title('Complejidad Temporal del Algoritmo')
        ax4.set_xlabel('Número de Movimiento')
        ax4.set_ylabel('Nodos Evaluados (log scale)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Agregar texto explicativo
        explanation = (
            "Análisis:\n"
            "• El algoritmo Minimax explora el árbol de decisiones\n"
            "• La poda alfa-beta reduce significativamente los nodos evaluados\n"
            "• A medida que el juego progresa, hay menos movimientos posibles\n"
            "• El tiempo de ejecución es proporcional a los nodos evaluados"
        )
        
        plt.figtext(0.02, 0.02, explanation, fontsize=10, 
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        plt.show()
    
    def mostrar_costo_jugada(self, nodos_evaluados: int, tiempo_ms: float):
        """Muestra el costo de la jugada actual en la interfaz."""
        if nodos_evaluados > 0:
            # Área para mostrar el costo
            costo_rect = pygame.Rect(10, self.VENTANA_TAMAÑO + 5, 300, 90)
            pygame.draw.rect(self.pantalla, (240, 240, 240), costo_rect)
            pygame.draw.rect(self.pantalla, NEGRO, costo_rect, 2)
            
            # Título
            titulo_costo = self.fuente.render("Costo de la Jugada IA:", True, NEGRO)
            self.pantalla.blit(titulo_costo, (15, self.VENTANA_TAMAÑO + 10))
            
            # Nodos evaluados
            nodos_texto = self.fuente.render(f"Nodos: {nodos_evaluados}", True, AZUL)
            self.pantalla.blit(nodos_texto, (15, self.VENTANA_TAMAÑO + 35))
            
            # Tiempo
            tiempo_texto = self.fuente.render(f"Tiempo: {tiempo_ms:.1f}ms", True, ROJO)
            self.pantalla.blit(tiempo_texto, (15, self.VENTANA_TAMAÑO + 60))
    
    def dibujar_boton_analisis(self):
        """Dibuja el botón para mostrar el análisis matemático."""
        if len(self.analysis_data['moves']) > 0:
            # Posición del botón
            button_width = 150
            button_height = 40
            button_x = self.VENTANA_TAMAÑO - button_width - 10
            button_y = self.VENTANA_TAMAÑO + 50
            
            self.analysis_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            # Dibujar botón
            pygame.draw.rect(self.pantalla, VIOLETA, self.analysis_button_rect)
            pygame.draw.rect(self.pantalla, NEGRO, self.analysis_button_rect, 2)
            
            # Texto del botón
            button_text = self.fuente.render("Ver Análisis", True, BLANCO)
            text_rect = button_text.get_rect(center=self.analysis_button_rect.center)
            self.pantalla.blit(button_text, text_rect)
    
    def verificar_click_analisis(self, pos_mouse: Tuple[int, int]) -> bool:
        """Verifica si se hizo clic en el botón de análisis."""
        if self.analysis_button_rect and self.analysis_button_rect.collidepoint(pos_mouse):
            return True
        return False
    
    def ejecutar_juego(self):
        """
        Ejecuta el bucle principal del juego.
        """
        ejecutando = True
        
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if self.game_over:
                        if evento.key == pygame.K_r:
                            self.reiniciar_juego()
                        elif evento.key == pygame.K_m:
                            self.volver_al_menu()
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.showing_difficulty_menu:
                        # Manejo del menú de dificultad
                        difficulty_selected = self.obtener_click_dificultad(evento.pos)
                        if difficulty_selected:
                            self.current_difficulty = difficulty_selected
                            self.showing_difficulty_menu = False
                            self.reiniciar_juego()
                    
                    elif not self.game_over and not self.ai_thinking and self.current_player == self.human_player:
                        # Verificar si se hizo clic en el botón de análisis
                        if self.verificar_click_analisis(evento.pos):
                            self.mostrar_analisis_matematico()
                        else:
                            # Manejo del juego
                            pos_clic = self.obtener_posicion_clic(evento.pos)
                            if pos_clic:
                                fila, col = pos_clic
                                if self.realizar_movimiento(fila, col, self.human_player):
                                    self.winner = self.verificar_ganador(self.board)
                                    if self.winner:
                                        self.game_over = True
                                    else:
                                        self.current_player = self.ai_player
                                        self.ai_thinking = True
                    
                    elif self.game_over:
                        # Permitir ver análisis incluso cuando el juego terminó
                        if self.verificar_click_analisis(evento.pos):
                            self.mostrar_analisis_matematico()
            
            # Turno de la IA
            if not self.showing_difficulty_menu and not self.game_over and self.current_player == self.ai_player and self.ai_thinking:
                # Pequeña pausa para mostrar el mensaje de "pensando"
                pygame.time.wait(500)
                
                fila, col = self.obtener_movimiento_ia()
                self.realizar_movimiento(fila, col, self.ai_player)
                
                self.winner = self.verificar_ganador(self.board)
                if self.winner:
                    self.game_over = True
                else:
                    self.current_player = self.human_player
                
                self.ai_thinking = False
            
            # Dibujar todo
            if self.showing_difficulty_menu:
                self.dibujar_menu_dificultad()
            else:
                self.dibujar_tablero()
                self.dibujar_interfaz()
            
            pygame.display.flip()
            self.reloj.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    """Función principal para ejecutar el juego."""
    juego = TresEnRayaPygame(use_alpha_beta=True)
    juego.ejecutar_juego()


if __name__ == "__main__":
    main()
