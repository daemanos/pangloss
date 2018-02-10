import panflute as pf

def replace_refs(elem, doc):
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


