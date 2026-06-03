# Git Interview Questions — Part 2
### Principal Architect Interview Sheet — PRs, Git Flow, Remote, Clone/Fork, gc, LFS
---

> **Topics:** Pull Requests · Git Flow · Remote Commands · Clone vs Fork · `git gc` · `git lfs`
> Scenario-based questions with clear, simple answers for 0–1 year experience interns.

---

## Section 1 — Pull Requests (PR)

---

**Q1. What is a Pull Request? Explain it like you're explaining it to someone on their very first day.**

**Answer:**
A Pull Request (PR) is a formal way of saying: *"I've made some changes on my branch — please review them before merging into the main codebase."*

It's not a Git feature — it's a platform feature (GitHub, GitLab, Bitbucket). When you raise a PR:
1. Your teammates can **see exactly what lines changed**
2. They can **leave comments or request changes**
3. Once approved, someone **merges it**

Think of it as a code review gate before your work goes live. You never push directly to `main` — you always go through a PR.

---

**Q2. Walk me through the end-to-end steps of raising a PR from scratch — from writing code to it being merged.**

**Answer:**

```bash
# Step 1: Create and switch to your feature branch
git checkout -b feature/add-search-bar

# Step 2: Write your code, then stage and commit
git add .
git commit -m "feat: add search bar to homepage"

# Step 3: Push your branch to remote
git push origin feature/add-search-bar
```

**Step 4:** Go to GitHub/GitLab → click **"New Pull Request"** → select:
- **Base branch:** `develop` (where you want to merge INTO)
- **Compare branch:** `feature/add-search-bar` (your work)

**Step 5:** Fill in:
- A clear **title**
- A **description** of what changed and why
- Link any related issue (e.g., `Closes #42`)

**Step 6:** Assign **reviewers**

**Step 7:** Reviewers leave comments → you address them → push new commits (they auto-update the PR)

**Step 8:** Once approved → **Merge** the PR

---

**Q3. Scenario: You opened a PR and your reviewer left 5 comments requesting changes. How do you update your PR?**

**Answer:**
You do NOT close and reopen the PR. Just push new commits to the same branch — the PR updates automatically.

```bash
# Make the requested changes locally
git add .
git commit -m "fix: address PR review comments - input validation"

# Push to the same branch
git push origin feature/add-search-bar
```

The PR will now show the new commits. GitHub/GitLab will mark the conversation threads as "resolved" once the reviewer re-checks. You can also leave comments on the PR explaining what you changed and why.

---

**Q4. Scenario: You're reviewing a teammate's PR and you notice their branch is 10 commits behind `develop`. The PR might have merge conflicts. What do you tell them to do?**

**Answer:**
Tell them to **sync their branch with the latest `develop`** before you can properly review. They have two options:

**Option A — Merge `develop` into their branch (safer, preserves history):**
```bash
git checkout feature/add-search-bar
git fetch origin
git merge origin/develop
# Resolve any conflicts, then push
git push origin feature/add-search-bar
```

**Option B — Rebase onto `develop` (cleaner history):**
```bash
git checkout feature/add-search-bar
git fetch origin
git rebase origin/develop
# Resolve conflicts at each step, then:
git push origin feature/add-search-bar --force-with-lease
```

Option A is safer for shared PRs. Option B gives a cleaner commit history but rewrites commits.

---

**Q5. What is a Draft PR? When would you create one?**

**Answer:**
A Draft PR signals: *"I'm still working on this — don't merge it yet, but feedback is welcome."*

You'd use a Draft PR when:
- You want early feedback on your approach before finishing
- You want CI/CD checks to run on your branch
- You're working on something complex and want to document progress
- You want to flag the work so the team knows it's in progress

```
GitHub: Click "New Pull Request" → dropdown arrow → "Create Draft Pull Request"
GitLab: Check the "Mark as draft" checkbox
```

When you're ready, click **"Ready for Review"** — it converts to a normal PR.

---

**Q6. You accidentally committed a secret API key and pushed it. Someone on your team catches it during PR review before merge. What's the immediate action plan?**

**Answer:**
This is a security incident even if it hasn't merged yet. Steps:

