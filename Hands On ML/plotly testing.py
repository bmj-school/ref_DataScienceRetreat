#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 17:34:30 2018

@author: batman
"""
print_imports()

import plotly as py
py.plotly.plotly.tools.set_credentials_file(username='notbatman', api_key='1hy2cho61mYO4ly5R9Za')
import plotly.graph_objs as pg

trace0 = pg.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = pg.Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = pg.Data([trace0, trace1])

py.plot(data, filename = 'basic-line')

py.offline.plot({
    "data": [pg.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": pg.Layout(title="hello world")
})