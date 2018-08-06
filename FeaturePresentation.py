import sublime
import sublime_plugin

basicmode = None

class capture(sublime_plugin.EventListener):

    def on_pre_close(self, view):

        # Test to see if basic mode is enabled
        if basicmode is True:
            return

        # If we're reading a scratch, go ahead and process the changes
        if view.is_scratch() is True and view.settings().has('feature_presentation_initial_view_id'):

            # Get the scratchpad's contents
            text = view.substr(sublime.Region(0, view.size()))

            scratch_view_settings = view.settings()

            # Check if this is the last scratch view for the same initial view
            # If it isn't: show a message saying that text could not be copied (due to problem with changing regions if length of text is changed)
            viewsWithHigherIndex = list(filter(lambda v: v.settings().get('feature_presentation_initial_view_id') == scratch_view_settings.get('feature_presentation_initial_view_id') and scratch_view_settings.get('feature_presentation_index') < v.settings().get('feature_presentation_index'), sublime.active_window().views()))
            if len(viewsWithHigherIndex) > 0:
                sublime.message_dialog("Not inserting text because this is not the last scratch view")
                return

            # Get the old view by id saved in scratch view settings
            source_view = list(filter(lambda v: v.id() == scratch_view_settings.get('feature_presentation_initial_view_id'), sublime.active_window().views()))[0]

            source_view_settings = source_view.settings()

            # Copy new text and original region start and end into source view
            source_view_settings.set('feature_presentation_new_text', text)
            source_view_settings.set('feature_presentation_original_text_region_start', scratch_view_settings.get('feature_presentation_original_text_region_start'))
            source_view_settings.set('feature_presentation_original_text_region_end', scratch_view_settings.get('feature_presentation_original_text_region_end'))

            # Replace text in original buffer
            source_view.run_command('fp_replace')
            return


class fp_replace(sublime_plugin.TextCommand):

    def run(self, edit):
        # Get new text
        new_text = self.view.settings().get('feature_presentation_new_text')

        # Get original region
        sel_start = self.view.settings().get('feature_presentation_original_text_region_start')
        sel_end = self.view.settings().get('feature_presentation_original_text_region_end')
        region = sublime.Region(sel_start, sel_end)

        # Replace text in original document
        self.view.replace(edit, region, new_text)


class feature_presentation(sublime_plugin.TextCommand):

    def run(self, edit):

        # Make thisngs easier later
        sv = self.view

        # Get selection start and end points
        sel = sv.sel()[0]
        sel_start = sv.text_point(sv.rowcol(sel.begin())[0], 0)
        sel_end = sv.text_point(sv.rowcol(sel.end())[0], 0)

        # Grab contents of fp_basic setting
        global basicmode
        basicmode = sv.settings().get("fp_basic")

        # Get id of initial view
        source_id = sv.id()

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

        # Create new view for focused text
        self.clone_text()

    def clone_text(self):

        # Make things easier later
        sv = self.view

        for idx, sel in enumerate(sv.sel()):

            # Create a new view for modifications
            focus = sv.window().new_file()

            # Name the view
            focus.set_name('...' + str(idx))

            # Set view as scratch
            focus.set_scratch(True)

            # Match syntax highlighting
            focus.set_syntax_file(sv.settings().get('syntax'))

            # New view's settings
            new_settings = focus.settings()

            # Store original view's id in new view
            new_settings.set('feature_presentation_initial_view_id', sv.id())
            new_settings.set('feature_presentation_index', idx)

            # Store original view's selected text and region start/end into new view's settings
            sel_start = sel.begin() #sv.text_point(sv.rowcol(sel.begin())[0], 0)
            sel_end = sel.end() #sv.text_point(sv.rowcol(sel.end())[0], 0)
            otex = sv.substr(sel)
            new_settings.set('feature_presentation_original_text', otex)
            new_settings.set('feature_presentation_original_text_region_start', sel_start)
            new_settings.set('feature_presentation_original_text_region_end', sel_end)

            # Append selected text
            focus.run_command('append', {
                'characters': otex,
                'force': False,
                'scroll_to_end': False
            })

        # Clear selection
        sv.sel().clear()