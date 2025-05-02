from collections import deque
import heapq
from data import communes, hospitals
import math
import random

def straight_line_distance(x1, y1, x2, y2):
 return ((math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))*100)/1.2

class Node:
    def __init__(self, state, path_cost=0, parent=None, heuristic=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.heuristic = heuristic

    def __repr__(self):
        return f"Node(state={self.state}, path_cost={self.path_cost})"

    def expand(self, problem):
        return [
            Node(next_state, 
                 parent=self, 
                 path_cost=self.path_cost + cost, 
                 heuristic=problem.calculate_heuristic(next_state))
            for (next_state, action, cost) in problem.successor(self.state)
        ]

    def solution(self):
        node, path = self, []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

    def __lt__(self, other):
        return (self.path_cost + self.heuristic) < (other.path_cost + other.heuristic)

class Problem:
    def __init__(self, initial_state, specialty_needed, communes, hospitals):
        self.initial_state = initial_state
        self.specialty_needed = specialty_needed
        self.communes = communes
        self.hospitals = hospitals

    def initial(self):
        return self.initial_state

    def goal_test(self, state):
        if state in self.hospitals:
            return self.specialty_needed in self.hospitals[state]["departments"]
        return False

    def successor(self, state):
        if state in self.communes:
            neighbors = self.communes[state]["neighbors"]
            return [(neighbor, f"Move to {neighbor}", cost) for neighbor, cost in neighbors.items()]
        else:
            return []

    def calculate_heuristic(self, state):
        # Check if the state is a commune
        if state in self.communes:
            state_coordinates = self.communes[state]["coordinates"]
        # Check if the state is a hospital
        elif state in self.hospitals:
            state_coordinates = (self.hospitals[state]["x"], self.hospitals[state]["y"])
        else:
            print(f"Warning: State '{state}' not found in communes or hospitals.")
            return float('inf')  # Return a high heuristic value if the state is not found

        distance = float('inf')
        # Iterate over all hospitals to find the one closest to the current state that has the required specialty
        for hospital in self.hospitals:
            if self.specialty_needed in self.hospitals[hospital]["departments"]:
                hospital_coordinates = (self.hospitals[hospital]["x"], self.hospitals[hospital]["y"])
                distance = min(distance, straight_line_distance(
                    state_coordinates[0], state_coordinates[1],
                    hospital_coordinates[0], hospital_coordinates[1]
                ))
        return distance

def calculate_path_distance(path, problem):
    total_distance = 0
    for i in range(len(path) - 1):
        state = path[i]
        next_state = path[i + 1]
        if state in problem.communes and next_state in problem.communes[state]["neighbors"]:
            total_distance += problem.communes[state]["neighbors"][next_state]
    return total_distance

def bfs(problem):
    node = Node(problem.initial_state)
    if problem.goal_test(node.state):
        return node.solution(), 0

    frontier = deque([node])
    explored = set()

    while frontier:
        node = frontier.popleft()
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and all(frontier_node.state != child.state for frontier_node in frontier):
                if problem.goal_test(child.state):
                    return child.solution(), calculate_path_distance(child.solution(), problem)
                frontier.append(child)
    
    return None, 0

def dfs(problem):
    node = Node(problem.initial_state)
    if problem.goal_test(node.state):
        return node.solution(), 0

    frontier = [node]
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node.solution(), calculate_path_distance(node.solution(), problem)
        
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and all(frontier_node.state != child.state for frontier_node in frontier):
                frontier.append(child)

    return None, 0

def astar(problem):
    node = Node(problem.initial_state, heuristic=problem.calculate_heuristic(problem.initial_state))
    if problem.goal_test(node.state):
        return node.solution(), 0

    frontier = []
    heapq.heappush(frontier, node)
    explored = set()

    while frontier:
        node = heapq.heappop(frontier)
        if problem.goal_test(node.state):
            return node.solution(), calculate_path_distance(node.solution(), problem)

        explored.add(node.state)

        for child in node.expand(problem):
            if child.state in explored:
                continue

            in_frontier = any(frontier_node.state == child.state for frontier_node in frontier)
            if not in_frontier:
                heapq.heappush(frontier, child)
            else:
                for i, frontier_node in enumerate(frontier):
                    if frontier_node.state == child.state:
                        if child.path_cost + child.heuristic < frontier_node.path_cost + frontier_node.heuristic:
                            frontier[i] = child
                            heapq.heapify(frontier)
                        break

    return None, 0

def ida_star(problem):
    def search(node, g, bound):
        f = g + node.heuristic
        if f > bound:
            return f, None
        if problem.goal_test(node.state):
            return f, node.solution()
        min_bound = float('inf')
        for child in node.expand(problem):
            new_g = g + (child.path_cost - node.path_cost)
            t, result = search(child, new_g, bound)
            if result is not None:
                return t, result
            if t < min_bound:
                min_bound = t
        return min_bound, None
    
    start_node = Node(problem.initial_state, heuristic=problem.calculate_heuristic(problem.initial_state))
    bound = start_node.heuristic
    while True:
        t, result = search(start_node, 0, bound)
        if result is not None:
            return result, calculate_path_distance(result, problem)
        if t == float('inf'):
            return None, 0
        bound = t

def steepest_ascent_hill_climbing(problem):
    current = Node(problem.initial_state, heuristic=problem.calculate_heuristic(problem.initial_state))
    path_to_end_state = [current.state]

    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            print("No more neighbors to explore.")
            break

        better_neighbors = [neighbor for neighbor in neighbors if neighbor.heuristic < current.heuristic]

        if not better_neighbors:
            print("No better neighbors found, terminating.")
            break

        probability = 0.3
        if random.random() < probability:
            neighbor = random.choice(better_neighbors)
        else:
            neighbor = min(better_neighbors, key=lambda node: node.heuristic)

        current = neighbor
        path_to_end_state.append(current.state)

        if problem.goal_test(current.state):
            print("Goal state reached.")
            return path_to_end_state, current.state, True, calculate_path_distance(path_to_end_state, problem)

    print("Algorithm terminated without finding a solution.")
    return path_to_end_state, current.state, False, calculate_path_distance(path_to_end_state, problem)

def stochastic_hill_climbing(problem, max_moves):
    current = Node(problem.initial_state, heuristic=problem.calculate_heuristic(problem.initial_state))
    path_to_end_state = [current.state]
    moves = 0

    while moves < max_moves:
        moves += 1
        neighbors = current.expand(problem)
        if not neighbors:
            print("No more neighbors to explore.")
            break

        neighbor = random.choice(neighbors)
        current = neighbor
        path_to_end_state.append(current.state)

        if problem.goal_test(current.state):
            print("Goal state reached.")
            return path_to_end_state, current.state, True, calculate_path_distance(path_to_end_state, problem)

    print("Algorithm terminated without finding a solution.")
    return path_to_end_state, current.state, False, calculate_path_distance(path_to_end_state, problem)


# Example usage:
initial_state = "draria"
specialty_needed = "infectious diseases"
problem = Problem(initial_state, specialty_needed, communes, hospitals)

print("\nBFS Solution path:")
bfs_solution, bfs_distance = bfs(problem)
print(bfs_solution)
print(f"Total Distance: {bfs_distance}")
print("\n" + "-"*50 + "\n")

print("A* Solution path:")
astar_solution, astar_distance = astar(problem)
print(astar_solution)
print(f"Total Distance: {astar_distance}")
print("\n" + "-"*50 + "\n")

print("DFS Solution path:")
dfs_solution, dfs_distance = dfs(problem)
print(dfs_solution)
print(f"Total Distance: {dfs_distance}")
print("\n" + "-"*50 + "\n")

#print("Steepest Ascent Hill Climbing Solution path:")
#solution_path, end_state, is_goal, sahc_distance = steepest_ascent_hill_climbing(problem)
#if solution_path:
 #   print("Path to End State:", solution_path)
  #  print("End State:", end_state)
  #  print("Goal Test:", is_goal)
   # print(f"Total Distance: {sahc_distance}")
#else:
 #   print("No solution found.")
#print("\n" + "-"*50 + "\n")

print("Stochastic Hill Climbing Solution path:")
stochastic_hill_climbing_solution, end_state, is_goal, shc_distance = stochastic_hill_climbing(problem, 20)
print(stochastic_hill_climbing_solution)
print(f"Total Distance: {shc_distance}")
print("\n" + "-"*50 + "\n")
