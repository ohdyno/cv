pandoc -s cv_en_john_doe.md -o cv_en_john_doe.docx
python md_to_tex.py cv_en_john_doe.md english "scale=0.85"
pdflatex cv_en_john_doe.tex
