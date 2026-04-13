# Release Management

This document describes the release process for this integration.

## Overview

Releases are managed with [release-please](https://github.com/googleapis/release-please), which automates version bumping and changelog generation based on [Conventional Commits](https://www.conventionalcommits.org/).

**Version source of truth:** `custom_components/hidrograficopt/manifest.json`

## How It Works

### The Release Cycle

```text
1. Developer commits to main (Conventional Commits format)
        ↓
2. release-please opens/updates a release PR automatically
        ↓
3. Developer reviews the PR
        ↓
4. Developer merges the PR when ready
        ↓
5. release-please creates the GitHub Release + Git tag
   manifest.json version is already updated in the merged PR
```

### The Release PR

After any `feat`, `fix`, or `perf` commit reaches `main`, release-please opens a pull request titled:

```text
chore(main): release X.Y.Z
```

The PR:

- Has the label `autorelease: pending`
- Contains an updated `CHANGELOG.md`
- Contains the version bump in `manifest.json`
- Is updated automatically as more commits land on `main`

### Version Bumping Rules

This project is already at `1.x`, so standard SemVer applies:

| Commit type                   | Version change |
| ----------------------------- | -------------- |
| `feat`                        | minor bump     |
| `fix`, `perf`                 | patch bump     |
| `feat!` or `BREAKING CHANGE:` | major bump     |

### What Appears in the Changelog

Only user-facing changes appear in the public changelog:

| Type                                               | Visible |
| -------------------------------------------------- | ------- |
| `feat`                                             | Yes     |
| `fix`                                              | Yes     |
| `perf`                                             | Yes     |
| `refactor`, `chore`, `build`, `docs`, `test`, `ci` | Hidden  |

## Developer Scripts

### `script/version`

Reads the canonical version from `manifest.json`.

```bash
./script/version
./script/version --tag
./script/version --check
```

`--check` verifies that `manifest.json` and `.release-please-manifest.json` stay aligned.

## Typical Release Workflow

```bash
# 1. Work normally and use Conventional Commits
git commit -m "fix(sensor): correct next tide timestamp conversion"

# 2. Push to main
# 3. Review the release PR opened by release-please
# 4. Merge the release PR when you want to publish a release
```

## GitHub Repository Setup (One-Time)

These settings must be configured on GitHub.com.

### Required: GitHub Actions Permissions

In `Settings -> Actions -> General -> Workflow permissions`, set:

- `Read and write permissions`
- Enable `Allow GitHub Actions to create and approve pull requests`

### Recommended: Branch Protection for `main`

Require pull requests and successful checks before merge.

## Files

| File                                   | Purpose                                   |
| -------------------------------------- | ----------------------------------------- |
| `.github/workflows/release-please.yml` | Opens and updates release PRs             |
| `release-please-config.json`           | Changelog sections and version bump rules |
| `.release-please-manifest.json`        | Current version tracked by release-please |
| `CHANGELOG.md`                         | Auto-generated in release PRs             |
| `script/version`                       | Local version utility                     |
