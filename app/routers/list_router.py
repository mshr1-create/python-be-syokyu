from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.crud import list_crud
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList

router = APIRouter(
    prefix="/lists",
    tags=["Todo List"],
)

@router.get("/")
def get_todo_lists(
    session: Session = Depends(get_db)
):
    return list_crud.get_todo_lists(session)

@router.get("/{todo_list_id}", response_model=ResponseTodoList)
async def get_todo_list(
    todo_list_id: int,
    session: Session = Depends(get_db),
):
    return list_crud.get_todo_list(todo_list_id, session)

@router.post("/", response_model=ResponseTodoList)
async def post_todo_list(
    data: NewTodoList,
    session: Session = Depends(get_db),
):
    return list_crud.post_todo_list(data, session)

@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(
    todo_list_id: int,
    data: UpdateTodoList,
    session: Session = Depends(get_db),
):
    return list_crud.put_todo_list(todo_list_id, data, session)

@router.delete("/{todo_list_id}")
async def delete_todo_list(
    todo_list_id: int,
    session: Session = Depends(get_db),
):
    return list_crud.delete_todo_list(todo_list_id, session)