from .workflow import Workflow, Workstation, Workplace, Workitem
from .definition import CopyTasting, Journalist, ChiefEditor

def init_app(app):
    # Attention the order in which the definition is crucial in composing the work places.
    Workflow.register(CopyTasting())
    Workflow.register(Journalist())
    Workflow.register(ChiefEditor())
    
    Workflow(app=app)
    Workstation(app=app)
    Workplace(app=app)
    Workitem(app=app)