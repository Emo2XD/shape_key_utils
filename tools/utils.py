import bpy


def get_collections_in_current_scene(self, context:bpy.types.Context):
    """Callback function to get collections in current scene for shape key at once feature"""
    enum_list = []
    default = ('__default__', '__default__', '')
    enum_list.append(default)


    scene = context.scene
    if scene is not None:
        for c in scene.collection.children_recursive:
            enum = (c.name, c.name, '')
            enum_list.append(enum)
    return enum_list