1. **Invalidate/rotate the API key immediately** — assume it's compromised the moment it was pushed (bots scan GitHub in seconds)
2. **Remove it from the branch:**
```bash
# Remove the secret from the last commit
git reset --soft HEAD~1
# Edit the file to remove the secret
git add .
git commit -m "remove: accidentally committed API key"
git push origin your-branch --force-with-lease
```
3. **If it was pushed earlier in history**, use `git filter-repo` or BFG Repo Cleaner to scrub it from all commits
4. **Add the file to `.gitignore`** or use environment variables going forward
5. **Never use `--force` on `main`** — coordinate with the team

The key lesson: secrets never belong in code. Use `.env` files + `.gitignore`, or a secrets manager.

---

## Section 2 — Git Flow

---

**Q7. Explain Git Flow. Draw out the branch structure and describe what each branch is for.**

**Answer:**
Git Flow is a branching strategy with 5 branch types:

```
main         ──────────────────────────────────────────▶  (production, always stable)
               ↑ merge                        ↑ merge (hotfix)
release/1.2  ────────────────────▶            |
               ↑ merge                        |
develop      ──────────────────────────────── ┤          (integration branch)
               ↑ merge      ↑ merge           |
feature/A  ──────▶        feature/B ──▶       |
                                    hotfix/x ─┘
```

| Branch | Purpose |
|---|---|
| `main` | Production code only. Every commit here is a live release. |
| `develop` | Integration branch. All features merge here first. |
| `feature/*` | One branch per feature, branched off `develop`. |
| `release/*` | Branched off `develop` when ready for release. Only bug fixes go here. |
| `hotfix/*` | Branched off `main` for urgent production fixes. Merged to BOTH `main` and `develop`. |

---

**Q8. What is the correct flow for developing a new feature called "dark mode" using Git Flow?**

**Answer:**

```bash
# 1. Branch off develop
git checkout develop
git pull origin develop
git checkout -b feature/dark-mode

# 2. Build the feature with commits
git commit -m "feat: add dark mode toggle"
git commit -m "feat: persist dark mode in localStorage"

# 3. When done, push and raise a PR into develop
git push origin feature/dark-mode
# → Open PR: feature/dark-mode → develop

# 4. After PR is approved and merged, delete the feature branch
git branch -d feature/dark-mode
git push origin --delete feature/dark-mode
```

You **never** merge a feature directly into `main`. It always goes `feature → develop → release → main`.

---

**Q9. When does a `release` branch get created, and what can you commit to it?**

**Answer:**
A `release` branch is created when `develop` has enough features for a new version and you want to prepare for a production release — but you need a "freeze" period for final QA.

```bash
# Branch off develop when you're ready to ship
git checkout develop
git checkout -b release/2.1.0

# Only bug fixes and version bumps go here — NO new features
git commit -m "fix: correct date format on invoice"
git commit -m "chore: bump version to 2.1.0"
```

Once QA is happy:
```bash
# Merge into main (ship it)
git checkout main
git merge --no-ff release/2.1.0
git tag -a v2.1.0 -m "Release 2.1.0"

# Also merge back into develop (to keep the bug fixes)
git checkout develop
git merge --no-ff release/2.1.0

git branch -d release/2.1.0
```

The release branch is a **stabilization zone** — not a place for new features.

---

**Q10. A critical bug is found in production at 2 AM. Walk me through the complete hotfix Git Flow.**

**Answer:**

```bash
# 1. Branch directly off main (NOT develop)
git checkout main
git pull origin main
git checkout -b hotfix/fix-login-crash

# 2. Fix the bug
git add .
git commit -m "fix: resolve null session token on login"

# 3. Merge into main and tag a new patch version
git checkout main
git merge --no-ff hotfix/fix-login-crash
git tag -a v2.0.1 -m "Hotfix: login crash fix"
git push origin main --tags

# 4. CRITICAL: also merge into develop so the fix isn't lost
git checkout develop
git merge --no-ff hotfix/fix-login-crash
git push origin develop

# 5. Clean up
git branch -d hotfix/fix-login-crash
git push origin --delete hotfix/fix-login-crash
```

**Why merge into `develop` too?** Because if you only fix `main`, next time `develop` is released to production, the bug comes back.

