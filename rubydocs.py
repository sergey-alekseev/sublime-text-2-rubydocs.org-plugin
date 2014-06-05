import sublime, sublime_plugin
import urllib2
import json

class RubydocsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            word = self.view.word(region)
            if not word.empty():
                keyword = self.view.substr(word)
                response = urllib2.urlopen("http://api.rubydocs.com/search?q=%s" % keyword).read()
                content = json.loads(response)['content']
                view = sublime.active_window().new_file()
                view.insert(edit, 0, content)
