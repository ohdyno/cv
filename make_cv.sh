#!/usr/bin/env zsh

pandoc -s resume.md -o resume.docx
python3 md_to_tex.py resume.md english "scale=0.85"
pdflatex resume.tex
