
# Backend Developer Assignment (Python, MongoDB)
We would like you to build an API with the functionality listed below.
 
This test should take a few hours. Please avoid spending an excessive amount of time on the assignment: we appreciate simple and understandable solutions.
If you run out of time then please submit a partial solution with brief comments about what you would do next.

We hope you are able to produce production-level code for this task.
 
Requirements:
 - Use Python 3 and the Flask library.
 - Use MongoDB as a datastore for the data provided in the file "songs.json".
 - All routes should return valid JSON.
 - Define a descriptive name for the route and declare the methods (GET, POST, etc.) it supports.
 - Write tests for the API.
 - Write a README with all instructions to set up the project.
 - Take into consideration that the number of songs and ratings will grow to millions of documents as well as the number of users using the API.
 
List of routes to implement:
- A
  - Returns a list of songs with the data provided by the "songs.json".
  - Add a way to paginate songs.
 
- B
  - Returns the average difficulty for all songs.
  - Takes an optional parameter "level" to filter for only songs from a specific level.
 
- C
  - Returns a list of songs matching the search string.
  - Takes a required parameter "message" containing the user's search string.
  - The search should take into account song's artist and title.
  - The search should be case insensitive.
 
- D
  - Adds a rating for the given song.
  - Takes required parameters "song_id" and "rating"
  - Ratings should be between 1 and 5 inclusive.
 
- E
  - Returns the average, the lowest and the highest rating of the given song id.
 
To simplify development you can run MongoDB in a Docker container using the following command:
 
docker run --detach --name songs_db --publish 127.0.0.1:27017:27017 mongo:4.4
 
And then connect to it at localhost:27017
 
Your assignment will be assessed with the following criteria (in order of importance):
1. How structured, simple and understandable is the code (quality)
2. How well the service/API will handle a large number of songs and ratings (scalability)
3. The coverage and quality of the automated tests
4. How easy it is for us to set up and run your project (including running tests)



## Running the app
1. [Install `Docker`](https://docs.docker.com/get-docker/) if you don't have it already.
1. [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it already.
1. Navigate to the `<repo root>/music_app` on command line.
1. Run `docker run --detach --name songs_db --publish 127.0.0.1:27017:27017 mongo:4.4`
1. Run `uv run start`
    - The command will tell you the the IP and port the API is published at.
1. Call `http://<IP>:<PORT>/recreate_database` to setup the database with the songs from the json file
    - e.g. http://127.0.0.1:5000/recreate_database
1. Access the other endpoints at `http://<IP>:<PORT>/songs` etc.

### Running tests
1. [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it already.
2. Run `uv run pytest`.