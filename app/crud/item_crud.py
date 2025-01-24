from fastapi import Depends, HTTPException, status

from app.const import TodoItemStatusCode
from app.dependencies import get_db

from app.models.item_model import ItemModel
from app.models.list_model import ListModel

from app.schemas.item_schema import NewTodoItem, UpdateTodoItem

from sqlalchemy.orm import Session

# TODOリストに紐づくTODOアイテムを取得するエンドポイント
def get_todo_items(
    db: Session, 
    todo_list_id: int
):
    db_items = db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id).all()
    return db_items

def get_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id: int
):
    db_item = db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id,ItemModel.id == todo_item_id ).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo Item not found"
        )
    return db_item

# TODO 項目作成エンドポイント
def post_todo_item(
    db: Session,
    todo_list_id: int,
    data:NewTodoItem
):
    new_db_item = ItemModel(
        todo_list_id=todo_list_id,
        title=data.title,
        description=data.description,
        due_at=data.due_at,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value 
    )
    db.add(new_db_item)
    db.commit()
    db.refresh(new_db_item)
    return new_db_item

# TODO項目更新エンドポイント
def update_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id: int,
    data: UpdateTodoItem
):
    db_item = db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first()
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
    
    db.commit()
    db.refresh(db_item)
    return db_item

# TODO項目削除エンドポイント
def delete_todo_item(
    db: Session,
    todo_list_id: int,
    todo_item_id:int
):
    db_item = db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo Item not found"
        ) 
    
    db.delete(db_item)
    db.commit()
    return {}