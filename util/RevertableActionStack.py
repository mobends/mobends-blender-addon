# <pep8 compliant>

class RevertibleActionHandle:
    def __init__(self, stack) -> None:
        self.stack = stack

    # end __init__

    def __enter__(self):
        print('Entered RevertableActionHandle!')

    # end __enter__

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exiting RevertableActionHandle!')

        self.stack.restore()

    # end __exit__


class RevertibleActionStack:
    """
    Allows to take actions and then revert back to an
    original state.
    """

    def __init__(self) -> None:
        self.stack = []

    # end __init__

    def save(self) -> RevertibleActionHandle:
        self.stack.append([])

        return RevertibleActionHandle(self)

    # end save

    def restore(self):
        revert_actions = self.stack.pop()

        if revert_actions is None:
            raise RuntimeError("The amount of 'restores' has to"
                               "match the amount of 'saves'")

        for action in reversed(revert_actions):
            print(action)
            action()

    # end restore

    def _push_revert_action(self, action):
        self.stack[-1].append(action)

    # end _push_revert_action
