# Git Interview Questions for Interns
### Principal Architect Interview Sheet — 0 to 1 Year Experience
---

> **Format:** Scenario-based questions testing conceptual understanding, reasoning, and correct command usage.
> Topics: stash, rebase, merge, cherry-pick, bisect, reflog, hotfix, grep, and more.

---

## Section 1 — Git Stash

---

**Q1. You're mid-way through a bug fix on `feature/login` when your lead asks you to urgently review code on `main`. You can't commit half-done work. What do you do?**

**Answer:**
Use `git stash` to temporarily save your uncommitted changes without making a commit.

```bash
git stash
git checkout main
# do your review
git checkout feature/login
git stash pop
```

`git stash` shelves your working directory changes. `stash pop` brings them back and removes the stash entry. Think of it as a clipboard for your half-done work.

---

**Q2. You stashed your work yesterday, did two more stashes today, and now you need to get back a specific old stash — not the latest one. How?**

**Answer:**
Use `git stash list` to view all stashes, then `git stash apply stash@{2}` to apply a specific one.

```bash
git stash list
# Output:
# stash@{0}: WIP on feature/login: abc1234 Add input validation
# stash@{1}: WIP on feature/login: abc1234 Half-done CSS
# stash@{2}: WIP on main: def5678 Yesterday's fix

git stash apply stash@{2}
```

`apply` keeps the stash in the list. Use `stash pop` if you want to apply AND remove it in one step.

---

**Q3. What is the difference between `git stash apply` and `git stash pop`? When would you prefer one over the other?**

**Answer:**

| Command | What it does |
|---|---|
| `git stash apply` | Applies the stash but **keeps** it in the stash list |
| `git stash pop` | Applies the stash and **removes** it from the stash list |

Use `apply` when you want to apply the same stash to multiple branches (e.g., testing on two branches). Use `pop` when you're done and just want to restore and move on.

---

**Q4. You stashed some changes but now realize you don't need them at all. How do you clean up your stash list?**

**Answer:**

```bash
# Drop a specific stash
git stash drop stash@{0}

# Drop ALL stashes at once
git stash clear
```

Be careful with `stash clear` — it's irreversible. Prefer `drop` when you're sure about a specific one.

---

## Section 2 — git grep

---

**Q5. A production bug mentions something about a function called `calculateTax`. The codebase has 200+ files. How do you quickly find every file where this function is referenced, without leaving the terminal?**

**Answer:**

```bash
git grep "calculateTax"
```

This searches through all tracked files in the repo instantly. It's faster than `grep -r` because it only looks at files Git knows about and skips `node_modules`, build folders, etc. by default.

```bash
# To also see line numbers:
git grep -n "calculateTax"

# Search only in .js files:
git grep "calculateTax" -- "*.js"
```

---

**Q6. A teammate asks: "Why use `git grep` instead of just `grep -r`?" What do you say?**

**Answer:**
`git grep` is aware of the Git index — it only searches files tracked by Git, so it automatically skips ignored directories like `node_modules/`, `dist/`, `.env`, etc. It's also significantly faster on large repos because it leverages Git's internal object storage. `grep -r` blindly searches everything on disk, including files you don't care about.

---

## Section 3 — Branching & Hotfix

---

**Q7. Your team follows Git Flow. A critical bug is found in production (on `main`). Your `develop` branch has 3 unfinished features that must NOT go to production. Walk me through exactly what you do.**

**Answer:**
Create a `hotfix` branch directly off `main`, fix the bug, then merge it back to both `main` AND `develop`.

```bash
# Step 1: Branch off main (not develop!)
git checkout main
git checkout -b hotfix/payment-crash

# Step 2: Fix the bug, then commit
git add .
git commit -m "fix: resolve null pointer in payment processor"

# Step 3: Merge into main and tag it
git checkout main
git merge --no-ff hotfix/payment-crash
git tag -a v1.0.1 -m "Hotfix: payment crash"

# Step 4: Also merge into develop so it gets the fix too
git checkout develop
git merge --no-ff hotfix/payment-crash

# Step 5: Delete the hotfix branch
git branch -d hotfix/payment-crash
```

The `--no-ff` flag preserves the merge commit so the history clearly shows a hotfix was applied.

---

**Q8. Why should a hotfix branch always be created from `main` (or `master`) and NOT from `develop`?**

**Answer:**
Because `develop` contains unreleased, possibly unstable features that haven't been tested for production. If you branch off `develop`, your hotfix will accidentally carry all that unfinished work into production. By branching from `main`, you get a clean snapshot of exactly what is live — nothing more.

