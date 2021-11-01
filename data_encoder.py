# <pep8 compliant>

import struct
from .data import BoneData, AnimationData, Keyframe


def encode_float(value):
    return struct.pack('>f', value)


def encode_keyframe(keyframe: Keyframe) -> bytes:
    hasPosition = keyframe['position'] != [0, 0, 0]
    hasRotation = keyframe['rotation'] != [0, 0, 0, 1]
    hasScale = keyframe['scale'] != [1, 1, 1]

    flags = 0
    if hasPosition:
        flags |= 1
    if hasRotation:
        flags |= 2
    if hasScale:
        flags |= 4

    value = struct.pack('>B', flags)

    if hasPosition:
        value += encode_float(keyframe['position'][0])
        value += encode_float(keyframe['position'][1])
        value += encode_float(keyframe['position'][2])

    if hasRotation:
        value += encode_float(keyframe['rotation'][0])
        value += encode_float(keyframe['rotation'][1])
        value += encode_float(keyframe['rotation'][2])
        value += encode_float(keyframe['rotation'][3])

    if hasScale:
        value += encode_float(keyframe['scale'][0])
        value += encode_float(keyframe['scale'][1])
        value += encode_float(keyframe['scale'][2])

    return value


def encode_bone(bone_key: str, bone: BoneData) -> bytes:
    value = bone_key.encode() + b'\0'
    for frame in bone.keyframes:
        value += encode_keyframe(frame)

    return value


def encode_animation(animation: AnimationData) -> bytes:
    amount_of_keyframes = 0
    for bone_key in animation.bones:
        bone = animation.bones[bone_key]
        if len(bone.keyframes) > amount_of_keyframes:
            amount_of_keyframes = len(bone.keyframes)

    # Encoding the amount of keyframes
    value = struct.pack('>I', amount_of_keyframes)
    # Encoding the amount of bones
    value += struct.pack('>I', len(animation.bones))

    for bone_key in animation.bones:
        bone = animation.bones[bone_key]
        value += encode_bone(bone_key, bone)

    return value


def encode_data(data) -> bytes:
    """ Encodes object data into base64 """

    HEADER = b'BENDSANIM'

    encoded = HEADER
    encoded += struct.pack('>I', data['version'])
    encoded += encode_animation(data['animation'])
    return encoded
