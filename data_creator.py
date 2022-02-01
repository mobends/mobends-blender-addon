# <pep8 compliant>

import bpy
import mathutils
import math
from typing import List
from .statics import FORMAT_VERSION
from .data import BoneData
from .data.ContextController import ContextController
from .data import ArmatureData
from .data import AnimationData


def get_bone_local_rest_matrix(scene_bone: bpy.types.PoseBone) -> mathutils.Matrix:
    """
    Retrieves a bone's rest transformation relative to it's parent.
    """

    if scene_bone.parent is None:
        return scene_bone.bone.matrix_local.copy()

    parent_mat_inv = scene_bone.parent.bone.matrix_local.inverted()
    return parent_mat_inv @ scene_bone.bone.matrix_local
# end get_bone_local_rest_matrix


def get_bone_local_matrix(scene_bone: bpy.types.PoseBone):
    """
    Retrieves a bone's posed transformation relative to it's parent.
    """

    if scene_bone.parent is None:
        return scene_bone.matrix.copy()

    parent_mat_inv = scene_bone.parent.matrix.inverted()
    return parent_mat_inv @ scene_bone.matrix
# end get_bone_local_matrix


def get_bone_pose_matrix(scene_bone: bpy.types.PoseBone) -> mathutils.Matrix:
    # Bone matrix relative to parent, with constraints
    local_mat = get_bone_local_matrix(scene_bone)
    # Bone rest matrix relative to parent
    local_rest_mat = get_bone_local_rest_matrix(scene_bone)
    local_rest_mat.invert()
    # Final matrix in pose space
    return local_rest_mat @ local_mat
# end get_bone_pose_matrix


def get_bone_rot_matrix(scene_bone: bpy.types.PoseBone):
    """
    Retrieves a bone's rest rotation transformation.
    """

    mat = scene_bone.bone.matrix_local.to_3x3()
    mat.resize_4x4()

    additional_rotation = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')
    additional_rotation2 = mathutils.Matrix.Rotation(math.radians(180), 4, 'Y')

    # mathutils.Matrix.Scale(-1, 4, mathutils.Vector((1, 0, 0))) @
    return mat @ additional_rotation @ additional_rotation2 @ mathutils.Matrix.Scale(-1, 4, mathutils.Vector((0, 0, 1)))
# end get_bone_local_matrix


def fetch_bone_data(scene_bone: bpy.types.PoseBone, bone: BoneData) -> None:
    # The post matrix is relative to the rest transform.
    pose_mat = get_bone_pose_matrix(scene_bone)

    # We need to get an offset and rotation inline with the global axes.

    rot_mat = get_bone_rot_matrix(scene_bone)
    pose_mat = rot_mat @ pose_mat @ rot_mat.inverted()

    (pos, quat, scale) = pose_mat.decompose()

    bone.add_keyframe({
        'position': [pos.x, pos.y, pos.z],
        'rotation': [quat.x, quat.y, quat.z, quat.w],
        'scale':    [scale.x, scale.y, scale.z]
    })
# end fetch_bone_data


def fetch_pose(animation: AnimationData, bl_armature: bpy.types.Object) -> None:
    for frame_bone in bl_armature.pose.bones:
        if frame_bone.name in animation.bones:
            fetch_bone_data(frame_bone, animation.bones[frame_bone.name])
# end fetch_pose


def create_data(context: bpy.types.Context, EXPORT_SEL_ONLY=False):
    scene = context.scene
    scene_objects = context.selected_objects if EXPORT_SEL_ONLY else scene.objects
    context_ctrl = ContextController(context)

    # bpy.data.objects['Armature'].animation_data.nla_tracks['NlaTrack'].strips.items()

    armatures: dict[str, tuple[bpy.types.Armature, ArmatureData]] = {}
    for obj in filter(lambda o: o.type == 'ARMATURE' and o.animation_data is not None, scene_objects):
        armatures[obj.name] = (obj, ArmatureData.parse_scene_armature(obj))

    animations: List[AnimationData] = []

    def fetch_animation(bl_armature: bpy.types.Object, armature: ArmatureData, start_frame: int, end_frame: int,
                        action: str) -> AnimationData:
        nonlocal scene

        animation = AnimationData.from_armature(armature, bl_armature.name, action)

        # Up to and including the end frame.
        for frame in range(start_frame, end_frame + 1):
            scene.frame_set(frame, subframe=0.0)

            fetch_pose(animation, bl_armature)

        return animation
    # end fetch_animation

    original_frame = scene.frame_current

    with context_ctrl.save():
        for (bl_armature, armature) in armatures.values():
            # We have to remove active action from objects, it overwrites strips actions otherwise...
            context_ctrl.object_set_animation_data_action(bl_armature, None)

            # We save each unmuted strip, mute them, then unmute one-by-one to capture their animation.
            strips = []
            for track in bl_armature.animation_data.nla_tracks:
                if track.mute:
                    continue
                for strip in track.strips:
                    if strip.mute:
                        continue
                    strips.append(strip)
                    strip.mute = True

            for strip in strips:
                strip.mute = False
                animations.append(
                    fetch_animation(bl_armature, armature, int(strip.frame_start), int(strip.frame_end), strip.name)
                )
                strip.mute = True

            for strip in strips:
                strip.mute = False

    scene.frame_set(original_frame, subframe=0.0)

    return [{
        'key': animation.target,
        'version': FORMAT_VERSION,
        'meta': bpy.app.version_string,
        'animation': animation,
    } for animation in animations]
# end create_data