---

**Q11. Your team argues: "Git Flow is overkill, let's just use `main` and feature branches." How do you respond?**

**Answer:**
Both approaches are valid — it depends on the team's release cadence.

**Git Flow is great when:**
- You have scheduled, versioned releases (e.g., v1.0, v2.1)
- Multiple versions of the product are live simultaneously
- QA needs a dedicated stabilization period before shipping

**Trunk-based development (just `main` + short-lived feature branches) is better when:**
- You deploy continuously (multiple times per day)
- The team is small and moves fast
- You have strong automated test coverage

As a Principal Architect, you'd pick Git Flow for enterprise software with formal releases, and trunk-based for SaaS products with continuous delivery. The worst answer is using a complex workflow without knowing why.

---

## Section 3 — Remote Commands

---

**Q12. You've built a project locally and now want to push it to a brand new GitHub repository. What are the exact commands?**

**Answer:**

```bash
# 1. Initialize Git in your project (if not already)
git init

# 2. Stage and commit your work
git add .
git commit -m "initial commit"

# 3. Connect your local repo to the remote
git remote add origin https://github.com/yourusername/your-repo.git

# 4. Rename default branch to main (if needed)
git branch -M main

# 5. Push and set the upstream tracking
git push -u origin main
```

After step 5, future pushes can just be `git push` without specifying `origin main` — Git remembers the tracking relationship.

---

**Q13. What does `git remote -v` show and why is it useful?**

**Answer:**

```bash
git remote -v
# Output:
# origin  https://github.com/your-org/project.git (fetch)
# origin  https://github.com/your-org/project.git (push)
```

It shows all the remote connections your local repo has, and the URLs for both fetching and pushing. Useful when:
- You want to **verify** you're pointing to the right repo
- You have **multiple remotes** (e.g., `origin` = your fork, `upstream` = the original repo)
- Debugging why a push or pull is going to the wrong place

---

**Q14. You forked a repo and cloned your fork. The original repo has new commits. How do you pull those changes into your fork?**

**Answer:**
You add the original repo as a second remote called `upstream`.

```bash
# 1. Add the original repo as upstream (only done once)
git remote add upstream https://github.com/original-owner/repo.git

# Verify both remotes exist
git remote -v
# origin    https://github.com/you/repo.git (fetch)
# upstream  https://github.com/original-owner/repo.git (fetch)

# 2. Fetch from upstream
git fetch upstream

# 3. Merge upstream changes into your local main
git checkout main
git merge upstream/main

# 4. Push the updated main to your fork
git push origin main
```

---

**Q15. How do you rename a remote, change its URL, or remove it entirely?**

**Answer:**

```bash
# Rename a remote (e.g., origin → github)
git remote rename origin github

# Change the URL of a remote (e.g., switching from HTTPS to SSH)
git remote set-url origin git@github.com:yourusername/repo.git

# Remove a remote entirely
git remote remove upstream

# Verify changes
git remote -v
```

You'd change the URL when switching from HTTPS to SSH authentication, or when a repo gets moved/renamed on the platform.

---

## Section 4 — git clone vs git fork

---

**Q16. What is `git clone`? What does it actually do under the hood?**

**Answer:**

```bash
git clone https://github.com/some-org/some-project.git
```

`git clone` creates a **full local copy** of a remote repository, including:
- All commits and full history
- All branches (though only `main` is checked out by default)
- All tags
- A remote called `origin` pointing back to the source

Under the hood it:
1. Creates a new directory
2. Initializes a `.git` folder inside it
3. Downloads all objects (commits, trees, blobs) from the remote
4. Sets `origin` to the cloned URL
5. Checks out the default branch

```bash
# Clone into a custom folder name
git clone https://github.com/org/project.git my-local-name

# Clone only the latest snapshot (no full history — faster for large repos)
git clone --depth 1 https://github.com/org/project.git
```

---

**Q17. What is the difference between `git clone` and forking a repository? This trips up a lot of interns.**

**Answer:**

