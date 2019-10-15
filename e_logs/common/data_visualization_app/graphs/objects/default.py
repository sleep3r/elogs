import plotly.graph_objs as go


def ShiftTimeline(x, y, title):
    """
    Timeline plot for data in shifts

    Parameters
    ----------
    x : list of numbers
        description
    y : list of Shifts
        description
    title: string
        graph title

    Returns
    -------
    fig : plotly figure
    """
    trace = go.Scatter(x=[shift.start_time for shift in x], y=y)
    xaxis = go.XAxis(showgrid=True, showline=True, showticklabels=True,
                     ticktext=[str(shift.start_time) + f' Смена {shift.order}' for shift in x],
                     tickvals=[shift.start_time for shift in x],
                     )

    layout = go.Layout(title=title, xaxis=xaxis, )

    return go.Figure(data=[trace], layout=layout)


def ShiftHistogram(x, y, title):
    """
    Historgram for data in shifts

    Parameters
    ----------
    x : list of numbers
        description
    y : list of Shifts
        description
    title: string
        graph title

    Returns
    -------
    fig : plotly figure
    """
    print(x, y)
    trace = go.Histogram(x=y, xbins=dict(start=0.0, end=100.0, size=10))
    layout = go.Layout(title=title)

    return go.Figure(data=[trace], layout=layout)


verbose_names = {
    "ShiftTimeline": ShiftTimeline,
    "ShiftHistogram": ShiftHistogram
}
