import re
import yaml
import panflute as pf
from itertools import groupby

from panflute.elements import MetaString, builtin2meta

def yaml2meta(val):
    """
    Convert a type parsed from a YAML document to a panflute MetaValue.

    Arguments:
        val -- the value to convert
    """
    if isinstance(val, str):
        return MetaString(val)
    else:
        return builtin2meta(val)

def read_config(fn):
    """
    Read a configuration file and convert the elements to MetaValues.

    Arguments:
        fn -- the name of a config file to read
    """
    with open(fn) as f:
        data = yaml.safe_load(f)

    return {key: yaml2meta(val) for key, val in data.items()}

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
