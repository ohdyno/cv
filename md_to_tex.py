import os.path
import re
import sys

new_page_sections = []

def personal_info_from_md_line(txt):
    """Return personal info for lines with links
    
    e.g.
    input:  "`email`    [abc@example.com](mailto:abc@example.com)"
    output: "abc@example.com"
    """

    txt = txt.split("[")[1]
    txt = txt.split("]")[0]
    return txt

def split_cv_line(txt):
    """Return a tuple of the side bar text and title
    
    e.g.
    input:  "*Gen 2000 -- Dec 2020* Example GmbH -- Intern"
    output: ("Gen 2000 -- Dec 2020", "Example GmbH -- Intern")
    """

    if not txt.startswith("*"):
        return "", txt

    txt = txt.split("*", 1)[1]
    txt = txt.split("*", 1)
    side_text = txt[0].strip()
    title = txt[1].strip()
    return side_text, title

def md_to_tex(markdown_text):
    """Convert links in markdown texts to LaTex links"""
    
    # Regular expression to find markdown links
    markdown_link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    # Function to replace markdown links with LaTeX links
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        return f'\\href{{{url}}}{{{text}}}'
    
    # Replace all markdown links in the text
    latex_text = markdown_link_pattern.sub(replace_link, markdown_text)
    return latex_text

class CvSection():

    def __init__(self, title):
        self.title = title

    def to_tex(self):
        tex_code = "\\section{{{}}}".format(self.title)
        if self.title in new_page_sections:
            tex_code = "\\newpage\n\n" + tex_code
        return tex_code

class CvSubSection():

    def __init__(self, title):
        self.title = title

    def to_tex(self):
        tex_code = "\\subsection{{{}}}".format(self.title)
        return tex_code

class CvEntryOrItem():

    def __init__(self, side_txt, title):
        self.side_txt = side_txt
        self.title = title

    def to_tex(self):
        title = self.title
        bold_cventry_field = None
        if title.startswith("-"):
            # For each list item an individual `itemize` environment is created.
            # The redundant begins and ends of `itemize` environments are later removed
            # in the `content_to_tex` method of the `CurriculumVitae` class.
            # \cvitem{}{\begin{itemize}\item ... \end{itemize}}
            # \cvitem{}{\begin{itemize}\item ... \end{itemize}}
            # \cvitem{}{\begin{itemize}\item ... \end{itemize}}
            title = "\\begin{itemize}\\item " + title[1:] + "\\end{itemize}"
        elif title.startswith("    -"):
            title ="\\quad -" + title[5:]
        elif "**" in title:
            title_split = title.split(sep="**", maxsplit=2)
            bold_cventry_field = title_split[1].strip()
            title = title_split[2].strip()
        while "*" in title:
            title_split = title.split(sep="*", maxsplit=2)
            title = title_split[0] + "\\emph{" + title_split[1] + "}" + title_split[2]
        if bold_cventry_field is None:
            return f"\\cvitem{{{self.side_txt}}}{{{title}}}"
        else:
            return f"\\cventry{{{self.side_txt}}}{{{bold_cventry_field}}}{{{title}}}{{}}{{}}{{}}"

