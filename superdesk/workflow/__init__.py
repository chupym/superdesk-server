from .workflow import Workflow, Workstation, Workplace, Workitem
from .definition import CopyTasting, ChiefEditor

def init_app(app):
    # Attention the order in which the definition is crucial in composing the work places.
    Workflow.register(CopyTasting())
    Workflow.register(ChiefEditor())
    
    Workflow(app=app)
    model_workplace = Workplace(app=app)
    Workstation(app=app, model_workplace=model_workplace)
    Workitem(app=app)