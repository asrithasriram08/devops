# Exercise 4 - Docker Networking

This exercise places a Flask API, MySQL, and Redis on the same user-defined
bridge network. Docker's embedded DNS lets the containers reach one another by
the names `mysql` and `redis`.

## Run

```powershell
docker network create --driver bridge my-bridge-net
docker build -t flask-api .
docker run -d --name mysql --network my-bridge-net -e MYSQL_ROOT_PASSWORD=dev-only-password mysql:8
docker run -d --name redis --network my-bridge-net redis:7
docker run -d --name flask --network my-bridge-net -p 5001:5001 flask-api
curl http://localhost:5001/about
docker network inspect my-bridge-net
```

The password is a local lab value only; it must not be reused as a credential.
The Flask container can resolve the other containers by name:

```powershell
docker exec flask getent hosts mysql
docker exec flask getent hosts redis
```

## Clean up

```powershell
docker rm -f flask mysql redis
docker network rm my-bridge-net
```
