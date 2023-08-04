Issues:

On mac, ran into this error:

sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) SCRAM authentication requires libpq version 10 or above

fix was:

export DOCKER_DEFAULT_PLATFORM=linux/amd64, and re-build your images.

https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentication-problem


To stop docker run:

Open a new shell and execute

$ docker ps # get the id of the running container
$ docker stop <containerid> # kill it (gracefully)

Imported into a Gitlab project.