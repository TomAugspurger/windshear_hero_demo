import holoviews as hv
from bokeh.server.server import Server
import os
from IPython.core.display import display, HTML
import ipywidgets as widgets
import qrcode
from holoviews.streams import FreehandDraw
import geoviews as gv


def make(plot, port=0, websocket_origin='pangeo.informaticslab.co.uk', url_path='annotable'):
    renderer = hv.renderer('bokeh')
    app = renderer.app(plot)
    server = Server({f'/{url_path}': app}, port=port, allow_websocket_origin=[websocket_origin])
    
    server.start()
    
    prefix = os.environ['JUPYTERHUB_SERVICE_PREFIX']
    url = f"https://{websocket_origin}{prefix}proxy/{server.port}/{url_path}"
    display(HTML(f'<a href={url}>{url}</a>'))
    display(qrcode.make(url))
    
    stop_button = widgets.Button(description=f"Stop {url_path}")
    stop_button.on_click(lambda b: server.stop())
    display(stop_button)
    
    return server


def warning(color="orange"):
    warning = gv.Polygons([]).opts(line_color=color, line_width=3, 
                                      fill_color=color, fill_alpha=0.2)
    pen = FreehandDraw(source=warning)

    return pen, warning
    