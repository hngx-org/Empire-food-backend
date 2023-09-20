class Response:
    messaage: str
    statusCode: int
    data: dict

    def __init__(self, msg, code, data = None):
        self.msg = msg
        self.code = code
        self.data = data
