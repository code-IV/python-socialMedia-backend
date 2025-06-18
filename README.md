# Social Networking App Backend

This service provides basic functionality for a social networking application.
As a user you can:
- signup and login
- create, edit, delete and view posts
- like or dislike other users’ posts but not my own, and also edit or remove your reaction

## Documentation

API documentation created automatically by the FastAPI is available in Swagger format at http://localhost:8000/docs (or the host you are running the app on).


## Deployment

For running the application you must have [git](https://git-scm.com/downloads) and [python 3.10](https://www.python.org/downloads/release/python-31011/) installed.

Clone the repository to the host folder with command:

```
git clone https://github.com/ILapshin/csv-web-service.git
```
Or copy source code and unpack the archive to the destination folder.


### Running Directly Via Uvicorn

1. Navigate to repository root folder. Create and activate python virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install requirements:

```
pip3 install -r requirements.txt
```

3. Create ```.env``` file with environment variables:

URL for connetion to a database. Originally the app is developed using SQLite, you can use it like ```DB_URL=sqlite:///./sqlite.db```.
```
DB_URL=URL_TO_YOUR_DB
```
Secret key for creating access tokens.
```
SECRET_KEY=YOUR_SECRET_KEY
```
4. Run server with command 

```
uvicorn src.main:app 
```

Application will be running on http://localhost:8000. 

Saved CSV files and SQLite database will be stored in ```./uploads``` directory

### Running With Docker

To run the app in the container you must have [Docker to be installed](https://docs.docker.com/engine/install/).

1. Create docker image:

```
docker build -t social-network-app .
```

2. Create docker volume for storing permanent data:
```
docker volume create app-storage
```

3. Run docker container:
```
docker run -p 8000:8000 -v app-storage:/code -e "DB_URL=[URL_TO_UOUR_DB]" -e "SECRET_KEY=[YOUR_SECRET_KEY]" social-network-app 
```


## Testing

All api endpoint are covered by unit tests via pytest.