# Source\search_algorithms.py
from collections import deque
import heapq
import time
import sys
import tracemalloc

def measure_performance(func):
    """Decorator to measure time, memory and expanded nodes"""
    def wrapper(maze, start, goal):
        tracemalloc.start()
        start_time = time.time()
        
        path, expanded_nodes = func(maze, start, goal)
        
        search_time = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return path, expanded_nodes, search_time, peak / 1024  # Convert to KB
    return wrapper

@measure_performance
def bfs(maze, start, goal):
    """Breadth-First Search implementation"""
    queue = deque()
    queue.append(start)
    visited = {start: None}
    expanded_nodes = 0
    
    while queue:
        current = queue.popleft()
        expanded_nodes += 1
        
        if current == goal:
            break
            
        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)
                
    # Reconstruct path
    path = []
    if goal in visited:
        current = goal
        while current != start:
            path.append(current)
            current = visited[current]
        path.reverse()
        
    return path, expanded_nodes

@measure_performance
def dfs(maze, start, goal):
    """Depth-First Search implementation"""
    stack = [start]
    visited = {start: None}
    expanded_nodes = 0

    while stack:
        current = stack.pop()
        expanded_nodes += 1

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()
            return path, expanded_nodes

        # Get neighbors and reverse to maintain order
        neighbors = maze.get_neighbors(current)
        neighbors.reverse()

        for neighbor in neighbors:
            if neighbor not in visited:
                visited[neighbor] = current
                stack.append(neighbor)

    return [], expanded_nodes

@measure_performance
def ucs(maze, start, goal):
    """Uniform-Cost Search implementation"""
    heap = []
    heapq.heappush(heap, (0, start))
    visited = {start: (None, 0)}
    expanded_nodes = 0
    
    while heap:
        current_cost, current = heapq.heappop(heap)
        expanded_nodes += 1
        
        if current == goal:
            break
            
        for neighbor in maze.get_neighbors(current):
            new_cost = current_cost + 1
            if neighbor not in visited or new_cost < visited[neighbor][1]:
                visited[neighbor] = (current, new_cost)
                heapq.heappush(heap, (new_cost, neighbor))
                
    path = []
    if goal in visited:
        current = goal
        while current != start:
            path.append(current)
            current = visited[current][0]
        path.reverse()
        
    return path, expanded_nodes

def heuristic(a, b):
    """Heuristic function using Manhattan distance"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
@measure_performance
def a_star(maze, start, goal):
    """A* Search Algorithm"""
    heap = []
    heapq.heappush(heap, (0, start))  # (cost, node)
    visited = {start: (None, 0)}  # {node: (previous_node, g_cost)}
    expanded_nodes = 0
    
    while heap:
        current_cost, current = heapq.heappop(heap)
        expanded_nodes += 1
        
        if current == goal:
            break
        
        for neighbor in maze.get_neighbors(current):
            new_cost = visited[current][1] + 1  # g(n) = g(current) + 1
            f_cost = new_cost + heuristic(neighbor, goal)  # f(n) = g(n) + h(n)
            
            if neighbor not in visited or new_cost < visited[neighbor][1]:
                visited[neighbor] = (current, new_cost)
                heapq.heappush(heap, (f_cost, neighbor))
    
    path = []
    if goal in visited:
        current = goal
        while current != start:
            path.append(current)
            current = visited[current][0]
        path.reverse()
    
    return path, expanded_nodes