---

## Section 4 — git merge vs git rebase

---

**Q9. Your `feature/search` branch is 5 commits behind `main`. A teammate says "just rebase it." Another says "just merge it." Explain the difference — what does each actually do to your commit history?**

**Answer:**

**Merge** creates a new "merge commit" that joins the two branch histories. Your original commits stay as-is.

```
main:    A - B - C - M  (M = merge commit)
                    /
feature: D - E ----
```

**Rebase** replays your feature commits on top of the latest `main` as if you had started from there. History looks linear and clean.

```
Before rebase:       After rebase:
main:  A - B - C    main:  A - B - C - D' - E'
feature: A - D - E  (D and E are rewritten as D', E')
```

Use **merge** for shared/public branches. Use **rebase** to clean up your local feature branch before opening a pull request.

---

**Q10. When should you NEVER use `git rebase`? Why?**

**Answer:**
Never rebase commits that have already been pushed to a shared/public branch (e.g., `main`, `develop`). Rebase rewrites commit history (new SHA hashes). If others have pulled those original commits, rebasing creates a diverged history that causes serious merge conflicts for your teammates. The golden rule: **rebase only local, unshared commits.**

---

**Q11. You rebased your feature branch and now have a conflict in one file. Git has paused mid-rebase. What are your options?**

**Answer:**

```bash
# Option 1: Resolve the conflict, then continue
# Edit the conflicted file, then:
git add conflicted-file.js
git rebase --continue

# Option 2: Skip this commit entirely (rarely used)
git rebase --skip

# Option 3: Panic mode — abort and go back to where you started
git rebase --abort
```

`--abort` is your safety net. It resets your branch to exactly where it was before you ran rebase.

---

## Section 5 — git cherry-pick

---

**Q12. Your teammate fixed a critical bug on their branch `fix/csrf-token`. That branch isn't ready to merge yet (it has other WIP changes). But you urgently need just that one bug-fix commit in your branch. What do you do?**

**Answer:**
Use `git cherry-pick` to copy just that one commit into your current branch.

```bash
# First, find the commit hash
git log fix/csrf-token --oneline
# Output: a3f9c21 fix: resolve CSRF token mismatch

# Cherry-pick it into your current branch
git cherry-pick a3f9c21
```

Cherry-pick creates a **new commit** on your branch with the same changes but a different hash. The original commit on `fix/csrf-token` is untouched.

---

**Q13. What's the risk of overusing `git cherry-pick` across branches?**

**Answer:**
Cherry-pick duplicates commits — the same change exists with two different hashes in two branches. When those branches eventually merge, Git may not recognize they introduced the same change, leading to **duplicate commits** or **merge conflicts**. It's a tactical tool, not a workflow. Use it sparingly, and only when a full merge or rebase isn't appropriate.

---

## Section 6 — git bisect

---

**Q14. A bug was introduced sometime in the last 100 commits, but nobody knows when. How do you find the exact commit that broke things — without manually checking each commit?**

**Answer:**
Use `git bisect` — it does a binary search through your commit history.

```bash
# Start bisect
git bisect start

# Tell Git the current commit is bad
git bisect bad

# Tell Git a known good commit (e.g., last week's stable tag)
git bisect good v2.0.0

# Git will now checkout a middle commit. Test it, then tell Git:
git bisect good   # if this commit is fine
# OR
git bisect bad    # if the bug exists here

# Repeat until Git identifies the first bad commit
# When done:
git bisect reset
```

Git halves the search space each time. 100 commits → found in ~7 steps.

---

**Q15. Can you automate `git bisect` so you don't have to manually test each step?**

**Answer:**
Yes! If you have a test script that exits with `0` for pass and non-zero for fail, you can run:

```bash
git bisect start
git bisect bad HEAD
git bisect good v2.0.0
git bisect run npm test
# OR
git bisect run ./scripts/check-bug.sh
```

Git will automatically run your script at each step and determine good/bad by the exit code. Fully automated debugging.

---

## Section 7 — git reflog

---

**Q16. You accidentally ran `git reset --hard HEAD~3` and lost 3 commits. Your teammate says "don't panic, use reflog." What does that mean?**

**Answer:**
`git reflog` records every time your `HEAD` moved — including resets, checkouts, and rebases. Even after a hard reset, the commits aren't gone yet (just unreferenced).

```bash
# See the history of where HEAD has been
git reflog
# Output:
# abc1234 HEAD@{0}: reset: moving to HEAD~3
# def5678 HEAD@{1}: commit: Add user profile page
# ...

# Recover by resetting back to before the accident
git reset --hard def5678
```

