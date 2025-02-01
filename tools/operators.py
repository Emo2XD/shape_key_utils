import bpy
from ..setup_tools.register import register_wrap
from . import utils as ut
from . import constants as ct
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

    @classmethod
    def poll(self, context):
        sk_collection = getattr(context.scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        return len(sk_collection) > 0

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
class SHAPEKEYUTILS_OT_add_missing_shape_key(bpy.types.Operator):
    bl_idname = "shape_key_utils.add_missing_shape_key"
    bl_label = "Add Missing Shape Key"
    bl_description = "Add missing shape key to mesh object inside collection compare to shape key interface."

    
    @classmethod
    def poll(self, context):
        return (len(getattr(context.scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)) > 0 ) and \
            (getattr(context.scene, ct.TARGET_COLLECTION) is not None)

    def execute(self, context):
        ut.add_missing_shape_keys(context)
        self.report({'INFO'}, f"added missing shape key, see console for more detail")
        return {"FINISHED"}



# @register_wrap
# class SHAPEKEYUTILS_OT_lock_shape(bpy.types.Operator):
#     bl_idname = "shape_key_utils.lock_shape"
#     bl_label = "Lock Shape"
#     bl_description = "Lock shape. Shift click to lock others, ctrl click to only lock current, alt click for toggle all."

#     index: bpy.props.IntProperty(name='index') # type: ignore

#     def execute(self, context):
#         # sn = bpy.context.scene
#         # sk_inter_coll = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
#         # sk_inter = sk_inter_coll[self.index]
#         # sk_inter.lock_shape = not sk_inter.lock_shape
#         self.report({'INFO'}, f"lock shape (not implemented yet.)")
#         return {'FINISHED'}



@register_wrap
class SHAPEKEYUTILS_OT_set_lock_all_at_once(bpy.types.Operator):
    bl_idname = "shape_key_utils.set_lock_all_at_once"
    bl_label = "Lock All Shape Key"
    bl_description = "Lock all shape key in the collection"

    unlock: bpy.props.BoolProperty(name="Lock", default=False) # type: ignore

    def execute(self, context):
        # sn = bpy.context.scene
        # sk_inter_coll = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        # sk_inter = sk_inter_coll[self.index]
        # sk_inter.lock_shape = not sk_inter.lock_shape
        ut.lock_all_shape_key_at_once(context, self.unlock)
        self.report({'INFO'}, f"Unlock all" if self.unlock else "Lock all")
        return {'FINISHED'}
    




@register_wrap
class SHAPEKEYUTILS_OT_set_show_only_at_once(bpy.types.Operator):
    bl_idname = "shape_key_utils.set_show_only_at_once"
    bl_label = "Set Show Only Active Shape Key"
    bl_description = "Set show active shape key at once in target collection"

    show_only: bpy.props.BoolProperty(name="Show Only", default=False) # type: ignore

    def execute(self, context):
        # sn = bpy.context.scene
        # sk_inter_coll = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        # sk_inter = sk_inter_coll[self.index]
        # sk_inter.lock_shape = not sk_inter.lock_shape
        ut.show_only_shape_key_at_once(context, self.show_only)
        self.report({'INFO'}, f"{'Enable' if self.show_only else 'Desable'} show only active shape key")
        return {'FINISHED'}
    

@register_wrap
class SHAPEKEYUTILS_OT_set_shape_key_edit_mode(bpy.types.Operator):
    bl_idname = "shape_key_utils.set_shape_key_edit_mode"
    bl_label = "Set Shape Key Edit Mode At Once"
    bl_description = "Set shape key edit mode at once on the object in the target collection."

    shape_key_edit_mode: bpy.props.BoolProperty(name="Shape Key Edit Mode", default=False) # type: ignore

    def execute(self, context):
        # sn = bpy.context.scene
        # sk_inter_coll = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        # sk_inter = sk_inter_coll[self.index]
        # sk_inter.lock_shape = not sk_inter.lock_shape
        ut.shape_key_edit_mode_at_once(context, self.shape_key_edit_mode)
        self.report({'INFO'}, f"{'Enable' if self.shape_key_edit_mode else 'Desable'} shap key edit mode")
        return {'FINISHED'}


@register_wrap
class SHAPEKEYUTILS_OT_reset_shape_key_at_once(bpy.types.Operator):
    bl_idname = "shape_key_utils.reset_shape_key_at_once"
    bl_label = "Reset Shape Key At Once"
    bl_description = "Reset shape key value to zero. Shift click to exclude active."

    exclude_active : bpy.props.BoolProperty(name="Exclude Active", default=True) # type: ignore

    def execute(self, context):
        # sn = bpy.context.scene
        # sk_inter_coll = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        # sk_inter = sk_inter_coll[self.index]
        # sk_inter.lock_shape = not sk_inter.lock_shape
        ut.reset_shape_key_value_at_once(context, self.exclude_active)
        self.report({'INFO'}, "All shape key value is zero{}".format("." if not self.exclude_active else ", excluding active shape key interface."))
        return {'FINISHED'}
    
    def invoke(self, context, event):
        
        shift_pressed = event.shift
        
        if shift_pressed:
            self.exclude_active = True
        else:
           self.exclude_active = False

        return self.execute(context)


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
