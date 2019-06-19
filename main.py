import spotipy
import spotipy.util as util
import yaml
import sys

def read_songs_file():
	song_list = []
	with open("songs.txt") as f:
		songs = f.readlines()
		for song in songs:
			songArray = song.split('-')
			songName = songArray[1][1:] + "-" + songArray[2].replace("\n", "")
			song_list.append(songName)
	return song_list

def load_config():
	stream = open('config.yaml')
	return yaml.load(stream)


def auth_token(user_config):
	token = util.prompt_for_user_token(
		user_config['username'], 
		scope='playlist-modify-private,playlist-modify-public',
		client_id=user_config['client_id'], 
		client_secret=user_config['client_secret'], 
		redirect_uri=user_config['redirect_uri']
	)
	if token:
		return spotipy.Spotify(auth=token)


def search_track(sp, song_list):
	all_track_ids = []
	unavailable_track_ids = []
	for song in song_list:
		results = sp.search(q=song, type='track')
		try:
			track_id = results['tracks']['items'][0]['id']
			all_track_ids.append(track_id)
		except:
			# print("Can't find song:", song)
			unavailable_track_ids.append(song)

	return all_track_ids, unavailable_track_ids

def add_track_to_playlist(user_config, sp, all_track_ids):
	sp.user_playlist_add_tracks(
		user=user_config['username'], playlist_id=user_config['playlist_id'], tracks=all_track_ids)


def write_unavailable_songs(unavailable_track_ids):
	with open("unavailable_songs.txt", 'w') as f:
		for tracks in unavailable_track_ids:
			f.writelines(tracks + "\n")

def main():
	song_list = read_songs_file()

	user_config = load_config()
	sp = auth_token(user_config)
	all_track_ids, unavailable_track_ids = search_track(sp, song_list)
	add_track_to_playlist(user_config, sp, all_track_ids)
	write_unavailable_songs(unavailable_track_ids)

if __name__ == "__main__":
  main()

