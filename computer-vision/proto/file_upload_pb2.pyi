from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TritonPredictRequest(_message.Message):
    __slots__ = ("chunk",)
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    def __init__(self, chunk: _Optional[bytes] = ...) -> None: ...

class TritonPredictResponse(_message.Message):
    __slots__ = ("classification", "frame_time", "latitude", "longitude")
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    classification: str
    frame_time: str
    latitude: str
    longitude: str
    def __init__(self, classification: _Optional[str] = ..., frame_time: _Optional[str] = ..., latitude: _Optional[str] = ..., longitude: _Optional[str] = ...) -> None: ...

class UploadVideoRequest(_message.Message):
    __slots__ = ("chunk",)
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    def __init__(self, chunk: _Optional[bytes] = ...) -> None: ...

class UploadVideoResponse(_message.Message):
    __slots__ = ("predictions",)
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    predictions: _containers.RepeatedCompositeFieldContainer[TritonPredictResponse]
    def __init__(self, predictions: _Optional[_Iterable[_Union[TritonPredictResponse, _Mapping]]] = ...) -> None: ...

class UploadImageRequest(_message.Message):
    __slots__ = ("chunk",)
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    chunk: bytes
    def __init__(self, chunk: _Optional[bytes] = ...) -> None: ...

class UploadImageResponse(_message.Message):
    __slots__ = ("prediction",)
    PREDICTION_FIELD_NUMBER: _ClassVar[int]
    prediction: TritonPredictResponse
    def __init__(self, prediction: _Optional[_Union[TritonPredictResponse, _Mapping]] = ...) -> None: ...
