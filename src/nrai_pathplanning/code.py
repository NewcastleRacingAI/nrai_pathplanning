import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import splprep, splev

# min track width is 3m (trackdrive D8.1 / fig 4) in (https://www.formulastudent.de/fileadmin/user_upload/all/2026/rules/FS_Driverless_Specification_2026_v1.1.pdf)
DEFAULT_TRACK_WIDTH = 3.0
MAX_STEP = 6.0  # 5m rule + tolerance for diagonal (hopefully) / first hop from the car


def pathfind(cones):
    return plan_path(cones)

# the main function it takes the cones and returns the centre line for the car to follow
def plan_path(cones, track_width: float = DEFAULT_TRACK_WIDTH, smooth: bool = True):
    if not cones or len(cones) < 2:
        return []
    try:
        left = np.asarray(cones[0], dtype=float).reshape(-1, 2)
        right = np.asarray(cones[1], dtype=float).reshape(-1, 2)
    except (ValueError, TypeError):
        return []

    if len(left) >= 1 and len(right) >= 1:
        pts = _delaunay_midpoints(left, right)
        if len(pts) == 0:
            pts = _both_sides_fallback(left, right)
    elif len(left) >= 2:
        pts = _one_sided_path(left, side="left", track_width=track_width)
    elif len(right) >= 2:
        pts = _one_sided_path(right, side="right", track_width=track_width)
    else:
        return []

    if len(pts) == 0:
        return []

    ordered = _search_centerline(pts)
    if smooth:
        ordered = _smooth(ordered)
    return [tuple(p) for p in ordered]

# safe/stop contract helper for the controller side the controller should brake here
# if no cones are visible since it would signal the end of the track 
# it returns True when there is no path i.e. the signal for the controller to stop
def should_stop(path):
    return len(path) == 0
# connects blue and yellow cones into triangles and takes the midpoint of each blue to yellow link
def _delaunay_midpoints(left: np.ndarray, right: np.ndarray):
    all_pts = np.vstack([left, right])
    colour = np.array([0] * len(left) + [1] * len(right))  

    if len(all_pts) < 3:
        return _both_sides_fallback(left, right)
    try:
        tri = Delaunay(all_pts)
    except Exception: 
        return _both_sides_fallback(left, right)

    seen, mids = set(), []
    for s in tri.simplices:
        for a, b in ((s[0], s[1]), (s[1], s[2]), (s[2], s[0])):
            if colour[a] == colour[b]:
                continue  # same-side edge, skip
            key = (min(a, b), max(a, b))
            if key in seen:
                continue
            seen.add(key)
            mids.append((all_pts[a] + all_pts[b]) / 2.0)
    return np.array(mids) if mids else np.empty((0, 2))

# this an extra step i added
# its backup for when there are too few cones to triangulate andn pairs them by distance and takes midpoints
def _both_sides_fallback(left: np.ndarray, right: np.ndarray):
    if len(left) == 0 or len(right) == 0:
        return np.empty((0, 2))
    l = left[np.argsort(left[:, 1])]
    r = right[np.argsort(right[:, 1])]
    n = min(len(l), len(r))
    return (l[:n] + r[:n]) / 2.0

# when only one cone colour is visible builds the line 
# by shifting that side inward by half the track width
def _one_sided_path(wall: np.ndarray, side: str, track_width: float):
    wall = wall[np.argsort(wall[:, 1])]
    half = track_width / 2.0
    out, n = [], len(wall)
    for i in range(n):
        if i == 0:
            t = wall[1] - wall[0]
        elif i == n - 1:
            t = wall[-1] - wall[-2]
        else:
            t = wall[i + 1] - wall[i - 1]
        norm = np.linalg.norm(t)
        if norm < 1e-9:
            continue
        t = t / norm
        right_of_travel = np.array([t[1], -t[0]])      
        sign = 1.0 if side == "left" else -1.0          
        out.append(wall[i] + sign * half * right_of_travel)
    return np.array(out) if out else np.empty((0, 2))

# walks forward from the car to pickup the next point with the least turn and ignores stray off-track points
def _search_centerline(points: np.ndarray, max_turn_deg: float = 100.0,
                       angle_weight: float = 2.0, max_step: float = MAX_STEP):
    pts = [np.asarray(p, dtype=float) for p in np.asarray(points)]
    if not pts:
        return np.empty((0, 2))

    max_turn = np.radians(max_turn_deg)
    cur = np.array([0.0, 0.0])      
    heading = np.array([0.0, 1.0])  
    remaining = pts[:]
    path = []

    while remaining:
        best, best_cost, best_dir = None, np.inf, None
        for p in remaining:
            v = p - cur
            d = float(np.linalg.norm(v))
            if d < 1e-6 or d > max_step:
                continue 
            direction = v / d
            cosang = float(np.clip(np.dot(heading, direction), -1.0, 1.0))
            ang = np.arccos(cosang)
            if ang > max_turn:
                continue 
            cost = d * (1.0 + angle_weight * (ang / np.pi))
            if cost < best_cost:
                best, best_cost, best_dir = p, cost, direction
        if best is None:
            break
        path.append(best)
        heading = best_dir
        cur = best
        remaining = [q for q in remaining if not np.array_equal(q, best)]

    return np.array(path) if path else np.empty((0, 2))

# fits a smooth spline through the points so the steering target is not jagged
def _smooth(points: np.ndarray, n_out: int = 50):
    pts = np.asarray(points)
    if len(pts) < 4:
        return pts
    try:
        tck, _ = splprep([pts[:, 0], pts[:, 1]], s=len(pts) * 0.1)
        u = np.linspace(0.0, 1.0, n_out)
        x, z = splev(u, tck)
        return np.column_stack([x, z])
    except Exception:
        return pts
