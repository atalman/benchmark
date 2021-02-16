
"""
Compute the benchmark score given a frozen score configuration and current benchmark data.
"""
import argparse
import json
import math
import sys
import os

from torchbenchmark.score.compute_score import TorchBenchScore
from tabulate import tabulate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--configuration",
        help="frozen benchmark configuration generated by generate_score_config.py")
    parser.add_argument("--benchmark_data_file",
        help="pytest-benchmark json file with current benchmark data")
    parser.add_argument("--benchmark_data_dir",
        help="directory containing multiple .json files for each of which to compute a score")
    args = parser.parse_args()

    if args.configuration is not None:
        with open(args.configuration) as cfg_file:
            score_config = TorchBenchScore(cfg_file)
    else:
        if args.benchmark_data_file is None and args.benchmark_data_dir is None:
            parser.print_help(sys.stderr)
            raise ValueError("Invalid command-line arguments. You must specify a config, a data file, or a data dir.")
        score_config = TorchBenchScore()

    if args.benchmark_data_file is not None:
        with open(args.benchmark_data_file) as data_file:
            data = json.load(data_file)
        score = score_config.compute_score(data)

    elif args.benchmark_data_dir is not None:
        scores = [('File', 'Score', 'PyTorch Version')]
        for f in os.listdir(args.benchmark_data_dir):
            path = os.path.join(args.benchmark_data_dir, f)
            if os.path.isfile(path) and os.path.splitext(path)[1] == '.json':
                with open(path) as data_file:
                    data = json.load(data_file)
                    score = score_config.compute_score(data)
                    scores.append((f, score, data['machine_info']['pytorch_version']))

        print(tabulate(scores, headers='firstrow'))

    # print(f"Benchmark Score: {score} (rounded) {int(round(score))}")
