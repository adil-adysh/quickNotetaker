import os
import subprocess
import tempfile

PANDOC_EXE = os.path.join(
    "addon", "globalPlugins", "quickNotetaker", "lib", "pandoc", "pandoc.exe"
)

def run_pandoc_test(md_content, test_name):
    """
    Helper to run pandoc on given markdown content and check DOCX output.
    """
    if not os.path.isfile(PANDOC_EXE):
        raise FileNotFoundError(f"Pandoc executable not found: {PANDOC_EXE}")
    with tempfile.TemporaryDirectory() as tempdir:
        md_path = os.path.join(tempdir, f"{test_name}.md")
        docx_path = os.path.join(tempdir, f"{test_name}.docx")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        args = [
            PANDOC_EXE,
            "-f", "markdown",
            "-t", "docx",
            "-s",
            "-i", md_path,
            "-o", docx_path
        ]
        try:
            subprocess.run(args, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Pandoc stderr for {test_name}:", e.stderr.decode(errors="ignore"))
            raise AssertionError(f"Pandoc failed for {test_name} with exit code {e.returncode}")
        assert os.path.isfile(docx_path), f"DOCX file was not created for {test_name}."
        print(f"Pandoc conversion succeeded for {test_name}.")

def test_pandoc_markdown_to_docx():
    """
    Run several markdown to docx conversion tests with increasing complexity.
    """
    # Simple test
    run_pandoc_test("# Hello World\nThis is a test.", "simple")

    # Table test
    table_md = """
| Name | Age | City |
|------|-----|------|
| Alice|  30 | NY   |
| Bob  |  25 | LA   |
"""
    run_pandoc_test(table_md, "table")

    # Code block test
    code_md = """
```python
def hello():
    print('Hello, world!')
```
"""
    run_pandoc_test(code_md, "codeblock")

    # List test
    list_md = """
1. First item
2. Second item
   - Subitem A
   - Subitem B
3. Third item
"""
    run_pandoc_test(list_md, "list")

    # Link and formatting test
    link_md = """
**Bold text**, *italic text*, and a [link](https://example.com).
"""
    run_pandoc_test(link_md, "formatting")

    # Complex markdown test
    complex_md = """
# Title

## Section 1

Some text with `inline code` and a footnote.[^1]

> Blockquote

---

### Table

| Product | Price |
|---------|-------|
| Apple   | $1    |
| Banana  | $2    |

### List

- Item 1
- Item 2
  - Subitem 2a
  - Subitem 2b

### Code

```js
console.log('Hello!');
```

[^1]: This is a footnote.
"""
    run_pandoc_test(complex_md, "complex")

if __name__ == "__main__":
    test_pandoc_markdown_to_docx()
