from pydantic import BaseModel, Field


class Author(BaseModel):
    name: str
    email: str
    username: str


class Committer(BaseModel):
    name: str
    email: str
    username: str


class User(BaseModel):
    login: str
    id: int
    url: str
    html_url: str


class Pusher(BaseModel):
    name: str
    email: str


class Repository(BaseModel):
    name: str
    full_name: str
    private: bool
    html_url: str


class Reactions(BaseModel):
    total_count: int
    plus_one: int = Field(alias="+1")
    minus_one: int = Field(alias="-1")
    laugh: int
    hooray: int
    confused: int
    heart: int
    rocket: int
