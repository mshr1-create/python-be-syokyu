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
    session: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10,
):
    return item_crud.get_todo_items(session, todo_list_id, page, per_page)

@router.get("/{todo_item_id}")
def get_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    session: Session = Depends(get_db),
):
    return item_crud.get_todo_item(session, todo_list_id, todo_item_id)

@router.post("/", response_model=ResponseTodoItem)
async def post_todo_item(
    todo_list_id: int,
    data: NewTodoItem,
    session: Session = Depends(get_db),
):
    return item_crud.post_todo_item(session, todo_list_id, data)

@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
async def put_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    data: UpdateTodoItem,
    session: Session = Depends(get_db),
):
    return item_crud.update_todo_item(session, todo_list_id, todo_item_id, data)

@router.delete("/{todo_item_id}")
def delete_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    session: Session = Depends(get_db),
):
    return item_crud.delete_todo_item(session, todo_list_id, todo_item_id)