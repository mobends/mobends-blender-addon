# <pep8 compliant>

bl_info = {
    "name": "Mo' Bends Exporter",
    "author": "Iwo Plaza",
    "version": (1, 1, 0),
    "blender": (2, 81, 0),
    "location": "File > Import-Export",
    "description":
        "Exports all animations in a binary format.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}


import bpy
from bpy.props import (
    BoolProperty
)
from bpy_extras.io_utils import (
    ExportHelper
)
from .export_mobends import save_scene


class ExportMoBends(bpy.types.Operator, ExportHelper):
    """Export a Mo' Bends animation JSON file"""

    bl_idname = "export_anim.mobends"
    bl_label = "Export Mo' Bends"
    bl_options = {'PRESET'}

    filename_ext = ".bendsanim"

    use_selection = BoolProperty(
        name="Selection Only",
        description="Export selected objects only",
        default=False,
        )

    def execute(self, context):
        return save_scene(context, self.filepath, self.use_selection)
    # end execute

# end ExportMoBends


def menu_func_export(self, context):
    self.layout.operator(ExportMoBends.bl_idname, text="Mo' Bends (.bendsanim)")


def register():
    bpy.utils.register_class(ExportMoBends)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportMoBends)


if __name__ == "__main__":
    register()