| | `git clone` | Fork |
|---|---|---|
| What it is | Git command | Platform feature (GitHub/GitLab) |
| Where the copy lives | **Your local machine** | **Your remote account** (e.g., github.com/you/repo) |
| Connected to original? | Yes, via `origin` remote | Loosely — you can add `upstream` manually |
| Can you push to original? | Only if you have permission | No — you push to your fork, then raise a PR |
| Used for | Working on a repo you have access to | Contributing to repos you DON'T own |

**Typical open-source workflow:**
1. **Fork** the repo on GitHub (creates `github.com/you/repo`)
2. **Clone** your fork locally (`git clone github.com/you/repo`)
3. Make changes, push to your fork
4. Raise a **PR** from your fork to the original repo

So in practice: **fork = remote copy for contribution, clone = local copy for development.** You almost always do both.

---

**Q18. You cloned a repo and see only the `main` branch locally, but there are 10 branches on the remote. How do you access them?**

**Answer:**
All remote branches were downloaded — they're just not checked out locally yet. They exist as `remote-tracking branches`.

```bash
# See all branches (local + remote)
git branch -a
# Output:
# * main
#   remotes/origin/feature/dark-mode
#   remotes/origin/develop
#   ...

# Check out a remote branch locally
git checkout -b feature/dark-mode origin/feature/dark-mode

# Shorthand (Git 2.23+)
git switch feature/dark-mode
```

Git automatically sets up the tracking relationship so `git pull` on that branch will pull from the right remote branch.

---

## Section 5 — git gc and Dangling Commits

---

**Q19. What is `git gc` and when would you run it?**

**Answer:**
`git gc` stands for **garbage collection**. Over time, Git accumulates loose object files — old commits from deleted branches, abandoned stashes, leftover reflog entries. `git gc` cleans these up and compresses history into efficient pack files.

```bash
git gc
# OR for a more thorough cleanup:
git gc --aggressive --prune=now
```

Git runs `git gc` automatically in the background occasionally. You'd run it manually when:
- The repo is growing unusually large
- You've deleted many branches and want to free space
- After removing large files from history
- After running `git filter-repo` to rewrite history

It's safe to run at any time. It doesn't delete anything that's still reachable from a branch or tag.

---

**Q20. What is a dangling commit? How does it happen and what does `git gc` do to it?**

**Answer:**
A **dangling commit** (also called an unreachable or orphaned commit) is a commit that exists in Git's object store but is no longer reachable from any branch, tag, or `HEAD`.

**How they're created:**
```bash
# Make some commits on a branch
git checkout -b experiment
git commit -m "trying something"
git commit -m "more experiments"

# Delete the branch WITHOUT merging
git branch -D experiment
# → Those 2 commits are now dangling — no branch points to them
```

Also created by:
- `git reset --hard` (commits you jumped back from)
- `git rebase` (old versions of rebased commits)
- Dropped stashes

**Finding dangling commits:**
```bash
git fsck --lost-found
# Output: dangling commit a3f9c21...
```

**What `git gc` does:** After the reflog expires (default 90 days), `git gc` permanently deletes dangling commits. Before that window, `git reflog` can recover them.

---

**Q21. Is there any scenario where dangling commits are actually useful?**

**Answer:**
Yes — they're your safety net. When you accidentally `git reset --hard` or delete a branch, those commits become dangling but are NOT immediately gone. You have ~90 days (reflog expiry) to recover them.

```bash
# Find the dangling commit hash
git fsck --lost-found

# Or check reflog for recent HEAD positions
git reflog

# Recover by creating a new branch from it
git checkout -b recovered-work a3f9c21
```

So dangling commits = **recoverable work**. `git gc` is what makes them permanently unrecoverable. This is why the advice "everything committed in Git is safe" is largely true — until `gc` prunes it.

---

## Section 6 — git lfs (Large File Storage)

---

**Q22. What is `git lfs` and why does it exist? What problem does it solve?**

**Answer:**
Git is designed for **text files** (code). When you add large binary files — videos, PSD files, ML model weights, audio files, ZIP archives — Git stores a full copy of every version in history. A 100MB design file edited 50 times = 5GB of repo history. Cloning becomes painfully slow.

**`git lfs` (Large File Storage)** solves this by storing large files **outside the main Git repo**, on a separate LFS server. Inside the repo, Git only stores a tiny **pointer file** (a few bytes) that says "the real file is over there."

