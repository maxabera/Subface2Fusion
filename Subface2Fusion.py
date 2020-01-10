__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import adsk.core, adsk.fusion, adsk.cam
import traceback

from . import read_json
from . import app_context
from . import file_import
from . import fusion_node
from . import fusion_beam
from . import fusion_face
from . import fusion_hole


def run(context):

    try:
        print("zaciatok")
        app_context.app = adsk.core.Application.get()
        app_context.ui = app_context.app.userInterface

        # Create a document.
        # doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)                   
        # Get all components in the active design.

        app_context.product = app_context.app.activeProduct
        app_context.design = adsk.fusion.Design.cast(app_context.product)

        app_context.capture_design_history(False)

        subface_file_path = file_import.get_file_name("")
        if subface_file_path is not None:
            subface_json = read_json.load_subface_json(subface_file_path)

            app_context.active_attrs = read_json.read_attributes_json(subface_json)
            node_list = read_json.read_nodes_json(subface_json)
            beam_list = read_json.read_beams_json(subface_json)
            faces_list = read_json.read_faces_json(subface_json)
            bolt_list = read_json.read_bolts_json(subface_json)

            nofo = len(node_list) + len(beam_list) + len(faces_list)

            # Show dialog
            # Set styles of progress dialog.
            app_context.progressDialog = app_context.ui.createProgressDialog()
            app_context.progressDialog.cancelButtonText = 'Cancel'
            app_context.progressDialog.isBackgroundTranslucent = False
            app_context.progressDialog.isCancelButtonShown = True
            app_context.progressDialog.show('Progress Dialog', 'Percentage: %p, Current Value: %v, Total steps: %m', 0, nofo)
            fusion_node.create_nodes(node_list, bolt_list, progress=app_context.progressDialog)
            fusion_beam.create_beams(beam_list, progress=app_context.progressDialog)
            fusion_face.create_faces(faces_list, bolt_list, skip_coplanar=True)
            # fusion_hole.create_holes(faces_list, skip_coplanar=True)

            app_context.progressDialog.hide()

    except:
        if app_context.ui:
            app_context.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()), "title")
