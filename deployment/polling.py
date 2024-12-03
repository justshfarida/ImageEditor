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
SERVICE_NAME = "skibidi"  # Swarm service name
CHECK_INTERVAL = 60  # in seconds

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

def update_swarm_service(tag):
    """Update the Swarm service with the new image tag."""
    client = docker.from_env()
    image = f"{DOCKER_HUB_REPO}:{tag}"
    try:
        logger.info(f"Pulling image: {image}")
        client.images.pull(DOCKER_HUB_REPO, tag=tag)

        # Update the service to use the new image
        logger.info(f"Updating Swarm service {SERVICE_NAME} to use image {image}")
        service = client.services.get(SERVICE_NAME)
        service.update(image=image)
        logger.info(f"Service {SERVICE_NAME} updated successfully to image {image}.")
    except docker.errors.NotFound:
        logger.error(f"Service {SERVICE_NAME} not found. Ensure the service exists in the Swarm.")
    except Exception as e:
        logger.error(f"Error updating the service: {e}")

def main():
    load_dotenv()

    last_tag = None
    while True:
        logger.info("Checking for updates...")
        latest_tag = get_latest_tag()
        if latest_tag and latest_tag != last_tag:
            logger.info(f"New image version detected: {latest_tag}")
            update_swarm_service(latest_tag)
            last_tag = latest_tag
        else:
            logger.info("No updates found.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()