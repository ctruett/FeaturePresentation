import sublime
import sublime_plugin

region = ''
text = ''


class capture(sublime_plugin.EventListener):

    def on_pre_close(self, view):

        # Get settings from scratchpad view
        settings = view.settings()
        file_name = settings.get('file_name')
        sel_start = settings.get('sel_start')
        sel_end = settings.get('sel_end')

        # Construct a region for the replace we'll use later
        global region
        region = sublime.Region(sel_start, sel_end)

        # If we're reading a scratch, go ahead and process the changes
        if view.is_scratch() is True:

            # Get the string value of the scratchpad's contents
            global text
            text = view.substr(sublime.Region(0, view.size()))

            # Get the old view from our window object, and switch to it
            oldview = sublime.active_window().find_open_file(file_name)
            sublime.active_window().focus_view(oldview)

            # Replace text in original buffer
            oldview.run_command('fp_replace')
            return


class fp_replace(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.replace(edit, region, text)


class feature_presentation(sublime_plugin.TextCommand):

    def run(self, edit):
        # Get selection as region
        sel = sublime.Region(self.view.sel()[0].begin(),
                             self.view.sel()[0].end())

        # Make things easier later
        view = self.view
        offsets = [sel.begin(), sel.end()]

        # Create new view for focused text
        self.clone_text(sel, view.file_name(), offsets)

    def clone_text(self, region, file_name, offsets):

        # Create a new view for modifications
        focus = self.view.window().new_file()

        # Name the view
        focus.set_name('...')

        # Set it as a scratchpad
        focus.set_scratch(True)

        # Match syntax highlighting
        focus.set_syntax_file(self.view.settings().get('syntax'))

        # Set up storage variables
        focus.settings().set('file_name', file_name)
        focus.settings().set('sel_start', offsets[0])
        focus.settings().set('sel_end', offsets[1])

        text = ''
        lines = self.view.lines(region)

        # Populate new view with selection
        for line in lines:
            text += '%s\n' % self.view.substr(line)

        focus.run_command('append', {
            'characters': text,
            'force': True,
            'scroll_to_end': False
        })
