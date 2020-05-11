# <pep8 compliant>

import bpy
from .statics import FORMAT_VERSION


def create_bone_data(scene_bone):
    return {
        'keyframes': []
    }
# end create_bone_data


def create_armature_data(scene_armature):
    armature = {
        'bones': {}
    }

    for scene_bone in scene_armature.pose.bones:
        if not scene_bone.name.startswith('helper:'):
            armature['bones'][scene_bone.name] = create_bone_data(scene_bone)
    
    return armature
# end create_armature_data


def get_bone_local_rest_matrix(scene_bone):
    if scene_bone.parent == None:
        return scene_bone.bone.matrix_local.copy()
    
    parent_mat_inv = scene_bone.parent.bone.matrix_local.inverted()
    return parent_mat_inv @ scene_bone.bone.matrix_local
# end get_bone_local_rest_matrix


def get_bone_local_matrix(scene_bone):
    if scene_bone.parent == None:
        return scene_bone.matrix.copy()
    
    parent_mat_inv = scene_bone.parent.matrix.inverted()
    return parent_mat_inv @ scene_bone.matrix
# end get_bone_local_matrix


def fetch_bone_data(scene_bone, bone):
    # Bone matrix relative to parent, with constraints
    local_mat = get_bone_local_matrix(scene_bone)
    # Bone rest matrix relative to parent
    local_rest_mat = get_bone_local_rest_matrix(scene_bone)
    local_rest_mat.invert()
    # Final matrix in pose space
    pose_mat = local_rest_mat @ local_mat

    (pos, quat, scale) = pose_mat.decompose()

    bone['keyframes'].append({
        'position': [ pos.x, pos.y, pos.z ],
        'rotation': [ quat.x, quat.y, quat.z, quat.w ],
        'scale': [ scale.x, scale.y, scale.z ]
    })
# end fetch_bone_data


def fetch_animation_data(armatures, scene_armature):
    armature = armatures[scene_armature.name]

    for frame_bone in scene_armature.pose.bones:
        if frame_bone.name in armature['bones']:
            fetch_bone_data(frame_bone, armature['bones'][frame_bone.name])
# end fetch_animation_data


def create_data(context, EXPORT_SEL_ONLY=False, EXPORT_SINGLE_ARMATURE=False):
    scene = context.scene
    scene_objs = context.selected_objects if EXPORT_SEL_ONLY else scene.objects
    scene_frames = range(scene.frame_start, scene.frame_end + 1)  # Up to and including the end frame.

    armatures = {}
    for obj in scene_objs:
        if obj.type == 'ARMATURE':
            armature = create_armature_data(obj)
            armatures[obj.name] = armature
    
    orig_frame = scene.frame_current

    # Loop through all frames in the scene.
    for frame in scene_frames:
        scene.frame_set(frame, subframe=0.0)
        frame_objs = context.selected_objects if EXPORT_SEL_ONLY else scene.objects

        for frame_obj in frame_objs:
            if frame_obj.type == 'ARMATURE' and frame_obj.name in armatures:
                fetch_animation_data(armatures, frame_obj)

    scene.frame_set(orig_frame, subframe=0.0)

    if EXPORT_SINGLE_ARMATURE:
        armature = None
        for a in armatures:
            armature = armatures[a]

        return {
            'version': FORMAT_VERSION,
            'meta': bpy.app.version_string,
            'bones': armature['bones']
        }
    else:
        return {
            'version': FORMAT_VERSION,
            'meta': bpy.app.version_string,
            'armatures': armatures
        }

# end create_data