import os
import sys
import json
import HtmlHud

class HMenu(HtmlHud.HudApp):
    def __init__(self, lines, css=[], js=[]):
        htmlHudDir = os.environ["HTML_HUD"]
        themes = [htmlHudDir+"/hmenu/hmenu.css"] + css
        scripts = [htmlHudDir+"/hmenu/hmenu.js"] + js
        HtmlHud.HudApp.__init__(self, themes, scripts)
        #save the lines so we can use them in the startup routine
        self.lines = map(lambda l: l.rstrip(), lines)

    def js_callback(self, value):
        print value
        sys.exit(0)

    def startup(self):
        self.run_js("add_lines(%s)" % json.dumps(self.lines))


if __name__ == '__main__':
    hmenu = HMenu(sys.stdin.readlines())
    hmenu.run()
