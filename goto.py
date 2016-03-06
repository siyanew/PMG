import sys, token, tokenize

# Copyright (c) 2003 Entrian Solutions. All rights reserved.
# Released under the Python Software License - see www.python.org

__author__ = "Richie Hindle <richie@entrian.com>"
__version__ = 1.0


class MissingLabelError(Exception):
    """'goto' without matching 'label'."""
    pass

# Source filenames -> line numbers of plain gotos -> target label names.
_plainGotoCache = {}

# Source filenames -> line numbers of computed gotos -> identifier names.
_computedGotoCache = {}

# Source filenames -> line numbers of labels -> label names.
_labelCache = {}

# Source filenames -> label names -> line numbers of those labels.
_labelNameCache = {}

# Source filenames -> comefrom label names -> line numbers of those comefroms.
_comefromNameCache = {}

def _addToCaches(moduleFilename):
    """Finds the labels and gotos in a module and adds them to the caches."""

    # The token patterns that denote gotos and labels.
    plainGotoPattern = [(token.NAME, 'goto'), (token.OP, '.')]
    computedGotoPattern = [(token.NAME, 'goto'), (token.OP, '*')]
    labelPattern = [(token.NAME, 'label'), (token.OP, '.')]
    comefromPattern = [(token.NAME, 'comefrom'), (token.OP, '.')]

    # Initialise this module's cache entries.
    _plainGotoCache[moduleFilename] = {}
    _computedGotoCache[moduleFilename] = {}
    _labelCache[moduleFilename] = {}
    _labelNameCache[moduleFilename] = {}
    _comefromNameCache[moduleFilename] = {}

    # Tokenize the module; 'window' is the last two (type, string) pairs.
    window = [(None, ''), (None, '')]
    try:
        for tokenType, tokenString, (startRow, startCol), (endRow, endCol), line \
                in tokenize.generate_tokens(open(moduleFilename, 'r').readline):
            # Plain goto: "goto .x"
            if window == plainGotoPattern:
                _plainGotoCache[moduleFilename][startRow] = tokenString

            # Computed goto: "goto *identifier"  XXX Allow expressions.
            elif window == computedGotoPattern:
                _computedGotoCache[moduleFilename][startRow] = tokenString

            # Comefrom: "comefrom .x"  XXX Non-determinism via multiple comefroms.
            if window == comefromPattern:
                _comefromNameCache[moduleFilename][tokenString] = startRow

            # Label: "label .x"  XXX Computed labels.
            elif window == labelPattern:
                _labelCache[moduleFilename][startRow] = tokenString
                _labelNameCache[moduleFilename][tokenString] = startRow

            # Move the token window back by one.
            window = [window[1], (tokenType, tokenString)]
    except TypeError:
        pass

def _trace(frame, event, arg):
    try:
        # If this is the first time we've seen this source file, cache it.
        filename = frame.f_code.co_filename
        if filename not in _plainGotoCache:
            _addToCaches(filename)

        # Is there a goto on this line?
        targetLabel = _plainGotoCache[filename].get(frame.f_lineno)
        if not targetLabel:
            # No plain goto.  Is there a computed goto?
            identifier = _computedGotoCache[filename].get(frame.f_lineno)
            if identifier:
                # If eval explodes, just let the exception propagate.
                targetLabel = eval(identifier, frame.f_globals, frame.f_locals)

        # Jump to the label's line.
        if targetLabel:
            try:
                targetLine = _labelNameCache[filename][targetLabel]
            except KeyError:
                raise MissingLabelError, "Missing label: %s" % targetLabel
            frame.f_lineno = targetLine

        # Is there a label on this line with a corresponding comefrom?
        label = _labelCache[filename].get(frame.f_lineno)
        if label:
            targetComefromLine = _comefromNameCache[filename].get(label)
            if targetComefromLine:
                frame.f_lineno = targetComefromLine

        return _trace
    except TypeError:
        pass

# Install the trace function, including all preceding frames.
sys.settrace(_trace)
frame = sys._getframe().f_back
while frame:
    frame.f_trace = _trace
    frame = frame.f_back

# Define the so-called keywords for importing: 'goto', 'label' and 'comefrom'.
class _Label:
    """Allows arbitrary x.y attribute lookups."""
    def __getattr__(self, name):
        return None

goto = None
label = _Label()
comefrom = _Label()
