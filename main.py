import panel as pn


# def get_DF(ticker):


def create_app():
    widget = pn.widgets.TextInput(name='A widget2', value='A string')
    slider = pn.widgets.FloatSlider(name='Another widget', width=200)
    return pn.Column(widget, slider, width=200)

def main():
    APP_ROUTES = {"/app1": create_app, "app2": pn.pane.Markdown("# App2")}

    pn.serve(APP_ROUTES, port=5006 ,  autoreload = True ) #, allow_websocket_origin=["127.0.0.1:5006"], address="127.0.0.1", show=False)
    
    return


if __name__ == '__main__':
     main()

