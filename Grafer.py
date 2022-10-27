from collections import deque

                    #A  B  C  D  E  F  G  H  I  J
adjacency_matrix = [[0, 0, 1, 1, 1, 0, 1, 1, 1, 1], # A -> C, D, E, G, H, I, J
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # B -> D
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1], # C -> A, I, J
                    [1, 1, 0, 0, 1, 1, 1, 1, 0, 0], # D -> A, B, E, F, G, H
                    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0], # E -> A, D, G
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1], # F -> D, J
                    [1, 0, 0, 1, 1, 0, 0, 0, 0, 1], # G -> A, D, E, J
                    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0], # H -> A, D
                    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1], # I -> A, C, J
                    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]] # J -> A, C, F, G, I

adjacency_list = {"A": ["C", "D", "E", "G", "H", "I", "J"],
                  "B": ["D"],
                  "C": ["A", "I", "J"],
                  "D": ["A", "B", "E", "F", "G", "H"],
                  "E": ["A", "D", "G"],
                  "F": ["D", "J"],
                  "G": ["A", "D", "E", "J"],
                  "H": ["A", "D"],
                  "I": ["A", "C", "J"],
                  "J": ["A", "C", "F", "G", "I"]}

def breadth_first_search(graph_to_search, start_node, goal_node):
    queue = deque()
    queue.append(start_node)
    explored = [start_node]
    prev_node_map = {start_node : None}
    while queue:
        current_node = queue.popleft()
        if current_node == goal_node:
            break
        else:
            for next_node in graph_to_search[current_node]:
                if next_node not in explored:
                    explored.append(next_node)
                    queue.append(next_node)
                    prev_node_map[next_node] = current_node

    shortest_path = []
    node = goal_node
    while node:
        shortest_path.insert(0, node)
        node = prev_node_map[node]

    return shortest_path

print(breadth_first_search(adjacency_list, "B", "I"))