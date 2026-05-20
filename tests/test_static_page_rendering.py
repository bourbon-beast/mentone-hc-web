import re
import shutil
import subprocess
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def extract_function(source: str, name: str) -> str:
    match = re.search(
        rf"  function {re.escape(name)}\([^)]*\) \{{\n.*?\n  \}}",
        source,
        re.DOTALL,
    )
    if not match:
        raise AssertionError(f"Could not find function {name}")
    return textwrap.dedent(match.group(0))


@unittest.skipIf(shutil.which("node") is None, "node is required for static page JS tests")
class StaticPageRenderingTests(unittest.TestCase):
    def run_node(self, script: str) -> str:
        return subprocess.check_output(
            ["node", "-e", script],
            cwd=ROOT,
            text=True,
        )

    def test_fixture_letter_results_are_classified(self):
        fixtures_html = (ROOT / "fixtures.html").read_text()
        result_cell = extract_function(fixtures_html, "resultCell")

        script = f"""
        {result_cell}
        const cases = [
          ['W', 'win', '>W<'],
          ['L', 'loss', '>L<'],
          ['D', 'draw', '>D<'],
          ['3-1', 'win', '>3-1<'],
        ];
        for (const [value, klass, text] of cases) {{
          const html = resultCell(value);
          if (!html.includes(`fix-result ${{klass}}`) || !html.includes(text)) {{
            throw new Error(`${{value}} rendered incorrectly: ${{html}}`);
          }}
        }}
        """

        self.run_node(script)

    def test_news_apostrophe_categories_render_without_inline_handlers(self):
        news_html = (ROOT / "news.html").read_text()
        render_filters = extract_function(news_html, "renderFilters")

        script = f"""
        const CATEGORIES = ['All', "Men's", "Women's", 'Juniors', 'Masters', 'Club'];
        {render_filters}
        const html = renderFilters("Men's");
        if (html.includes('onclick=')) {{
          throw new Error(`filter HTML still uses inline handlers: ${{html}}`);
        }}
        for (const category of ["Men's", "Women's"]) {{
          if (!html.includes(`data-category="${{category}}"`)) {{
            throw new Error(`missing data category for ${{category}}: ${{html}}`);
          }}
        }}
        """

        self.run_node(script)


if __name__ == "__main__":
    unittest.main()
