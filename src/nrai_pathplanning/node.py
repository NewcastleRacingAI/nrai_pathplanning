from .code import pathfind
import argparse
from multiprocessing import Queue
import logging

def main(args: argparse.Namespace):
    topics: dict[str, Queue] = args.topics or {}
    logging.basicConfig(format=args.logger_format or "", level=args.actual_verbosity() if args.actual_verbosity else logging.INFO)
    logger = logging.getLogger()
    logger.info("Initializing...")


    # --- Set up Code ---
    if args.planning_topic not in topics:
        raise ValueError(f"No '{args.planning_topic}' topic to listen to.")

    planning_queue = topics[args.planning_topic]
    control_queue = topics.get(args.control_topic, None)
    
    while True:
        logger.debug("Starting loop")
        while planning_queue.qsize() > 1:
            logger.debug("Emptying queue")
            planning_queue.get_nowait()
        cones = planning_queue.get()
        logger.debug("Received %s", cones)
        path = pathfind(cones)

        #logger.info("Cones: %s => Path %s", cones, path)

        if control_queue is not None:
            control_queue.put(path)
            logger.debug("Sent %s", path)

if __name__ == "__main__":
    main()