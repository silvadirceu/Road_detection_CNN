from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4
from models.media.data.road_frame_data import RoadFrameData


class RoadVideoData:
    def __init__(self):
        self.__id: UUID = uuid4()
        self.frames_data: List[RoadFrameData] = field(default_factory=lambda: [])

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        pass
        
