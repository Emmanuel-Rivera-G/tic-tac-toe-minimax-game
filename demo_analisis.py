"""
Demostración del análisis matemático del algoritmo Minimax.
Este archivo muestra cómo se comporta el algoritmo con diferentes configuraciones.
"""

import matplotlib.pyplot as plt
import numpy as np
import time

from src.tic_tac_toe_minimax_game.tres_en_raya_pygame import TresEnRayaPygame

def ejecutar_demo_analisis():
    """
    Ejecuta una demostración del análisis matemático del algoritmo Minimax.
    """
    print("🎮 Demostración del Análisis Matemático del Algoritmo Minimax")
    print("=" * 60)
    
    # Crear una instancia del juego
    juego = TresEnRayaPygame(use_alpha_beta=True)
    
    # Simular varios movimientos de la IA para recopilar datos
    print("📊 Simulando movimientos de la IA...")
    
    # Configurar diferentes tableros de prueba
    tableros_prueba = [
        # Tablero vacío
        [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']],
        
        # Tablero con algunos movimientos
        [['X', ' ', ' '],
         [' ', 'O', ' '],
         [' ', ' ', ' ']],
        
        # Tablero más avanzado
        [['X', 'O', 'X'],
         ['O', 'X', ' '],
         [' ', ' ', ' ']],
        
        # Tablero cerca del final
        [['X', 'O', 'X'],
         ['O', 'X', 'O'],
         [' ', ' ', ' ']]
    ]
    
    dificultades = ['Fácil', 'Normal', 'Difícil', 'Imposible']
    
    for i, tablero in enumerate(tableros_prueba):
        print(f"\n🎯 Analizando tablero {i+1}...")
        
        for dificultad in dificultades:
            juego.board = [fila[:] for fila in tablero]  # Copiar el tablero
            juego.current_difficulty = dificultad
            
            # Medir el rendimiento
            start_time = time.time()
            
            try:
                if juego.get_possible_moves(juego.board):
                    move = juego.obtener_movimiento_ia()
                    end_time = time.time()
                    
                    print(f"  {dificultad:>10}: {juego.nodes_evaluated:>6} nodos, "
                          f"{(end_time - start_time)*1000:>6.1f}ms")
                else:
                    print(f"  {dificultad:>10}: No hay movimientos posibles")
            except Exception as e:
                print(f"  {dificultad:>10}: Error - {str(e)}")
    
    print("\n✨ Análisis completado!")
    print("\n💡 Observaciones:")
    print("• Los nodos evaluados aumentan exponencialmente con la profundidad")
    print("• La poda alfa-beta reduce significativamente el número de nodos")
    print("• El tiempo de ejecución es proporcional a los nodos evaluados")
    print("• A medida que el juego progresa, hay menos movimientos posibles")
    
    # Crear gráficos de demostración
    mostrar_graficos_teoria()

def mostrar_graficos_teoria():
    """
    Muestra gráficos teóricos del comportamiento del algoritmo Minimax.
    """
    print("\n📈 Generando gráficos de análisis teórico...")
    
    # Crear datos teóricos
    profundidades = np.arange(1, 10)
    nodos_sin_poda = 3 ** profundidades
    nodos_con_poda = 3 ** (profundidades * 0.6)  # Aproximación de la poda alfa-beta
    
    # Crear figura con subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Análisis Teórico del Algoritmo Minimax', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Complejidad teórica
    ax1.semilogy(profundidades, nodos_sin_poda, 'r-o', label='Sin poda alfa-beta')
    ax1.semilogy(profundidades, nodos_con_poda, 'g-s', label='Con poda alfa-beta')
    ax1.set_title('Complejidad Teórica por Profundidad')
    ax1.set_xlabel('Profundidad')
    ax1.set_ylabel('Nodos Evaluados (log scale)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Efectividad de la poda
    reduccion_porcentual = ((nodos_sin_poda - nodos_con_poda) / nodos_sin_poda) * 100
    ax2.plot(profundidades, reduccion_porcentual, 'b-o', linewidth=2, markersize=8)
    ax2.set_title('Efectividad de la Poda Alfa-Beta')
    ax2.set_xlabel('Profundidad')
    ax2.set_ylabel('Reducción (%)')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)
    
    # Gráfico 3: Tiempo estimado de ejecución
    tiempo_sin_poda = nodos_sin_poda * 0.001  # Asumiendo 1ms por 1000 nodos
    tiempo_con_poda = nodos_con_poda * 0.001
    
    ax3.semilogy(profundidades, tiempo_sin_poda, 'r-o', label='Sin poda')
    ax3.semilogy(profundidades, tiempo_con_poda, 'g-s', label='Con poda')
    ax3.set_title('Tiempo Estimado de Ejecución')
    ax3.set_xlabel('Profundidad')
    ax3.set_ylabel('Tiempo (segundos, log scale)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Gráfico 4: Comparación de dificultades
    dificultades = ['Fácil', 'Normal', 'Difícil', 'Imposible']
    profundidades_dif = [1, 3, 6, 9]
    nodos_dif = [3**p for p in profundidades_dif]
    colores = ['lightgreen', 'yellow', 'orange', 'red']
    
    bars = ax4.bar(dificultades, nodos_dif, color=colores, alpha=0.7, edgecolor='black')
    ax4.set_title('Nodos Evaluados por Dificultad')
    ax4.set_ylabel('Nodos Evaluados')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3)
    
    # Agregar valores en las barras
    for bar, valor in zip(bars, nodos_dif):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                f'{valor}', ha='center', va='bottom', fontweight='bold')
    
    # Texto explicativo
    explanation = (
        "Análisis del Algoritmo Minimax:\n"
        "• Sin poda: O(b^d) donde b=3 (branching factor), d=profundidad\n"
        "• Con poda alfa-beta: O(b^(d/2)) en el mejor caso\n"
        "• La poda puede reducir hasta 90% de los nodos evaluados\n"
        "• El tiempo de ejecución crece exponencialmente con la profundidad"
    )
    
    plt.figtext(0.02, 0.02, explanation, fontsize=10, 
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    plt.show()

def main():
    """
    Función principal de la demostración.
    """
    print("🚀 Iniciando demostración del análisis matemático...")
    print("📋 Este programa mostrará:")
    print("  1. Simulación de movimientos de la IA")
    print("  2. Análisis de rendimiento por dificultad")
    print("  3. Gráficos teóricos del algoritmo")
    print()
    
    try:
        ejecutar_demo_analisis()
        print("\n✅ Demostración completada exitosamente!")
        print("💡 Ahora puedes ejecutar el juego principal para ver el análisis en tiempo real.")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {str(e)}")
        print("🔧 Asegúrate de que todas las dependencias estén instaladas:")
        print("   pip install pygame matplotlib numpy")

if __name__ == "__main__":
    main()
