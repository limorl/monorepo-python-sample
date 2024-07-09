## Pull Request Title Format

Pull request title and description should be: should be:
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>

The body or footer can begin with `BREAKING CHANGE:` followed by a short description to create a `major` release.

Where `<type>` can be one of the following:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing or correcting existing tests
- `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- `ci`: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
- `chore`: Other changes that don't modify src or test files

Examples:
- breaking(greeting-service): updated greeting API
- feat(login): add new login button
- docs(authentication): add authentication documentation
- feat(authentication): add jwt support
- fix(database): resolve connection leak
- style(greeting-service): correct typo messages


## Description

Please include a summary of the changes and the related issue. Please also include relevant motivation and context.

- **Related Issue:** # (issue number)

- **Motivation and Context:** (Why is this change required? What problem does it solve?)
