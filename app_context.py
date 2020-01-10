import adsk
import adsk.core
import adsk.fusion
from . import attributes

ui = None
product = None
design = None
progressDialog = None
root_comp = None
handlers = list()

app = adsk.core.Application.get()
if app:
    ui = app.userInterface


def createNewComponent():
    # Get the active design.
    global ui
    global product
    global design
    global progressDialog
    global root_comp
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    root_comp = design.rootComponent
    allOccs = design.rootComponent.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component


active_attrs = attributes.Attributes()

def capture_design_history(value=False):
    if design is not None:
        if value:
            design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        else:
            design.designType = adsk.fusion.DesignTypes.DirectDesignType


