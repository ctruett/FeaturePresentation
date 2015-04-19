import sublime
import sublime_plugin

# Set up storage variables
file_name = ''
region = ''
text = ''
otex = ''
basicmode = None


class capture(sublime_plugin.EventListener):

    def on_pre_close(self, view):

        # Test to see if basic mode is enabled
        if basicmode is True:
            return

        # If we're reading a scratch, go ahead and process the changes
        if view.is_scratch() is True:

            # Get the scratchpad's contents
            global text
            text = view.substr(sublime.Region(0, view.size()))

            # Get the old view from our window object, and switch to it
            oldview = sublime.active_window().find_open_file(file_name)

            # Replace text in original buffer
            oldview.run_command('fp_replace')
            return


class fp_replace(sublime_plugin.TextCommand):

    def run(self, edit):
        # Replace text in original document
        self.view.replace(edit, region, text)


class feature_presentation(sublime_plugin.TextCommand):

    def run(self, edit):

        # Make things easier later
        sv = self.view

        # Get selection start and end points
        sel = sv.sel()[0]
        sel_start = sv.text_point(sv.rowcol(sel.begin())[0], 0)
        sel_end = sv.text_point(sv.rowcol(sel.end())[0], 0)

        # Grab contents of fp_basic setting
        global basicmode
        basicmode = sv.settings().get("fp_basic")

        # If basic mode is enabled...
        if basicmode is True:

            # Get contents of test settings
            active = sv.settings().get('infocus')

            # Prepare storage for folded regions
            regions = []

            # Find the midpoint of the selection
            midpoint = sel.begin() + sel.size() / 2

            # Set up top and bottom regions
            tr = sublime.Region(0, sel_start - 1)
            br = sublime.Region(sel_end, sv.size())
            regions = [tr, br]

            # If fp is not activated, activate it!
            if active is None:
                sv.fold(regions)
                sv.settings().set('infocus', True)

            # If fp is not activated, activate it!
            if active is False:
                sv.fold(regions)
                sv.settings().set('infocus', True)

            # If fp is activated, deactivate it!
            if active is True:
                sv.unfold(regions)
                sv.settings().set('infocus', False)

            # Center the screen around the previously isolated region
            sv.show_at_center(midpoint)
            return

        # Store filename
        global file_name
        file_name = sv.file_name()

        # Get selection as region
        global region
        region = sublime.Region(sel_start, sel_end)

        # Store original text
        global otex
        otex = sv.substr(region)

        # Create new view for focused text
        self.clone_text()

    def clone_text(self):

        # Create a new view for modifications
        focus = self.view.window().new_file()

        # Name the view
        focus.set_name('...')

        # Set view as scratch
        focus.set_scratch(True)

        # Match syntax highlighting
        focus.set_syntax_file(self.view.settings().get('syntax'))

        # Append selected text
        focus.run_command('append', {
            'characters': otex,
            'force': False,
            'scroll_to_end': False
        })
