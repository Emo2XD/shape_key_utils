import bpy
from ..setup_tools.register import register_wrap
from . import constants as ct
from . import operators as ot

@register_wrap
class SHAPEKEYUTILS_UL_shape_key_interface_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # layout.label(text=item.name)
            split = layout.split(factor=0.5, align=False)
            split.prop(item, 'name', text="", emboss=False)
            split.prop(item, 'value', text="", emboss=False)
            row = split.row(align = True)
            row.emboss = 'NONE_OR_STATUS'

            row.prop(item, 'lock_shape', text="", emboss=False, icon='DECORATE_LOCKED' if item.lock_shape else 'DECORATE_UNLOCKED')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="")


@register_wrap
class SHAPEKEYUTILS_PT_shape_key_utils(bpy.types.Panel):
    """Collection shape key
    """
    bl_idname = "SHAPEKEYUTILS_PT_shape_key_utils" 
    bl_label = "Shape Key At Once"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shape Key" # tab name

    def draw(self, context):
        layout = self.layout
        layout.label(text='Target Collection')

        sn = context.scene
        layout.prop(sn, ct.TARGET_COLLECTION, text="")
        layout.prop(sn, ct.RECURSIVE, text="Recursive")
        layout.prop(sn, ct.AUTO_LOCK, text="Auto Lock")
        # layout.operator(ot.SHAPEKEYUTILS_OT_test_x.bl_idname, text="Test")
        layout.operator(ot.SHAPEKEYUTILS_OT_get_sk_interface_from_collection.bl_idname, text="Retrieve Interface")
        layout.operator(ot.SHAPEKEYUTILS_OT_add_missing_shape_key.bl_idname, text="Add Missing Shape Keys")


        row = layout.row()
        row.template_list(SHAPEKEYUTILS_UL_shape_key_interface_items.__name__, "", sn, ct.SHAPE_KEY_INTERFACE_COLLECTION, sn, ct.SHAPE_KEY_INDEX)

        col = row.column(align=True)
        col.operator(ot.SHAPEKEYUTILS_OT_add_shape_key_interface.bl_idname, text="", icon='ADD')
        col.operator(ot.SHAPEKEYUTILS_OT_remove_shape_key_interface.bl_idname, text="", icon='REMOVE')
        

        col.separator()
        col.operator(ot.SHAPEKEYUTILS_OT_move_shape_key_interface.bl_idname, text="", icon='TRIA_UP').move_type = 'UP'
        col.operator(ot.SHAPEKEYUTILS_OT_move_shape_key_interface.bl_idname, text="", icon='TRIA_DOWN').move_type = 'DOWN'

        col.separator()
        col.operator(ot.SHAPEKEYUTILS_OT_set_lock_all_at_once.bl_idname, text="", icon='DECORATE_LOCKED').unlock = False
        col.operator(ot.SHAPEKEYUTILS_OT_set_lock_all_at_once.bl_idname, text="", icon='DECORATE_UNLOCKED').unlock = True

        row = layout.row(align=True)
        row.operator(ot.SHAPEKEYUTILS_OT_set_show_only_at_once.bl_idname, text="", icon="SOLO_ON").show_only = True
        row.operator(ot.SHAPEKEYUTILS_OT_set_show_only_at_once.bl_idname, text="", icon="SOLO_OFF").show_only = False

        split = row.split(factor=0.7)
        split.separator()
        split.operator(ot.SHAPEKEYUTILS_OT_reset_shape_key_at_once.bl_idname, text="", icon="PANEL_CLOSE")

        row = layout.row(align=True)
        row.operator(ot.SHAPEKEYUTILS_OT_set_shape_key_edit_mode.bl_idname, text="Enable", icon="EDITMODE_HLT").shape_key_edit_mode = True
        row.operator(ot.SHAPEKEYUTILS_OT_set_shape_key_edit_mode.bl_idname, text="Desable", icon="EDITMODE_HLT").shape_key_edit_mode = False
        return