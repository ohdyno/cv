#!/usr/bin/env zsh

FILENAME="cv"
pandoc -s "$FILENAME".md -o "$FILENAME".docx
python3 md_to_tex.py "$FILENAME".md english "scale=0.85"
pdflatex "$FILENAME".tex
open "$FILENAME".pdf