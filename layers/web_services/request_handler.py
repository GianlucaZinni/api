import json
from datetime import date, datetime
from decimal import Decimal


class RequestHandler:
    def __init__(self,event, logger, log_event: bool = True):
        self.logger = logger
        self.qs = event.get("queryStringParameters", {})
        self.resource = event["resource"]
        self.method = event["httpMethod"]
        self.username = event.get("requestContext", {}).get("authorizer", {}).get("username")
        # Verifica si el cuerpo del evento contiene JSON válido antes de analizarlo
        if event["body"]:
            try:
                self.body = json.loads(event["body"])
            except json.JSONDecodeError as e:
                self.body = None
                self.logger.error(f"Error al analizar el cuerpo JSON: {e}")
        else:
            self.body = None

        if log_event:
            self.logger.info(f"Event: {event}")
        self.logger.info(f"Parameters: {self.qs}")
        
    @staticmethod
    def json_serial(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def is_resource(self, resource):
        return self.resource == resource
    
    def is_get(self):
        return self.method == "GET"
    
    def is_post(self):
        return self.method == "POST"
    
    def is_delete(self):
        return self.method == "DELETE"
    
    def is_put(self):
        return self.method == "PUT"

    def build_response(self, status_code, body=None, message:str = None):
        response = {
            "status_code": status_code,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,GET",
            },
        }
        if body:
            response["body"] = json.dumps(body, default=self.json_serial)
        elif message:
            response["body"] = json.dumps({"message": message}, default=self.json_serial)
        
        self.logger.info(f"Response: {response}")
        
        return response
    
    def response_ok(self, body=None, message:str = None):
        return self.build_response(200, body, message)
    
    def response_not_found(self, body=None, message:str = None):
        message = message if message else "Not Found"
        return self.build_response(404, body, message)
    
    def response_bad_request(self, body=None, message:str = None):
        message = message if message else "Bad Request"
        return self.build_response(400, body, message)