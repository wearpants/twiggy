import multiprocessing
import sys
import atexit

class Outputter(object):
    """
    Does the work of formatting and writing a message.

    Multiple implementations are expected.
    """

    def __init__(self, format, async = False, **kwargs):
        self._format = format
        self._init(async, **kwargs)

        if not async:
            self.output = self.__sync_output
            self.close = self._close
            self._open()
        else:
            self.output = self.__async_output
            self.close = self.__async_close
            self.__queue = multiprocessing.JoinableQueue(100)
            self.__child = multiprocessing.Process(target=self.__child_main, args=(self,))
            self.__child.start() # XXX s.b. daemon?

        atexit.register(self.close)

    # use a plain function so Windows is cool
    @staticmethod
    def __child_main(self):
        self._open()
        while True:
            msg = self.__queue.get()
            if msg != "SHUTDOWN":
                self.__sync_output(msg)
                self.__queue.task_done()
            else:
                assert self.__queue.empty(), "Shutdown but queue not empty"
                self._close()
                self.__queue.task_done()
                break

    def _init(self, async, **kwargs):
        self.init_kwargs = kwargs

    def _open(self):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError

    def _write(self, x):
        raise NotImplementedError

    def __sync_output(self, msg):
        x = self._format(msg)
        self._write(x)

    def __async_output(self, msg):
        self.__queue.put_nowait(msg)

    def __async_close(self):
        self.__queue.put_nowait("SHUTDOWN") # XXX maybe just put?
        self.__queue.close()
        self.__queue.join()


class FileOutputter(Outputter):

    def _open(self):
        self.file = open(**self.init_kwargs)

    def _close(self):
        self.file.close()

    def _write(self, x):
        self.file.write(x)

class StreamOutputter(Outputter):

    def _init(self, async, stream=sys.stderr):
        if async:
            raise ValueError("Async not supported")

        self.stream = stream

    def _open(self):
        pass

    def _close(self):
        pass

    def _write(self, x):
        self.stream.write(x)