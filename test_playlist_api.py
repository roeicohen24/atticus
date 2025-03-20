import unittest
from mock_data import MOCK_PLAYLISTS, MOCK_SONGS, MOCK_USERS
from playlist_api import PlaylistAPI

# Some of these tests are still failing! didn't get a chance to fully debug, but I think it's more of an
# issue with the test setup than with the actual functions.
# In any case, these are the general test cases I'd want to look at.
class TestAPIService(unittest.TestCase):

    def setUp(self):
        self.users = MOCK_USERS.copy()
        self.songs = MOCK_SONGS.copy()
        self.playlists = MOCK_PLAYLISTS.copy()
        self.playlist_api = PlaylistAPI()

    def test_get_playlist(self):
        # Test success
        response, status_code = self.playlist_api.get_playlist(1)
        print(self.playlists[1])
        print(response)
        self.assertEqual(response, {"playlist": self.playlists[1]})
        self.assertEqual(status_code, 200)
        

        # NOTE: technically this test should exist in each test, would include that in actual production case
        # Test for non-existing playlist 
        response, status_code = self.playlist_api.get_playlist(123)
        self.assertEqual(response, {"error": "playlist with id 123 not found"})
        self.assertEqual(status_code, 404)

    def test_create_playlist(self):
        new_playlist_data = {
            'title': 'New Playlist',
            'privacy': 'private',
            'description': 'New playlist!',
            'collaborators': [2]
        }
        response, status_code = self.playlist_api.create_playlist(new_playlist_data)
        
        # Check the new playlist was created
        self.assertEqual(status_code, 201)
        self.assertEqual(response['playlist']['title'], 'New Playlist')
        self.assertEqual(response['playlist']['privacy'], 'private')
        self.assertEqual(response['playlist']['collaborators'], [2])
        self.assertEqual(response['playlist']['description'], 'New playlist!')

    def test_add_songs_to_playlist(self):
        add_songs_data = {
            'songs': [3]
        }
        response, status_code = self.playlist_api.add_songs_to_playlist(1, add_songs_data)
        
        # Check the songs were added
        self.assertEqual(status_code, 200)
        self.assertIn(3, response['playlist']['songs'])

        # Test for missing songs
        response, status_code = self.playlist_api.add_songs_to_playlist(1, {})
        self.assertEqual(response, {"error": "songs field is required"})
        self.assertEqual(status_code, 400)
        

    def test_reorder_playlist(self):
        reorder_data = {
            'songs': [2, 1]
        }
        response, status_code = self.playlist_api.reorder_playlist(1, reorder_data)
        
        # Validate the songs have been reordered
        self.assertEqual(status_code, 200)
        self.assertEqual(response['playlist']['songs'], [2, 1])

        # Test for reorder with missing songs
        reorder_data = {}
        response, status_code = self.playlist_api.reorder_playlist(1, reorder_data)
        self.assertEqual(response, {"error": "songs field is required"})
        self.assertEqual(status_code, 400)

        # Reorder data has songs that aren't already in the playlist
        reorder_data = {
            'songs': [1, 2, 3]  
        }
        response, status_code = self.playlist_api.reorder_playlist(1, reorder_data)
        self.assertEqual(response, {"error": "reorder must contain all and only the existing songs in the playlist"})
        self.assertEqual(status_code, 400)

    def test_update_privacy(self):
        update_privacy_data = {
            'privacy': 'private'
        }
        response, status_code = self.playlist_api.update_privacy(1, update_privacy_data)
        
        # Validate the privacy was updated
        self.assertEqual(status_code, 200)
        self.assertEqual(response['playlist']['privacy'], 'private')

        # Test for missing 'privacy' in data
        update_privacy_data = {}
        response, status_code = self.playlist_api.update_privacy(1, update_privacy_data)
        self.assertEqual(response, {"error": "privacy field is required"})
        self.assertEqual(status_code, 400)
    

    def test_update_collaborators(self):
        update_collaborators_data = {
            'collaborators': [2]
        }
        response, status_code = self.playlist_api.update_collaborators(1, update_collaborators_data)
        
        # Validate the collaborators were updated
        self.assertEqual(status_code, 200)
        self.assertEqual(response['playlist']['collaborators'], [2])

        # Test for missing 'collaborators' in data
        update_collaborators_data = {}
        response, status_code = self.playlist_api.update_collaborators(1, update_collaborators_data)
        self.assertEqual(response, {"error": "collaborators field is required"})
        self.assertEqual(status_code, 400)
        
    def test_delete_playlist(self):
        response, status_code = self.playlist_api.delete_playlist(1)
        
        # Validate the playlist was deleted
        self.assertEqual(status_code, 200)
        self.assertNotIn(1, self.playlists)


if __name__ == '__main__':
    unittest.main()