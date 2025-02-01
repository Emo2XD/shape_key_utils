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
    # sk_interface["lock_shape"] = False

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
    It retrieves every shape key name from objects in target collection, 
    and add to shape key interface collection.
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
            # sk_interface["lock_shape"] = False


    setattr(sn, ct.SHAPE_KEY_INDEX, original_index)

    return


def get_index_of_key(d:dict, key:str)->int:
    """get index of key from dictionary"""
    keys = list(d.keys())
    try:
        return keys.index(key)
    except ValueError:
        return None


def set_active_shape_key_index_by_name(obj:bpy.types.Object, sk_name:str, auto_lock:bool=True):
    """sets active shape key index by name with error_handled
    This fucntion sets active shape_key, and lock status.
    """
    shape_keys = obj.data.shape_keys
    if shape_keys is None:
        print(f"object '{obj.name}' does not have shape key")
        return

    index = get_index_of_key(obj.data.shape_keys.key_blocks, sk_name)

    if auto_lock:
        for kb in shape_keys.key_blocks:
            kb.lock_shape = True

    
    if index is None:
        print(f"object '{obj.name}' does not have key '{sk_name}'")
        return

    obj.active_shape_key_index = index

    # TODO: maybe unnecessary? because we update by shape key interface.
    if auto_lock:
        shape_keys.key_blocks[index].lock_shape = False
    return



def setup_sk_interface_auto_lock(sk_name:str):
    """Set shape key interface auto lock status. (without activating setter for setting lock status)"""
    kbi_collection = getattr(bpy.context.scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)

    for kbi in kbi_collection:
        # kbi.lock_shape = True
        kbi['lock_shape'] = True # suppress setter activation

    # kbi_collection[sk_name].lock_shape = False
    kbi_collection[sk_name]['lock_shape'] = False # suppress setter activation
    
    return
    
def set_sk_interface_lock_shape_callback(self, value):
    """ Callback function for set shape key interface lock status. (when you create custom setter, you also have to create getter.)
    """
    self["lock_shape"] = value
    context = bpy.context
    target_collection = getattr(context.scene, ct.TARGET_COLLECTION)

    if target_collection is None:
        print("No collection is selected for shape key interface")
        return

    recursive = getattr(context.scene, ct.RECURSIVE)
    sk_interface_name = self.name
    sk_interface_val = self.value
    objs = myu.get_mesh_object_in_collection(target_collection, recursive)


    for o in objs:
        shape_key = o.data.shape_keys
        if shape_key is not None:
            kb = shape_key.key_blocks.get(sk_interface_name)
            if kb is not None:
                kb.lock_shape = value
    
    return


def get_sk_interface_lock_shape_callback(self):
    # return self["lock_shape"]
    return self.get('lock_shape', self.bl_rna.properties['lock_shape'].default) # to avoid value not assigned error.



def set_auto_lock_callback(self, value):
    """ Callback function for auto lock property"""
    self[ct.AUTO_LOCK] = value
    if value == True:
        scene = bpy.context.scene
        ski_collection = getattr(scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)
        if len(ski_collection) > 0:
            index = getattr(scene, ct.SHAPE_KEY_INDEX)
            ski_collection[index].lock_shape = False # intentionally call setter.
            setattr(scene, ct.SHAPE_KEY_INDEX, index)# intentionally call setter.


def get_auto_lock_callback(self):
    # return self[ct.AUTO_LOCK] self.get("testprop", self.bl_rna.properties["testprop"].default)
    return self.get(ct.AUTO_LOCK, self.bl_rna.properties[ct.AUTO_LOCK].default)


def update_sk_interface_callback(self, context):
    """ Callback function when update shape key interface index.
    When update shape key interface index, this function loops all the targeted 
    object's shape key and set active key slot
    """
    # print(getattr(context.scene, ct.SHAPE_KEY_INDEX))
    target_collection = getattr(context.scene, ct.TARGET_COLLECTION)
        

    recursive = getattr(context.scene, ct.RECURSIVE)
    sk_interface_collection = getattr(context.scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)

    if len(sk_interface_collection) == 0:
        return

    sk_interface_index =  getattr(context.scene, ct.SHAPE_KEY_INDEX)
    sk_interface_name = sk_interface_collection[sk_interface_index].name
    lock_others = getattr(context.scene, ct.AUTO_LOCK)

    if lock_others:
        setup_sk_interface_auto_lock(sk_interface_name)

    if target_collection is None:
        print("No collection is selected for shape key interface")
        return

    objs = myu.get_mesh_object_in_collection(target_collection, recursive)


    for o in objs:
        set_active_shape_key_index_by_name(o, sk_interface_name, lock_others)



    return


def set_shape_key_value_callback(self, context):
    """Callback function when setting value in shape key interface.
    When setting value to shape key interface, this callback function update
    all the corresponding shape key value in the collection.
    """
    target_collection = getattr(context.scene, ct.TARGET_COLLECTION)

    if target_collection is None:
        print("No collection is selected for shape key interface")
        return

    recursive = getattr(context.scene, ct.RECURSIVE)
    sk_interface_name = self.name
    sk_interface_val = self.value
    objs = myu.get_mesh_object_in_collection(target_collection, recursive)


    for o in objs:
        shape_key = o.data.shape_keys
        if shape_key is not None:
            kb = shape_key.key_blocks.get(sk_interface_name)
            if kb is not None:
                kb.value = sk_interface_val
    
    return



