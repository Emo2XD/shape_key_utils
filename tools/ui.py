import bpy
from ..setup_tools.register import register_wrap
from . import constants as ct
from . import operators as ot

@register_wrap
class SHAPEKEYUTILS_UL_shape_key_interface_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # layout.label(text=item.name)
            layout.prop(item, 'name')
            layout.prop(item, 'value')
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
        scene = context.scene
        # col.prop_search(scene, 'col_string', bpy.data, 'collections')
        # col.prop_search(scene, 'col_string', scene.collection, 'children_recursive')
        layout.prop(scene, ct.TARGET_COLLECTION)

        row = layout.row()
        row.template_list(SHAPEKEYUTILS_UL_shape_key_interface_items.__name__, "", scene, ct.SHAPE_KEY_INTERFACE_COLLECTION, scene, ct.SHAPE_KEY_INDEX)

        col = row.column(align=True)
        col.operator(ot.SHAPEKEYUTILS_OT_add_shape_key_interface.bl_idname, text="", icon='ADD')
        # row.template_list("MY_UL_items", "", scene, "my_collection", scene, "my_collection_index")
        return
