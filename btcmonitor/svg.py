#!/usr/bin/env python
import svgwrite
import time
from xdg import XDG_CACHE_HOME


def data_interval(data, t):
    min_time = int(time.time()) - t
    return([[t, v] for [t, v] in data if t > min_time])


def scale(time_value):
    [times, values] = zip(*time_value)
    return(min(times), max(times), min(values), max(values))


def btc_graph(btc_price_history):
    reduced_history = data_interval(btc_price_history, 2*60*60)
    (t_min, t_max, v_min, v_max) = scale(reduced_history)
    [t0, v0] = reduced_history[0]
    dwg = svgwrite.Drawing(
        XDG_CACHE_HOME / 'btc_graph.svg',
        profile='tiny'
    )
    height = 18 
    width = 3 * 24

    time_scale = (t_max - t_min) / width
    value_scale = (v_max - v_min) / height

    for [t, v] in reduced_history[1:]:
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
