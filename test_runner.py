import sublime
import sublime_plugin
import unittest

class __bespoke_docs_test_replace_cursor_position(sublime_plugin.TextCommand):
    def run(self, edit):
        cursor_placeholder = self.view.find('\|', 0)

        if not cursor_placeholder or cursor_placeholder.empty():
            return

        self.view.sel().clear()
        self.view.sel().add(cursor_placeholder.begin())
        self.view.replace(edit, cursor_placeholder, '')

class ViewTestCase(unittest.TestCase):

    def setUp(self):
        self.window = sublime.active_window()
        self.view = self.window.new_file()
        self.view.set_scratch(True)

        # TODO there's probably a better way to initialise the testcase default settings
        settings = self.view.settings()
        settings.set('auto_indent', False)
        settings.set('lower_case_primitives', False)
        settings.set('param_description', True)
        settings.set('per_section_indent', False)
        settings.set('return_description', True)
        settings.set('short_primitives', False)
        settings.set('spacer_between_sections', False)
        settings.set('function_description', True)

        if int(sublime.version()) < 3000:
            self.edit = self.view.begin_edit()

    def tearDown(self):
        if int(sublime.version()) < 3000:
            self.view.sel().clear()
            self.view.end_edit(self.edit)
            self.window.run_command('close')
        else:
            self.view.close()

    def set_view_content(self, content):
        if isinstance(content, list):
            content = '\n'.join(content)
        self.view.run_command('insert', {'characters': content})
        self.view.run_command('__bespoke_docs_test_replace_cursor_position')
        self.view.set_syntax_file(self.get_syntax_file())

    def get_syntax_file(self):
        raise NotImplementedError('Must be implemented')

    def get_view_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def run_bespoke_docs(self):
        self.view.run_command('bespoke_docs')

    def assert_bespoke_docs_result(self, expected):
        if isinstance(expected, list):
            expected = '\n'.join(expected)

        # TODO test selections; for now just removing the placeholders
        expected = expected.replace('|CURSOR|', '')
        expected = expected.replace('|SELECTION_BEGIN|', '')
        expected = expected.replace('|SELECTION_END|', '')

        self.assertEquals(expected, self.get_view_content())

class TestJavaScript(ViewTestCase):

    def get_syntax_file(self):
        return 'Packages/Ecmascript Syntax/ecmascript.sublime-syntax'

    def test_basic(self):
        self.set_view_content("\n/**|\nbasic")
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result('\n/**\n * \n */\nbasic')

    def test_empty_doc_blocks_are_created(self):
        self.set_view_content('/**')
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            "/**",
            " * |CURSOR|",
            " */"
        ])

    def test_that_function_template_is_added(self):
        self.set_view_content('/**|\nfunction foo () {')
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * |SELECTION_BEGIN|[foo description]|SELECTION_END|',
            ' * @return {[type]} [description]',
            ' */',
            'function foo () {'
        ])

    def test_parameters_are_added_to_function_templates(self):
        self.set_view_content('/**|\nfunction foo (bar, baz) {')
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * |SELECTION_BEGIN|[foo description]|SELECTION_END|',
            ' * @param  {[type]} bar [description]',
            ' * @param  {[type]} baz [description]',
            ' * @return {[type]}     [description]',
            ' */',
            'function foo (bar, baz) {'
        ])

    def test_parameters_are_added_to_function_template_with_description_disabled(self):
        self.set_view_content('/**|\nfunction foo (bar, baz) {')
        self.view.settings().set('function_description', True)
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * @param  |SELECTION_BEGIN|{[type]}|SELECTION_END| bar [description]',
            ' * @param  {[type]} baz [description]',
            ' * @return {[type]}     [description]',
            ' */',
            'function foo (bar, baz) {'
        ])

    def test_parameters_are_added_to_function_template_with_description_disabled_and_spacers_between_sections(self):
        self.set_view_content('/**|\nfunction foo (bar, baz) {')
        self.view.settings().set('function_description', False)
        self.view.settings().set('spacer_between_sections', True)
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * @param  |SELECTION_BEGIN|{[type]}|SELECTION_END| bar [description]',
            ' * @param  {[type]} baz [description]',
            ' *',
            ' * @return {[type]}     [description]',
            ' */',
            'function foo (bar, baz) {'
        ])

    def test_parameters_are_added_to_function_template_with_description_disabled_and_spacer_after_description_isset(self):
        self.set_view_content('/**|\nfunction foo (bar, baz) {')
        self.view.settings().set('function_description', False)
        self.view.settings().set('spacer_between_sections', 'after_description')
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * @param  |SELECTION_BEGIN|{[type]}|SELECTION_END| bar [description]',
            ' * @param  {[type]} baz [description]',
            ' * @return {[type]}     [description]',
            ' */',
            'function foo (bar, baz) {'
        ])

    def test_params_across_multiple_lines_should_be_identified(self):
        self.set_view_content([
            '/**|',
            'function foo(bar,',
            '             baz,',
            '             quux',
            '             ) {'
        ])
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * |SELECTION_BEGIN|[foo description]|SELECTION_END|',
            ' * @param  {[type]} bar  [description]',
            ' * @param  {[type]} baz  [description]',
            ' * @param  {[type]} quux [description]',
            ' * @return {[type]}      [description]',
            ' */',
            'function foo(bar,',
            '             baz,',
            '             quux',
            '             ) {'
        ])

    def test_vars_initialised_to_number_get_placeholders(self):
        self.set_view_content([
            '/**|',
            'var foo = 1;'
        ])
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * |SELECTION_BEGIN|[foo description]|SELECTION_END|',
            ' * @type {Number}',
            ' */',
            'var foo = 1;'
        ])

    def test_vars_string_double_quotes(self):
        self.set_view_content([
            '/**|',
            'var foo = "a";'
        ])
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * |SELECTION_BEGIN|[foo description]|SELECTION_END|',
            ' * @type {String}',
            ' */',
            'var foo = "a";'
        ])

    def test_vars_string_single_quotes(self):
        self.set_view_content([
            '/**|',
            'var foo = \'a\';'
        ])
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * |SELECTION_BEGIN|[foo description]|SELECTION_END|',
            ' * @type {String}',
            ' */',
            'var foo = \'a\';'
        ])

    def test_vars_unknown_type(self):
        self.set_view_content([
            '/**|',
            'var foo = bar;'
        ])
        self.run_bespoke_docs()
        self.assert_bespoke_docs_result([
            '/**',
            ' * |SELECTION_BEGIN|[foo description]|SELECTION_END|',
            ' * @type {[type]}',
            ' */',
            'var foo = bar;'
        ])

class RunBespokeDocsTests(sublime_plugin.WindowCommand):

    def run(self):

        self.window.run_command('show_panel', {'panel': 'console'})

        print('')
        print('BespokeDocs Tests')
        print('=================')

        suite = unittest.TestSuite()
        test_loader = unittest.TestLoader()

        # TODO move all test cases into tests directory and make test loader auto load testcases from the folder

        suite.addTests(test_loader.loadTestsFromTestCase(TestJavaScript))

        # TODO toggle test verbosity
        unittest.TextTestRunner(verbosity=1).run(suite)

        self.window.focus_group(self.window.active_group())
