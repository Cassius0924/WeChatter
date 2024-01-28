from pydantic import BaseModel

from wechatter.models.github.base import Repository, User


class Forkee(BaseModel):
    name: str
    full_name: str
    private: bool
    owner: User
    html_url: str


class GithubForkWebhook(BaseModel):
    forkee: Forkee
    repository: Repository
    sender: User
