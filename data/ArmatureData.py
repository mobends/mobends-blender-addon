# <pep8 compliant>
from typing import List


class ArmatureData:
    def __init__(self, bones: List[str]):
        super().__init__()
        self.bones_names = bones

    # end __init__

    @classmethod
    def parse_scene_armature(cls, scene_armature):
        bone_names = list(
            filter(
                lambda name: not name.startswith('helper:'),
                map(lambda bone: bone.name, scene_armature.pose.bones)
            )
        )

        return cls(bone_names)

    # end create_from_scene_armature

# end ArmatureData
