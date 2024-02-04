from abstractions.http_server import HttpServer
from dependency_injector.wiring import Provide, inject
from services.container import Container


@inject
def main(service: HttpServer = Provide[Container.grpc_server]) -> None:
    service.run(Container.config.ocr_host(), Container.config.ocr_port())


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()
