import logging

class SparkLogger:

    @staticmethod
    def create():
        formatter = logging.Formatter(
                 fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger('spark_client')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def get():
        return logging.getLogger('spark_client')
