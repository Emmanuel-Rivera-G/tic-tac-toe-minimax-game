# Tres en Raya con Algoritmo Minimax

Juego de Tres en Raya (Tic-Tac-Toe) con inteligencia artificial basada en el algoritmo Minimax, incluyendo análisis matemático en tiempo real y visualizaciones gráficas.

## 🎮 Características

- **Algoritmo Minimax** con poda Alfa-Beta
- **Interfaz gráfica** con pygame
- **Análisis matemático** en tiempo real
- **Visualizaciones** con matplotlib
- **Múltiples niveles de dificultad** (Fácil, Normal, Difícil, Imposible)
- **Métricas de rendimiento** (nodos evaluados, tiempo de ejecución)

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Emmanuel-Rivera-G/tic-tac-toe-minimax-game.git
   cd tic-tac-toe-minimax-game
   ```

2. Instala las dependencias usando Poetry:
   ```bash
   poetry install
   ```

## 🎯 Uso

### Ejecutar el juego
```bash
poetry run dev
```

### Comandos adicionales
```bash
# Ejecutar análisis matemático
poetry run python demo_analisis.py

# Ejecutar versión de consola
poetry run python src/tic_tac_toe_minimax_game/tres_en_raya.py

# Ejecutar pruebas
poetry run pytest
```

## 🎮 Cómo Jugar

1. **Selecciona la dificultad**: Fácil, Normal, Difícil o Imposible
2. **Haz tu movimiento**: Haz clic en una celda vacía del tablero
3. **Observa el análisis**: Después de cada movimiento de la IA, verás nodos evaluados y tiempo de ejecución
4. **Ver análisis completo**: Haz clic en el botón "Ver Análisis" para abrir los gráficos

## 🏗️ Estructura del Proyecto

```
tic-tac-toe-minimax-game/
├── src/
│   └── tic_tac_toe_minimax_game/
│       ├── minimax.py          # Algoritmo Minimax con poda alfa-beta
│       ├── tres_en_raya.py     # Versión consola
│       └── tres_en_raya_pygame.py  # Interfaz gráfica + análisis
├── demo_analisis.py            # Demostración del análisis matemático
├── pyproject.toml
└── README.md
```

## 🔧 Dependencias

- **Python 3.8+**
- **pygame**: Interfaz gráfica
- **matplotlib**: Visualizaciones
- **numpy**: Operaciones matemáticas

## 🧮 Algoritmo Minimax

### Niveles de Dificultad
- **Fácil**: Profundidad 1, 40% movimientos aleatorios
- **Normal**: Profundidad 3, 20% movimientos aleatorios
- **Difícil**: Profundidad 6, 10% movimientos aleatorios
- **Imposible**: Profundidad 9, 0% movimientos aleatorios