def add_missing_shape_keys(context:bpy.types.Context):
    """Add missing shape keys to objects in target collection."""
    scene = context.scene
    target_collection = getattr(scene, ct.TARGET_COLLECTION)

    if target_collection is None:
        print("No collection is selected for shape key interface")
        return

    recursive = getattr(scene, ct.RECURSIVE)
    sk_interface_collection = getattr(scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    objs = myu.get_mesh_object_in_collection(target_collection, recursive)

    for o in objs:
        if o.data.shape_keys == None:
            o.shape_key_add(name="Basis") # make sure every objects have at least one shape key.


    for o in objs:
        for kbi in sk_interface_collection:
            if o.data.shape_keys.key_blocks.get(kbi.name) == None:
                new_kb = o.shape_key_add(name=kbi.name, from_mix=False)
                new_kb.value = kbi.value
                new_kb.lock_shape = kbi.lock_shape
                print(f"Shape key '{kbi.name}' was added to object '{o.name}'")



def lock_all_shape_key_at_once(context:bpy.types.Context, unlock:bool=False):
    set_key_block_prop_at_once(context=context, prop_name='lock_shape', set_value=(not unlock), exclude_active=False)
    return


def show_only_shape_key_at_once(context:bpy.types.Context, show:bool=False):
    set_obj_prop_at_once(context=context, prop_name='show_only_shape_key', set_value=show)
    return
    

def shape_key_edit_mode_at_once(context:bpy.types.Context, display:bool=False):
    set_obj_prop_at_once(context=context, prop_name='use_shape_key_edit_mode', set_value=display)
    return


def reset_shape_key_value_at_once(context:bpy.types.Context, exclude_active:bool=False):
    set_key_block_prop_at_once(context=context, prop_name='value', set_value=0.0, exclude_active=exclude_active)
    return


def set_key_block_prop_at_once(context:bpy.types.Context, prop_name:str, set_value:any, exclude_active:bool=False):
    """Set key block properties to all given objects
    Example Usage:
    to change shape key value
        set_key_block_prop_at_once(objs, 'value', 0)
    
    to change lock status
        set_key_block_prop_at_once(objs, 'lock_shape', True)
    """
    scene = context.scene
    target_collection = getattr(scene, ct.TARGET_COLLECTION)

    if target_collection is None:
        print("No collection is selected for shape key interface")
        return


    recursive = getattr(scene, ct.RECURSIVE)
    sk_interface_collection = getattr(scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    objs = myu.get_mesh_object_in_collection(target_collection, recursive)


    # set_key_block_prop_at_once(objs, prop_name=prop_name, set_value=0.0)
    for o in objs:
        set_prop_to_key_blocks(o, prop_name, set_value)

    if len(sk_interface_collection) == 0:
        return
    
    active_index = getattr(scene, ct.SHAPE_KEY_INDEX)
    active_ski = sk_interface_collection[active_index] # ski = shape key interface
    orig_value = active_ski.value

    # update shape key interface 
    for ski in sk_interface_collection:
        ski[prop_name] = set_value # intentionaly avoid activating setter.
    
    if exclude_active:
        active_ski.value = orig_value # intentionally activate setter

    return


def set_obj_prop_at_once(context:bpy.types.Context, prop_name:str, set_value:any):
    """Set object property at once to all the given objects
     Example Usage:
    to change show only shape key (Pin icon button in shape key)
        set_shape_key_prop_at_once(objs, 'show_only_shape_key', True)
    """
    scene = context.scene
    target_collection = getattr(scene, ct.TARGET_COLLECTION)

    if target_collection is None:
        print("No collection is selected for shape key interface")
        return

    # sk_interface_collection = getattr(scene, ct.SHAPE_KEY_INTERFACE_COLLECTION)
    recursive = getattr(scene, ct.RECURSIVE)
    objs = myu.get_mesh_object_in_collection(target_collection, recursive)

    for o in objs:
        setattr(o, prop_name, set_value)
        # set_shape_key_obj_prop(o, prop_name, set_value)
        # shape_key = o.data.shape_keys
        # if shape_key is not None:
        #     setattr(shape_key, prop_name, set_value)


    return


def set_prop_to_key_blocks(obj:bpy.types.Object, prop_name:str, set_value:any):
    """Set property to all key blocks on object (Error Handled)
    Example Usage:
    to change shape key value
        set_prop_to_key_blocks(obj, 'value', 0)
    
    to change lock status
        set_prop_to_key_blocks(obj, 'lock_shape', True)
    """
    
    shape_key = obj.data.shape_keys
    if shape_key is not None:
        for kb in shape_key.key_blocks:
            setattr(kb, prop_name, set_value)

    return


# def set_shape_key_obj_prop(obj:bpy.types.Object, prop_name:str, set_value:any):
#     """Set object shape key property (Error handled)
#      Example Usage:
#     to change show only shape key (Pin icon button in shape key)
#         set_prop_to_shape_key(obj, 'show_only_shape_key', True)
#     """
#     shape_key = obj.data.shape_keys
#     if shape_key is not None:
#         setattr(shape_key, prop_name, set_value)
#     return
