__author__ = "Jiri Manak <jiri.manak@aberamax.com>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2020 Subface2Fusion Released under terms of the AGPLv3 License"

import adsk
import adsk.core
import adsk.fusion
from . import fusion_finger
from . import fusion_pad
from . import fusion_fibridge
from . import fusion_phalanx
from . import fusion_parts as fup
from . import part_font
from . import part_cradle
from . import app_context
from . import material
from . import fusion_marking
from . import color_constants
from . import part_node_marking
from . import fusion_bolt




def create_nodes(node_list, bolt_list, progress=None):
    succesfully_finished = True

    a_font = part_font.Font()
    a_cradle = part_cradle.Cradle()
    a_cradle_wedge = part_cradle.CradleWedge()

    make_fingers = True
    make_pads = True
    make_bridges = True
    make_phalanxes = True
    make_nodemark = True
    make_bolts = True
    weld = True

    for node_idx, a_node in enumerate(node_list):

        new_comp = app_context.createNewComponent()

        negative_bodies = adsk.core.ObjectCollection.create()
        positive_bodies = adsk.core.ObjectCollection.create()

        if progress is not None:
            if progress.wasCancelled:
                succesfully_finished = False
                break
            # Update progress value of progress dialog
            progress.progressValue = node_idx

        if new_comp is None:
            app_context.ui.messageBox('New component failed to create', 'New Component Failed')
            return

        if make_fingers:
            for fii in a_node.list_of_fingers:
                if not fii.is_ignored:
                    positive_bodies = fup.append_to_collection(fusion_finger.build_object(fii, new_comp), positive_bodies)

        if make_pads:
            for pd in a_node.list_of_pads:
                positive_bodies = fup.append_to_collection(fusion_pad.build_object(pd, new_comp), positive_bodies)

        if make_bridges:
            for fib in a_node.list_of_fibridges:
                positive_bodies = fup.append_to_collection(fusion_fibridge.build_object(fib, new_comp), positive_bodies)

        if make_bolts:
            node_bolts = list()
            for blt in bolt_list:
                if blt.node_id == node_idx:
                    node_bolts.append(blt)

            blts = fusion_bolt.Bolt(node_bolts, do_trunk=False, overshot=0.1)

            negative_bodies = fup.append_to_collection(blts.create_negative_bodies(new_comp), negative_bodies)

        if make_nodemark:
            for nm in a_node.list_of_node_markings:
                if nm.type == part_node_marking.NodeMarkType.MIDDLE:
                    fm = fusion_marking.NodeMarkingMiddle(a_node.node_id, nm, a_cradle, a_font)
                    positive_bodies = fup.append_to_collection(fm.create_positive_bodies(new_comp), positive_bodies)
                    negative_bodies = fup.append_to_collection(fm.create_negative_bodies(new_comp), negative_bodies)
                if nm.type == part_node_marking.NodeMarkType.PAD_EDGE:
                    fm = fusion_marking.NodeMarkingPadEdge(a_node.node_id, nm, a_cradle_wedge, a_font)
                    positive_bodies = fup.append_to_collection(fm.create_positive_bodies(new_comp), positive_bodies)
                    negative_bodies = fup.append_to_collection(fm.create_negative_bodies(new_comp), negative_bodies)

        main_body = positive_bodies.item(0)
        positive_bodies.removeByIndex(0)
        if weld:
            combineFeatures = new_comp.features.combineFeatures
            combineFeatureInput = combineFeatures.createInput(main_body, positive_bodies)
            main_body.name = a_node.name("body_")
            combineFeatureInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
            combineFeatureInput.isKeepToolBodies = False
            combineFeatureInput.isNewComponent = False
            combineFeatures.add(combineFeatureInput)

        occs = app_context.design.rootComponent.allOccurrencesByComponent(new_comp)
        occ = occs.item(0)
        occ.appearance = material.plastic_abs_appearance(color_constants.ORANGE)
        occ.component.name = a_node.name()

        if make_phalanxes:
            for fii in a_node.list_of_fingers:
                if not fii.is_ignored:
                    negative_bodies = fup.append_to_collection(fusion_phalanx.build_object(fii, new_comp), negative_bodies)

        if weld:
            combineFeatures = new_comp.features.combineFeatures
            combineFeatureInput = combineFeatures.createInput(main_body, negative_bodies)
            combineFeatureInput.isKeepToolBodies = False
            combineFeatureInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
            combineFeatureInput.isNewComponent = False
            combineFeatures.add(combineFeatureInput)


