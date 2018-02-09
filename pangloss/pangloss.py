#!/usr/bin/python

import re
import panflute as pf
from itertools import groupby
from functools import partial
from collections import OrderedDict

label_re = re.compile(r'\{#ex:(\w+)\}')

leipzigjs_fmt = """
<div data-gloss>
<p>{}</p>
<p>{}</p>
<p>‘{}’</p>
</div>
"""

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

    return re.sub(r"[\w']+", repl, s)


def break_plain(plain):
    """
    Break a Plain element with SoftBreaks into a list of Para elements.
    """
    is_break = lambda el: isinstance(el, pf.SoftBreak)
    content = list(plain.content)

    # group sequences of non-breaks together as paragraphs and throw out breaks
    return [pf.Para(*list(g)) for k, g in groupby(content, is_break) if not k]


def output_gb4e(lst):
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


def output_leipzigjs(lst):
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


formats = {
        'latex': output_gb4e,
        'html': output_leipzigjs
        }


def gloss(elem, doc):
    if isinstance(elem, pf.OrderedList):
        if elem.style == 'Example':
            if doc.format in formats:
                return formats[doc.format](elem)
            else:
                return None

def gloss_refs(elem, doc):
    if isinstance(elem, pf.Cite):
        text = elem.content[0].text
        if text[:4] == '@ex:':
            if doc.format == 'latex':
                return pf.RawInline("(\\ref{ex:" + text[4:] + "})",
                        format = 'latex')
            elif doc.format == 'html':
                # TODO
                pass

def main(doc = None):
    return pf.run_filters([gloss, gloss_refs], doc = doc)

if __name__ == '__main__':
    main()
