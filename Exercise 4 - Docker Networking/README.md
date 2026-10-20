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
The Flask container can resolve the other containers by name and verify TCP
connectivity to the service ports:

```powershell
docker exec flask python -c "import socket; [(socket.create_connection((host, port), 5).close(), print(f'{host}:{port} reachable')) for host, port in [('mysql', 3306), ('redis', 6379)]]"
```

Expected output includes:

```text
mysql:3306 reachable
redis:6379 reachable
```

Run the checks after the MySQL container has finished initializing. A
successful connection verifies that the containers can communicate over the
user-defined bridge network; the Flask API itself does not use MySQL or Redis.

## Clean up

```powershell
docker rm -f flask mysql redis
docker network rm my-bridge-net
```
