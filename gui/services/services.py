import os
from typing import Union
from abstractions.controller import Controller
from abstractions.geolocator import Geolocator
from abstractions.http_handler import HttpHandler
from controllers.send_file_controller import SendFileController
from proto.grpc_client import GrpcClient
from services.nominatin_service import NominatinService
from geopy.geocoders import Nominatim
from services.settings import COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT

grpc_client: HttpHandler = GrpcClient(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
send_file_controller: Union[Controller, SendFileController] = SendFileController(grpc_client)
geolocator: Geolocator = NominatinService(geolocator = Nominatim(user_agent="RoadCondition"))
