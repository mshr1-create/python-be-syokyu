from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

from app.crud import list_crud
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList

router = APIRouter(
    prefix="/lists",
    tags=["Todo List"],
)

# GET /listsのエンドポイントを実装しているパスオペレーション関数に、pageとper_pageのクエリ文字列を追加する

@router.get("/")
def get_todo_lists(
    session: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10,
):
    return list_crud.get_todo_lists(session, page, per_page)

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
    return list_crud.create_todo_list(data, session)

@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(
    todo_list_id: int,
    data: UpdateTodoList,
    session: Session = Depends(get_db),
):
    return list_crud.update_todo_list(todo_list_id, data, session)

@router.delete("/{todo_list_id}")
def delete_todo_list(
    todo_list_id: int,
    session: Session = Depends(get_db),
):
    return list_crud.delete_todo_list(todo_list_id, session)