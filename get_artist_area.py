from pandas import DataFrame
from musicbrainzngs import set_useragent, search_artists, browse_releases, get_artist_by_id

# Setup
set_useragent("MusicMap", "1.0")

def get_artist_id(artist_names):
    artist_id = []
    search_results = search_artists(artist_names) #Gathers the artists profile from the musixbrainz database
    artist_dataframe = DataFrame(search_results['artist-list']) #Stores the artist information into a dataframe


#Checks if the name of the artists from the 'artist_dataframe' matches with anything within the artist_names list, if does, add their IDs to the artist_data list
    for name in artist_names:
        id = artist_dataframe.loc[artist_dataframe['name'] == name, 'id'].tolist()  
        artist_id.extend(id)
    
    return artist_id

#In the unfiltered_dataframe, it gathers IDs from artist_id and assigns them to a column named 'id'. Maps each IDs with a true or false statement, depending if the artists released more than 15 songs
def filter_ID(unfiltered_id):
    unfiltered_dataframe = DataFrame({'id': unfiltered_id})
    filtered_dataframe = unfiltered_dataframe[unfiltered_dataframe['id'].map(lambda id: browse_releases(id)['release-count']) > 10]
    filtered_id = set(filtered_dataframe['id'])

    return filtered_id



def area_name(filtered_id):
    Location_data = []

    for id in filtered_id:
        try:
            artist_general_data = get_artist_by_id(id)
            if len(artist_general_data['artist']) > 0:
                if 'area' in artist_general_data['artist'] or 'begin-area' in artist_general_data['artist']:
                    artist_area = artist_general_data['artist']['area']['name']
                    artist_name = artist_general_data['artist']['name']
                    Location_data.append([artist_name, artist_area])
        except Exception as e:
            print(f"Error processing ID {id}")

    return Location_data