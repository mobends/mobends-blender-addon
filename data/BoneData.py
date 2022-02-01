# <pep8 compliant>

from typing import Dict, List

Keyframe = Dict[str, List[float]]


class BoneData:
    name: str
    keyframes: List[Keyframe]

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.keyframes = []
    # end __init__

    def add_keyframe(self, keyframe: Keyframe) -> None:
        self.keyframes.append(keyframe)
    # end add_keyframe

    def clone(self):
        return BoneData(self.name, self.inverted)
    # end clone
# end BoneData
