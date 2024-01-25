from pydantic import BaseModel
from wechatter.models.github.base import User, Repository
from wechatter.models.github.pr_webhook import PullRequest


class Review(BaseModel):
    id: int
    node_id: str
    user: User
    body: str
    commit_id: str
    submitted_at: str
    state: str
    html_url: str
    pull_request_url: str
    author_association: str


class GithubPrReviewWebhook(BaseModel):
    action: str
    review: Review
    pull_request: PullRequest
    repository: Repository
    sender: User
