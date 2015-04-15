import sublime
import sublime_plugin

region = ''
text = ''
otex = ''


class capture(sublime_plugin.EventListener):

    def on_pre_close(self, view):

        # Get settings from scratchpad view
        settings = view.settings()
        file_name = settings.get('file_name')

        # If we're reading a scratch, go ahead and process the changes
        if view.is_scratch() is True:

            # Get the string value of the scratchpad's contents
            global text
            text = view.substr(sublime.Region(0, view.size()))

            # Get the old view from our window object, and switch to it
            oldview = sublime.active_window().find_open_file(file_name)

            # Replace text in original buffer
            oldview.run_command('fp_replace')
            return


class fp_replace(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.replace(edit, region, text)


class feature_presentation(sublime_plugin.TextCommand):

    def run(self, edit):
        # Get selection as region
        global region
        region = sublime.Region(self.view.sel()[0].begin(),
                                self.view.sel()[0].end())

        global otex
        otex = self.view.substr(region)

        # Make things easier later
        view = self.view

        # Create new view for focused text
        self.clone_text(view.file_name())

    def clone_text(self, file_name):

        # Create a new view for modifications
        focus = self.view.window().new_file()

        # Name the view
        focus.set_name('...')

        # Set it as a scratchpa
        focus.set_scratch(True)

        # Match syntax highlighting
        focus.set_syntax_file(self.view.settings().get('syntax'))

        # Set up storage variables
        focus.settings().set('file_name', file_name)

        focus.run_command('append', {
            'characters': otex,
            'force': False,
            'scroll_to_end': False
        })
