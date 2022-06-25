def fix_docker_hostname(hostname: str) -> str:
    """
    Make a localhost available on host from docker container
    Adapted from https://forums.docker.com/t/how-to-reach-localhost-on-host-from-docker-container/113321
    """
    if hostname == "localhost":
        return "host.docker.internal"  # TODO: test this on Linux
    return hostname
