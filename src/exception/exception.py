class DBTransactionError(Exception):
    def __init__(self):
        self.code = "DB001"
        self.message = "Database transaction error"