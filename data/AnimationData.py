# <pep8 compliant>
from typing import Dict
from .ArmatureData import ArmatureData
from .BoneData import BoneData


class AnimationData:
    def __init__(self, bones: Dict[str, BoneData], target: str, action: str):
        super().__init__()
        self.bones = bones
        self.target = target
        self.action = action
    # end __init__

    @classmethod
    def from_armature(cls, armature_data: ArmatureData, target: str = 'character', action: str = 'default_action'):
        bones = {}

        for bone in armature_data.bones:
            bones[bone.name] = bone.clone()

        return cls(bones, target, action)
    # end from_armature
# end ArmatureData
