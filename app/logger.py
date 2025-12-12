import logging
import os
import sys

def get_logger(name: str = 'chatbot-law-PoC'):
    logger = logging.getLogger(name)

    ## 중복 핸들러 방지(Streamlit은 rerun 시 로거가 중복 생성될 수 있음)
    if logger.handlers:
        return logger

    level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logger.setLevel(level)

    ## 중요! 상위(root) 로거로 전파 방지
    logger.propagate = False

    handler = logging.StreamHandler(stream=sys.stdout) ## stdout -> EB/CloudWatch로 수집됨
    formatter = logging.Formatter(
        fmt = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    ) 

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger