from abstractions.http_server import HttpServer
from containers.containers import Container
from dependency_injector.wiring import Provide, inject


@inject
def main(service: HttpServer = Provide[Container.server]) -> None:
    service.run(Container.config.host(), Container.config.port())


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()
