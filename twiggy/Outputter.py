import multiprocessing
import threading
import sys
import atexit

class Outputter(object):
    """
    Does the work of formatting and writing a message.

    Multiple implementations are expected.

    Outputters transparently support asynchronous logging using the
    multiprocessing module. This is off by default, as it can cause log
    messages to be dropped. See the msgBuffer argument.

    :arg msgBuffer: number of messages to buffer in memory when using
    asynchronous logging. `0` turns asynchronous output off, a negative
    integer means an unlimited buffer, a positive integer is the size
    of the buffer.

    :arg format: a callable (probably a Formatter) taking a Message and
    formatting it for output.

    :cvar use_locks: use locks when running in a synchronous,
    multithreaded environment. Threadsafe subclasses may disable locking
    for higher throughput. Defaults to true.
    """

    use_locks = True

    def __init__(self, format, msgBuffer=0):
        self._format = format # XXX should this default to None, meaning use class-level _default_format?

        if msgBuffer == 0: # synchronous
            self._lock = threading.Lock() if self.use_locks else None
            self.output = self.__sync_output
            self.close = self._close
            self._open()
        else:
            self.output = self.__async_output
            self.close = self.__async_close
            self.__queue = multiprocessing.JoinableQueue(msgBuffer)
            self.__child = multiprocessing.Process(target=self.__child_main, args=(self,))
            self.__child.start() # XXX s.b. daemon=True? don't think so, b/c atexit instead

        atexit.register(self.close)

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

    def _open(self):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError

    def _write(self, x):
        raise NotImplementedError

    def __sync_output(self, msg):
        x = self._format(msg)
        if self.use_locks:
            with self._lock:
                self._write(x)
        else:
            self._write(x)

    def __async_output(self, msg):
        self.__queue.put_nowait(msg)

    def __async_close(self):
        self.__queue.put_nowait("SHUTDOWN") # XXX maybe just put?
        self.__queue.close()
        self.__queue.join()

class NullOutputter(object):
    """An duck-typed outputter that just discards its messages"""

    def output(self, msg):
        pass

    def close(self):
        pass

class FileOutputter(Outputter):
    """Output to file

    `name`, `mode`, `buffering` are passed to `open(..)`
    """
    def __init__(self, format, name, mode='a', buffering=1, msgBuffer=0):
        self.filename = name
        self.mode = mode
        self.buffering = buffering
        super(FileOutputter, self).__init__(format, msgBuffer)

    def _open(self):
        self.file = open(self.filename, self.mode, self.buffering)

    def _close(self):
        self.file.close()

    def _write(self, x):
        self.file.write(x)

class StreamOutputter(Outputter):
    """Output to an externally-managed stream."""
    def __init__(self, format, stream=sys.stderr):
        self.stream = stream
        super(StreamOutputter, self).__init__(format)

    def _open(self):
        pass

    def _close(self):
        pass

    def _write(self, x):
        self.stream.write(x)