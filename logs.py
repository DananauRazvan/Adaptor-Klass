import logging

def logs(file_name, file_log):
    logging.basicConfig(level=logging.DEBUG, filename='logs/log.log', filemode='w',
                        format="%(asctime)s - %(levelname)s - %(message)s")

    logger = logging.getLogger(file_name)
    handler = logging.FileHandler(file_log)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger