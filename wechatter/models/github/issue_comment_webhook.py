from pydantic import BaseModel
from wechatter.models.github.base import User, Repository, Reactions
from wechatter.models.github.issue_webhook import Issue


class Comment(BaseModel):
    url: str
    id: int
    user: User
    created_at: str
    body: str
    reactions: Reactions


class GithubIssueCommentWebhook(BaseModel):
    action: str
    issue: Issue
    comment: Comment
    repository: Repository
    sender: User
