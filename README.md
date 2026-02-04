*This project has been created by [الـ LOGIN ديالك هنا]*

# A-Maze-ing

## Description
A-Maze-ing is a Python project designed to generate, visualize, and solve mazes. 
The project is built with modularity in mind, separating the core generation 
logic into a reusable package and providing a robust command-line application 
to interact with it.

## Features
- **Maze Generation**: Implements a DFS (Depth-First Search) algorithm to create perfect mazes.
- **"42" Pattern**: A mandatory hardcoded visual pattern integrated into the maze.
- **Solver**: A pathfinding algorithm to find the optimal path from entry to exit.
- **Hexadecimal Representation**: Mazes are exported in a specific bitmask hexadecimal format.
- **Visualization**: An ASCII-based terminal display with colors for a better user experience.

## Installation
The core logic is available as a reusable Python package called `mazegen`.

1. **Activate your virtual environment**:
   ```bash
   source venv/bin/activate