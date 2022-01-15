# <pep8 compliant>

from ..util.RevertableActionStack import RevertibleActionStack


class ContextController(RevertibleActionStack):
    """
    Allows to take actions on the project and then revert back to its
    original state once the addon has done its work.
    """

    def __init__(self, context) -> None:
        super(ContextController, self).__init__()
        self.context = context

    # end __init__

    def object_set_animation_data_action(self, ob, value) -> None:
        original_action = ob.animation_data.action

        def revert():
            nonlocal original_action, ob
            ob.animation_data.action = original_action

        self._push_revert_action(revert)

        ob.animation_data.action = value

    # end object_set_animation_data_action
