# <pep8 compliant>

import os
import mathutils
import bpy
import json
from .data import create_data


def save(context,
         filepath,
         export_selection_only=True
         ):

    # Exit edit mode before exporting, so current object states are exported properly.
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # Fetching data from the context
    data = create_data(context)

    # Exporting the data as JSON
    with open(filepath, 'w', encoding='utf8', newline='\n') as f:
        f.write(json.dumps(data, indent=4))

    return { 'FINISHED' }