import os

from integration.rag_services.constants import FileTypes


def resolve_file_type(path):
    #  resolve the file type based on given path, return None if not supported
    _, file_extension = os.path.splitext(path)
    if file_extension == '.json':
        return FileTypes.JSON
    elif file_extension == '.pdf':
        return FileTypes.PDF
    else:
        return None