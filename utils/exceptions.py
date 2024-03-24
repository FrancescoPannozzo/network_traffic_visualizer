CUSTOM_FILE_ERROR_MSG = "WARNING, the custom file seems to be not formatted properly, please read the README for infos"

class CustomFileError(Exception):
    def __init__(self, message=CUSTOM_FILE_ERROR_MSG):
        self.message = message
        super().__init__(self.message)
