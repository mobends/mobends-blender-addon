# <pep8 compliant>

import os
import mathutils
import bpy
import json
from .data import create_data
from .data_encoder import encode_data

def save(context,
         filepath,
         export_selection_only=True,
         export_single_armature=False
         ):

    # Exit edit mode before exporting, so current object states are exported properly.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # Fetching data from the context
    data = create_data(context, export_selection_only, export_single_armature)

    if export_single_armature:
        data = encode_data(data, single_armature=export_single_armature)
        with open(filepath, 'wb') as f:
            f.write(data)

    else:
        # Exporting the data as JSON
        with open(filepath, 'w', encoding='utf8', newline='\n') as f:
            f.write(json.dumps(data, indent=4))

    return { 'FINISHED' }