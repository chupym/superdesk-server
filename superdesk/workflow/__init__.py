from .workflow import WorkflowResource, WorkstationResource, WorkstationService, \
WorkplaceResource, WorkplaceService, WorkitemResource, WorkitemService, WorkflowService
from .definition import CopyTasting, Journalist, ChiefEditor
import superdesk
from superdesk.workflow.definition import WebEditor

def init_app(app):
    # Attention the order in which the definition is crucial in composing the work places.
    WorkflowService.register(CopyTasting())
    WorkflowService.register(Journalist())
    WorkflowService.register(ChiefEditor())
    WorkflowService.register(WebEditor())

    endpoint_name = WorkflowResource.endpoint_name
    service = WorkflowService(endpoint_name, backend=superdesk.get_backend())
    WorkflowResource(endpoint_name, app=app, service=service)

    endpoint_name = WorkstationResource.endpoint_name
    service = WorkstationService(endpoint_name, backend=superdesk.get_backend())
    WorkstationResource(endpoint_name, app=app, service=service)

    endpoint_name = WorkplaceResource.endpoint_name
    service = WorkplaceService(endpoint_name, backend=superdesk.get_backend())
    WorkplaceResource(endpoint_name, app=app, service=service)

    endpoint_name = WorkitemResource.endpoint_name
    service = WorkitemService(endpoint_name, backend=superdesk.get_backend())
    WorkitemResource(endpoint_name, app=app, service=service)
