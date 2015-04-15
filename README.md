
Feature Presentation
====================

![demo](demo.gif)

While working with a large document, sometimes it's necessary to focus on a specific bit of text without any distractions. In the past, I would insert line breaks before and after the region I wanted to focus on, but that is both slow and sloppy.

Enter Feature Presentation.

This plugin allows you to focus on single portion of your document.  To activate Feature Presentation, select the portion of your document that you would like to isolate, and press a keyboard shortcut.

After editing, close the window and whatever change you made will be applied to your original document.


### Installation

Available on [Package Control](https://packagecontrol.io/packages/Feature%20Presentation)

After installation, add

    { "keys": ["alt+i"], "command": "feature_presentation" }

to your keybindings, changing `alt+i` to whatever you want.

### Basic mode

![basic mode demo](demo-basic.gif)

Basic mode, which folds the text around your selection instead of creating a new window, can be enabled by adding

    "fp_basic": true

to your user preferences.


### Bugs

* Fold markers move around a little bit when isolating a block of text that has a fold in it 