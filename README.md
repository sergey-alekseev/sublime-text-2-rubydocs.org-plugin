# Sublime Text 2 plugin: RubyDocs

This plugin is a client for [RubyDocs](http://rubydocs.org/) API.

## Using

Open the command palette (cmd-shift-p) and choose "RubyDocs" while your cursor is on a word.

Make a keybind by adding the following to your `User/Default (OSX).sublime-keymap`:

  { "keys": ["super+shift+h"], "command": "rubydocs" }

## Installing

First, you need to have `git` installed and in your `$PATH`.
Afterwards you may need to restart Sublime Text 2 before the plugin will work.

### OSX

    $ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    $ git clone git://github.com/sergey-alekseev/sublime-text-2-rubydocs.org-plugin.git RubyDocs

### Linux (Ubuntu like distros)

    $ cd ~/.config/sublime-text-2/Packages/
    $ git clone git://github.com/sergey-alekseev/sublime-text-2-rubydocs.org-plugin.git RubyDocs

### Windows 7:

    Copy the directory to: "C:\Users\<username>\AppData\Roaming\Sublime Text 2\Packages"

### Windows XP:

    Copy the directory to: "C:\Documents and Settings\<username>\Application Data\Sublime Text 2\Packages"
