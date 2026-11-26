import unittest

from minimark import convert


class BlockTests(unittest.TestCase):
    def test_heading_levels(self):
        self.assertEqual(convert("## Hi"), "<h2>Hi</h2>")

    def test_paragraph_joins_lines(self):
        self.assertEqual(convert("a\nb"), "<p>a b</p>")

    def test_unordered_list(self):
        self.assertEqual(convert("- a\n- b"), "<ul><li>a</li><li>b</li></ul>")

    def test_ordered_list(self):
        self.assertEqual(convert("1. a\n2. b"), "<ol><li>a</li><li>b</li></ol>")

    def test_code_block_escapes(self):
        self.assertEqual(
            convert("```\n<b>\n```"), "<pre><code>&lt;b&gt;</code></pre>"
        )

    def test_quote_and_rule(self):
        self.assertEqual(convert("> hi\n\n---"), "<blockquote>hi</blockquote>\n<hr>")

    def test_unclosed_code_fence_does_not_hang(self):
        self.assertIn("<pre>", convert("```\nabc"))


if __name__ == "__main__":
    unittest.main()
