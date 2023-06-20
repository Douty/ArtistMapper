from flask import Flask, session, request, redirect, render_template, jsonify
from flask_session import Session
from dotenv import load_dotenv
from os import getenv, urandom
from User_Spotify_data import get_artist_name
from get_artist_area import get_artist_id,filter_ID,area_name
from Get_coordinates import country,convert,rel_frequency
from folium.plugins import HeatMap
from pandas import DataFrame
from waitress import serve
import numpy as np
import folium
import spotipy



def create_app():
    load_dotenv()
    client_ID=getenv("SPOTIPY_CLIENT_ID")
    api_key=getenv("SPOTIPY_CLIENT_SECRET")
    redirect_link=getenv("SPOTIPY_REDIRECT_URI")

    app = Flask(__name__)

    #load the various tokens
    app.config['SECRET_KEY'] = urandom(64)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    Session(app)


    scope="user-top-read"

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    spotify_authentication = spotipy.oauth2.SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True)
    spotify = spotipy.Spotify(auth_manager=spotify_authentication)




    def artist_coordinates():
        artist_names = get_artist_name(spotify)  #Gathers the artists names from spotify 
        unfiltered_id = get_artist_id(artist_names) #Store all the artists unfiltered_IDs
        filtered_id = filter_ID(unfiltered_id) #fliters the unwanted artists to the 'filtered_id' varable
        area_names = area_name(filtered_id) # Gets the artists starting 'area' name
        countries = country(area_names)
        coordinates = convert(countries)
        relative_frequency = rel_frequency(coordinates)
        
        return area_names,relative_frequency

    def create_map():

        user_data, relative_frequency = artist_coordinates()

        user_data = DataFrame(data=user_data, columns=["Name", "Location"])
        html_user_data = user_data.to_html()

        country_map = folium.Map(height="100%", width="100%", max_bounds=True, zoom_start=7, min_zoom=3, max_zoom=4,tiles='Mapbox')
        HeatMap(relative_frequency, gradient={0.3: 'green', 0.6: 'yellow', 1: 'red'}, radius=50, min_opacity=0.4).add_to(
            country_map)

        html_country_map = country_map._repr_html_()

        return html_user_data, html_country_map
        

    @app.route("/map")
    def main():
        user_data, country_map = create_map()
        return render_template("map.html", table_data=user_data, map=country_map)



    @app.route('/')
    def index():
        if request.args.get("code"):
            spotify_authentication.get_access_token(request.args.get("code"))
            return redirect('map')
        #redirect the user back to the main page. 

        '''if not spotify_authentication.validate_token(cache_handler.get_cached_token()):
            auth = spotify_authentication.get_authorize_url()
            sign_in_link = f'<a href="{auth}">Connect your Spotify</a>'
            return render_template("index.html",sign_in_link=sign_in_link)'''
        
        auth = spotify_authentication.get_authorize_url()
        sign_in_link = f'<a href="{auth}">Connect your Spotify</a>'
        return render_template("index.html",sign_in_link=sign_in_link)
            

    if __name__ == '__main__':
        serve(app, host='0.0.0.0',port=8080,threads=2)
    
    return app