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
            # row.operator(ot.SHAPEKEYUTILS_OT_lock_shape.bl_idname, text="", emboss=False, icon='DECORATE_LOCKED' if item.lock_shape else 'DECORATE_UNLOCKED').index = index

            # layout.prop(item, 'name', text="", emboss=False)
            # layout.prop(item, 'value', text="", emboss=False)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="")


@register_wrap
class SHAPEKEYUTILS_PT_shape_key_utils(bpy.types.Panel):
    """Collection shape key
    """
    bl_idname = "SHAPEKEYUTILS_PT_shape_key_utils" 
    bl_label = "Collection shape key"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shape Key" # tab name
    # bl_parent_id = ""

    # @classmethod
    # def poll(cls, context):
    #     return (context.active_object is not None) and context.active_object.is_mip

    def draw(self, context):
        layout = self.layout

        # col = layout.column(align=True)
            

        # col = self.layout.column(align=True)
        layout.label(text='Target Collection')

#         col.props_enum
        # light = bpy.data.lights[0]
        # layout.props_enum(light, "type")
        sn = context.scene
        # col.prop_search(scene, 'col_string', bpy.data, 'collections')
        # col.prop_search(scene, 'col_string', scene.collection, 'children_recursive')
        layout.prop(sn, ct.TARGET_COLLECTION, text="")
        layout.prop(sn, ct.RECURSIVE, text="Recursive")
        layout.prop(sn, ct.AUTO_LOCK, text="Auto Lock")
        layout.operator(ot.SHAPEKEYUTILS_OT_test_x.bl_idname, text="Test")
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

        # split = layout.split(factor = 0.5, align=True)
        # row = split.row(align=True)
        row = layout.row(align=True)
        row.prop(sn, ct.SHOW_ONLY_SHAPE_KEY, text="", icon="PINNED" if getattr(sn, ct.SHOW_ONLY_SHAPE_KEY) else "UNPINNED")
        row.prop(sn, ct.USE_SHAPE_KEY_EDIT_MODE, text="", icon="EDITMODE_HLT")



        
        return
