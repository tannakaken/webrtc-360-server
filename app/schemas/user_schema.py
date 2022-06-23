from datetime import datetime
from pydantic import Field, EmailStr
from pydantic.main import BaseModel


class UserModify(BaseModel):
    """
    ユーザーを修正するためのスキーマ
    """
    name: str = Field(example="John Doe", description="ユーザーの名前")
    "ユーザーの名前"


class UserBase(UserModify):
    """
    ユーザーの共通スキーマ
    """
    email: EmailStr = Field(example="user@example.net",
                            description="ユーザーのメールアドレス")
    "ユーザーのメールアドレス"


class UserCreate(UserBase):
    """
    ユーザーを作成するためのスキーマ
    """
    password: str = Field(example="password", description="ユーザーのパスワード")
    "ユーザーのパスワード"


class User(UserBase):
    """
    ユーザーの取得情報
    """
    created_at: datetime = Field(description="作成日時")
    "作成日時"


class UserItemsResponse(BaseModel):
    """
    ユーザー検索のページネーション結果
    """
    items: list[User] = Field(description="検索結果の中からページネーションされたもの")
    "検索結果の中からページネーションされたもの"
    total_count: int = Field(example=1, description="検索結果全体のページネーション前の個数")
    "検索結果全体のページネーション前の個数"

    def __init__(self, items: list[User], total_count: int) -> None:
        super().__init__(items=items, total_count=total_count)
