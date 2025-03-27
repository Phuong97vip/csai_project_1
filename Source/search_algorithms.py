from collections import deque
import heapq

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

        neighbors = maze.get_neighbors(current)
        neighbors.sort(key=lambda pos: abs(pos[0]-goal[0]) + abs(pos[1]-goal[1]), reverse=True)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited[neighbor] = current
                stack.append(neighbor)

    return [], expanded_nodes

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

