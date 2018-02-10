#!/usr/bin/python
import sys
import panflute as pf

from pangloss.config import merge_settings
from pangloss.backend import formats
from pangloss.refs import replace_refs

def gloss(elem, doc):
    if isinstance(elem, pf.OrderedList):
        if elem.style == 'Example':
            if doc.format in formats:
                backend = doc.get_metadata(doc.format + 'Backend')
                if backend in formats[doc.format]:
                    return formats[doc.format][backend](elem)
            else:
                return None

def main():
    doc = pf.load(input_stream=sys.stdin)
    merge_settings(doc)
    pf.dump(pf.run_filters([gloss, replace_refs], doc=doc),
            output_stream=sys.stdout)

if __name__ == '__main__':
    main()
