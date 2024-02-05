from abstractions.http_server import HttpServer
from dependency_injector.wiring import Provide, inject
from containers.container import Container


@inject
def main(server: HttpServer = Provide[Container.server]) -> None:
    server.run(Container.config.ocr_host(), Container.config.ocr_port())


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()