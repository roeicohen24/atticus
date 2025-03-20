from mock_data import MOCK_PLAYLISTS, MOCK_SONGS, MOCK_USERS

class PlaylistAPI:
    AUTHENTICATED_USER=1 # simulates authenticated user that we would get from the request
    
    def get_playlist(self, playlist_id):
        """
        Simulates the "GET /api/playlists/[playlist_id]" endpoint.

        Takes an id and returns the object.
        """
    
        playlist = MOCK_PLAYLISTS.get(playlist_id)       
        # Django ORM: Playlist.objects.get(id=id)
        # SQL: SELECT * FROM playlist WHERE id=id

        if not playlist:
            return {"error": f"playlist with id {playlist_id} not found"}, 404
        
        return {"playlist": playlist}, 200
    
    def create_playlist(self, data):
        """
        Simulates the "POST /api/playlists" endpoint. 

        Creates a new playlist given the provided data.
        """
        new_playlist_id = max(MOCK_PLAYLISTS.keys()) + 1 
        new_playlist = {
            "id": new_playlist_id,
            "title": data.get('title', 'New Playlist'),
            "privacy": data.get('privacy', 'private'),
            "description": data.get('description'),
            "author": PlaylistAPI.AUTHENTICATED_USER,
            "collaborators": data.get('collaborators'),
            "songs": []
        }

        # Django ORM: Playlist.objects.create(data)
        # INSERT INTO playlist (title, privacy, description, author, collaborators, songs)
        # VALUES ('New Playlist', 'private', NULL, 'AuthenticatedUser', NULL, ARRAY[1, 2, 3]);
        MOCK_PLAYLISTS[new_playlist_id] = new_playlist
        return {"playlist": new_playlist}, 201
    
    def add_songs_to_playlist(self, playlist_id, data):
        """
        Simulates the "PUT /api/playlists/[playlist_id]" endpoint.

        Adds songs to the playlist.
        """
        playlist = MOCK_PLAYLISTS.get(playlist_id)

        if not playlist:
            return {"error": f"playlist with id {playlist_id} not found"}, 404
        
        # Django ORM: Playlist.objects.get(id=id), playlist.songs = data['songs'], playlist.save()
        # SQL similar to above
        if 'songs' not in data:
            return {"error": "songs field is required"}, 400
        
        playlist['songs'].extend(data['songs'])

        return {"playlist": playlist}, 200
    
    def reorder_playlist(self, playlist_id, data):
        """
        Simulates the "PUT /api/playlists/[playlist_id]/reorder" endpoint.

        Reorders the songs in a playlist.
        """
        playlist = MOCK_PLAYLISTS.get(playlist_id)

        if not playlist:
            return {"error": f"playlist with id {playlist_id} not found"}, 404
        
        if 'songs' not in data:
            return {"error": "songs field is required"}, 400
        
        if set(data['songs'] != set(playlist['songs'])):
            return {"error": "reorder must contain all and only the existing songs in the playlist"}, 400
        # Django ORM + SQL similar to above PUT endpoint

        playlist['songs'] = data['songs']
        return {"playlist": playlist}, 200
    
    def update_privacy(self, playlist_id, data):
        """
        Simulates the "PUT /api/playlists/[playlist_id]/privacy"
        
        Updates the privacy setting of a playlist.
        """
        playlist = MOCK_PLAYLISTS.get(playlist_id)
        if not playlist:
            return {"error": f"playlist with id {playlist_id} not found"}, 404
        
        if 'privacy' not in data:
            return {"error": "privacy field is required"}, 400
        # Django ORM + SQL similar to above PUT endpoint
        playlist['privacy'] = data['privacy']
        return {"playlist": playlist}, 200
    
    def update_collaborators(self, playlist_id, data):
        """
        Simulates the "PUT /api/playlists/[playlist_id]/collaborators"

        Updates the collaborators of a playlist.
        """
        playlist = MOCK_PLAYLISTS.get(playlist_id)
        if not playlist:
            return {"error": f"playlist with id {playlist_id} not found"}, 404
        
        #Note that the author also shouldn't be in the collaborators, and no duplicates
        if 'collaborators' not in data: 
            return {"error": "collaborators field is required"}, 400
        # Django ORM + SQL similar to above PUT endpoint

        playlist['collaborators'] = data['collaborators']
        return {"playlist": playlist}, 200

    def delete_playlist(self, playlist_id):
        """
        DELETE /api/playlists/[playlist_id]
        Deletes a playlist.
        """
        playlist = MOCK_PLAYLISTS.get(playlist_id)
        if not playlist:
            return {"error": f"playlist with id {playlist_id} not found"}, 404
        
        #django ORM: get playlist then playlist.delete
        # SQL: DELETE FROM playlist WHERE id = id;
        
        del MOCK_PLAYLISTS[playlist_id]
        return {"playlist": playlist}, 200
 