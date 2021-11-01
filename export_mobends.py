# <pep8 compliant>

import os
import bpy
from .data_creator import create_data
from .data_encoder import encode_data


def save_scene(context,
               filepath_base,
               export_selection_only=True,
               ):

    directory_path = os.path.dirname(filepath_base)

    # Exit edit mode before exporting, so current object states are exported properly.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # Fetching data from the context
    data_list = create_data(context, export_selection_only)

    for data in data_list:
        encoded = encode_data(data)
        animation = data['animation']
        filepath = os.path.join(directory_path, f"{animation.target}_{animation.action}.bendsanim")
        with open(filepath, 'wb') as f:
            f.write(encoded)

    return {'FINISHED'}
