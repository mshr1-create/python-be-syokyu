import os
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from .models.item_model import ItemModel
from .models.list_model import ListModel
from .dependencies import get_db


DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(default=None, title="Set Todo Item status as completed")


class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


@app.get("/echo", tags=["Hello"])
def get_echo(message: str, name: str):
    return {"Message": f"{message} {name}!"}

#API の HTTP メソッド GET でパスを /health パラメータを持たないエンドポイントを作成
@app.get("/health", tags=["System"])
def get_health():
    return{"status": "ok"}

@app.get("/lists/{todo_list_id}", response_model=ResponseTodoList, tags=["Todo List"])
def get_todo_list(
    todo_list_id: int,
    session: Session = Depends(get_db),
):
    #DBから該当レコードを1件取得
    db_item =session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo List not found"
        )
    # レコードを返却　→　Pydantic(ResponseTodoList)に変換される
    return db_item

# 新規TODOリストを登録するエンドポイント
# DBセッション注入、response_modelで登録結果を返す
@app.post("/lists", response_model=ResponseTodoList, tags=["Todo List"] )
def post_todo_list(
    data:NewTodoList,
    session: Session = Depends(get_db),
):
    new_db_item = ListModel(
        title=data.title,
        description=data.description,
    )
    session.add(new_db_item)
    session.commit()
    session.refresh(new_db_item)
    return new_db_item


# TODOリストを更新するエンドポイント
# DBセッション注入、response_modelで登録結果を返す
@app.put("/lists/{todo_list_id}", response_model=ResponseTodoList, tags=["Todo List"])
def put_todo_list(
    todo_list_id: int,
    data: UpdateTodoList,
    session: Session = Depends(get_db),
):
    db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo List not found"
        )
    if data.title is not None:
        db_item.title = data.title
    if data.description is not None:
        db_item.description = data.description
       
    session.commit()
    session.refresh(db_item)
    return db_item

# TODOリストを削除するエンドポイント
# DBセッション注入、response_modelで登録結果を返す
# API のレスポンス形式 空の Json を返却
@app.delete("/lists/{todo_list_id}", response_model=None, tags=["Todo List"])
def delete_todo_list(
    todo_list_id: int,
    session: Session = Depends(get_db),
):
    db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            dertail="Todo List not found"
        )
    
    session.delete(db_item)
    session.commit()
    return {}

# TODOリストに紐づくTODOアイテムを取得するエンドポイント
# DBセッション注入、response_modelで登録結果を返す
# APIのパス/lists/{todo_list_id}/items/{todo_item_id}
@app.get("/lists/{todo_list_id}/items/{todo_item_id}", response_model=ResponseTodoItem, tags=["Todo Item"])
def get_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    session: Session = Depends(get_db),
):
    db_item = session.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id,ItemModel.id == todo_item_id ).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo Item not found"
        )
    return db_item

# TODO 項目作成エンドポイント
# DBセッション注入、response_modelで登録結果を返す
# APIのパス/lists/{todo_list_id}/items
# パスパラメータでtodo_list_idを受け取る。
# リクエストボディでNewTodoItem型のパラメータを受け取る。
@app.post("/lists/{todo_list_id}/items", response_model=ResponseTodoItem, tags=["Todo Item"])
def post_todo_item(
    todo_list_id: int,
    data:NewTodoItem,
    session: Session = Depends(get_db),
):
    new_db_item = ItemModel(
        todo_list_id=todo_list_id,
        title=data.title,
        description=data.description,
        due_at=data.due_at,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value 
    )
    session.add(new_db_item)
    session.commit()
    session.refresh(new_db_item)
    return new_db_item

# TODO項目更新エンドポイント
# DBセッション注入、response_modelで登録結果を返す
# APIのパス/lists/{todo_list_id}/items/{todo_item_id}
# パスパラメータでtodo_list_idとtodo_item_idを受け取る。
# リクエストボディでUpdateTodoItem型のパラメータを受け取る。
@app.put("/lists/{todo_list_id}/items/{todo_item_id}", response_model=ResponseTodoItem, tags=["Todo Item"])
def put_todo_item(
    todo_list_id: int,
    todo_item_id: int,
    data: UpdateTodoItem,
    session: Session = Depends(get_db),
):
    db_item = session.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo Item not found"
        )
    if data.title is not None:
        db_item.title = data.title
    if data.description is not None:
        db_item.description = data.description
    if data.due_at is not None:
        db_item.due_at = data.due_at
    if data.complete is not None:
        db_item.status_code = TodoItemStatusCode.COMPLETED.value if data.complete else TodoItemStatusCode.NOT_COMPLETED.value
    
    session.commit()
    session.refresh(db_item)
    return db_item

# TODO項目削除エンドポイント
# DBセッション注入、response_modelで登録結果を返す
# APIのパス/lists/{todo_list_id}/items/{todo_item_id}
# パスパラメータでtodo_list_idとtodo_item_idを受け取る。
# API のレスポンス形式 空の Json を返却 {}
@app.delete("/lists/{todo_list_id}/items/{todo_item_id}", response_model=None, tags=["Todo Item"])
def delete_todo_item(
    todo_list_id: int,
    todo_item_id:int,
    session: Session = Depends(get_db),
):
    db_item = session.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo Item not found"
        ) 
    
    session.delete(db_item)
    session.commit()
    return {}

