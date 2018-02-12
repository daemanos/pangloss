import re
import panflute as pf
from itertools import groupby
from functools import partial

# regular expression for label formats
label_re = re.compile(r'\{#ex:(\w+)\}')
word_re = re.compile(r"[\w']+")

# == GENERIC ==================================================================

def break_plain(plain):
    """
    Break a Plain element with SoftBreaks into a list of Para elements.
    """
    is_break = lambda el: isinstance(el, pf.SoftBreak)
    content = list(plain.content)

    # group sequences of non-breaks together as paragraphs and throw out breaks
    return [pf.Para(*list(g)) for k, g in groupby(content, is_break) if not k]


def ex2gloss(ex):
    """
    Convert an example into its gloss parts.
    """
    lines = break_plain(ex.content[0])
    return map(partial(pf.stringify, newlines=False), lines)

# == LATEX ====================================================================

def smallcapify(s):
    """
    Convert words in a string that are in all caps to use small caps, via the
    LaTeX \\textsc{} command. Used to auto-convert glossing abbreviations given
    in all caps (like PERF for perfective) to small caps in glosses. Words that
    are merely capitalized (like Mary) will be left alone.
    """

    def repl(match):
        word = match.group()
        if all(64 < ord(c) < 91 for c in word):
            return "\\textsc{" + word.lower() + "}"
        else:
            return word

    return re.sub(word_re, repl, s)


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
        orig, gloss, trans = ex2gloss(li)
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

# == HTML =====================================================================

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
        orig, gloss, trans = ex2gloss(li)
        html += leipzigjs_fmt.format(orig, gloss, trans)

    return pf.RawBlock(html, format='html')

# == EXPORT ===================================================================

# available formats and backends
formats = {
        'latex': {
            'gb4e': gb4e
            },
        'html': {
            'leipzigjs': leipzigjs
            }
        }


def isgloss(ex):
    """
    Determine if the given example item is a valid gloss.
    """
    return len(break_plain(ex.content[0])) == 3


def replace_glosses(elem, doc, backend=lambda x: x):
    """
    Replace the glosses in a document.

    Arguments:
        elem -- the element to replace
        doc -- the current document
        backend -- a backend function to be applied at each gloss list
    """

    if isinstance(elem, pf.OrderedList) and elem.style == 'Example':
        if all(map(isgloss, elem.content)):
            return backend(elem)
