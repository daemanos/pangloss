#!/usr/bin/python
import sys
import panflute as pf
from functools import partial

from pangloss.config import merge_settings
from pangloss.backend import formats, replace_glosses
from pangloss.refs import replace_refs

def main():
    doc = pf.load(input_stream=sys.stdin)
    if doc.format not in formats:
        pass # die

    merge_settings(doc)

    fmt = formats[doc.format]
    backend = doc.get_metadata(doc.format + 'Backend')
    if backend not in fmt:
        pass # die

    filters = [partial(replace_glosses, backend=fmt[backend]), replace_refs]
    pf.dump(pf.run_filters(filters, doc=doc), output_stream=sys.stdout)

if __name__ == '__main__':
    main()
