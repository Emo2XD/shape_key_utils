import bpy
from ..myblendrc_utils import utils as myu
from . import constants as ct
from typing import List
from collections import OrderedDict

# def get_collections_in_current_scene(self, context:bpy.types.Context):
#     """Callback function to get collections in current scene for shape key at once feature"""
#     enum_list = []
#     default = ('__default__', '__default__', '')
#     enum_list.append(default)


#     scene = context.scene
#     if scene is not None:
#         for c in scene.collection.children_recursive:
#             enum = (c.name, c.name, '')
#             enum_list.append(enum)
#     return enum_list

# TODO: adds option to use custom name other than 'Key'?
def add_shape_key_interface(sn:bpy.types.Scene):
    """Add shape key interface
    add shape key interface to sn.shape_key_interface_collection
    """
    sk_interface_collection = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    sk_interface = sk_interface_collection.add()


    sk_interface.name = myu.new_unique_name_gen('Key', [f.name for f in sk_interface_collection])

    # active_slot_index = getattr(sn, ct.SHAPE_KEY_INDEX)
    setattr(sn, ct.SHAPE_KEY_INDEX, len(sk_interface_collection)-1)


    return



def remove_active_shape_key_interface(sn:bpy.types.Scene):
    """remove shape key interface
    Remove shape key interface to sn.shape_key_interface_collection
    
    Args:
        sn: Scene
        type:str, 'UP' or 'DOWN'

    """
    sk_interface_collection = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    active_slot_index = getattr(sn, ct.SHAPE_KEY_INDEX)

    sk_interface_collection.remove(active_slot_index)

    new_index = min(len(sk_interface_collection)-1, active_slot_index)

    setattr(sn, ct.SHAPE_KEY_INDEX, new_index)
    return


def move_shap_key_interface(sn:bpy.types.Scene, move_type:str='UP'):
    """Move shapkey interface
    """
    sk_interface_collection = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    active_slot_index = getattr(sn, ct.SHAPE_KEY_INDEX)
    sk_len = len(sk_interface_collection)
    

    move_from = active_slot_index
    if move_type == 'UP':
        move_to = (active_slot_index - 1) % sk_len
        
    elif move_type == 'DOWN':
        move_to = (active_slot_index + 1) % sk_len
    else:
        print(f"WARNING: move_type must be 'UP' or 'DOWN', but {move_type} was given")
        return

    sk_interface_collection.move(move_from, move_to)

    setattr(sn, ct.SHAPE_KEY_INDEX, move_to)
    return
    




def get_unique_key_block_name_in_collection(collection:bpy.types.Collection, recursive:bool=False)->List[str]:
    """ Get unique key blocks from objects in given collection.
    """
    key_block_name_set = set()

    objs = myu.get_mesh_object_in_collection(collection, recursive)

    for o in objs:
        obj_key_block_names =  [kb.name for kb in myu.get_key_blocks_from_object(o) ]
        key_block_name_set = key_block_name_set.union(set(obj_key_block_names))

    return list(key_block_name_set)


# def add_kb_to_interface(sk_name:str, interface_collection):
#     """Add key block name to given interface collection
#     sk_name: string name of key block
#     interface_collection: bpy.props.CollectionProperty(type=ShapeKeyInterfaceCollection) 
    # """




def get_sk_from_collection_and_add_to_interface(self, context:bpy.types.Context):
    """Get Shape Key interface from collection.
    """
    sn = context.scene
    
    use_recursive = getattr(sn, ct.RECURSIVE)
    target_collection = getattr(sn, ct.TARGET_COLLECTION) 
    key_block_names = get_unique_key_block_name_in_collection(target_collection, use_recursive)

    sk_interface_collection = getattr(sn, ct.SHAPE_KEY_INTERFACE_COLLECTION)

    original_index = getattr(sn, ct.SHAPE_KEY_INDEX)

    for kb_n in key_block_names:
        # Avoid duplication
        if kb_n not in sk_interface_collection:
            sk_interface = sk_interface_collection.add()
            sk_interface.name = kb_n


    setattr(sn, ct.SHAPE_KEY_INDEX, original_index)

    return


def get_index_of_key(d:dict, key:str)->int:
    """get index of key from dictionary"""
    keys = list(d.keys())
    try:
        return keys.index(key)
    except ValueError:
        return None


def set_active_shape_key_index_by_name(obj:bpy.types.Object, sk_name:str):
    """sets active shape key index by name with error_handled
    """
    shape_keys = obj.data.shape_keys
    if shape_keys is None:
        print(f"object '{obj.name}' does not have shape key")
        return

    index = get_index_of_key(obj.data.shape_keys.key_blocks, sk_name)

    
    if index is None:
        print(f"object '{obj.name}' does not have key '{sk_name}'")
        return

    obj.active_shape_key_index = index
    return
    
    pass


def set_active_index_callback(self, context):
    """ Callback function when update shape key interface index.
    When update shape key interface index, this function loops all the targeted 
    object's shape key and set active key slot
    """
    # print(getattr(context.scene, ct.SHAPE_KEY_INDEX))
    target_collection = getattr(context.scene, ct.TARGET_COLLECTION)
    recursive = getattr(context.scene, ct.RECURSIVE)
    sk_interface_collection = getattr(context.scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    sk_interface_index =  getattr(context.scene, ct.SHAPE_KEY_INDEX)
    sk_interface_name = sk_interface_collection[sk_interface_index].name
    objs = myu.get_mesh_object_in_collection(target_collection, recursive)


    for o in objs:
        set_active_shape_key_index_by_name(o, sk_interface_name)

    return



