#!/usr/bin/env python
import svgwrite
import time
from xdg import XDG_CACHE_HOME




def scale(time_value):
    [times, values] = zip(*time_value)
    return(min(times), max(times), min(values), max(values))


def btc_graph(btc_price_history):
    (t_min, t_max, v_min, v_max) = scale(btc_price_history)
    [t0, v0] = btc_price_history[0]
    dwg = svgwrite.Drawing(
        XDG_CACHE_HOME / 'btc_graph.svg',
        profile='tiny'
    )
    height = 18 
    width = 3 * 24

    time_scale = (t_max - t_min) / width
    value_scale = (v_max - v_min) / height

    # Draw grid
    n = 0
    while True:
        grid_position = int(v_min/100) * 100 + n * 100
        if grid_position >= v_min or grid_position <= v_max:
            dwg.add(
                dwg.line(
                    (0, (v_max-grid_position)/value_scale),
                    (width, (v_max-grid_position)/value_scale),
                    stroke='green', stroke_width = 0.6
                )
            )
        if grid_position > v_max:
            break
        n += 1

    # Draw the graph
    for [t, v] in btc_price_history[1:]:
        if (t - t0) < 300:
            dwg.add(
                dwg.line(
                    ((t0-t_min)/time_scale, (v_max - v0)/value_scale),
                    ((t-t_min)/time_scale, (v_max - v)/value_scale),
                    stroke='green'
                )
            )
        [t0, v0] = [t, v]

    dwg.save()
