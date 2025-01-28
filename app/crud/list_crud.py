from fastapi import Depends, HTTPException, status

from app.dependencies import get_db

from app.models.list_model import ListModel

from app.schemas.list_schema import NewTodoList, UpdateTodoList

from sqlalchemy.orm import Session

# TODO リスト一覧取得用関数にて、pageおよびper_pageを引数として受け取るようにして、これら2つの引数を基にデータを返却するように処理の記述
def get_todo_lists(
    db: Session,
    page: int,
    per_page: int
):
    offset = (page - 1) * per_page
    db_lists = db.query(ListModel)\
                 .order_by(ListModel.id)\
                 .limit(per_page)\
                 .offset(offset)\
                 .all()
    return db_lists

# TODOリストを取得するエンドポイント
def get_todo_list(
    todo_list_id: int,
    db: Session
):
    #DBから該当レコードを1件取得
    db_list =db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo List not found"
        )
    # レコードを返却　→　Pydantic(ResponseTodoList)に変換される
    return db_list

# 新規TODOリストを登録するエンドポイント
def create_todo_list(
    data:NewTodoList,
    db: Session,
):
    new_db_list = ListModel(
        title=data.title,
        description=data.description,
    )
    db.add(new_db_list)
    db.commit()
    db.refresh(new_db_list)
    return new_db_list

# TODOリストを更新するエンドポイント
def update_todo_list(
    todo_list_id: int,
    data: UpdateTodoList,
    db: Session,
):
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo List not found"
        )
    if data.title is not None:
        db_item.title = data.title
    if data.description is not None:
        db_item.description = data.description
       
    db.commit()
    db.refresh(db_item)
    return db_item

# TODOリストを削除するエンドポイント
def delete_todo_list(
    todo_list_id: int,
    db: Session
):
    db_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if db_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo List not found"
        )
    
    db.delete(db_list)
    db.commit()
    return {}
