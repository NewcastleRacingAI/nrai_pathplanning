def pathfind(cones):
    left = cones[0]
    right = cones[1]
    midpoints = []

    for L in left:
        best = None
        min_d = 999
        for R in right:
            d = abs(L[1] - R[1])          #diff in z value
            if d < min_d:                
                min_d = d
                best = R

        if best:
            mx = (L[0] + best[0]) / 2
            mz = (L[1] + best[1]) / 2
            midpoints.append((mx, mz))
    return midpoints
