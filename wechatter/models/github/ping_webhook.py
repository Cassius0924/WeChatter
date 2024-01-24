from pydantic import BaseModel
from wechatter.models.github.base import User, Repository


class Hook(BaseModel):
    type: str


class GithubPingWebhook(BaseModel):
    zen: str
    hook: Hook
    repository: Repository
    sender: User


"""
{
  "zen": "Keep it logically awesome.",
  "hook_id": 456157229,
  "hook": {
    "type": "Repository",
    "id": 456157229,
    "name": "web",
    "active": true,
    "events": [
      "*"
    ],
    "config": {
      "content_type": "form",
      "insecure_ssl": "0",
      "url": "http://123.57.134.250:4000/webhook/github"
    },
    "updated_at": "2024-01-22T05:41:02Z",
    "created_at": "2024-01-22T05:41:02Z",
    "url": "https://api.github.com/repos/Cassius0924/.dotfiles/hooks/456157229",
    "test_url": "https://api.github.com/repos/Cassius0924/.dotfiles/hooks/456157229/test",
    "ping_url": "https://api.github.com/repos/Cassius0924/.dotfiles/hooks/456157229/pings",
    "deliveries_url": "https://api.github.com/repos/Cassius0924/.dotfiles/hooks/456157229/deliveries",
    "last_response": {
      "code": null,
      "status": "unused",
      "message": null
    }
  },
  "repository": {
    "id": 739787387,
    "node_id": "R_kgDOLBhCew",
    "name": ".dotfiles",
    "full_name": "Cassius0924/.dotfiles",
    "private": true,
    "owner": {
      "login": "Cassius0924",
      "id": 62874592,
      "node_id": "MDQ6VXNlcjYyODc0NTky",
      "avatar_url": "https://avatars.githubusercontent.com/u/62874592?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/Cassius0924",
      "html_url": "https://github.com/Cassius0924",
      "followers_url": "https://api.github.com/users/Cassius0924/followers",
      "following_url": "https://api.github.com/users/Cassius0924/following{/other_user}",
      "gists_url": "https://api.github.com/users/Cassius0924/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/Cassius0924/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/Cassius0924/subscriptions",
      "organizations_url": "https://api.github.com/users/Cassius0924/orgs",
      "repos_url": "https://api.github.com/users/Cassius0924/repos",
      "events_url": "https://api.github.com/users/Cassius0924/events{/privacy}",
      "received_events_url": "https://api.github.com/users/Cassius0924/received_events",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/Cassius0924/.dotfiles",
    "description": null,
    "fork": false,
    "url": "https://api.github.com/repos/Cassius0924/.dotfiles",
    "forks_url": "https://api.github.com/repos/Cassius0924/.dotfiles/forks",
    "keys_url": "https://api.github.com/repos/Cassius0924/.dotfiles/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/Cassius0924/.dotfiles/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/Cassius0924/.dotfiles/teams",
    "hooks_url": "https://api.github.com/repos/Cassius0924/.dotfiles/hooks",
    "issue_events_url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/events{/number}",
    "events_url": "https://api.github.com/repos/Cassius0924/.dotfiles/events",
    "assignees_url": "https://api.github.com/repos/Cassius0924/.dotfiles/assignees{/user}",
    "branches_url": "https://api.github.com/repos/Cassius0924/.dotfiles/branches{/branch}",
    "tags_url": "https://api.github.com/repos/Cassius0924/.dotfiles/tags",
    "blobs_url": "https://api.github.com/repos/Cassius0924/.dotfiles/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/Cassius0924/.dotfiles/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/Cassius0924/.dotfiles/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/Cassius0924/.dotfiles/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/Cassius0924/.dotfiles/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/Cassius0924/.dotfiles/languages",
    "stargazers_url": "https://api.github.com/repos/Cassius0924/.dotfiles/stargazers",
    "contributors_url": "https://api.github.com/repos/Cassius0924/.dotfiles/contributors",
    "subscribers_url": "https://api.github.com/repos/Cassius0924/.dotfiles/subscribers",
    "subscription_url": "https://api.github.com/repos/Cassius0924/.dotfiles/subscription",
    "commits_url": "https://api.github.com/repos/Cassius0924/.dotfiles/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/Cassius0924/.dotfiles/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/Cassius0924/.dotfiles/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/Cassius0924/.dotfiles/contents/{+path}",
    "compare_url": "https://api.github.com/repos/Cassius0924/.dotfiles/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/Cassius0924/.dotfiles/merges",
    "archive_url": "https://api.github.com/repos/Cassius0924/.dotfiles/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/Cassius0924/.dotfiles/downloads",
    "issues_url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues{/number}",
    "pulls_url": "https://api.github.com/repos/Cassius0924/.dotfiles/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/Cassius0924/.dotfiles/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/Cassius0924/.dotfiles/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/Cassius0924/.dotfiles/labels{/name}",
    "releases_url": "https://api.github.com/repos/Cassius0924/.dotfiles/releases{/id}",
    "deployments_url": "https://api.github.com/repos/Cassius0924/.dotfiles/deployments",
    "created_at": "2024-01-06T14:45:21Z",
    "updated_at": "2024-01-06T14:50:57Z",
    "pushed_at": "2024-01-21T13:27:22Z",
    "git_url": "git://github.com/Cassius0924/.dotfiles.git",
    "ssh_url": "git@github.com:Cassius0924/.dotfiles.git",
    "clone_url": "https://github.com/Cassius0924/.dotfiles.git",
    "svn_url": "https://github.com/Cassius0924/.dotfiles",
    "homepage": null,
    "size": 4,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": "Lua",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": true,
    "has_pages": false,
    "has_discussions": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 0,
    "license": null,
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [

    ],
    "visibility": "private",
    "forks": 0,
    "open_issues": 0,
    "watchers": 0,
    "default_branch": "master"
  },
  "sender": {
    "login": "Cassius0924",
    "id": 62874592,
    "node_id": "MDQ6VXNlcjYyODc0NTky",
    "avatar_url": "https://avatars.githubusercontent.com/u/62874592?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/Cassius0924",
    "html_url": "https://github.com/Cassius0924",
    "followers_url": "https://api.github.com/users/Cassius0924/followers",
    "following_url": "https://api.github.com/users/Cassius0924/following{/other_user}",
    "gists_url": "https://api.github.com/users/Cassius0924/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/Cassius0924/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/Cassius0924/subscriptions",
    "organizations_url": "https://api.github.com/users/Cassius0924/orgs",
    "repos_url": "https://api.github.com/users/Cassius0924/repos",
    "events_url": "https://api.github.com/users/Cassius0924/events{/privacy}",
    "received_events_url": "https://api.github.com/users/Cassius0924/received_events",
    "type": "User",
    "site_admin": false
  }
}
"""
