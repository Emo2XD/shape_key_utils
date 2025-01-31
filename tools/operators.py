import bpy
from ..setup_tools.register import register_wrap
from . import utils as ut
from . import constants as ct
from .. myblendrc_utils import utils as myu
from typing import List
from pprint import pprint



@register_wrap
class SHAPEKEYUTILS_OT_add_shape_key_interface(bpy.types.Operator):
    bl_idname = "shape_key_utils.add_shape_key_interface"
    bl_label = "Add Shape Key Interface"

    def execute(self, context):
        self.report({'INFO'}, f"add shape key interface executed")
        ut.add_shape_key_interface(context.scene)
        return {'FINISHED'}


@register_wrap
class SHAPEKEYUTILS_OT_remove_shape_key_interface(bpy.types.Operator):
    bl_idname = "shape_key_utils.remove_shape_key_interface"
    bl_label = "Remove Shape Key Interface"


    @classmethod
    def poll(self, context):
        sk_collection = getattr(context.scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        return len(sk_collection) > 0

    def execute(self, context):
        ut.remove_active_shape_key_interface(context.scene)
        self.report({'INFO'}, f"remove shape key interface executed")
        return {'FINISHED'}


@register_wrap
class SHAPEKEYUTILS_OT_move_shape_key_interface(bpy.types.Operator):
    bl_idname = "shape_key_utils.move_shape_key_interface"
    bl_label = "Move Shap Key Interface"
    bl_description = "Move shape key interface up / down"

    
    move_type: bpy.props.EnumProperty(name='Type', items=[('UP', 'UP', ''), ('DOWN', 'DOWN', '')]) # type: ignore

    def execute(self, context):
        ut.move_shap_key_interface(context.scene, move_type=self.move_type)
        return {"FINISHED"}


# @register_wrap
# class SHAPEKEYUTILS_OT_remove_shape_key_at_once(bpy.types.Operator):
#     """Remove shape keys at once from objects in the current target collection"""
#     pass

# def get_objects_in_collection(collection:bpy.types.Collection, recursive:bool=False)->List[bpy.types.Object]:
#     """Get objects in collection.
#     """

#     collection_list = [collection]

#     if recursive == True:
#         collection_list += collection.children_recursive 

#     object_list = []

#     for col in collection_list:
#         object_list += col.objects[:]

#     return object_list


# def get_mesh_object_in_collection(collection:bpy.types.Collection, recursive:bool=False)->List[bpy.types.Object]:
#     """Get mesh objects in colleciton
#     """
#     objs = get_objects_in_collection(collection, recursive)
#     return [o for o in objs if o.type == 'MESH']


# def get_key_blocks_from_object(obj:bpy.types.Object):
#     """Get key blocks in shape key. (Handles no shape key error.)"""
#     key_blocks = []

#     try:
#         key_blocks = obj.data.shape_keys.key_blocks[:]
#     except AttributeError:
#         key_blocks = []

#     return key_blocks


# def get_unique_key_block_name_in_collection(collection:bpy.types.Collection, recursive:bool=False)->List[str]:
#     """ Get unique key blocks from objects in given collection.
#     """
#     key_block_name_set = set()

#     objs = get_mesh_object_in_collection(collection, recursive)

#     for o in objs:
#         obj_key_block_names =  [kb.name for kb in  get_key_blocks_from_object(o) ]
#         key_block_name_set = key_block_name_set.union(set(obj_key_block_names))


#     return list(key_block_name_set)


@register_wrap
class SHAPEKEYUTILS_OT_get_sk_interface_from_collection(bpy.types.Operator):
    bl_idname = "shape_key_utils.get_sk_interface_from_collection"
    bl_label = "Get Shape Key Interface From Collection"
    bl_description = "Get shape key interface from currently targeted collection."

    
    @classmethod
    def poll(self, context):
        return getattr(context.scene, ct.TARGET_COLLECTION) is not None

    def execute(self, context):
        ut.get_sk_from_collection_and_add_to_interface(self, context)
        return {"FINISHED"}

@register_wrap
class SHAPEKEYUTILS_OT_test_x(bpy.types.Operator):
    """Test"""
    bl_idname = "shape_key_utils.test_x"
    bl_label = "Test X"
    


    def execute(self, context):
        # objs = get_mesh_object_in_collection(getattr(context.scene, ct.TARGET_COLLECTION), recursive=True)
        # pprint(objs)
        # pprint(get_unique_key_block_name_in_collection(getattr(context.scene, ct.TARGET_COLLECTION), recursive=True))
       

        return {"FINISHED"}
