# Pac-Man Search Algorithms

This project implements various search algorithms (BFS, DFS, UCS, and A* Star) to solve Pac-Man pathfinding problems. The implementation uses Pygame for visualization and provides a graphical interface to observe the different search algorithms in action.

## Features

- Multiple search algorithm implementations:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Uniform Cost Search (UCS)
  - A* Star Search
- Interactive Pygame visualization
- Customizable maze generation
- Real-time algorithm visualization

## Requirements

- Python 3.x
- Pygame
- Other dependencies (if any)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd csai_project_1
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main program:
```bash
python Source/main.py
```

You can specify which search algorithm to use with the `--algorithm` argument:
```bash
python Source/main.py --algorithm BFS DFS UCS Astar
```

Available algorithm choices:
- BFS
- DFS
- UCS
- Astar

## Project Structure

```
csai_project_1/
├── Source/
│   ├── main.py          # Main program entry point
│   ├── constants.py     # Game constants and configurations
│   └── runtime.py       # Pygame runtime implementation
└── README.md
```

## Controls

- Use the mouse to interact with the game interface
- Follow on-screen instructions to start the simulation
- Observe the different search algorithms in action

## License

[Specify your license here]

## Contributing

[Add contribution guidelines if applicable] 