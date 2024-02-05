from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileRequest(_message.Message):
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

class VideoPredictResponse(_message.Message):
    __slots__ = ("predictions",)
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    predictions: _containers.RepeatedCompositeFieldContainer[TritonPredictResponse]
    def __init__(self, predictions: _Optional[_Iterable[_Union[TritonPredictResponse, _Mapping]]] = ...) -> None: ...

class ImagePredictResponse(_message.Message):
    __slots__ = ("predictions",)
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    predictions: TritonPredictResponse
    def __init__(self, predictions: _Optional[_Union[TritonPredictResponse, _Mapping]] = ...) -> None: ...

class ImageDataOCrResponse(_message.Message):
    __slots__ = ("latitude", "longitude", "datetime", "speed")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    latitude: str
    longitude: str
    datetime: str
    speed: str
    def __init__(self, latitude: _Optional[str] = ..., longitude: _Optional[str] = ..., datetime: _Optional[str] = ..., speed: _Optional[str] = ...) -> None: ...

class GpsCoordinates(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: str
    longitude: str
    def __init__(self, latitude: _Optional[str] = ..., longitude: _Optional[str] = ...) -> None: ...

class GeoLocation(_message.Message):
    __slots__ = ("latitude", "longitude", "street")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    STREET_FIELD_NUMBER: _ClassVar[int]
    latitude: str
    longitude: str
    street: str
    def __init__(self, latitude: _Optional[str] = ..., longitude: _Optional[str] = ..., street: _Optional[str] = ...) -> None: ...

class PotholeRoadAttr(_message.Message):
    __slots__ = ("latitude", "longitude", "area", "depth")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    AREA_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    latitude: str
    longitude: str
    area: str
    depth: str
    def __init__(self, latitude: _Optional[str] = ..., longitude: _Optional[str] = ..., area: _Optional[str] = ..., depth: _Optional[str] = ...) -> None: ...

class RoadAttr(_message.Message):
    __slots__ = ("potholes", "curb", "crack", "dirty", "traffic_signs")
    POTHOLES_FIELD_NUMBER: _ClassVar[int]
    CURB_FIELD_NUMBER: _ClassVar[int]
    CRACK_FIELD_NUMBER: _ClassVar[int]
    DIRTY_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_SIGNS_FIELD_NUMBER: _ClassVar[int]
    potholes: _containers.RepeatedCompositeFieldContainer[PotholeRoadAttr]
    curb: _containers.RepeatedCompositeFieldContainer[GpsCoordinates]
    crack: _containers.RepeatedCompositeFieldContainer[GpsCoordinates]
    dirty: _containers.RepeatedCompositeFieldContainer[GpsCoordinates]
    traffic_signs: _containers.RepeatedCompositeFieldContainer[GpsCoordinates]
    def __init__(self, potholes: _Optional[_Iterable[_Union[PotholeRoadAttr, _Mapping]]] = ..., curb: _Optional[_Iterable[_Union[GpsCoordinates, _Mapping]]] = ..., crack: _Optional[_Iterable[_Union[GpsCoordinates, _Mapping]]] = ..., dirty: _Optional[_Iterable[_Union[GpsCoordinates, _Mapping]]] = ..., traffic_signs: _Optional[_Iterable[_Union[GpsCoordinates, _Mapping]]] = ...) -> None: ...

class RoadFrameDataResponse(_message.Message):
    __slots__ = ("id", "video_id", "video_time", "datetime", "speed", "geoposition", "attributes", "image")
    ID_FIELD_NUMBER: _ClassVar[int]
    VIDEO_ID_FIELD_NUMBER: _ClassVar[int]
    VIDEO_TIME_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    GEOPOSITION_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    id: int
    video_id: str
    video_time: float
    datetime: str
    speed: float
    geoposition: GeoLocation
    attributes: RoadAttr
    image: str
    def __init__(self, id: _Optional[int] = ..., video_id: _Optional[str] = ..., video_time: _Optional[float] = ..., datetime: _Optional[str] = ..., speed: _Optional[float] = ..., geoposition: _Optional[_Union[GeoLocation, _Mapping]] = ..., attributes: _Optional[_Union[RoadAttr, _Mapping]] = ..., image: _Optional[str] = ...) -> None: ...

class RoadVideoDataResponse(_message.Message):
    __slots__ = ("id", "frames_data")
    ID_FIELD_NUMBER: _ClassVar[int]
    FRAMES_DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    frames_data: _containers.RepeatedCompositeFieldContainer[RoadFrameDataResponse]
    def __init__(self, id: _Optional[str] = ..., frames_data: _Optional[_Iterable[_Union[RoadFrameDataResponse, _Mapping]]] = ...) -> None: ...
