import logging
import requests
import docker
import time
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DOCKER_HUB_REPO = "dzinski/django"
CONTAINER_NAME = "django-app"
CHECK_INTERVAL = 60  # in seconds

current_directory = os.path.dirname(os.path.abspath(__file__))
env_file_path = os.path.join(current_directory, '.env')
volume = {
    env_file_path: {"bind": "/app/.env", "mode": "ro"}
}

def get_latest_tag():
    """Fetch the latest tag of the Docker image from Docker Hub."""
    url = f"https://hub.docker.com/v2/repositories/{DOCKER_HUB_REPO}/tags/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        tags = response.json()["results"]
        latest_tag = sorted(tags, key=lambda t: t["last_updated"], reverse=True)[0]["name"]
        return latest_tag
    except Exception as e:
        logger.error(f"Error fetching tags from Docker Hub: {e}")
        return None

def pull_and_run_image(tag, env_vars):
    """Pull the image with the specified tag and run it."""
    client = docker.from_env()
    image = f"{DOCKER_HUB_REPO}:{tag}"
    try:
        logger.info(f"Pulling image: {image}")
        client.images.pull(DOCKER_HUB_REPO, tag=tag)
        
        # Stop and remove the running container (if exists)
        try:
            container = client.containers.get(CONTAINER_NAME)
            logger.info(f"Stopping and removing container: {CONTAINER_NAME}")
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            logger.info(f"No existing container with name {CONTAINER_NAME} found.")
        
        # Run the new container
        logger.info(f"Running new container: {CONTAINER_NAME}")
        client.containers.run(image, name=CONTAINER_NAME, detach=True, ports={"80": 3000}, environment=env_vars, volumes=volume)
        logger.info(f"Container {CONTAINER_NAME} is now running.")
    except Exception as e:
        logger.error(f"Error pulling or running the image: {e}")

def main():
    load_dotenv()

    env_vars = {key: os.getenv(key) for key in os.environ.keys() if os.getenv(key)}

    last_tag = None
    while True:
        logger.info("Checking for updates...")
        latest_tag = get_latest_tag()
        if latest_tag and latest_tag != last_tag:
            logger.info(f"New image version detected: {latest_tag}")
            pull_and_run_image(latest_tag, env_vars)
            last_tag = latest_tag
        else:
            logger.info("No updates found.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()