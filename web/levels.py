from collections import OrderedDict

LEVELS = [
    {
        "key": "0e91d682d",
        "name": "Level 1",
        "limits": [10, 7 ,5],
        "content": [
            ".........",
            ".........",
            "..@.2.@..",
            "....^....",
            "..*^^^*..",
            "....^....",
            "..@.*.@..",
            ".........",
            "........."
        ]
    },
    {
        "key": "dd59137da",
        "name": "Level 2",
        "limits": [10, 7 ,5],
        "content": [
            "2.@......",
            "..*^.....",
            "@...@....",
            ".^*.*^...",
            "..@...@..",
            "...^*.*^.",
            "....@...@",
            ".....^*..",
            "......@.."
        ]
    }
]


def level_list():
    return LEVELS


def level_get(key):
    for level in LEVELS:
        if key == level['key']:
            return level

    return None
