import logging
from concurrent.futures import ThreadPoolExecutor


class AsyncFileHandler(logging.FileHandler):
    def __init__(self, filename, *args, **kwargs):
        self.executor = ThreadPoolExecutor(max_workers=2)
        super().__init__(filename, *args, **kwargs)

    def emit(self, record):
        self.executor.submit(super().emit, record)
