"""
run.py

Script to inject all the sensitive info needed to connect and run the bot, then run it.
Before executing, ensure that values for all properties in config.json have been provided.
"""

import json
import os
import random
import string
import subprocess
import sys


def main():
    run_target = handle_client_server_arg()

    if run_target is None:
        print(
            "Usage: python3 run.py run_target, where run_target = 'client' or 'server'"
        )
        return

    user_config = handle_user_config(run_target)

    if user_config is None:
        print(
            "config.json must exist in main directory (same as this script), and must be fully specified. See README.md"
        )
        return

    if run_target == "client":
        # Ensure server running first
        serverCheck = subprocess.run(
            ["docker", "container", "ls"], capture_output=True, text=True
        )

        if serverCheck.stdout.find(f"{user_config['label']}-server") == -1:
            print("Server must be running first")
            return

        run_client(user_config)
    else:
        kill_client_if_running(user_config)
        run_server(user_config)


def handle_client_server_arg():
    if len(sys.argv) < 2:
        return None

    run_target = sys.argv[1].lower()

    if run_target not in ["client", "server"]:
        return None

    return run_target


def handle_user_config(run_target):
    try:
        user_config = json.loads(get_file_contents("config.json"))

        # Validate config contents
        if user_config["label"] == "" or not user_config["label"].isalnum():
            return None

        if not int(user_config["clientPort"]):
            return None

        if (
            user_config["discord"]["serverID"] == ""
            or user_config["discord"]["botToken"] == ""
        ):
            return None

        if (
            user_config["spotify"]["clientID"] == ""
            or user_config["spotify"]["clientSecret"] == ""
        ):
            return None

        password = handle_password(run_target)

        if password == "":
            return None

        user_config["password"] = password

        return user_config
    except (FileNotFoundError, KeyError, ValueError):
        return None


def handle_password(run_target):
    password = ""

    # If server, generate new password
    if run_target == "server":
        alphanumerics = list(
            string.ascii_lowercase + string.ascii_uppercase + string.digits
        )

        for _ in range(15):
            password += alphanumerics[random.randint(0, len(alphanumerics) - 1)]

    # If client, extract password from running server
    else:
        server_config = get_file_contents_as_lines("Server/application.yml")

        for line in server_config:
            if "password: " in line:
                password = line.replace("password: ", "").replace('"', "").strip()
                break

    return password


def run_client(user_config):
    write_file_contents("Client/config.json", user_config, is_json=True)

    # Change current working directory to client
    os.chdir("./Client")

    instance_label = "INSTANCE_LABEL"
    client_port = "CLIENT_PORT"

    dockerComposeRaw = get_file_contents("docker-compose.template.yaml")

    dockerComposeUpdated = dockerComposeRaw.replace(
        instance_label, user_config["label"]
    ).replace(client_port, user_config["clientPort"])

    write_file_contents("docker-compose.yaml", dockerComposeUpdated)

    print("docker-compose.yaml has been created / overwritten...")

    print("Building and running WidenBot client...")

    # Run container
    subprocess.run(["docker", "compose", "up", "--build", "--force-recreate"])


def run_server(user_config):
    # Change current working directory to server
    os.chdir("./Server")

    # Create application.yml and docker-compose.yaml with injected secrets from config
    lavalink_password = "LAVALINK_PASSWORD"
    spotify_client_id = "SPOTIFY_CLIENTID"
    spotify_client_secret = "SPOTIFY_CLIENTSECRET"
    instance_label = "INSTANCE_LABEL"

    lavalinkConfigRaw = get_file_contents("application.template.yml")

    lavalinkConfigUpdated = (
        lavalinkConfigRaw.replace(lavalink_password, user_config["password"])
        .replace(spotify_client_id, user_config["spotify"]["clientID"])
        .replace(spotify_client_secret, user_config["spotify"]["clientSecret"])
    )

    write_file_contents("application.yml", lavalinkConfigUpdated)

    print("application.yml has been created / overwritten...")

    dockerComposeRaw = get_file_contents("docker-compose.template.yaml")

    dockerComposeUpdated = dockerComposeRaw.replace(
        lavalink_password, user_config["password"]
    ).replace(instance_label, user_config["label"])

    write_file_contents("docker-compose.yaml", dockerComposeUpdated)

    print("docker-compose.yaml has been created / overwritten...")

    # Run container
    subprocess.run(["docker", "compose", "up", "--build", "--force-recreate"])


def kill_client_if_running(user_config):
    # Check for client
    serverCheck = subprocess.run(
        ["docker", "container", "ls"], capture_output=True, text=True
    )

    if serverCheck.stdout.find(f"{user_config['label']}-client") == -1:
        return

    print("Killing currently running client...")

    subprocess.run(
        ["docker", "container", "kill", f"{user_config['label']}-client"],
        capture_output=True,
    )

    print("Old client has been killed...")


def get_file_contents(path):
    with open(path, "r") as f:
        raw = f.read()
        return raw


def get_file_contents_as_lines(path):
    with open(path, "r") as f:
        raw = f.readlines()
        return raw


def write_file_contents(path, contents, is_json=False):
    with open(path, "w") as f:
        if is_json:
            json.dump(contents, f)
        else:
            f.write(contents)


if __name__ == "__main__":
    main()
