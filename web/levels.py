from collections import OrderedDict

_LEVELS = [
    {
        "key": "0e91d682d",
        "name": "Level 1",
        "content": """

        .........
        .........
        ..@.2.@..
        ....^....
        ..*^^^*..
        ....^....
        ..@.*.@..
        .........
        .........

        """
    },
    {
        "key": "dd59137da",
        "name": "Level 2",
        "content": """

        2.@......
        ..*^.....
        @...@....
        .^*.*^...
        ..@...@..
        ...^*.*^.
        ....@...@
        .....^*..
        ......@..

        """
    }
]

LEVELS = []

for level in _LEVELS:
    LEVELS.append({
        'key': level['key'],
        'name': level['name'],
        'content': level['content'].strip().replace(" ", "").split("\n")
    })

def level_list():
    return LEVELS


def level_get(key):
    for level in LEVELS:
        if key == level['key']:
            return level

    return None
