Issues:

On mac, ran into this error:

sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) SCRAM authentication requires libpq version 10 or above

fix was:

export DOCKER_DEFAULT_PLATFORM=linux/amd64, and re-build your images.