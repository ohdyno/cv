# Luca-CV

## Use

- Replace `photo.jpg` with your photo.
- Update `cv_en_john_doe.md`.
- Run `make_cv.ps1` to generate `cv_en_john_doe.docx`,`cv_en_john_doe.tex`, `cv_en_john_doe.pdf`.

## Requirements

- [Python](https://www.python.org/)
- [Pandoc](https://pandoc.org/)
- pdflatex (included in [MiKTeX](https://miktex.org))

## Version History

### v2.0

Add optional argument for LaTeX's `gemoetry` options to `md_to_tex.py`.
```
python md_to_tex.py cv_en_john_doe.md english "scale=0.85"
```

The variable `new_page_sections` defines the name of sections which get a `\newpage` in the LaTeX.
Leave the variable emty to not add any `\newpage`.
```
new_page_sections = [
    "Project Experience",
    "Keywords",
    "Projekterfahrung",
    "Stichworte",
]
```

Add support for markdown links.
```
*Jun 2022* [Certified Scrum Storyteller -- Flaccid Scrum School](https://example.com)
```

Properly convert markdown lists to `itemize` environments in LaTeX.
```
- consectetur adipiscing elit
- sed do eiusmod tempor incididunt
- ut labore et dolore magna aliqua
```
```
\cvitem{}{\begin{itemize}
          \item  consectetur adipiscing elit
          \item  sed do eiusmod tempor incididunt
          \item  ut labore et dolore magna aliqua
          \end{itemize}}
```

Add support for html comments.
```
<!-- This comment will not be included in your CV -->
```

Minor fixes and adjustments.

### v1.0

[How I manage my CV with Markdown, Pandoc, Python, and LaTeX](https://lucaf.eu/2022/08/18/cv-markdown-pandoc-python-latex.html)

## Acknowledgment

[Template photo](https://unsplash.com/photos/dLij9K4ObYY) by [Joe Shields](https://unsplash.com/@fortyozsteak)
