#!/usr/bin/env zsh

pandoc -s cv.md -o cv.docx
python3 md_to_tex.py cv.md english "scale=0.85"
pdflatex cv.tex