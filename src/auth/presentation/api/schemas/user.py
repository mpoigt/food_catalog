from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from domain.enums.role import Role


class RegisterSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class AdminCreateUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    role: Role


class UserUpdateAdminSchema(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None
    role: Role | None = None
    is_blocked: bool | None = None
    password: str | None = Field(default=None, min_length=8)


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr
    role: Role
    is_blocked: bool


class PaginatedUsersSchema(BaseModel):
    total: int
    page: int
    limit: int
    items: list[UserResponseSchema]
