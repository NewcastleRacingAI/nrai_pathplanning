import os
import pickle
from .code import pathfind

import time

def main(args: argparse.Namespace):
    topics: dict[str, Queue] = args.topics or {}

    # --- Set up Code ---
    if args.planning_topic not in topics:
        raise ValueError(f"No '{args.planning_topic}' topic to listen to.")

    planning_queue = topics[args.planning_topic]
    control_queue = topics.get(args.control_topic, None)
    
    while True:
        cones = planning_queue.get()
        path = pathfind(cones)

        if control_queue is not None:
            control_queue.put(path)

if __name__ == "__main__":
    main()