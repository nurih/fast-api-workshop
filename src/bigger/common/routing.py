import os
from fastapi import APIRouter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_router_by_folder(module_path: str) -> APIRouter:
    '''
    Returns an API Router constructed from the path of the module.

        Parameters:
            module_path (str): The file path of the module consuming this router.

        Returns: 
            router (APIRouter): A router with folder name as the tag (Capitalized), 
            and the route prefix. 
    '''
    folder_name = os.path.basename(os.path.dirname(module_path))
    tag = folder_name.capitalize()

    logger.info(f'... Created route with prefix "/{folder_name}" tagged "{tag}".')

    return APIRouter(
        prefix=f"/{folder_name}",
        tags=[tag]
    )
