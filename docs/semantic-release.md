# Semantic Release

In this sample repo, packages are not released to a private or remote package registry.
A simple versioning approach is taken to manage package versioning using [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/).


## Package Versioning
* Each package has it's own version in this monorepo
* Package version is incremented following the [Semantic Versioning Convention](https://semver.org/) - This requires conventional commit messages as described bellow
* The configuration of `python-semantic-release` this will be centralized in the root's `pyproject.toml` file.
* The monorepo root is not considered a package, but its version is managed and incremented whenever one of the packages is incremented
* Since the branch policy uses squash and merge - all commit messages are squashed into a single one which is assumed to be of the [conventional commit message format](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html) (more details below)
* Whenever Pull Request is created, the CI will fail if this convention is not followed
* When the code is merged into main, the versions are bumped  

### Package Version Bump
Following the [Semantic Versioning Convention](https://semver.org/) this is how version is incremented:
Given a version number MAJOR.MINOR.PATCH, increment the:
* MAJOR version when you make incompatible API changes
* MINOR version when you add functionality in a backward compatible manner
* PATCH version when you make backward compatible bug fixes

**In this repo we implement an imperfect, yet simple approach to version bumping:
In each pull request, all updated packages, including the monorepo root, will be incremented according to simple rules applied on the PR message.
Even if one package requires a PATCH version bump and another package requires a MINOR package bump, they will both be incremented in a MINOR patch**

### Commit Messages Format
To allow automatic versioning, we'll need to follw a [conventional commit message format](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html):
```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer(optional)>
```

>> Note: When commiting to your local feature brach, running `git commit` will open an editor with the above format.
You can edit it and close it to complete the commit.
>> Note: Once your feature branch is ready to be `squashed and merged` into `main`, you can use all messages or create a new one in the above format
>> Note: When packages are not released to a registry, your local development environment is always using the latest code regardless of the actual version. The version is used to indicate what is deployed to production and whether it requires an update

**Example**: Commit message which will trigger a PATCH version bump:
```
docs(configuration): fixed typo in README.md

Fixed typo in configuration package README.ms file
```

**Example**: Commit message which will trigger a PATCH version bump:
```
feat(environment): add support in primary and secondary reagion of Service Environment

- Updated ServiceEnvironment to include primary region property to indicate where the centralized resources are managed.
- A primary region is set per each staging environment
```

**Example**: Commit message which triggers a MAJOR version bump:
```
feat(auth): add OAuth2 support

Implemented OAuth2 support to allow users to authenticate via external providers. This includes:
- Adding OAuth2 configuration options
- Implementing the authentication flow
- Updating the user model to support OAuth2 tokens

BREAKING CHANGE: The user model has been updated to include OAuth2 token fields, which might require database migration.
```

> The body or footer can begin with `BREAKING CHANGE: <description>` to create a major release.

The configuration of the types allowed:
```
[tool.semantic_release.commit_parser_options]
allowed_tags = [
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "style",
    "refactor",
    "test",
]
minor_tags = ["feat"]
patch_tags = ["fix", "perf",]
```

The configuration of version bump rule:
```
[tool.semantic_release.release_rules]
breaking = "major"
feat = "minor"
fix = "patch"
docs = "patch"
style = "patch"
chore = "patch"
test = "path"
```

### "Release" Process
Since in this sample repo, packages are not released to a package registry, the equivalent to release, is merging into `main`.

1. When a PR is created - CI Checks will enforce commit message format
2. When merged to main - Run python-semantic-release tool to:
- Analyze commits since the last release.
- Determine the next version number based on the commit messages.
- Update the version in pyproject.toml and any other configured version_variable files.
- Create Git tags for all the monorepo - A Tag will be created with the monorepo root version, for example `v1.0.3`
- Generate or update the CHANGELOG.md for updated package
- a Manifest file in the monorepo root will indicate the package versions associated with this merge
