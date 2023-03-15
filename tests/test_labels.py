from games import game_data


def test_all_exits_have_a_label(exits_from_callback_specs, exits_from_room_data):
    for exit_key in exits_from_callback_specs | exits_from_room_data:
        assert exit_key in game_data.exit_labels, \
            f'No label found for {exit_key!r} exit key'
