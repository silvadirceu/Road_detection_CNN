from abstractions.controllers.grpc_server_controller import HttpServer
from containers.container import Container
from dependency_injector.wiring import Provide, inject


@inject
def main(cv_controller = Provide[Container.cv_controller]) -> None:
    pass


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()
