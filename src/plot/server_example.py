import colorcet as cc
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import Button
from bokeh.layouts import column
import random


def make_document(doc):

    # make a list of groups
    strategies = ["DD", "DC", "CD", "CCDD"]

    # initialize some vars
    step = 0
    callback_obj = None
    colors = cc.glasbey_dark
    # create a list to hold all CDSs for active strategies in next step
    sources = []

    # Create a figure container
    fig = figure(title="Streaming Line Plot - Step 0", width=800, height=400)

    # get step 0 data for initial strategies
    for i in range(len(strategies)):
        step_data = dict(
            step=[step], strategy=[strategies[i]], ncount=[random.choice(range(1, 100))]
        )
        data_source = ColumnDataSource(step_data)
        color = colors[i]
        # this will create one fig.line renderer for each strategy & its data for this step
        fig.line(x="step", y="ncount", source=data_source, color=color, line_width=2)
        # add this CDS to the sources list
        sources.append(data_source)

    def button1_run():
        nonlocal callback_obj
        if button1.label == "Run":
            button1.label = "Stop"
            button1.button_type = "danger"
            callback_obj = doc.add_periodic_callback(button2_step, 100)
        else:
            button1.label = "Run"
            button1.button_type = "success"
            doc.remove_periodic_callback(callback_obj)

    def button2_step():
        nonlocal step
        data = []
        step += 1
        fig.title.text = "Streaming Line Plot - Step " + str(step)
        for i in range(len(strategies)):
            step_data = dict(
                step=[step],
                strategy=[strategies[i]],
                ncount=[random.choice(range(1, 100))],
            )
            data.append(step_data)
        for source, data in zip(sources, data):
            source.stream(data)

    # add on_click callback for button widget
    button1 = Button(label="Run", button_type="success", width=390)
    button1.on_click(button1_run)
    button2 = Button(label="Step", button_type="primary", width=390)
    button2.on_click(button2_step)

    doc.add_root(column(fig, button1, button2))
    doc.title = "Now with live updating!"


if __name__ == "__main__":
    apps = {
        "/app1": Application(FunctionHandler(make_document)),
        "/app2": Application(FunctionHandler(make_document)),
    }

    server = Server(
        apps,
        port=5006,
        allow_websocket_origin=["*"],
        check_unused_sessions=1000 * 30,
        unused_session_lifetime=1000 * 60 * 60 * 24,
        session_expiration_duration=1000 * 60 * 60 * 24 * 1.1,
        session_token_expiration=1000 * 60 * 60 * 24,
        address="0.0.0.0",
    )
    server.start()

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
