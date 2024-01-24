from pydantic import BaseModel
from wechatter.models.github.base import User, Repository, Reactions


class Issue(BaseModel):
    html_url: str
    number: int
    title: str
    user: User
    state: str
    reactions: Reactions


class GithubIssueWebhook(BaseModel):
    action: str
    issue: Issue
    repository: Repository
    sender: User


"""
{
  "action": "opened",
  "issue": {
    "url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/1",
    "repository_url": "https://api.github.com/repos/Cassius0924/.dotfiles",
    "labels_url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/1/labels{/name}",
    "comments_url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/1/comments",
    "events_url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/1/events",
    "html_url": "https://github.com/Cassius0924/.dotfiles/issues/1",
    "id": 2093165520,
    "node_id": "I_kwDOLBhCe858wyvQ",
    "number": 1,
    "title": "test webhook",
    "user": {
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
    "labels": [

    ],
    "state": "open",
    "locked": false,
    "assignee": null,
    "assignees": [

    ],
    "milestone": null,
    "comments": 0,
    "created_at": "2024-01-22T06:13:23Z",
    "updated_at": "2024-01-22T06:13:23Z",
    "closed_at": null,
    "author_association": "OWNER",
    "active_lock_reason": null,
    "body": null,
    "reactions": {
      "url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/1/reactions",
      "total_count": 0,
      "+1": 0,
      "-1": 0,
      "laugh": 0,
      "hooray": 0,
      "confused": 0,
      "heart": 0,
      "rocket": 0,
      "eyes": 0
    },
    "timeline_url": "https://api.github.com/repos/Cassius0924/.dotfiles/issues/1/timeline",
    "performed_via_github_app": null,
    "state_reason": null
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
    "open_issues_count": 1,
    "license": null,
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [

    ],
    "visibility": "private",
    "forks": 0,
    "open_issues": 1,
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
