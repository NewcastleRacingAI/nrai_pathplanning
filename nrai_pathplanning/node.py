import os
import pickle
import time
import functools
print = functools.partial(print, flush=True)
from code import pathfind

FIFO_IN = "/tmp/PERCEPTION_ZedYoloTrack"
FIFO_OUT = "/tmp/PATHPLANNING_Path"

# creates the pipe so that it removes any leftover one first so it does not crash on a second run
def _ensure_fifo(path):
    if os.path.exists(path):
        os.remove(path)
    os.mkfifo(path, 0o600)
    
# reads cones from the perception pipe to run pathfind and
# writes the path to the controller pipe and loops forever
def main(args=None):
    _ensure_fifo(FIFO_OUT)
    print(
        f"NRAI_PATHPLANNING: start FIFO_IN={FIFO_IN}, "
        f"FIFO_OUT={FIFO_OUT}"
    )
    while True:
        try:
            print(f"NRAI_PATHPLANNING: opening {FIFO_IN}")
            fd_in = os.open(FIFO_IN, os.O_RDONLY)
        except FileNotFoundError:
            print(f"NRAI_PATHPLANNING: retry")
            time.sleep(0.5)
            continue
        with open(fd_in, "rb") as fin:
            print(f"NRAI_PATHPLANNING: opened {FIFO_IN}.")
            while True:
                try:
                    cones = pickle.load(fin)
                except EOFError:
                    print("NRAI_PATHPLANNING: input pipe closed")
                    break
                try:
                    length = len(cones)
                except Exception:
                    length = "N/A"
                print(f"NRAI_PATHPLANNING: received cones type={type(cones).__name__} len={length}")
                path = pathfind(cones)
                try:
                    plen = len(path)
                except Exception:
                    plen = "N/A"
                print(f"NRAI_PATHPLANNING: computed path type={type(path).__name__} len={plen}")
                try:
                    fd_out = os.open(FIFO_OUT, os.O_WRONLY)
                    with open(fd_out, "wb") as fout:
                        pickle.dump(path, fout)
                        print(f"NRAI_PATHPLANNING: wrote path to {FIFO_OUT}")
                except FileNotFoundError:
                    print(f"NRAI_PATHPLANNING: {FIFO_OUT} not configured yet")
                except BrokenPipeError:
                    print(f"NRAI_PATHPLANNING: {FIFO_OUT} reader went away")
                    
if __name__ == "__main__":
    main()
