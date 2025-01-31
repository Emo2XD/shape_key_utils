import bpy
from .setup_tools.register import register_prop, register_wrap
from .tools import constants as ct
from .tools import utils as ut

# register_prop(
#         bpy.types.Scene, 
#         ct.TARGET_COLLECTION, 
#         bpy.props.EnumProperty(
#             name=ct.TARGET_COLLECTION,
#             description="Objects in this collection will share the same shape key",
#             items=ut.get_collections_in_current_scene
#             ))

# def set_unique_key_name(self, value):
#     self['Name'] = value
#     print("set_unique_key_name called")

#     return

# register_prop(
#         bpy.types.Scene,
#         'col_string', bpy.props.StringProperty(name='col_string')
#         )


def poll_is_collection_in_active_scene(self, collection):
    return collection in bpy.context.scene.collection.children_recursive

register_prop(
        bpy.types.Scene,
        ct.TARGET_COLLECTION, bpy.props.PointerProperty(type=bpy.types.Collection, poll=poll_is_collection_in_active_scene)
        )


@register_wrap
class ShapeKeyInterfaceCollection(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name") # type: ignore
    value: bpy.props.FloatProperty(name="Value", subtype='FACTOR', min=0.0, max=1.0, default=0.0) # type: ignore



# bpy.types.Scene.shape_key_interface_collection = bpy.props.CollectionProperty(type=ShapeKeyInterfaceCollection)

register_prop(
        bpy.types.Scene,
        ct.SHAPE_KEY_INTERFACE_COLLECTION,
        bpy.props.CollectionProperty(type=ShapeKeyInterfaceCollection)
        )

register_prop(
        bpy.types.Scene,
        ct.SHAPE_KEY_INDEX,
        bpy.props.IntProperty(name=ct.SHAPE_KEY_INDEX, update=ut.set_active_index_callback),
        )



register_prop(
        bpy.types.Scene,
        ct.RECURSIVE,
        bpy.props.BoolProperty(name=ct.RECURSIVE, default=True, description='If True, search objects recursively in nested collections')
        )
