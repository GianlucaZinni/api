import logging
from layers.common.common_logging import logging_handler
from layers.web_services.request_handler import RequestHandler

LOG_LEVEL = "INFO"
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
logger.info("Starting REST API")

@logging_handler(log_level=LOG_LEVEL)
def handler(event, unused_context):
    request_handler = ApiRestHandler(event, logger)
    print(request_handler)
    
    if request_handler.is_resource("/employee"):
        if request_handler.is_post():
            return request_handler.new_employee()
        
class ApiRestHandler(RequestHandler):
    def __ini__(self, event):
        super().__init__(event, logger)
        self.logger = logger
        
    def new_employee(self):
        self.logger.info(f"Employee concepts: {self.body}")
        
        for item in self.body:
            print(item)
        
        return self.response_ok({"result": "new_employee ok"})
    
evn = {
    "resource": "/employee",
    "httpMethod": "POST",
    "body": '{"id": 123, "nombre": "Ejemplo", "edad": 30}'
}

print(handler(evn, ""))
