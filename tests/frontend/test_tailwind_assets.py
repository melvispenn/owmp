import shutil
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSS_DIR = PROJECT_ROOT / "owmp/static/css"
MIN_NODE_MAJOR = 22


def test_tailwind_input_uses_official_import():
    input_css = (CSS_DIR / "input.css").read_text()
    assert '@import "tailwindcss";' in input_css
    assert "@source" in input_css


def test_base_template_loads_generated_output_css():
    template = (PROJECT_ROOT / "owmp/templates/base.html").read_text()
    assert "{% static 'css/output.css' %}" in template


def test_tailwind_cli_builds_output_css(tmp_path):
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js 22 or newer is required for the Tailwind build")
    node_version = subprocess.run(  # noqa: S603 - executable is resolved from the local PATH above
        [node, "--version"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    try:
        node_major = int(node_version.removeprefix("v").split(".", 1)[0])
    except ValueError:
        pytest.skip("Unable to determine the installed Node.js version")
    if node_major < MIN_NODE_MAJOR:
        pytest.skip("Node.js 22 or newer is required for the Tailwind build")

    npm = shutil.which("npm")
    assert npm is not None
    result = subprocess.run(  # noqa: S603 - executable is resolved from the local PATH above
        [npm, "run", "css:build", "--", "-o", str(tmp_path / "output.css")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    output_css = tmp_path / "output.css"
    assert output_css.exists()
    assert output_css.stat().st_size > 0
