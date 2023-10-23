import logging
import os
from datetime import datetime
from functools import wraps

from pythonjsonlogger import jsonlogger

def init_logger(file_name, log_level=None):
    if not log_level:
        log_level = os.getenv("LOG_LEVEL", "INFO")
        
    logger = logging.getLogger(file_name)
    logger.setLevel(getattr(logging, log_level))
    return logger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, context, correlation_id, enviroment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context
        self.correlation_id = correlation_id
        self.enviroment = enviroment
        
    def add_fields(self, log_record, record, message_dict):
        super().add_field(log_record, record, message_dict)
        log_record["function"] = self.context.function_name or ""
        log_record["requestId"] = self.context.aws_request_id or ""
        log_record["functionVersion"] = self.context.function_version or ""
        log_record["correlationId"] = self.context.correlation_id or ""
        log_record["enviroment"] = self.context.enviroment or ""
        
        if not log_record.get("timestamp"):
            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
            
def setup_logging(log_level, context = None, correlation_id=None, enviroment=None):
    json_handler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        context=context, 
        correlation_id=correlation_id, 
        enviroment=enviroment or os.environ["ENVIROMENT"],
        rename_fields={"levelname": "level", "name": "filename"},
        fmt="%(levelname)% %(requestId)% %(name)% %(function)% %(functionVersion)% %(correlationId)% %(message)%",
    )
    json_handler.setFormatter(formatter)
    logging.basicConfig(handlers=[json_handler, formatter], force=True, level=log_level)
    
def logging_handler(log_level):
    def inner_decorator(func):
        @wraps(func)
        def wrapped(event, context):
            logger = logging.getLogger()
            logger.setLevel(log_level)
            try:
                return func(event, context)
            except Exception as _exception:
                logger.exception("ERROR")
                raise _exception
        return wrapped
    return inner_decorator