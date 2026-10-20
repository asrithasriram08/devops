import docker


client = docker.from_env()
container = client.containers.run(
    "flask-apparmor",
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True,
)

try:
    info = client.api.inspect_container(container.id)
    security_options = info["HostConfig"].get("SecurityOpt") or []
    if "apparmor=my-apparmor-profile" not in security_options:
        raise SystemExit("The requested AppArmor profile was not applied")

    exit_code, output = container.exec_run("cat /etc/shadow")
    decoded_output = output.decode(errors="replace")
    print(f"Attempt to read /etc/shadow: exit={exit_code}, output={decoded_output}")
    if exit_code == 0:
        raise SystemExit("AppArmor did not deny access to /etc/shadow")
    if not any(
        message in decoded_output.lower()
        for message in ("permission denied", "operation not permitted")
    ):
        raise SystemExit("The file-access test failed without an access-denied error")

    exit_code, output = container.exec_run("/bin/sh -c 'echo restricted'")
    decoded_output = output.decode(errors="replace")
    print(f"Attempt to execute /bin/sh: exit={exit_code}, output={decoded_output}")
    if exit_code == 0:
        raise SystemExit("AppArmor did not deny execution of /bin/sh")
    if not any(
        message in decoded_output.lower()
        for message in ("permission denied", "operation not permitted")
    ):
        raise SystemExit(
            "The command-execution test failed without an access-denied error"
        )
    print("AppArmor file-access and command-execution denials verified")
finally:
    container.remove(force=True)
