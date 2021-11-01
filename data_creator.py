# <pep8 compliant>

from typing import Any, List
import bpy
from .statics import FORMAT_VERSION
from .data import BoneData
from .data.ContextController import ContextController
from .data import ArmatureData
from .data import AnimationData


def get_bone_local_rest_matrix(scene_bone):
    if scene_bone.parent is None:
        return scene_bone.bone.matrix_local.copy()

    parent_mat_inv = scene_bone.parent.bone.matrix_local.inverted()
    return parent_mat_inv @ scene_bone.bone.matrix_local
# end get_bone_local_rest_matrix


def get_bone_local_matrix(scene_bone):
    if scene_bone.parent is None:
        return scene_bone.matrix.copy()

    parent_mat_inv = scene_bone.parent.matrix.inverted()
    return parent_mat_inv @ scene_bone.matrix
# end get_bone_local_matrix


def fetch_bone_data(scene_bone, bone: BoneData):
    # Bone matrix relative to parent, with constraints
    local_mat = get_bone_local_matrix(scene_bone)
    # Bone rest matrix relative to parent
    local_rest_mat = get_bone_local_rest_matrix(scene_bone)
    local_rest_mat.invert()
    # Final matrix in pose space
    pose_mat = local_rest_mat @ local_mat

    (pos, quat, scale) = pose_mat.decompose()

    bone.add_keyframe({
        'position': [pos.x, pos.y, pos.z],
        'rotation': [quat.x, quat.y, quat.z, quat.w],
        'scale':    [scale.x, scale.y, scale.z]
    })
# end fetch_bone_data


def fetch_pose(animation: AnimationData, bl_armature):
    for frame_bone in bl_armature.pose.bones:
        if frame_bone.name in animation.bones:
            fetch_bone_data(frame_bone, animation.bones[frame_bone.name])
# end fetch_pose


def create_data(context, EXPORT_SEL_ONLY=False):
    scene = context.scene
    scene_objects = context.selected_objects if EXPORT_SEL_ONLY else scene.objects
    context_ctrl = ContextController(context)

    # bpy.data.objects['Armature'].animation_data.nla_tracks['NlaTrack'].strips.items()

    armatures: dict[str, tuple[Any, ArmatureData]] = {}
    for obj in filter(lambda o: o.type == 'ARMATURE' and o.animation_data is not None, scene_objects):
        armatures[obj.name] = (obj, ArmatureData.parse_scene_armature(obj))

    animations: List[AnimationData] = []

    def fetch_animation(bl_armature, armature: ArmatureData, start_frame: int, end_frame: int,
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
