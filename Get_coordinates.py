from  geopy.geocoders import Nominatim


def country(country):
    countries =  (country[1] for country in country)
    return countries


def convert(countries):
    #grabs country data 
    globe_locator = Nominatim(user_agent="MusicMap")
    coordinates = []
    for country in countries:
        country_data = globe_locator.geocode(country)
        if country_data:
            country_lat,country_long = country_data.latitude, country_data.longitude
            coordinates.append((country_lat,country_long))

    return coordinates


#artist_coordinates = convert(countries)

def rel_frequency(coordinates):
    seen = {}
    Location_frequencies  = []

    #Count the total non repeated  locations
    for coordinate in coordinates:
        coordinate = tuple(coordinate)  # Convert the inner list to a tuple
        if coordinate in seen:
            
            seen[coordinate] += 1
        else:
            seen[coordinate] = 1
            

    total = sum(seen.values())  # Calculate the total sum of counts
    #calulates the relative frequency of the locations, creating a three column list.
    
    for key, value in seen.items():
        
        relative_frequency = value/ total # Divide each count by the total sum
        Location_frequencies.append([key[0], key[1], relative_frequency])
       

    return Location_frequencies
  

#location_frequencies = rel_frequency()

