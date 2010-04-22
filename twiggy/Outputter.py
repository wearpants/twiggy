import multiprocessing

class Outputter(object):
    """
    Does the work of formatting and writing a message.

    Multiple implementations are expected.
    """

    SHUTDOWN = object()

    def __init__(self, format, async = False, **kwargs):
        self._format = format
        self._init(**kwargs)

        if not async:
            self.output = self.__sync_output
            self.close = self._close
            self.open()
        else:
            self.output = self.__async_output
            self.close = self.__async_close
            self.__queue = multiprocessing.JoinableQueue(100)
            self.__child = multiprocessing.Process(target=self.__child_main, args=(self,))
            self.__child.daemon = True
            self.__child.start()

    # use a plain function so Windows is cool
    @staticmethod
    def __child_main(self):
        self._open()

        while True:
            msg = self.__queue.get()
            if msg is not self.SHUTDOWN:
                self.__sync_output(msg)
                self.__queue.task_done()
            else:
                assert self.__queue.empty(), "Shutdown but queue not empty"
                break

        self._close()
        self.__queue.task_done()

    def _init(self, **kwargs):
        raise NotImplementedError

    def _open(self):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError

    def _write(self):
        raise NotImplementedError

    def __sync_output(self, msg):
        x = self._format(msg)
        self._write(x)

    def __async_output(self, msg):
        self._queue.put_nowait(msg)

    def __async_close(self):
        self.__queue.close()
        self.__queue.join()