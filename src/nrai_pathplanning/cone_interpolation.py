import numpy as np

def generate_virtual_cones(visible_cones: np.ndarray, side: str, track_width: float = 3):
    """
    Generate virtual cones on the missing side using local direction.
    """
    if len(visible_cones) == 0:
        return np.empty((0, 2))   # No cones at all -> return empty

    # Step 1: Sort cones by Z (forward direction)
    visible = visible_cones[np.argsort(visible_cones[:, 1])]

    virtual = []                  # List to store generated virtual cones
    n = len(visible)

    # Step 2: Loop through every visible cone
    for i in range(n):

        if n == 1:   # Special case: only 1 cone visible
            # No direction info, so we assume the track goes forward (+Z)
            offset = np.array([track_width if side == "right" else -track_width, 0.0])

        else:        # Normal case: 2 or more cones
            # Step 3: Estimate local tangent (travel direction) at this cone
            if i == 0:                    # First cone
                tangent = visible[1] - visible[0]
            elif i == n - 1:              # Last cone
                tangent = visible[-1] - visible[-2]
            else:                         # Middle cones (best estimation)
                tangent = visible[i + 1] - visible[i - 1]

            # Normalize tangent vector to unit length
            tangent = tangent / (np.linalg.norm(tangent) + 1e-9)

            # Step 4: Calculate perpendicular normal (Right-hand rule)
            # Rotate tangent 90 degrees: [tx, ty] -> [ty, -tx]
            normal = np.array([tangent[1], -tangent[0]])

            # Step 5: Decide direction based on which side is missing
            sign = 1.0 if side == "right" else -1.0

            # Step 6: Full offset = width * direction * normal
            offset = sign * track_width * normal

        # Step 7: Add offset to the visible cone position
        virtual.append(visible[i] + offset)

    return np.array(virtual)