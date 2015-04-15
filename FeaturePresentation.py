import sublime
import sublime_plugin

# Set up storage variables
file_name = ''
region = ''
text = ''
otex = ''


class capture(sublime_plugin.EventListener):

    def on_pre_close(self, view):

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
        self.view.replace(edit, region, text)


class feature_presentation(sublime_plugin.TextCommand):

    def run(self, edit):

        # Store filename
        global file_name
        file_name = self.view.file_name()

        # Get selection as region
        global region
        region = sublime.Region(self.view.sel()[0].begin(),
                                self.view.sel()[0].end())

        # Store original text
        global otex
        otex = self.view.substr(region)

        # Create new view for focused text
        self.clone_text()

    def clone_text(self):

        # Create a new view for modifications
        focus = self.view.window().new_file()

        # Name the view
        focus.set_name('...')

        # Set it as a scratchpa
        focus.set_scratch(True)

        # Match syntax highlighting
        focus.set_syntax_file(self.view.settings().get('syntax'))

        # Append selected text
        focus.run_command('append', {
            'characters': otex,
            'force': False,
            'scroll_to_end': False
        })
