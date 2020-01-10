__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

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
