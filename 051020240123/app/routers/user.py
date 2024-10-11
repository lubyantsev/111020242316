from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import CreateUser, UpdateUser  # Предполагается, что такие схемы у вас есть
from app.backend.db_depends import get_db

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/", response_model=list[User])
async def all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=User)
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(create_user: CreateUser, db: Session = Depends(get_db)):
    new_user = User(**create_user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/update/{user_id}", response_model=User)
async def update_user(user_id: int, update_user: UpdateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in update_user.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()