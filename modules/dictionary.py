Database = {
    'endpoints': [
        ["name", "VARCHAR(255)"],
        ["url", "TEXT"]
    ],
    'user_games': [
        ["appid", "INTEGER"],
        ["name", "VARCHAR(255)"],
        ["playtime_forever", "INTEGER"],
        ["img_icon_url", "VARCHAR(255)"],
        ["has_community_visible_stats", "BOOLEAN"],
        ["playtime_windows_forever", "INTEGER"],
        ["playtime_mac_forever", "INTEGER"],
        ["playtime_linux_forever", "INTEGER"],
        ["playtime_deck_forever", "INTEGER"],
        ["rtime_last_played", "INTEGER"],
        ["capsule_filename", "VARCHAR(255)"],
        ["has_workshop", "BOOLEAN"],
        ["has_market", "BOOLEAN"],
        ["has_dlc", "BOOLEAN"],
        ["playtime_disconnected", "INTEGER"]
    ]
}

Endpoints = {
    'get_user_games': [
        'appid',
        'name',
        'playtime_forever',
        'img_icon_url',
        'has_community_visible_stats',
        'playtime_windows_forever',
        'playtime_mac_forever',
        'playtime_linux_forever',
        'playtime_deck_forever',
        'rtime_last_played',
        'capsule_filename',
        'has_workshop',
        'has_market',
        'has_dlc',
        'playtime_disconnected'
    ]
}