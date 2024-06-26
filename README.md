Dan's Plot Core is a minimal library that adds plots with low-latency interactivity to Python.

## flow
- A `Plot` is created.
- Geometry is added to the plot in logical coordinates.
    - Can be done directly, or with a `plot_*` convenience function.
        - Convenience functions obey the current `transform` and `primitive`
            - `transform` takes logical coordinates `x, y`, sample index `i`, and plot `series`, and gives logical coordinates `x, y` and color `r, g, b, a`
            - `primitive` takes logical coordinates `x, y` and color `r, g, b, a` and adds geometry to the plot.
- The plot is `show`n (or resized).
    - A logical view is calculated.
    - `late_vertexors` are allowed to know the number of pixels in the display, and the shape of the logical view, to add further geometry to the plot.
- The plot can be interacted with.
    - Logical coordinates are converted to display coordinates on each render.
        - This step is quick because it is done on the graphics card.
- The convenience function `plot` can do all of the above for simple usages.
