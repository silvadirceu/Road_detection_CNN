import os
from typing import Union
from dotenv import load_dotenv
from abstractions.controller import Controller
from abstractions.geolocator import Geolocator
from abstractions.http_handler import HttpHandler
from controllers.send_file_controller import SendFileController
from proto.grpc_client import GrpcClient
from services.nominatin_service import NominatinService
from geopy.geocoders import Nominatim

load_dotenv()
API_URL = os.environ.get("API_URL")
COMPUTER_VISION_SERVICE = os.environ.get("COMPUTER_VISION_SERVICE")
COMPUTER_VISION_PORT = os.environ.get("COMPUTER_VISION_PORT")

grpc_client: HttpHandler = GrpcClient(COMPUTER_VISION_SERVICE, COMPUTER_VISION_PORT)
send_file_controller: Union[Controller, SendFileController] = SendFileController(grpc_client)
geolocator: Geolocator = NominatinService(geolocator = Nominatim(user_agent="RoadCondition"))
