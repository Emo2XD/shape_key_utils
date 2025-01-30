import bpy
from ..setup_tools.register import register_wrap
from . import utils as ut
from . import constants as ct



@register_wrap
class SHAPEKEYUTILS_OT_add_shape_key_interface(bpy.types.Operator):
    bl_idname = "shape_key_utils.add_shape_key_interface"
    bl_label = "Add Shape Key Interface"

    def execute(self, context):
        self.report({'INFO'}, f"add shape key interface executed")
        ut.add_shape_key_interface(context.window_manager)
        return {'FINISHED'}


@register_wrap
class SHAPEKEYUTILS_OT_remove_shape_key_interface(bpy.types.Operator):
    bl_idname = "shape_key_utils.remove_shape_key_interface"
    bl_label = "Remove Shape Key Interface"


    @classmethod
    def poll(self, context):
        sk_collection = getattr(context.window_manager, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        return len(sk_collection) > 0

    def execute(self, context):
        ut.remove_active_shape_key_interface(context.window_manager)
        self.report({'INFO'}, f"remove shape key interface executed")
        return {'FINISHED'}


@register_wrap
class SHAPEKEYUTILS_OT_move_shape_key_interface(bpy.types.Operator):
    bl_idname = "shape_key_utils.move_shape_key_interface"
    bl_label = "Move Shap Key Interface"
    bl_description = "Move shape key interface up / down"

    
    move_type: bpy.props.EnumProperty(name='Type', items=[('UP', 'UP', ''), ('DOWN', 'DOWN', '')]) # type: ignore

    def execute(self, context):
        ut.move_shap_key_interface(context.window_manager, move_type=self.move_type)
        return {"FINISHED"}
