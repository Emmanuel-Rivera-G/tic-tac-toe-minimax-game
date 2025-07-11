# Mi Proyecto Python - Tres en Raya con Análisis Matemático

Este es un proyecto avanzado en Python que implementa el juego de Tres en Raya (Tic-Tac-Toe) con inteligencia artificial basada en el algoritmo Minimax, incluyendo análisis matemático en tiempo real y visualizaciones gráficas.

## 🎮 Características Principales

- **Algoritmo Minimax** con poda Alfa-Beta para IA óptima
- **Interfaz gráfica** intuitiva usando pygame
- **Análisis matemático en tiempo real** del algoritmo
- **Visualizaciones con matplotlib** para entender el comportamiento del algoritmo
- **Múltiples niveles de dificultad** (Fácil, Normal, Difícil, Imposible)
- **Métricas de rendimiento** (nodos evaluados, tiempo de ejecución)
- **Botón de análisis** para ver gráficos detallados del algoritmo

## 🚀 Nuevas Funcionalidades

### Análisis Matemático
- **Costo por jugada**: Muestra el número de nodos evaluados y tiempo de ejecución para cada movimiento de la IA
- **Gráficos interactivos**: Visualización del comportamiento del algoritmo usando matplotlib
- **Análisis de complejidad**: Comparación entre diferentes profundidades y estrategias
- **Estadísticas en tiempo real**: Métricas actualizadas durante el juego

### Visualizaciones Incluidas
1. **Nodos evaluados por movimiento**: Gráfico de barras mostrando el costo computacional
2. **Tiempo de ejecución**: Análisis temporal de cada decisión de la IA
3. **Profundidad vs Rendimiento**: Scatter plot coloreado por eficiencia
4. **Análisis de complejidad**: Gráfico logarítmico comparando teoría vs práctica

## 📦 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Emmanuel-Rivera-G/tic-tac-toe-minimax-game.git
   cd mi-proyecto-python
   ```

2. Instala las dependencias usando Poetry:
   ```bash
   poetry install
   ```

## 🎯 Uso

### Ejecutar el juego principal
```bash
poetry run python src/tic-tac-toe-minimax-game/tres_en_raya_pygame.py
```

### Ejecutar la demostración del análisis matemático
```bash
poetry run python demo_analisis.py
```

### Ejecutar las pruebas
```bash
poetry run pytest
```

## 🎮 Cómo Jugar

1. **Selecciona la dificultad**: Fácil, Normal, Difícil o Imposible
2. **Haz tu movimiento**: Haz clic en una celda vacía del tablero
3. **Observa el análisis**: Después de cada movimiento de la IA, verás:
   - Número de nodos evaluados
   - Tiempo de ejecución en milisegundos
4. **Ver análisis completo**: Haz clic en el botón "Ver Análisis" para abrir los gráficos de matplotlib

## 📊 Interpretación del Análisis

### Métricas Clave
- **Nodos evaluados**: Indica la complejidad computacional del movimiento
- **Tiempo de ejecución**: Muestra la eficiencia temporal del algoritmo
- **Profundidad**: Nivel de búsqueda utilizado según la dificultad

### Patrones Observables
- **Reducción exponencial**: A medida que el juego progresa, hay menos movimientos posibles
- **Efecto de la poda**: La poda alfa-beta reduce significativamente los nodos evaluados
- **Correlación tiempo-nodos**: El tiempo de ejecución es proporcional a los nodos evaluados

## 🏗️ Estructura del Proyecto

```
mi-proyecto-python/
├── src/
│   └── tic-tac-toe-minimax-game/
│       ├── __init__.py
│       ├── minimax.py          # Algoritmo Minimax con poda alfa-beta
│       ├── tres_en_raya.py     # Lógica del juego (consola)
│       └── tres_en_raya_pygame.py  # Interfaz gráfica + análisis
├── tests/
│   └── __init__.py
├── demo_analisis.py            # Demostración del análisis matemático
├── pyproject.toml
└── README.md
```

## 🔧 Dependencias

- **Python 3.12+**
- **pygame**: Interfaz gráfica del juego
- **matplotlib**: Visualizaciones y gráficos de análisis
- **numpy**: Operaciones matemáticas y análisis numérico
- **pytest**: Framework de pruebas (dependencia de desarrollo)

## 🧮 Algoritmo Minimax

### Complejidad Teórica
- **Sin poda**: O(b^d) donde b=3 (factor de ramificación), d=profundidad
- **Con poda alfa-beta**: O(b^(d/2)) en el mejor caso
- **Reducción práctica**: Hasta 90% menos nodos evaluados

### Niveles de Dificultad
- **Fácil**: Profundidad 1, 40% movimientos aleatorios
- **Normal**: Profundidad 3, 20% movimientos aleatorios
- **Difícil**: Profundidad 6, 10% movimientos aleatorios
- **Imposible**: Profundidad 9, 0% movimientos aleatorios

## 📈 Análisis de Rendimiento

El sistema recopila y analiza:
- Número de nodos evaluados por movimiento
- Tiempo de ejecución por decisión
- Profundidad de búsqueda utilizada
- Eficiencia de la poda alfa-beta
- Correlaciones entre métricas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Abre un issue para discutir cambios mayores
2. Haz fork del proyecto
3. Crea una rama para tu feature
4. Envía un pull request

## 📚 Aprendizajes

Este proyecto demuestra:
- Implementación práctica del algoritmo Minimax
- Optimización con poda alfa-beta
- Análisis de complejidad algoritmica
- Visualización de datos matemáticos
- Integración de múltiples librerías de Python
- Gestión de proyectos con Poetry
