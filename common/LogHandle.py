import logging
import os
import sys
from datetime import datetime

from common import utils


class Logger(logging.Logger):
    _log_dir = "log"

    def __init__(self, name):
        super().__init__(name)
        self.name = name

        format = logging.Formatter("%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s")
        time = datetime.today().strftime("%Y-%m-%d")
        file_path = os.path.join(utils.get_log_dir(), str(time) + ".log")

        fh = logging.FileHandler(file_path, encoding="utf-8")
        fh.setFormatter(format)

        sh = logging.StreamHandler(sys.stderr)
        sh.setFormatter(format)
        self.handlers = [fh, sh]
        self.level = logging.INFO


if __name__ == '__main__':
    log = Logger("shop")
    log.info("11111")
    log.debug("222222")
    log.error("33333")
    log.warning("44444")
    log.critical("555555555")

    # l = logging.getLogger("a.b.c")
    # a = logging.getLogger("a.b")
    # c = logging.getLogger("a")
    # print(l.parent)
    # print(a.parent)
    # print(c.parent)
