import unittest

from minimark.inline import render_inline


class InlineTests(unittest.TestCase):
    def test_bold_and_italic(self):
        self.assertEqual(
            render_inline("**a** and *b*"), "<strong>a</strong> and <em>b</em>"
        )

    def test_code_is_protected(self):
        self.assertEqual(render_inline("`*x*`"), "<code>*x*</code>")

    def test_html_is_escaped(self):
        self.assertEqual(render_inline("<script>"), "&lt;script&gt;")

    def test_link(self):
        self.assertEqual(
            render_inline("[go](https://example.com)"),
            '<a href="https://example.com">go</a>',
        )

    def test_javascript_links_are_dropped(self):
        out = render_inline("[x](javascript:alert(1))")
        self.assertNotIn("<a", out)
        self.assertNotIn("href", out)


if __name__ == "__main__":
    unittest.main()
