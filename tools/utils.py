import bpy
from ..myblendrc_utils import utils as myu
from . import constants as ct


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


def add_shape_key_interface(wm:bpy.types.WindowManager):
    """Add shape key interface
    add shape key interface to wm.shape_key_interface_collection
    """
    sk_interface_collection = getattr(wm, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    sk_interface = sk_interface_collection.add()


    sk_interface.name = myu.new_unique_name_gen('Key', [f.name for f in sk_interface_collection])

    active_slot_index = getattr(wm, ct.SHAPE_KEY_INDEX)
    setattr(wm, ct.SHAPE_KEY_INDEX, len(sk_interface_collection)-1)


    return



def remove_active_shape_key_interface(wm:bpy.types.WindowManager):
    """remove shape key interface
    Remove shape key interface to wm.shape_key_interface_collection
    
    Args:
        wm: WindowManager
        type:str, 'UP' or 'DOWN'

    """
    sk_interface_collection = getattr(wm, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    active_slot_index = getattr(wm, ct.SHAPE_KEY_INDEX)

    sk_interface_collection.remove(active_slot_index)

    new_index = min(len(sk_interface_collection)-1, active_slot_index)

    setattr(wm, ct.SHAPE_KEY_INDEX, new_index)
    return


def move_shap_key_interface(wm:bpy.types.WindowManager, move_type:str='UP'):
    """Move shapkey interface
    """
    sk_interface_collection = getattr(wm, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    active_slot_index = getattr(wm, ct.SHAPE_KEY_INDEX)
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

    setattr(wm, ct.SHAPE_KEY_INDEX, move_to)
    return
    