class CurriculumVitae():

    def __init__(self, language=None, geometry_options="scale=0.80"):
        if language is None:
            language = "english"
        self.language = language
        self.name = ("John", "Doe")
        self.title = None
        self.content = None
        self.photo = None
        self.geometry_options = geometry_options # options for the `geometry` Tex package

    def from_markdown(self, markdown_src):
        self.content = []
        # Remove html comments from the markdown source
        markdown_src = re.sub(r'<!--.*?-->', '', markdown_src, flags=re.DOTALL)
        lines = markdown_src.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("# "):
                line = line.removeprefix("# ")
                self.name = line.split(" ", 1)
                i += 1
                # The first non-empty line after the name is the title
                while lines[i] == "":
                    i += 1
                self.title = lines[i]
                i += 1
                continue
            
            if line.startswith("![]"):
                self.photo = line.split("(")[1].split(")")[0]
                i += 1
                continue

            if line.startswith("`email`"):
                self.email = personal_info_from_md_line(line)
                i += 1
                continue
            if line.startswith("`homepage`"):
                self.homepage = personal_info_from_md_line(line)
                i += 1
                continue
            if line.startswith("`linkedin`"):
                self.linkedin = personal_info_from_md_line(line)
                i += 1
                continue
            if line.startswith("`github`"):
                self.github = personal_info_from_md_line(line)
                i += 1
                continue
            
            if line.startswith("## "):
                self.content.append(CvSection(line.removeprefix("## ")))
                i += 1
                continue
            
            if line.startswith("### "):
                self.content.append(CvSubSection(line.removeprefix("### ")))
                i += 1
                continue

            if line.strip() != "":
                side_text, title = split_cv_line(line)
                self.content.append(CvEntryOrItem(side_text, title))
                i += 1
                continue

            i += 1

    def personal_data_to_tex(self):
        tex_out = []
        tex_out.append("\\name {{{}}}{{{}}}".format(self.name[0], self.name[1]))
        if hasattr(self, 'title') and self.title is not None:
            tex_out.append("\\title{{{}}}".format(self.title))
        if hasattr(self, 'photo') and self.photo is not None:
            tex_out.append("\\photo[80pt][0pt]{{{}}}".format(self.photo))
        if hasattr(self, 'email') and self.email is not None:
             tex_out.append("\\email{{{}}}".format(self.email))
        if hasattr(self, 'homepage') and self.homepage is not None:
             tex_out.append("\\homepage{{{}}}".format(self.homepage))
        if hasattr(self, 'linkedin') and self.linkedin is not None:
             tex_out.append("\\social[linkedin]{{{}}}".format(self.linkedin))
        if hasattr(self, 'github') and self.github is not None:
             tex_out.append("\\social[github]{{{}}}".format(self.github))
        
        tex_out = "\n".join(tex_out)
        return tex_out

    def remove_redundant_itemize(tex_code):
        """Remove redundant `itemize` environment statements from Tex code generated by the `CvEntryOrItem` class."""

        # \cvitem{}{\begin{itemize}\item ... \end{itemize}}
        # \cvitem{}{\begin{itemize}\item ... \end{itemize}}
        # \cvitem{}{\begin{itemize}\item ... \end{itemize}}
        tex_code = tex_code.replace("\\end{itemize}}\n\\cvitem{}{\\begin{itemize}", "\n")
        # \cvitem{}{\begin{itemize}\item ...
        # \item ...
        # \item ... \end{itemize}}
        tex_code = tex_code.replace("\\begin{itemize}", "\\begin{itemize}\n")
        # \cvitem{}{\begin{itemize}
        # \item ...
        # \item ...
        # \item ... \end{itemize}}
        tex_code = tex_code.replace("\\end{itemize}}", "\n          \\end{itemize}}")
        # \cvitem{}{\begin{itemize}
        # \item ...
        # \item ...
        # \item ...
        #           \end{itemize}}
        tex_code = tex_code.replace("\\item", "          \\item")
        # \cvitem{}{\begin{itemize}
        #           \item ...
        #           \item ...
        #           \item ...
        #           \end{itemize}}
        return tex_code

    def content_to_tex(self):
        content_lines = [item.to_tex() for item in self.content]
        tex_code = "\n".join(content_lines)
        tex_code = CurriculumVitae.remove_redundant_itemize(tex_code)
        return tex_code

    def to_tex(self):
        tex_template = open("cv_template.tex", "rt").read()
        tex_template = tex_template.replace("$geometry_options", self.geometry_options)
        tex_template = tex_template.replace("$language", self.language)
        tex_template = tex_template.replace("$personal_data", self.personal_data_to_tex())
        tex_template = tex_template.replace("$content", self.content_to_tex())
        tex_template = tex_template.replace("<", "\\textless")
        tex_template = tex_template.replace(">", "\\textgreater")
        tex_template = md_to_tex(tex_template)
        return tex_template


if __name__ == "__main__":
    src_filename = sys.argv[1]
    if len(sys.argv) > 2:
        language = sys.argv[2]
    else:
        language = None
    if len(sys.argv) > 3:
        geometry_options = sys.argv[3]
        cv = CurriculumVitae(language, geometry_options)
    else:
        cv = CurriculumVitae(language)
    
    cv.from_markdown(open(src_filename, "rt").read())
    open(os.path.splitext(src_filename)[0] + ".tex", "wt").write(cv.to_tex())
