from os import path
from copy import deepcopy

from panflute.elements import MetaString, MetaBool, MetaList
from pangloss.util import read_config

# default values for pangloss-specific settings
defaults = {
        'chapters': MetaBool(False),
        'chaptersDepth': MetaString('1'),
        'exampleLabelFormat': MetaString('({})'),
        'exampleRefFormat': MetaList(
            MetaString('ex. {}'),
            MetaString('exs. {}')
            ),
        'rangeDelim': MetaString('-'),
        'pairDelim': MetaString(','),
        'lastDelim': MetaString(','),
        'refDelim': MetaString(','),
        'linkReferences': MetaBool(False),
        'latexBackend': MetaString('gb4e'),
        'htmlBackend': MetaString('leipzigjs')
        }

# names of all pangloss settings
settings = list(defaults.keys())
local_config_setting = 'glossConfig'

# base directory for global config files
basedir = path.expanduser('~/.pangloss')

def merge_settings(doc):
    """
    Merge external settings into a document.

    Arguments:
        doc -- the document to merge into
    """

    extern = get_settings(doc, internal=False)
    for key, val in extern.items():
        if not (key in doc.metadata):
            doc.metadata[key] = val

def get_settings(doc=None, internal=True):
    """
    Get the actual values of all pangloss-relevant settings.

    Arguments:
        doc -- the current document (default: None)
        internal -- whether to include document metadata (default: True)

    If no document is given, only global settings will be considered.
    """
    config = deepcopy(defaults)

    # merge global configuration
    merge(config, global_config())

    if not (doc is None):
        # merge format-specific global configuration
        merge(config, global_config(doc.format))

        # merge local configuration
        if local_config_setting in doc.metadata:
            local_config = doc.get_metadata(local_config_setting)
        else:
            local_config = path.abspath('./pangloss.yaml')

        try:
            merge(config, read_config(local_config))
        except IOError:
            pass

        # merge document metadata
        if internal: merge(config, doc.metadata)

    return config


def merge(low, high):
    """
    Merge two configuration sources.

    Arguments:
        low -- the source with lower precedence
        high -- the source with higher precedence

    Returns: a merged configuration
    """

    # bail if merging to an empty higher source
    if high == {}: return low

    merged = {}
    for key, val in low.items():
        merged[key] = high[key] if key in high else val

    return merged


def global_config(fmt=None):
    """
    Get the global configuration data, optionally for a particular format.

    Arguments:
        fmt -- the format to get a config file for (default: None)

    Returns: the contents of the specified config file, or {} if it does not
    exist
    """

    if fmt is None:
        fn = path.join(basedir, 'config.yaml')
    else:
        fn = path.join(basedir, 'config-{}.yaml'.format(fmt))

    try:
        config = read_config(fn)
        return config
    except IOError:
        return {}
