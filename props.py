import bpy
from .setup_tools.register import register_prop, register_wrap
from .tools import constants as ct
from .tools import utils as ut


def poll_is_collection_in_active_scene(self, collection):
    return collection in bpy.context.scene.collection.children_recursive

register_prop(
        bpy.types.Scene,
        ct.TARGET_COLLECTION, bpy.props.PointerProperty(type=bpy.types.Collection, poll=poll_is_collection_in_active_scene)
        )

@register_wrap
class ShapeKeyInterfaceCollection(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name") # type: ignore
    value: bpy.props.FloatProperty(name="Value", subtype='FACTOR', min=0.0, max=1.0, default=0.0, update=ut.set_shape_key_value_callback) # type: ignore
    lock_shape: bpy.props.BoolProperty(name="lock_shape", set=ut.set_sk_interface_lock_shape_callback, get=ut.get_sk_interface_lock_shape_callback, default=False) # type: ignore

register_prop(
        bpy.types.Scene,
        ct.SHAPE_KEY_INTERFACE_COLLECTION,
        bpy.props.CollectionProperty(type=ShapeKeyInterfaceCollection)
        )

register_prop(
        bpy.types.Scene,
        ct.SHAPE_KEY_INDEX,
        bpy.props.IntProperty(name=ct.SHAPE_KEY_INDEX, update=ut.update_sk_interface_callback),
        )

register_prop(
        bpy.types.Scene,
        ct.AUTO_LOCK,
        bpy.props.BoolProperty(name=ct.AUTO_LOCK, default=True, get=ut.get_auto_lock_callback, set=ut.set_auto_lock_callback)
        )

register_prop(
        bpy.types.Scene,
        ct.RECURSIVE,
        bpy.props.BoolProperty(name=ct.RECURSIVE, default=True, description='If True, search objects recursively in nested collections')
        )