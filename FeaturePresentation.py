import sublime, sublime_plugin

class FeaturePresentation(sublime_plugin.TextCommand):
	def run(self, edit):

		activated = self.view.settings().get('infocus')

		for region in self.view.sel():
			regions = []

			midpoint = region.begin() + region.size()/2

			ss = self.view.text_point(self.view.rowcol(region.begin())[0] - 1, 0)
			se = self.view.text_point(self.view.rowcol(region.end())[0] + 1, 0)

			tr = sublime.Region(0,ss - 1)
			br = sublime.Region(se,self.view.size())

			regions = [tr,br]

			if activated == None:
				self.view.fold(regions)
				self.view.settings().set('infocus', True)

			if activated == False:
				self.view.fold(regions)
				self.view.settings().set('infocus', True)

			if activated == True:
				self.view.unfold(regions)
				self.view.settings().set('infocus', False)

			self.view.show_at_center(midpoint)