Reflog is your time machine. Entries are kept for ~90 days by default.

---

**Q17. What's the difference between `git log` and `git reflog`?**

**Answer:**

| `git log` | `git reflog` |
|---|---|
| Shows the commit history of the current branch | Shows the history of WHERE your HEAD has been |
| Only shows reachable commits | Shows ALL movements, including after resets |
| Shared — same for everyone who clones | Local only — exists only on your machine |
| Used for understanding project history | Used for recovering lost work |

---

## Section 8 — Reset, Revert & Clean

---

**Q18. What's the difference between `git reset` and `git revert`? When would you use each?**

**Answer:**

**`git reset`** moves the branch pointer backwards, effectively "un-doing" commits. It rewrites history.

```bash
git reset --soft HEAD~1   # Undo commit, keep changes staged
git reset --mixed HEAD~1  # Undo commit, keep changes unstaged (default)
git reset --hard HEAD~1   # Undo commit, DISCARD all changes
```

**`git revert`** creates a NEW commit that undoes the changes of a previous commit. History is preserved.

```bash
git revert a3f9c21
```

**Rule of thumb:** Use `reset` on local/unpushed commits. Use `revert` on public/shared branches — it's safe because it doesn't rewrite history.

---

**Q19. You have a bunch of untracked build files cluttering your working directory. How do you remove them quickly without touching your actual source code?**

**Answer:**

```bash
# Dry run first — see what WOULD be deleted
git clean -n

# Actually delete untracked files
git clean -f

# Delete untracked files AND untracked directories
git clean -fd

# Also remove ignored files (build artifacts, etc.)
git clean -fdx
```

Always do a dry run (`-n`) first. `git clean` is permanent — there's no undo.

---

## Section 9 — Remote & Collaboration

---

