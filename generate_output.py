import os
from src.algorithms.base_algo import BaseAlgo
from src.map_data import MapData
from src.algorithms.bfs import BFS
from src.algorithms.dfs import DFS
from src.algorithms.ucs import UCS
from src.algorithms.a_star import AStar

class AlgorithmRunner:
    OUTPUT_DIR = "output"
    
    def __init__(self, input_file_name):
        self.input_file_name = input_file_name
        self.map_data = None

    def parse_map(self, file_path):
        content = []
        with open(file_path, "r") as file:
            content = file.readlines()

        stones = list(map(int, content[0].split()))
        map_matrix = [list(line.strip('\n')) for line in content[1:]]

        self.map_data = MapData()
        self.map_data.set_map_matrix(map_matrix, stones)

    def run_algo(self, algo_cls: BaseAlgo, selected_algo: str):
        algoer = algo_cls()
        algoer.set_map(self.map_data.copy())
        algoer.run()

        path, maps, total_w = algoer.get_path()
        time_consumed, mem_consumed, num_explored = algoer.get_stats()

        print(f"Algorithm: {selected_algo}")
        print(f"Total steps: {len(path)}")
        print(f"Total weight: {total_w}")
        print(f"Time consumed: {time_consumed} seconds")
        print(f"Memory consumed: {mem_consumed} MB")
        print(f"Number of explored nodes: {num_explored}")
        print(f"Path: {''.join(path)}")

        self.export_output(selected_algo, len(path), total_w, num_explored, time_consumed, mem_consumed, ''.join(path))
        print("Output exported\n")

    def export_output(self, algo_name, total_steps, total_weight, num_explored, time_consumed, mem_consumed, path):
        inp_file_name = os.path.basename(self.input_file_name)
        out_file_name = inp_file_name.replace("input", "output")

        if "output" not in out_file_name:
            out_file_name = "output_" + out_file_name

        out_file_path = os.path.join(self.OUTPUT_DIR, out_file_name)

        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

        with open(out_file_path, 'a') as file:
            file.write(f"Algorithm: {algo_name}\n")
            file.write(f"Steps: {total_steps}, Weight: {total_weight}, Nodes: {num_explored}, Time: {time_consumed} seconds, Memory: {mem_consumed} MB\n")
            file.write(f"Path: {path}\n\n")


def main():
    for i in range(8, 11):
        file_path = f'data/input{i}.txt'
        runner = AlgorithmRunner(file_path)
        runner.parse_map(file_path)

        for algo in [BFS, DFS, UCS, AStar]:
            runner.run_algo(algo, algo.__name__)


if __name__ == "__main__":
    main()
