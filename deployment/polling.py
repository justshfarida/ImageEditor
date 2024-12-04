import logging
import requests
import docker
import time
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DOCKER_HUB_REPO = "skibidi05/django"
STACK_NAME = "skibidi-stack"  # Swarm stack name
CHECK_INTERVAL = 60  # in seconds
COMPOSE_FILE_PATH = "./docker-compose.yml"  # Path to your docker-compose file

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

def update_stack(tag):
    """Update the stack with the new image tag."""
    client = docker.from_env()
    
    # Modify the docker-compose.yml file with the new tag dynamically
    try:
        logger.info(f"Pulling image: {DOCKER_HUB_REPO}:{tag}")
        client.images.pull(DOCKER_HUB_REPO, tag=tag)
        
        # Update the docker-compose.yml file with the new image tag
        update_compose_file(tag)

        # Deploy the updated stack
        logger.info(f"Deploying the stack {STACK_NAME} with the updated image {tag}")
        client.stacks.deploy(
            name=STACK_NAME,
            compose_file=open(COMPOSE_FILE_PATH, 'r').read(),
            compose_file_override=True  # Ensures it deploys the updated file
        )
        logger.info(f"Stack {STACK_NAME} updated successfully with the new image {tag}.")
    except docker.errors.APIError as e:
        logger.error(f"Error pulling image or deploying stack: {e}")
    except Exception as e:
        logger.error(f"Error during stack update: {e}")

def update_compose_file(tag):
    """Update the docker-compose.yml file with the new image tag."""
    try:
        # Read the existing docker-compose.yml
        with open(COMPOSE_FILE_PATH, 'r') as file:
            compose_content = file.read()
        
        # Replace the image tag in the docker-compose.yml content
        new_content = compose_content.replace(
            f"{DOCKER_HUB_REPO}:latest", f"{DOCKER_HUB_REPO}:{tag}"
        )

        # Write the updated content back to the docker-compose.yml
        with open(COMPOSE_FILE_PATH, 'w') as file:
            file.write(new_content)
        logger.info(f"Updated docker-compose.yml with tag {tag}.")
    except Exception as e:
        logger.error(f"Error updating docker-compose.yml: {e}")

def main():
    load_dotenv()

    last_tag = None
    while True:
        logger.info("Checking for updates...")
        latest_tag = get_latest_tag()
        if latest_tag and latest_tag != last_tag:
            logger.info(f"New image version detected: {latest_tag}")
            update_stack(latest_tag)
            last_tag = latest_tag
        else:
            logger.info("No updates found.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
