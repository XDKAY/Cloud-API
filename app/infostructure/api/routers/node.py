from typing import List, Optional

from fastapi import APIRouter, status, Query

from app.core.schemes.node import NodeCreateScheme
from app.infostructure.dependencies.current_user import CurrentUserDep
from app.infostructure.dependencies.services import NodeServiceDep
from app.infostructure.db.mongo.models.node import Node


router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get("/")
async def get_nodes(current_user: CurrentUserDep, node_service: NodeServiceDep, parent_id: Optional[str] = Query(default=None)) -> List[Node]:
    list_nodes = await node_service.get_nodes(user_id=current_user.id, parent_id=parent_id)
    return list_nodes


@router.post("/", response_model=Node, status_code=status.HTTP_201_CREATED)
async def create_dir(
    current_user: CurrentUserDep, 
    node_scheme: NodeCreateScheme, 
    node_service: NodeServiceDep,
    ):

    node_model = await node_service.create_node(user_id=current_user.id, node_scheme=node_scheme)

    return node_model


@router.delete("/{node_id}")
async def delete_node(node_id: str, current_user: CurrentUserDep, node_service: NodeServiceDep):
    await node_service.delete_node(user_id=current_user.id, node_id=node_id)

    return {"message": f"The node with the id {node_id} was successfully deleted"}