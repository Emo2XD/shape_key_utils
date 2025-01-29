import bpy
from ..setup_tools.register import register_wrap



@register_wrap
class SHAPEKEYUTILS_OT_add_shape_key_interface(bpy.types.Operator):
    bl_idname = "shape_key_utils.add_shape_key_interface"
    bl_label = "Add Shape Key Interface"


    def execute(self, context):
        self.report({'INFO'}, f"add shapekey interface executed")
        return {'FINISHED'}

