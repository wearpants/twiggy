import multiprocessing
import threading
import sys
import atexit
from collections import deque

class Output(object):
    """
    Does the work of formatting and writing a message.

    :arg format: a callable taking a `Message` and formatting it for output. `None` means return the message unchanged.

    :cvar bool use_locks: use locks when running in a synchronous,
    multithreaded environment. Threadsafe subclasses may disable locking
    for higher throughput. Defaults to true.
    """

    use_locks = True

    @staticmethod
    def _noop_format(msg):
        """a format that that just returns the message unchanged - for internal use"""
        return msg

    def __init__(self, format=None):
        self._format = format if format is not None else self._noop_format
        self._sync_init()
        atexit.register(self.close)

    def _sync_init(self):
        """the guts of init - for internal use"""
        if self.use_locks:
            self._lock = threading.Lock()
            self.output = self.__sync_output_locked
        else:
            self.output = self.__sync_output_unlocked

        self.close = self._close
        self._open()

    def _open(self):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError

    def _write(self, x):
        raise NotImplementedError

    def __sync_output_locked(self, msg):
        x = self._format(msg)
        with self._lock:
            self._write(x)

    def __sync_output_unlocked(self, msg):
        x = self._format(msg)
        self._write(x)

class AsyncOutput(Output):
    """An Output with support for asynchronous logging

    Mixing in this Output transparently adds support for asynchronous logging
    using the multiprocessing module. This is off by default, as it can cause
    log messages to be dropped. See the msg_buffer argument.

    :arg int msg_buffer: number of messages to buffer in memory when using
    asynchronous logging. ``0`` turns asynchronous output off, a negative
    integer means an unlimited buffer, a positive integer is the size
    of the buffer.
    """

    def __init__(self, format=None, msg_buffer=0):
        self._format = format if format is not None else self._noop_format
        if msg_buffer == 0:
            self._sync_init()
        else:
            self._async_init(msg_buffer)
        atexit.register(self.close)

    def _async_init(self, msg_buffer):
        """the guts of init - for internal use"""
        self.output = self.__async_output
        self.close = self.__async_close
        self.__queue = multiprocessing.JoinableQueue(msg_buffer)
        self.__child = multiprocessing.Process(target=self.__child_main, args=(self,))
        self.__child.start() # XXX s.b. daemon=True? don't think so, b/c atexit instead

    # use a plain function so Windows is cool
    @staticmethod
    def __child_main(self):
        self._open()
        while True:
            # XXX should _close() be in a finally: ?
            msg = self.__queue.get()
            if msg != "SHUTDOWN":
                x = self._format(msg)
                self._write(x)
                del x, msg
                self.__queue.task_done()
            else:
                assert self.__queue.empty(), "Shutdown but queue not empty"
                self._close()
                self.__queue.task_done()
                break

    def __async_output(self, msg):
        self.__queue.put_nowait(msg)

    def __async_close(self):
        self.__queue.put_nowait("SHUTDOWN") # XXX maybe just put?
        self.__queue.close()
        self.__queue.join()


class NullOutput(Output):
    """An output that just discards its messages"""

    use_locks = False

    def _open(self):
        pass

    def _write(self, msg):
        pass

    def _close(self):
        pass

class DequeOutput(Output):
    """an output that stuffs messages in a deque"""

    use_locks = False

    def _open(self):
        self.deque = deque([])

    def _write(self, msg):
        self.deque.append(msg)

    def _close(self):
        self.deque.clear()


class FileOutput(AsyncOutput):
    """Output to file

    ``name``, ``mode``, ``buffering`` are passed to ``open(..)``
    """
    def __init__(self, name, format, mode='a', buffering=1, msg_buffer=0):
        self.filename = name
        self.mode = mode
        self.buffering = buffering
        super(FileOutput, self).__init__(format, msg_buffer)

    def _open(self):
        self.file = open(self.filename, self.mode, self.buffering)

    def _close(self):
        self.file.close()

    def _write(self, x):
        self.file.write(x)

class StreamOutput(Output):
    """Output to an externally-managed stream.

    The stream will be written to, but otherwise left alone (i.e., it will *not* be closed).
    """
    def __init__(self, format, stream=sys.stderr):
        self.stream = stream
        super(StreamOutput, self).__init__(format)

    def _open(self):
        pass

    def _close(self):
        pass

    def _write(self, x):
        self.stream.write(x)
