import re
import yaml

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