```
Without LFS: repo contains full 200MB video file × every version = enormous
With LFS:    repo contains 130-byte pointer → LFS server stores the actual file
```

Your git history stays lean. The actual files are downloaded on-demand.

---

**Q23. Walk me through setting up `git lfs` for a project that will contain large Figma export PNGs.**

**Answer:**

```bash
# Step 1: Install git-lfs (one time, system-wide)
git lfs install

# Step 2: In your repo, tell LFS which file types to track
git lfs track "*.png"
git lfs track "*.psd"
git lfs track "*.fig"

# Step 3: This creates/updates a .gitattributes file — commit it!
git add .gitattributes
git commit -m "chore: configure git lfs for design assets"

# Step 4: Now add and commit your large files normally
git add design-mockup.png
git commit -m "design: add homepage mockup"
git push origin main
```

From now on, any `.png`, `.psd`, or `.fig` files are automatically handled by LFS. Anyone who clones the repo gets the pointer files; actual binaries download when they check out the branch.

---

**Q24. What happens if a team member clones a repo that uses git lfs but they DON'T have git lfs installed?**

**Answer:**
They'll get the **pointer files** instead of the actual content. The files in their working directory will look like this instead of the real image/video:

```
version https://git-lfs.github.com/spec/v1
oid sha256:4d7a214614ab2935c943f9e0ff69d22eadbb8f32b1258daaa5e2ca24d17e2393
size 1048576
```

This is confusing and breaks their workflow. The fix:

```bash
# Install git lfs
git lfs install

# Pull the actual files
git lfs pull
```

**Lesson for the team:** Document `git lfs install` as a mandatory setup step in your `README.md` or `CONTRIBUTING.md`.

---

**Q25. What is the difference between `git lfs fetch`, `git lfs pull`, and `git lfs push`?**

**Answer:**

```bash
# Download LFS objects to local cache but don't update working directory
git lfs fetch

# Download AND update working directory (fetch + checkout)
git lfs pull

# Push LFS objects from local cache to remote LFS server
git lfs push origin main
```

Normally `git push` and `git pull` handle LFS automatically. You use these explicit commands when:
- Prefetching LFS files for offline work (`lfs fetch`)
- LFS files didn't download properly (`lfs pull`)
- Migrating a repo to a new LFS host (`lfs push`)

---

## Section 7 — Mixed Scenario Questions

---

**Q26. A new intern joins the team. They need to contribute to your open-source project on GitHub. What's the exact workflow you'd tell them to follow?**

**Answer:**

```bash
# 1. FORK the repo on GitHub (via the UI)
# → This creates github.com/intern/your-project

# 2. CLONE their fork locally
git clone https://github.com/intern/your-project.git
cd your-project

# 3. Add the ORIGINAL repo as upstream
git remote add upstream https://github.com/your-org/your-project.git

# 4. Create a feature branch (never work on main directly)
git checkout -b feature/fix-typo-in-readme

# 5. Make changes, commit
git add README.md
git commit -m "fix: correct typo in installation section"

# 6. Push to THEIR FORK (not upstream)
git push origin feature/fix-typo-in-readme

# 7. Raise a PR on GitHub:
#    Base: your-org/your-project → main
#    Compare: intern/your-project → feature/fix-typo-in-readme

# 8. Keep fork updated going forward
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

**Q27. You ran `git clone` and the repo is 4GB. It's taking forever. What can you do to speed it up?**

**Answer:**

```bash
# Option 1: Shallow clone — only get the latest snapshot, no full history
git clone --depth 1 https://github.com/org/huge-repo.git

# Option 2: Clone only one branch instead of all branches
git clone --single-branch --branch main https://github.com/org/huge-repo.git

# Option 3: Combine both
git clone --depth 1 --single-branch --branch main https://github.com/org/huge-repo.git
```

If the repo is large because of committed binary files (videos, binaries), that's a sign `git lfs` should have been set up from the start. A shallow clone is fine for most CI/CD pipelines and everyday development — you rarely need the full 5-year history.

---

**Q28. Explain what `git remote set-url` is useful for. Give a real-world example.**

**Answer:**
It changes where Git pushes and pulls to/from — without re-cloning the repo.

**Real-world example:** Your company moves from HTTPS authentication (username + password) to SSH keys:

```bash
# Current setup (HTTPS)
git remote -v
# origin  https://github.com/org/project.git (fetch)

