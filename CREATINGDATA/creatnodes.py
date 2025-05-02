from math import radians, cos, sin, asin, sqrt
from rawdata import communes
from itertools import combinations
import json
def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles
    return c * r
def find_symmetric_neighbor_tuples(communes):
    symmetric_tuples = []
    for tuple in combinations(communes.keys(), 3):
        # Check if all pairs are neighbors
        if all(communes[tuple[i]]['neighbors'].get(tuple[j]) and communes[tuple[j]]['neighbors'].get(tuple[i]) for i in range(3) for j in range(i+1, 3)):
            symmetric_tuples.append(tuple)
    return symmetric_tuples

def add_roundabouts_to_tuples(symmetric_tuples, communes):
    tuples_with_roundabouts = []
    for tuple in symmetric_tuples:
        # Calculate the average x (latitude) and y (longitude) coordinates separately
        avg_x = sum(communes[commune]['coordinates'][1] for commune in tuple) / len(tuple)
        avg_y = sum(communes[commune]['coordinates'][0] for commune in tuple) / len(tuple)

        # Create the roundabout name
        roundabout_name = "roundabout_" + '_'.join(tuple)

        # Initialize the roundabout neighbors dictionary
        roundabout_neighbors = {}

        # Calculate the distance from the roundabout to each neighboring commune
        for commune in tuple:
            distance = haversine(avg_y, avg_x, communes[commune]['coordinates'][0], communes[commune]['coordinates'][1])
            roundabout_neighbors[commune] = distance

        # Create the roundabout dictionary
        roundabout = {
            roundabout_name: {
                "coordinates": [avg_y, avg_x],
                "neighbors": roundabout_neighbors
            }
        }

        # Add the roundabout to the communes dictionary
        communes.update(roundabout)

        # Update the neighbors of the original elements to include the roundabout
        for commune in tuple:
            distance = haversine(communes[commune]['coordinates'][0], communes[commune]['coordinates'][1], avg_y, avg_x)
            communes[commune]['neighbors'][roundabout_name] = distance

        # Append the tuple with the roundabout to the list
        tuples_with_roundabouts.append(tuple + (roundabout_name,))

    # Write the updated communes dictionary to a JSON file
    with open('updated_communes.json', 'w') as file:
        json.dump(communes, file, indent=4)

    return tuples_with_roundabouts
sym=find_symmetric_neighbor_tuples(communes)
final=add_roundabouts_to_tuples(sym,communes)