import os
import pickle
from .code import pathfind

import time

fifo_in = '/tmp/PERCEPTION_ZedYoloTrack'
fifo_out = '/tmp/PATHPLANNING_Path'

def main(args=None):

    # Make FIFO output
    os.mkfifo(fifo_out, 0o600)
    
    while True:
        try:
            # FIFO input
            fd_in = os.open(fifo_in, os.O_RDONLY)
            with open(fd_in, "rb") as file:
                print(f"NRAI_PATHPLANNING: Successfully opened {fifo_in}.")
                while True:
                    cones = pickle.load(file)
                    path = pathfind(cones)
                    
                    try:
                        fd_out = os.open(fifo_out, os.O_WRONLY)
                        with open(fd_out, "wb") as fifo:
                            pickle.dump(path, fifo)
                    except FileNotFoundError:
                        print(f"NRAI_PATHPLANNING: Could not access FIFO {fifo_out}. Likely not yet configured.")
                    except BrokenPipeError:
                        print(f"NRAI_PATHPLANNING: FIFO {fifo_out} terminated")
                        
        except FileNotFoundError:
            print(f"NRAI_PATHPLANNING: Could not access FIFO {fifo_in}. Likely not yet configured.")
            time.sleep(0.5)
        except BrokenPipeError:
            print(f"NRAI_PATHPLANNING: FIFO {fifo_in} terminated")

if __name__ == "__main__":
    main()