**Q20. You pushed a commit to `main` by mistake (let's say the wrong branch). Your team has NOT pulled it yet. How do you fix it?**

**Answer:**

```bash
# Undo the last commit locally (keep changes staged)
git reset --soft HEAD~1

# Force push to overwrite remote (only safe because nobody pulled yet!)
git push origin main --force
```

This is one of the rare safe uses of `--force`. Communicate with your team BEFORE doing this. If even one person has pulled, use `git revert` instead to avoid rewriting shared history.

---

**Q21. What is `git fetch` vs `git pull`? When would you use one over the other?**

**Answer:**

**`git fetch`** downloads changes from the remote but does NOT touch your working directory or local branches.

**`git pull`** = `git fetch` + `git merge` (or rebase) — it downloads AND integrates changes immediately.

```bash
# Just check what's new on remote, no changes to your code
git fetch origin

# Download AND merge into your current branch
git pull origin main
```

Prefer `git fetch` when you want to inspect what changed before integrating. `git pull` is fine for routine syncing when you trust the incoming changes.

---

**Q22. What does `git push origin main --force-with-lease` do, and why is it safer than `--force`?**

**Answer:**
`--force-with-lease` only force-pushes if no one else has pushed new commits to the remote since you last fetched. If someone else has pushed in the meantime, Git refuses and warns you.

`--force` blindly overwrites whatever is on the remote — dangerous if a teammate just pushed.

```bash
# Safe force push
git push origin main --force-with-lease

# Dangerous — overwrites blindly
git push origin main --force
```

Always prefer `--force-with-lease` over `--force` when rewriting shared history is unavoidable.

---

## Section 10 — Tags & History

---

**Q23. Your team wants to mark the `v2.0.0` release in Git history. What command do you use, and what's the difference between a lightweight and an annotated tag?**

**Answer:**

```bash
# Lightweight tag (just a pointer, no metadata)
git tag v2.0.0

# Annotated tag (recommended for releases — stores tagger, date, message)
git tag -a v2.0.0 -m "Release version 2.0.0"

# Push tags to remote (tags don't push automatically)
git push origin v2.0.0
# OR push all tags
git push origin --tags
```

**Annotated tags** are preferred for releases because they store metadata and are listed in `git describe`. Lightweight tags are fine for personal bookmarks.

---

## Section 11 — Config & Aliases

---

**Q24. You're setting up Git on a new machine. What are the first two config commands you run?**

**Answer:**

```bash
git config --global user.name "Your Name"
git config --global user.email "you@company.com"
```

These are embedded in every commit you make. Getting them wrong means your commits show up under the wrong identity in GitHub/GitLab. Always set these first.

---

**Q25. You type `git status` dozens of times a day. How do you create a Git alias to shorten it to `git st`?**

**Answer:**

```bash
git config --global alias.st status
# Now "git st" works like "git status"

# Other useful aliases:
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.lg "log --oneline --graph --decorate --all"
```

Aliases are stored in `~/.gitconfig` and work across all your repos.

---

## Section 12 — Conceptual & Critical Thinking

---

**Q26. What is a detached HEAD state? How does it happen, and how do you get out of it?**

**Answer:**
Normally, `HEAD` points to a branch name (e.g., `main`). A **detached HEAD** means `HEAD` points directly to a commit hash instead of a branch. Any commits you make won't belong to any branch and can be lost.

**How it happens:**
```bash
git checkout a3f9c21   # Checking out a specific commit, not a branch
git checkout v1.0.0    # Checking out a tag
```

**How to get out:**
```bash
# Option 1: Go back to a branch
git checkout main

# Option 2: Save your detached work as a new branch first
git checkout -b my-experimental-work
```

---

**Q27. What is the `.gitignore` file and why does it matter? Give two examples of things you'd always put in it.**

**Answer:**
`.gitignore` tells Git which files/folders to never track. This keeps secrets, build artifacts, and machine-specific files out of your repository.

Common entries:

```
# Dependencies
node_modules/

# Environment secrets
.env
.env.local

# Build output
dist/
build/

# OS files
.DS_Store
Thumbs.db
```

If `.env` (containing API keys or passwords) gets committed and pushed, it can be a serious security incident — even if you delete it later, it stays in Git history.

---

**Q28. What's the difference between `git merge --ff`, `--no-ff`, and `--squash`?**

**Answer:**

```bash
# Fast-forward (default when possible): moves pointer, no merge commit
git merge --ff feature/button

# No fast-forward: always creates a merge commit even if FF is possible
git merge --no-ff feature/button

# Squash: combines all feature commits into ONE staged change (you commit it manually)
git merge --squash feature/button
git commit -m "feat: add submit button"
```

| Option | Use case |
|---|---|
| `--ff` | Keeping history clean on simple updates |
| `--no-ff` | Preserving the fact that a feature branch existed |
| `--squash` | Collapsing messy WIP commits into one clean commit before merging |

---

**Q29. Your teammate says "I'll just force push to fix it." What questions would you ask before letting them proceed?**

**Answer:**
This is about thinking before acting. Good answers include:

1. **Has anyone else pulled from that branch?** If yes, their local history will diverge — this will cause problems for everyone.
2. **Is it a shared/protected branch like `main` or `develop`?** Force pushing to protected branches should be blocked entirely.
3. **Can we use `git revert` instead?** It achieves the goal without rewriting history.
4. **Are you using `--force-with-lease`?** Safer than bare `--force`.
5. **Have you backed up the current state?** `git reflog` or create a temporary branch first.

The answer is almost always: don't force push to shared branches. Find a safer alternative.

---

**Q30. Walk me through what happens step-by-step when you run `git commit -m "fix: typo"`.**

**Answer:**
This tests whether you understand Git internals, not just commands.

1. Git takes a snapshot of everything in the **staging area** (index).
2. It creates a **tree object** representing the directory structure.
3. It creates a **commit object** containing: the tree hash, parent commit hash, author, timestamp, and your message.
4. All these objects are stored in `.git/objects/` as compressed, SHA-1 hashed files.
5. The current **branch pointer** (e.g., `refs/heads/main`) is updated to point to this new commit hash.
6. `HEAD` continues to point to the branch, which now points to the new commit.

Nothing is sent to the remote. The commit only lives locally until you `git push`.

---

## Quick Reference Cheat Sheet

| Scenario | Command |
|---|---|
| Save uncommitted work temporarily | `git stash` |
| List all stashes | `git stash list` |
| Apply a specific stash | `git stash apply stash@{n}` |
| Apply and delete latest stash | `git stash pop` |
| Search code in all tracked files | `git grep "pattern"` |
| Replay feature branch on top of main | `git rebase main` |
| Copy one commit to current branch | `git cherry-pick <hash>` |
| Find which commit introduced a bug | `git bisect start / good / bad` |
| Recover lost commits | `git reflog` |
| Undo a pushed commit safely | `git revert <hash>` |
| Remove untracked files | `git clean -fd` |
| Create a release tag | `git tag -a v1.0.0 -m "..."` |
| See where HEAD has been | `git reflog` |
| Safe force push | `git push --force-with-lease` |

---

*Prepared by: Principal Architect | Internal Intern Evaluation — Git Fundamentals*
