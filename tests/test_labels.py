from game.labels import exits, imperative


def test_all_exits_have_a_label(exits_from_callback_specs, exits_from_room_data):
    for exit_key in exits_from_callback_specs | exits_from_room_data:
        assert exit_key in exits, f'No label found for {exit_key!r} exit key'


def test_all_actions_have_a_label(actions_from_object_data):
    for action_key in actions_from_object_data:
        assert action_key in imperative, f'No label found for {action_key!r} action key'
