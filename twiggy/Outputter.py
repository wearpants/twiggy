class Outputter(object):
    """
    Does the work of formatting and writing a message.

    Multiple implementations are expected.

    format(msg) -> <whatever>
    format the message for writing. Output type is user-specified, as long as
    it's compatible with write()

    write(<whatever>) -> None
    writes out the formatted message

    """

    def __init__(self, format, write):
        self._format = format
        self._write = write

    def output(self, msg):
        x = self._format(msg)
        self._write(x)

    # XXX I prolly need a close() or somesuch