# Switch to SSH
git remote set-url origin git@github.com:org/project.git

# Verify
git remote -v
# origin  git@github.com:org/project.git (fetch)
```

Other scenarios:
- A repo gets renamed or moved to a new organization
- Your team migrates from GitHub to GitLab
- You want to point to a different fork temporarily

---

**Q29. What is `git push -u origin main` — what does the `-u` flag do, and why do you only need it once?**

**Answer:**
The `-u` flag sets up a **tracking relationship** between your local branch and the remote branch.

```bash
# First push: -u sets the tracking link
git push -u origin main

# All future pushes on this branch: just type
git push
# Git knows: "local main → push to origin/main"
```

Without `-u`, you'd have to type `git push origin main` every time. The tracking relationship is stored in `.git/config`:

```ini
[branch "main"]
    remote = origin
    merge = refs/heads/main
```

You only need `-u` once per branch per machine. After that, plain `git push` and `git pull` know exactly where to go.

---

**Q30. Final Boss Question: Your team's `main` branch history has 3 years of history, several large PSD files committed directly (each 50–100MB), and the repo is now 8GB. New developers take 20 minutes to clone it. What's your remediation plan as Principal Architect?**

**Answer:**
This is a real problem in growing teams. Here's the step-by-step plan:

**Step 1 — Assess the damage:**
```bash
# Find the biggest objects in history
git rev-list --objects --all | sort -k 2 | head -20
git gc
git count-objects -vH
```

**Step 2 — Remove large files from ALL history using `git filter-repo`:**
```bash
pip install git-filter-repo
git filter-repo --path design-assets/ --invert-paths
# This rewrites every commit that touched those files
```

**Step 3 — Set up `git lfs` PROPERLY going forward:**
```bash
git lfs install
git lfs track "*.psd" "*.ai" "*.sketch" "*.fig"
git add .gitattributes
git commit -m "chore: migrate large assets to git lfs"
```

**Step 4 — Re-add the design files through LFS:**
```bash
git add design-assets/
git commit -m "chore: re-add design assets via lfs"
```

**Step 5 — Force push the cleaned history (coordinate with entire team):**
```bash
git push origin --force --all
git push origin --force --tags
```

**Step 6 — All team members must re-clone:**
```bash
# Old clones are now out of sync — everyone must fresh clone
git clone https://github.com/org/project.git
git lfs install
git lfs pull
```

**Step 7 — Prevent recurrence:**
- Add a pre-commit hook that rejects files > 5MB without LFS
- Document the LFS setup in `README.md`
- Add `.gitattributes` rules for all binary formats

Result: Repo goes from 8GB → ~200MB. Clone time: 20 minutes → under 1 minute.

---

## Quick Reference — Commands Covered in This Sheet

| Topic | Key Commands |
|---|---|
| **PR workflow** | `git push origin branch`, raise PR on platform, `git push` to update PR |
| **Git Flow** | `feature/*` → `develop` → `release/*` → `main`; `hotfix/*` → `main` + `develop` |
| **Remote setup** | `git remote add origin <url>` |
| **Remote management** | `git remote -v`, `git remote rename`, `git remote set-url`, `git remote remove` |
| **Upstream sync** | `git remote add upstream <url>`, `git fetch upstream`, `git merge upstream/main` |
| **Cloning** | `git clone <url>`, `git clone --depth 1`, `git clone --single-branch` |
| **Fork workflow** | Fork on platform → clone fork → add upstream → PR back to original |
| **Garbage collection** | `git gc`, `git gc --aggressive --prune=now`, `git fsck --lost-found` |
| **LFS setup** | `git lfs install`, `git lfs track "*.ext"`, commit `.gitattributes` |
| **LFS sync** | `git lfs pull`, `git lfs fetch`, `git lfs push` |
| **Tracking branch** | `git push -u origin main` (first push), then just `git push` |

---

*Prepared by: Principal Architect | Internal Intern Evaluation — Git Advanced Topics (Part 2)*
