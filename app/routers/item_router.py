from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.crud import item_crud
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem, ResponseTodoItem

router = APIRouter(
    prefix="/lists/{todo_list_id}/items",
    tags=["Todo Items"],
)

@router.get("/")

def get_todo_items(
    todo_list_id: int,
    session: Session = Depends(get_db)
):
    return item_crud.get_todo_items(session, todo_list_id)

@router.get("/{todo_item_id}")
def get_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    session: Session = Depends(get_db),
):
    return item_crud.get_todo_item(todo_list_id, todo_item_id, session)

@router.post("/", response_model=ResponseTodoItem)
async def post_todo_item(
    todo_list_id: int,
    data: NewTodoItem,
    session: Session = Depends(get_db),
):
    return item_crud.post_todo_item(todo_list_id, data, session)

@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
async def put_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    data: UpdateTodoItem,
    session: Session = Depends(get_db),
):
    return item_crud.put_todo_item(todo_list_id, todo_item_id, data, session)

@router.delete("/{todo_item_id}")
async def delete_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    session: Session = Depends(get_db),
):
    return item_crud.delete_todo_item(todo_list_id, todo_item_id, session)