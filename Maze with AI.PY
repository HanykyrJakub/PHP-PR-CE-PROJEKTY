import heapq
import random
import time
import os
import sys

class MazeSolverAi:
    def __init__(self, maze):
        if not maze or not all(isinstance(row, list) for row in maze):
            raise ValueError("Invalid maze format. Maze must be a 2D list.")
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = self.find_point('S')
        self.end = self.find_point('E')
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.came_from = {}

    def find_point(self, point):
        """Find the start or end point."""
        for row in range(self.rows):
            if point in self.maze[row]:
                return (row, self.maze[row].index(point))
        raise ValueError(f"Point '{point}' not found in the maze.")

    def heuristic(self, a, b):
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node):
        """Get valid neighboring cells."""
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        neighbors = []
        for direction in directions:
            new_row, new_col = node[0] + direction[0], node[1] + direction[1]
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.maze[new_row][new_col] != 1:
                neighbors.append((new_row, new_col))
        return neighbors

    def solve(self, time_limit=100):
        """Solve the maze using A* algorithm with a time limit."""
        start_time = time.time()
        frontier = []
        heapq.heappush(frontier, (0, self.start))

        cost_so_far = {self.start: 0}
        self.came_from[self.start] = None

        while frontier:
            # Check if the time limit is exceeded
            elapsed_time = time.time() - start_time
            remaining_time = time_limit - elapsed_time
            if remaining_time <= 0:
                print("\nTime's up! The maze was not solved in 60 seconds.")
                return None

            # Display countdown
            print(f"\nTime remaining: {int(remaining_time)} seconds")

            current = heapq.heappop(frontier)[1]

            if current == self.end:
                total_time = time.time() - start_time
                print(f"Maze solved in {total_time:.2f} seconds.")
                return self.reconstruct_path()

            for neighbor in self.neighbors(current):
                new_cost = cost_so_far[current] + 1

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, self.end)
                    heapq.heappush(frontier, (priority, neighbor))
                    self.came_from[neighbor] = current

            # Display step-by-step progress
            self.display_step(current)
            time.sleep(0.3)  # 300ms delay between steps

        return None

    def reconstruct_path(self):
        """Rebuild the path from end to start."""
        current = self.end
        path = []
        while current is not None:
            path.append(current)
            current = self.came_from[current]
        path.reverse()  # Reverse the path to start from 'S'
        return path

    def display_step(self, current):
        """Display the maze at each step of the solving process."""
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console (works for Windows and Unix)
        solution_maze = [row[:] for row in self.maze]
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) == current:
                    solution_maze[row][col] = 'C'  # Mark the current position
                elif self.visited[row][col]:
                    solution_maze[row][col] = '.'  # Mark visited nodes
        solution_maze[self.start[0]][self.start[1]] = 'S'
        solution_maze[self.end[0]][self.end[1]] = 'E'

        for row in solution_maze:
            print(' '.join(map(str, row)))
        print("\nSolving... Current position:", current)

    def display_solution(self, path):
        """Display the maze with the final solution path."""
        solution_maze = [row[:] for row in self.maze]
        for (row, col) in path:
            if solution_maze[row][col] not in ('S', 'E'):
                solution_maze[row][col] = '.'

        for row in solution_maze:
            print(' '.join(map(str, row)))

# Iterative DFS-based Maze Generation
def generate_maze(rows, cols):
    """Generate a random maze using an iterative DFS algorithm."""
    maze = [[1 for _ in range(cols)] for _ in range(rows)]  # Initialize maze with walls (1)

    def carve_path_iteratively(x, y):
        """Iterative DFS to carve out paths."""
        stack = [(x, y)]
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        while stack:
            cx, cy = stack.pop()
            random.shuffle(directions)  # Randomize the directions
            
            for dx, dy in directions:
                nx, ny = cx + 2 * dx, cy + 2 * dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                    maze[cx + dx][cy + dy] = 0  # Carve the path between
                    maze[nx][ny] = 0  # Set the new cell as a passage
                    stack.append((nx, ny))

    # Start carving the maze from the top-left corner
    start_x, start_y = 0, 0
    maze[start_x][start_y] = 0  # Starting point
    carve_path_iteratively(start_x, start_y)

    # Set Start and End points
    maze[0][0] = 'S'
    maze[rows - 1][cols - 1] = 'E'
    return maze

# Generate a large maze (e.g., 15x15 or larger)
large_maze = generate_maze(10, 35)
solver = MazeSolverAi(large_maze)

# Solve the maze with a 60-second countdown
path = solver.solve(time_limit=120)

if path:
    print("Maze solved with A* AI! Here is the final path:")
    solver.display_solution(path)
else:
    print("No solution found.")
