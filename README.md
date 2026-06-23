# nrai_pathplanning

Newcastle Racing AI path planning module.

It takes the cones detected by perception (blue on the left of the track, yellow on
the right) and works out a centre line down the middle of the track for the car to
follow.

## How it fits in

This module runs as part of the autonomous pipeline and talks to the other modules
through named pipes (FIFOs). No ROS.

- Reads cones from `/tmp/PERCEPTION_ZedYoloTrack` (written by perception)
- Writes the path to `/tmp/PATHPLANNING_Path` (read by the controller)

Cones arrive as `[left, right]`, where each side is a list of `(x, z)` points. The
path is sent back as a list of `(x, z)` points, nearest the car first. An empty list
means "no drivable path, stop".

## How it works

1. Delaunay triangulation pairs blue and yellow cones across the track and takes the
   midpoint of each link.
2. A forward search joins those midpoints into one centre line and ignores stray
   off-track cones.
3. If only one cone colour is visible (common in tight corners), it offsets that side
   inward by half the track width instead of giving up.
4. The line is smoothed with a spline so the steering target is not jagged.

Step by step:

<img width="1210" height="1210" alt="delaunay_worksheet" src="https://github.com/user-attachments/assets/ca87c3d1-d8ec-4486-be72-3d322c08f1ea" />

## Files

- `nrai_pathplanning/code.py` - the planning algorithm (`plan_path` / `pathfind`).
- `nrai_pathplanning/node.py` - the FIFO node that reads cones and writes the path.

## Running

Needs Python 3.8 or newer with numpy and scipy.

```
pip install -r requirements.txt
cd nrai_pathplanning
python3 node.py
```
