import re
import panflute as pf
from functools import partial

from pangloss.util import smallcapify, break_plain

# regular expression for label formats
label_re = re.compile(r'\{#ex:(\w+)\}')


gb4e_fmt_labelled = """
\\ex\\label{{ex:{label}}}
\\gll {} \\\\
{} \\\\
\\trans `{}' \\\\
"""

gb4e_fmt = """
\\ex
\\gll {} \\\\
{} \\\\
\\trans `{}' \\\\
"""

def gb4e(lst):
    """
    Convert an example list into a series of gb4e-formatted interlinear
    glosses.

    Because example list references are replaced at parsing by Pandoc, the
    normal syntax of (@foo) cannot be used for labels; instead, a label syntax
    similar to that used for headers (and tables and figures with
    pandoc-crossref) is used, namely a {#ex:foo} inserted after the
    translation, which will be stripped and replaced with a LaTeX label on the
    relevant example.
    """

    latex = "\\begin{exe}\n"
    for li in lst.content:
        lines = break_plain(li.content[0])
        if len(lines) != 3: continue

        orig, gloss, trans = map(partial(pf.stringify, newlines=False), lines)
        gloss = smallcapify(gloss)

        label_match = label_re.search(trans)
        if label_match:
            label = label_match.group(1)
            trans = trans[:label_match.start() - 1]

            latex += gb4e_fmt_labelled.format(orig, gloss, trans, label=label)
        else:
            latex += gb4e_fmt.format(orig, gloss, trans)

    latex += "\\end{exe}"
    return pf.RawBlock(latex, format='latex')


leipzigjs_fmt = """
<div data-gloss>
<p>{}</p>
<p>{}</p>
<p>‘{}’</p>
</div>
"""

def leipzigjs(lst):
    """
    Convert an example list into a series of div's suitable for use with
    Leipzig.js.
    """

    html = ''
    for li in lst.content:
        lines = break_plain(li.content[0])
        if len(lines) != 3: continue

        orig, gloss, trans = map(partial(pf.stringify, newlines=False), lines)
        html += leipzigjs_fmt.format(orig, gloss, trans)

    return pf.RawBlock(html, format='html')


# available formats and backends
formats = {
        'latex': {
            'gb4e': gb4e
            },
        'html': {
            'leipzigjs': leipzigjs
            }
        }
