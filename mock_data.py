MOCK_USERS = {
    1: {
        "id": 1,
        "firstName": "roei",
        "lastName": "cohen",
        "userName": "roei_cohen",
        "email": "roei_cohen@example.com",
    },
    2: {
        "id": 2,
        "firstName": "joe",
        "lastName": "shmoei",
        "userName": "joe_shmoe",
        "email": "joe_shmoe@example.com",
    }
}

MOCK_SONGS = {
    1: {
        "id": 1,
        "title": "Song One",
        "artist": "Artist One",
        "album": "Album A"
    },
    2: {
        "id": 2,
        "title": "Song Two",
        "artist": "Artist Two",
        "album": "Album B"
    },
    3: {
        "id": 3,
        "title": "Song Three",
        "artist": "Artist Three",
        "album": "Album C"
    }
}

MOCK_PLAYLISTS = {
    1: {
        "id": 1,
        "title": "My First Playlist",
        "privacy": "public",
        "description": "This is my first playlist with some awesome songs.",
        "author": 1,  # Roei
        "collaborators": [],
        "songs": [1, 2] 
    },
    2: {
        "id": 2,
        "title": "Chill Vibes",
        "privacy": "private",
        "description": "A playlist for relaxing moments with smooth tunes.",
        "author": 2,  # Joe
        "collaborators": [1],  # Roei
        "songs": [2, 3] 
    }
}
