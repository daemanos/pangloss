#!/usr/bin/python
import sys
import panflute as pf

from pangloss.config import merge_settings
from pangloss.backend import formats

def gloss(elem, doc):
    if isinstance(elem, pf.OrderedList):
        if elem.style == 'Example':
            if doc.format in formats:
                backend = doc.get_metadata(doc.format + 'Backend')
                if backend in formats[doc.format]:
                    return formats[doc.format][backend](elem)
            else:
                return None

def gloss_refs(elem, doc):
    if isinstance(elem, pf.Cite):
        text = elem.content[0].text
        if text[:4] == '@ex:':
            if doc.format == 'latex':
                ref = "\\ref{ex:" + text[4:] + "}"

                fmt = doc.get_metadata('exampleRefFormat')
                pf.debug(fmt)
                if isinstance(fmt, list):
                    ref = (fmt[0]).format(ref)
                else:
                    ref = fmt.format(ref)

                return pf.RawInline(ref, format = 'latex')
            elif doc.format == 'html':
                # TODO
                pass

def main():
    doc = pf.load(input_stream=sys.stdin)
    merge_settings(doc)
    pf.dump(pf.run_filters([gloss, gloss_refs], doc=doc),
            output_stream=sys.stdout)

if __name__ == '__main__':
    main()
