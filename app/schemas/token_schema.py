from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(example="token", description="ログイン後に発行されるトークン")
    token_type: str = Field(example="bearer",
                            description="トークンの種類。通常bearer（持っているだけで意味のあるトークン）")

    def __init__(self, access_token: str, token_type: str = "bearer") -> None:
        super().__init__(access_token=access_token, token_type=token_type)
