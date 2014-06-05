#!/usr/bin/python

import functools
import os
import re
import subprocess
import threading

import sublime
import sublime_plugin


def open_url(url):
    sublime.active_window().run_command('open_url', {"url": url})


def main_thread(callback, *args, **kwargs):
    # sublime.set_timeout gets used to send things onto the main thread
    # most sublime.[something] calls need to be on the main thread
    sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)


def _make_text_safeish(text, fallback_encoding, method='decode'):
    # The unicode decode here is because sublime converts to unicode inside
    # insert in such a way that unknown characters will cause errors, which is
    # distinctly non-ideal... and there's no way to tell what's coming out of
    # git in output. So...
    try:
        unitext = getattr(text, method)('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        unitext = getattr(text, method)(fallback_encoding)
    except AttributeError:
        # strongly implies we're already unicode, but just in case let's cast
        # to string
        unitext = str(text)
    return unitext


class CommandThread(threading.Thread):
    def __init__(self, command, on_done, working_dir="", fallback_encoding=""):
        threading.Thread.__init__(self)
        self.command = command
        self.on_done = on_done
        self.working_dir = working_dir
        self.fallback_encoding = fallback_encoding

    def run(self):
        try:
            # Per http://bugs.python.org/issue8557 shell=True is required to
            # get $PATH on Windows. Yay portable code.
            shell = os.name == 'nt'
            if self.working_dir != "":
                os.chdir(self.working_dir)

            proc = subprocess.Popen(self.command,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                shell=shell, universal_newlines=True)
            output = proc.communicate()[0]
            main_thread(self.on_done,
                _make_text_safeish(output, self.fallback_encoding))
        except subprocess.CalledProcessError as e:
            main_thread(self.on_done, e.returncode)


class RubydocsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            word = self.view.word(region)
            if not word.empty():
                # scope: "text.html.basic source.php.embedded.block.html keyword.other.new.php"
                scope = self.view.scope_name(word.begin()).strip()
                extracted_scope = scope.rpartition('.')[2]
                keyword = self.view.substr(word)
                open_url("http://api.rubydocss.org/search?q=%s" % keyword)


    def run_command(self, command, callback=None, **kwargs):
        if not callback:
            callback = self.panel
        thread = CommandThread(command, callback, **kwargs)
        thread.start()

    def panel(self, output, **kwargs):
        active_window = sublime.active_window()
        if not hasattr(self, 'output_view'):
            self.output_view = active_window.get_output_panel("rubydocs")
        self.output_view.set_read_only(False)
        self.output_view.run_command('rubydocs_output', {
            'output': output,
            'clear': True
        })
        self.output_view.set_read_only(True)
        active_window.run_command("show_panel", {"panel": "output.rubydocs"})


class RubydocsOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, output = '', output_file = None, clear = False):
        if clear:
            region = sublime.Region(0, self.view.size())
            self.view.erase(edit, region)
        self.view.insert(edit, 0, output)
