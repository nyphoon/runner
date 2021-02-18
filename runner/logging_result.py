import logging


class LoggingResult:
    # use logging to save results since I'm lazy to handle multi-thread issues
    _loggers= {}

    @classmethod
    def get_logger(cls, name):
        print('get_logger', cls._loggers)
        return cls._loggers.get(name)

    @classmethod
    def create_logger(cls, name, log_path):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        cls._loggers[name] = logger

        return logger
