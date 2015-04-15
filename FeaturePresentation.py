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

        if basicmode is None or False:

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

            return


class fp_replace(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.replace(edit, region, text)


class feature_presentation(sublime_plugin.TextCommand):

    def run(self, edit):

        global basicmode
        basicmode = self.view.settings().get("fp_basic")

        if basicmode is True:
            activated = self.view.settings().get('infocus')

            for region in self.view.sel():
                regions = []

                midpoint = region.begin() + region.size() / 2

                ss = self.view.text_point(self.view.rowcol(region.begin())[0] - 1, 0)
                se = self.view.text_point(self.view.rowcol(region.end())[0] + 1, 0)

                tr = sublime.Region(0, ss - 1)
                br = sublime.Region(se, self.view.size())

                regions = [tr, br]

                if activated is None:
                    self.view.fold(regions)
                    self.view.settings().set('infocus', True)

                if activated is False:
                    self.view.fold(regions)
                    self.view.settings().set('infocus', True)

                if activated is True:
                    self.view.unfold(regions)
                    self.view.settings().set('infocus', False)

                self.view.show_at_center(midpoint)
            return

        if basicmode is None or False:
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
            return

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
