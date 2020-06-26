# Homework for a music app backend dev position

## Instructions
 Backend Test (Python, MongoDB)  
We would like you to build an API defining the routes listed below.  
This test should take roughly 1 or 2 hour.

Requirements:
 - Use python with Flask.
 - Use a MongoDB server for storing the data provided in the file "songs.json".
 - All routes should return a valid json dictionary.
 - Write tests for the API.
 - Follow the KISS principle.
 - Provide all instructions to do the setup, the easier it is for us to get it running the better. 
 - Please take into consideration that the number of songs and ratings will grow to millions of documents as well as the number of users using the API.

List of routes to implement:
- GET /songs
  - Returns a list of songs with some details on them
  - Add possibility to paginate songs.

- GET /songs/avg/difficulty
  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.

- GET /songs/search
  - Takes in parameter a 'message' string to search.
  - Return a list of songs. The search should take into account song's artist and title. The search should be case insensitive.

- POST /songs/rating
  - Takes in parameter a "song_id" and a "rating"
  - This call adds a rating to the song. Ratings should be between 1 and 5.

- GET /songs/avg/rating/<song_id>
  - Returns the average, the lowest and the highest rating of the given song id.

Bonus:
- Putting your work in a git repository is a plus (via github for example).


## Running the app
1. Install [Docker](https://docs.docker.com/get-docker/) if you don't have it already
1. Navigate to the `<project root>/music_app` on command line
1. Run `docker-compose up --detach`
1. Call http://localhost:5000/recreate_database to setup the database with the songs from the json file
1. Access the other endpoints at http://localhost:5000/songs etc.