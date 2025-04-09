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
    queue = deque([start])  # Hàng đợi FIFO
    visited = {start: None}  # Lưu trữ node cha
    expanded_nodes = 0  # Đếm số node đã mở rộng

    while queue:
        current = queue.popleft()  # Lấy node đầu tiên (FIFO)
        expanded_nodes += 1

        if current == goal:
            break  # Dừng khi tìm thấy đích

        for neighbor in maze.get_neighbors(current):
            if neighbor not in visited:
                visited[neighbor] = current  # Ghi nhận node cha
                queue.append(neighbor)  # Thêm vào cuối hàng đợi

    # Truy vết đường đi
    path = []
    if goal in visited:
        current = goal
        while current != start:
            path.append(current)
            current = visited[current]
        path.reverse()  # Đảo ngược để có thứ tự từ start đến goal

    return path, expanded_nodes

@measure_performance
def dfs(maze, start, goal):
    stack = [start]  # Khởi tạo ngăn xếp với node bắt đầu
    visited = {start: None}  # Dictionary lưu node cha và node hiện tại
    expanded_nodes = 0  # Biến đếm số node đã mở rộng

    while stack:
        current = stack.pop()  # Lấy node cuối cùng (LIFO)
        expanded_nodes += 1  # Tăng số node đã duyệt

        if current == goal:
            # Truy vết đường đi từ goal về start
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()  # Đảo ngược để có đường đi từ start đến goal
            return path, expanded_nodes

        # Đảo ngược thứ tự neighbors để duyệt theo thứ tự chuẩn
        neighbors = maze.get_neighbors(current)
        neighbors.reverse()

        for neighbor in neighbors:
            if neighbor not in visited:
                visited[neighbor] = current  # Đánh dấu node cha
                stack.append(neighbor)  # Thêm vào stack

    return [], expanded_nodes  # Trả về đường đi rỗng nếu không tìm thấy

@measure_performance
def ucs(maze, start, goal):
    heap = []
    heapq.heappush(heap, (0, start))  # Hàng đợi ưu tiên (chi phí, node)
    visited = {start: (None, 0)}  # Lưu (node cha, chi phí tích lũy)
    expanded_nodes = 0

    while heap:
        current_cost, current = heapq.heappop(heap)  # Lấy node có chi phí nhỏ nhất
        expanded_nodes += 1

        if current == goal:
            break  # Dừng khi tìm thấy đích

        for neighbor in maze.get_neighbors(current):
            new_cost = current_cost + 1  # Giả định chi phí mỗi bước là 1
            if neighbor not in visited or new_cost < visited[neighbor][1]:
                visited[neighbor] = (current, new_cost)
                heapq.heappush(heap, (new_cost, neighbor))  # Thêm vào hàng đợi ưu tiên

    # Truy vết đường đi
    path = []
    if goal in visited:
        current = goal
        while current != start:
            path.append(current)
            current = visited[current][0]  # Lấy node cha
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
