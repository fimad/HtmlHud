from gi.repository import WebKit, Gtk, Gdk
import signal
import json
import sys
import os

class HudWebview(WebKit.WebView):
    def __init__(self, themes, scripts, js_handler, startup_handler):
        WebKit.WebView.__init__(self)
        self.set_transparent(True)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0,0,0))
        #self.load_uri('file:///home/will/Coding/hmenu/test.html')
        htmlHudDir = os.environ["HTML_HUD"]
        self.load_html_string ("""
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="file://"""+htmlHudDir+"""/html-hud.css" />
        <script type="text/javascript" src="file://"""+htmlHudDir+"""/scripts/jquery-1.9.1.min.js"></script>
        <script type="text/javascript" src="file://"""+htmlHudDir+"""/scripts/jstween-1.1.min.js"></script>
        <script type="text/javascript" src="file://"""+htmlHudDir+"""/scripts/html-hud.js"></script>
        """
        + "\n".join(map(lambda js: '<script type="text/javascript" src="file://%s"></script>'%js, scripts))
        + "\n".join(map(lambda css: '<link rel="stylesheet" type="text/css" href="file://%s"></link>'%css, themes))
        + """
    </head>
    <body>
    </body>
</html>""", "file:///")
        self.connect("key_press_event", self.on_key_press_event)
        self.connect('title-changed', self.on_title_changed)
        self.connect('load-finished', self.on_load_finished)

        self.js_handler = js_handler
        self.startup_handler = startup_handler

    def on_key_press_event(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Escape":
            sys.exit(0)
        #print "Key %s (%d) was pressed" % (keyname, event.keyval)

    def on_load_finished(self, webview, frame):
        if self.startup_handler != None:
            self.startup_handler()


    def on_title_changed(self, widget, frame, title):
        if title != 'null' and self.js_handler != None:
            self.js_handler(json.loads(title))

class HudWindow(Gtk.Window):
    def __init__(self, width, height, themes, scripts, js_handler, startup_handler):
        Gtk.Window.__init__(self)

        self.resize(width,height)
        self.set_title("html-hud")
        #self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)

        #Set transparency
        screen = self.get_screen()
        rgba = screen.get_rgba_visual()
        self.set_visual(rgba)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0,0,0))

        #Add all the parts
        self.view = HudWebview(themes, scripts, js_handler, startup_handler)
        box = Gtk.Box()
        self.add(box)
        box.pack_start(self.view, True, True, 0)
        self.set_decorated(False)
        self.connect("destroy", lambda q: Gtk.main_quit())

        #Show all the parts
        self.show_all()

class HudApp:
    def __init__(self, themes=[], scripts=[]):
        #Get screen geometry
        s = Gdk.Screen.get_default()
        #Get all components
        self.win = HudWindow(s.get_width(), s.get_height(), themes, scripts, self.js_callback, self.startup)

        #Make sure Ctl-C works
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def run_js(self, js):
        self.win.view.execute_script(js)

    def run(self):
        Gtk.main()
        
    #Virtual Methods:

    #called when js passes a value to python
    def js_callback(self, value):
        pass

    #called after webkit is finished loading
    def startup(self):
        pass
