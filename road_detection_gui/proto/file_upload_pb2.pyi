from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileUploadRequest(_message.Message):
    __slots__ = ("file",)
    FILE_FIELD_NUMBER: _ClassVar[int]
    file: str
    def __init__(self, file: _Optional[str] = ...) -> None: ...

class FileUploadResponse(_message.Message):
    __slots__ = ("classification", "details")
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    classification: str
    details: str
    def __init__(self, classification: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...
