from data import ArmatureData


class MockBone:
    def __init__(self, name):
        super().__init__()
        self.name = name


class MockPose:
    def __init__(self):
        super().__init__()

        self.bones = []

    def add_bone(self, bone):
        self.bones.append(bone)


class MockArmature:
    def __init__(self):
        super().__init__()

        self.pose = MockPose()


def _create_mock_armature():
    mock_armature = MockArmature()

    return mock_armature


def test_bone_parsing():
    scene_armature = _create_mock_armature()
    scene_armature.pose.add_bone(MockBone('head'))
    scene_armature.pose.add_bone(MockBone('body'))
    scene_armature.pose.add_bone(MockBone('leftArm'))
    scene_armature.pose.add_bone(MockBone('helper:leftArm_ik'))

    armature_data = ArmatureData.parse_scene_armature(scene_armature)

    assert len(armature_data.bones_names), "There should only be 3 bone parsed"
    assert 'head' in armature_data.bones_names, "'head' should be a bone in armature"
    assert 'body' in armature_data.bones_names, "'body' should be a bone in armature"
    assert 'leftArm' in armature_data.bones_names, "'leftArm' should be a bone" \
                                                   " in armature"


def test_helper_bone_skipping():
    scene_armature = _create_mock_armature()
    scene_armature.pose.add_bone(MockBone('helper:bone'))

    armature_data = ArmatureData.parse_scene_armature(scene_armature)

    assert 'helper:bone' not in armature_data.bones_names, "Helper bones shouldn't" \
                                                           " be parsed"
