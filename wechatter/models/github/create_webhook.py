from pydantic import BaseModel
from wechatter.models.github.base import User, Repository


class GithubCreateWebhook(BaseModel):
    ref: str
    ref_type: str
    master_branch: str
    description: str
    pusher_type: str
    repository: Repository
    sender: User
