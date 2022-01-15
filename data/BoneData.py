# <pep8 compliant>

from typing import Dict, List

Keyframe = Dict[str, List[float]]


class BoneData:
    keyframes: List[Keyframe]

    def __init__(self):
        super().__init__()
        self.keyframes = []

    # end __init__

    def add_keyframe(self, keyframe: Keyframe) -> None:
        self.keyframes.append(keyframe)

    # end add_keyframe

# end BoneData
