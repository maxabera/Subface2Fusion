from . import app_context
import adsk
import adsk.core


def get_file_name(file_path):
    title = 'Import Faces JSON file'

    if not app_context.design:
        app_context.ui.messageBox('No active Fusion design', title)
        return

    dlg = app_context.ui.createFileDialog()
    dlg.title = 'Open JSON File'
    dlg.filter = 'JSON(*.json);;All Files (*.*)'
    if dlg.showOpen() != adsk.core.DialogResults.DialogOK:
        return None

    return dlg.filename
