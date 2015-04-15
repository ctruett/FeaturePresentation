
Feature Presentation
====================

While working with a large document, sometimes I want to focus on a specific portion without any distractions. In the past, I would insert line breaks before and after the region I wanted to focus on, but that is both slow and sloppy.

Enter Feature Presentation.

This plugin allows you to focus on single portion of your document.  To activate Feature Presentation, select the portion of your document that you would like to isolate, and press a keyboard shortcut.

After editing, close the window and whatever change you made will be applied to your original document.

### Demonstration

![demo](demo.gif)

### Installation

Available on [Package Control](https://packagecontrol.io/packages/Feature%20Presentation)

### Keybindings

Add `{ "keys": ["f8"], "command": "feature_presentation" }` to your keybindings, changing `f8` to whatever you want.

### Bugs to be squashed

* Fold markers move around a little bit when isolating a block of text that has a fold in it 