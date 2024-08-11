import numpy as np
import matplotlib.pyplot as plt
from joblib import load
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.spatial import ConvexHull
from skimage.feature import corner_harris, corner_peaks

# Load data
np_path_XYs = np.genfromtxt("examples/occlusion2.csv", delimiter=',')
np_path_XY2s = np.genfromtxt("examples/occlusion2_sol.csv", delimiter=',')

# Determine unique curve sizes
size = len(np.unique(np_path_XYs[:, 0]))
size2 = len(np.unique(np_path_XY2s[:, 0]))

# Extract curves
XY = [np_path_XYs[np_path_XYs[:, 0] == i][:, 2:] for i in range(size)]
XY2 = [np_path_XY2s[np_path_XY2s[:, 0] == i][:, 2:] for i in range(size2)]

# Plot curves
def plot_curves(curves):
    for i in range(len(curves)):
        fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
        for j in range(i + 1):
            ax.plot(curves[j][:, 0], curves[j][:, 1], linewidth=2)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

plot_curves(XY)
plot_curves(XY2)

# Initialize data structures for graph construction
start_points = [XY[i][0] for i in range(size)]
end_points = [XY[i][-1] for i in range(size)]

curve_num = {i: i // 2 for i in range(2 * size)}
partner = {i: i + 1 if i % 2 == 0 else i - 1 for i in range(2 * size)}
umap = {2 * i: start_points[i] for i in range(size)}
umap.update({2 * i + 1: end_points[i] for i in range(size)})

# Build adjacency list
def euclidean_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

adjacency_list = [[] for _ in range(2 * size)]

for i in range(size):
    adjacency_list[2 * i].append((2 * i + 1, i))
    adjacency_list[2 * i + 1].append((2 * i, i))
    for j in range(size):
        if i != j:
            if euclidean_distance(start_points[i], start_points[j]) < 5:
                adjacency_list[2 * i].append((2 * j, j))
            if euclidean_distance(start_points[i], end_points[j]) < 5:
                adjacency_list[2 * i].append((2 * j + 1, j))
            if euclidean_distance(end_points[i], start_points[j]) < 5:
                adjacency_list[2 * i + 1].append((2 * j, j))
            if euclidean_distance(end_points[i], end_points[j]) < 5:
                adjacency_list[2 * i + 1].append((2 * j + 1, j))

# DFS for closed curves
def dfs(node, start_node, visited, path, adj_list, partner, unique_cycles):
    path.append(node)
    visited.add(node)
    for neighbor, curve_number in adj_list[node]:
        if len(path) == 2 and partner[path[0]] == path[1] and euclidean_distance(umap[path[0]], umap[path[1]]) < 5:
            curve_path = [curve_num[path[0]]]
            cycle_representation = frozenset(curve_path)
            if cycle_representation not in unique_cycles and len(cycle_representation) > 0:
                unique_cycles[cycle_representation] = list(path) + [start_node]
        if neighbor == start_node and len(path) > 2:
            curve_path = [curve_num[path[i]] for i in range(len(path) - 1) if partner[path[i]] == path[i + 1]]
            if partner[path[-1]] == neighbor:
                curve_path.append(curve_num[neighbor])
            cycle_representation = frozenset(curve_path)
            if cycle_representation not in unique_cycles and len(cycle_representation) > 0:
                unique_cycles[cycle_representation] = list(path) + [start_node]
        elif neighbor not in visited:
            dfs(neighbor, start_node, visited, path, adj_list, partner, unique_cycles)
    path.pop()
    visited.remove(node)

def find_closed_curves(adj_list, num_nodes):
    unique_cycles = {}
    for start_node in range(num_nodes):
        visited = set()
        dfs(start_node, start_node, visited, [], adj_list, partner, unique_cycles)
    return unique_cycles

num_nodes = len(adjacency_list)
closed_curves = find_closed_curves(adjacency_list, num_nodes)

# Plot closed curves
for i, (curve_set, path) in enumerate(closed_curves.items()):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for el in curve_set:
        ax.plot(XY[el][:, 0], XY[el][:, 1], linewidth=2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Reconstruct curve from node sequence
def reconstruct_single_curve(node_sequence, umap, XY, partner):
    curve_points = []
    i = 0
    while i < len(node_sequence) - 1:
        cur_node = node_sequence[i]
        next_node = node_sequence[i + 1]
        if partner[cur_node] != next_node:
            i += 1
        else:
            start_point = umap[cur_node]
            end_point = umap[next_node]
            found_curve = False
            for curve in XY:
                if (np.array_equal(curve[0], start_point) and np.array_equal(curve[-1], end_point)) or (np.array_equal(curve[0], end_point) and np.array_equal(curve[-1], start_point)):
                    curve_points.extend(curve if np.array_equal(curve[0], start_point) else curve[::-1])
                    found_curve = True
                    break
            if not found_curve:
                raise ValueError("Curve with the specified start and end points not found in XY.")
            i += 2
    return np.array(curve_points)

# Load model and perform classification
model = load('model1.joblib')

# Example feature extraction
def extract_features(curve):
    scaler = StandardScaler()
    pca = PCA(n_components=2)
    curve = np.array(curve)
    scaled_curve = scaler.fit_transform(curve)
    pca_result = pca.fit_transform(scaled_curve)
    return pca_result.flatten()

def find_corners(curve):
    harris_corners = corner_harris(curve)
    corner_peaks_corners = corner_peaks(harris_corners)
    return corner_peaks_corners

def pca_bounding_box(corners):
    if len(corners) == 0:
        return np.array([])
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(corners)
    hull = ConvexHull(pca_result)
    return pca_result[hull.vertices]

for curve_set, node_sequence in closed_curves.items():
    new_path = reconstruct_single_curve(node_sequence, umap, XY, partner)
    fv = extract_features(new_path)
    fv = fv.reshape(1, -1)
    shape = model.predict(fv)
    if shape == 'rectangle':
        print(curve_set)
        corners = find_corners(new_path)
        print(corners)
        reg_corners = pca_bounding_box(corners)
        reg_corners = np.vstack([reg_corners, reg_corners[0]])
        fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
        ax.plot(reg_corners[:, 0], reg_corners[:, 1], linewidth=2)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

# Find open curves
def dfs_find_open_paths(node, parent, visited, path, curves_in_path, adj_list, unique_paths):
    path.append(node)
    visited.add(node)
    is_end = True
    for neighbor, curve_number in adj_list[node]:
        if neighbor != parent:
            is_end = False
            if neighbor not in visited:
                dfs_find_open_paths(neighbor, node, visited, path, curves_in_path + [curve_number], adj_list, unique_paths)
    if is_end and parent is not None and euclidean_distance(umap[parent], umap[node]) >= 5:
        path_representation = frozenset(curves_in_path)
        if path_representation not in unique_paths:
            unique_paths[path_representation] = list(path)
    path.pop()
    visited.remove(node)

def find_open_curves(adj_list, num_nodes):
    unique_paths = {}
    for start_node in range(num_nodes):
        visited = set()
        if len(adj_list[start_node]) == 1:
            dfs_find_open_paths(start_node, None, visited, [], [], adj_list, unique_paths)
    return unique_paths

open_curves = find_open_curves(adjacency_list, num_nodes)

# Plot open curves
for i, (path_set, path) in enumerate(open_curves.items()):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for el in path_set:
        ax.plot(XY[el][:, 0], XY[el][:, 1], linewidth=2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
