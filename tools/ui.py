import bpy
from ..setup_tools.register import register_wrap
from . import constants as ct
from . import operators as ot

@register_wrap
class SHAPEKEYUTILS_UL_shape_key_interface_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # layout.label(text=item.name)
            layout.prop(item, 'name', text="", emboss=False)
            layout.prop(item, 'value', text="", emboss=False)
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
        wm = context.window_manager
        # col.prop_search(scene, 'col_string', bpy.data, 'collections')
        # col.prop_search(scene, 'col_string', scene.collection, 'children_recursive')
        layout.prop(wm, ct.TARGET_COLLECTION, text="")

        row = layout.row()
        row.template_list(SHAPEKEYUTILS_UL_shape_key_interface_items.__name__, "", wm, ct.SHAPE_KEY_INTERFACE_COLLECTION, wm, ct.SHAPE_KEY_INDEX)

        col = row.column(align=True)
        col.operator(ot.SHAPEKEYUTILS_OT_add_shape_key_interface.bl_idname, text="", icon='ADD')
        col.operator(ot.SHAPEKEYUTILS_OT_remove_shape_key_interface.bl_idname, text="", icon='REMOVE')
        

        col.separator()
        col.operator(ot.SHAPEKEYUTILS_OT_move_shape_key_interface.bl_idname, text="", icon='TRIA_UP').move_type = 'UP'
        col.operator(ot.SHAPEKEYUTILS_OT_move_shape_key_interface.bl_idname, text="", icon='TRIA_DOWN').move_type = 'DOWN'
        
        return
