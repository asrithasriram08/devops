import docker


client = docker.from_env()
container = client.containers.run(
    "flask-apparmor",
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True,
)

try:
    exit_code, output = container.exec_run("cat /etc/shadow")
    print(f"Attempt to read /etc/shadow: exit={exit_code}, output={output.decode()}")
finally:
    container.remove(force=True)
