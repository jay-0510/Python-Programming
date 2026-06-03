# Git Interview Questions — Part 3 (Final)
### Principal Architect Interview Sheet — The Gaps That Trip Up Interns
---

> **Topics:** `git diff` · `git log` advanced · `git blame` · `git commit --amend` · Merge Conflict Resolution
> Commit Message Conventions · `git submodules` · Pre-commit Hooks · `.gitattributes`
>
> This is the wrap-up sheet. After Parts 1, 2, and 3 — Git is fully covered.

---

## Section 1 — git diff

---

**Q1. You've edited 3 files but haven't staged anything yet. How do you see exactly what changed line by line before staging?**

**Answer:**

```bash
git diff
```

This shows changes in your **working directory** that are NOT yet staged. The output looks like:

```diff
- const timeout = 3000;     ← removed line (red)
+ const timeout = 5000;     ← added line (green)
```

Key variants every intern must know:

```bash
# See changes in working directory (unstaged)
git diff

# See changes that ARE staged (ready to commit)
git diff --staged
# (alias: git diff --cached — same thing)

# Compare two branches
git diff main..feature/dark-mode

# Compare a specific file only
git diff main..feature/dark-mode -- src/app.js

# Compare two commits
git diff a3f9c21..d84f321

# Just see WHICH files changed, not the full diff
git diff --name-only main..feature/dark-mode
```

**The most common intern mistake:** Running `git diff` after `git add` and seeing nothing. That's because staged changes move out of `git diff` scope — use `git diff --staged` to see them.

---

**Q2. You're about to raise a PR. How do you do a quick self-review of everything your branch changed compared to `main` before submitting?**

**Answer:**

```bash
# See all line-level changes your branch introduces vs main
git diff main..HEAD

# Just see the list of files you touched
git diff --name-only main..HEAD

# See a summary: files changed, insertions, deletions
git diff --stat main..HEAD
# Output:
# src/auth/login.js   | 24 +++++++++------
# src/styles/app.css  |  8 +++--
# 2 files changed, 32 insertions(+), 14 deletions(-)
```

This is a habit every good engineer develops — a personal review pass before handing code to teammates. It often catches debug logs, commented-out code, or accidental changes you forgot about.

---

## Section 2 — git log Advanced

---

**Q3. You know the commit message contained the word "payment". How do you find it without scrolling through 500 commits?**

**Answer:**

```bash
# Search commit messages by keyword
git log --grep="payment"

# Case-insensitive search
git log --grep="payment" -i

# One-liner output for quick scanning
git log --grep="payment" --oneline
```

This is `git log --grep` — different from `git grep` (which searches file contents). Here you're searching **commit messages**.

---

**Q4. How do you visualize the full branch and merge history of a repo in the terminal — without a GUI tool?**

**Answer:**

```bash
git log --oneline --graph --decorate --all
```

Output looks like:

```
* a3f9c21 (HEAD -> main) fix: resolve payment crash
*   d84f321 Merge branch 'feature/dark-mode'
|\
| * 7bc4120 feat: add dark mode toggle
| * 3de9f88 feat: dark mode CSS variables
|/
* 1ac8934 feat: user profile page
```

This single command tells you everything: branch structure, merge points, HEAD position, tags. Make it an alias:

```bash
git config --global alias.tree "log --oneline --graph --decorate --all"
# Now just type: git tree
```

---

**Q5. A bug was introduced "sometime last week." How do you filter `git log` by date and by a specific author to narrow it down?**

**Answer:**

```bash
# Filter by date range
git log --since="2024-01-15" --until="2024-01-22" --oneline

# Filter by author
git log --author="Riya" --oneline

# Filter by file — see all commits that touched a specific file
git log --oneline -- src/auth/login.js

# Combine them all
git log --since="1 week ago" --author="Riya" --oneline -- src/auth/login.js
```

This is how senior engineers do rapid forensic debugging. Combining `--author`, `--since`, and a file path gets you to the guilty commit in seconds.

---

**Q6. How do you see the full diff of what a specific commit changed — not just the message?**

**Answer:**

```bash
# Show full diff of a specific commit
git show a3f9c21

# Show only the files it touched
git show a3f9c21 --name-only

# Show the diff of the most recent commit
git show HEAD

# Show the diff of 3 commits ago
git show HEAD~3
```

`git show` is your magnifying glass on a single commit. Use it constantly during code reviews and debugging.

---

## Section 3 — git blame

---

**Q7. A production bug is traced back to a specific line in `auth/login.js`. How do you find out who wrote that line, when, and in which commit?**

**Answer:**

```bash
git blame src/auth/login.js
```

Output:

```
a3f9c21 (Riya Sharma  2024-01-18 11:32:04 +0530 42) const token = req.headers['x-auth-token'];
d84f321 (Arjun Mehta 2024-01-10 09:15:33 +0530 43) if (!token) return res.status(401).send('Unauthorized');
```

Each line shows: **commit hash · author · date · line number · code**.

```bash
# Blame a specific line range only (lines 40–55)
git blame -L 40,55 src/auth/login.js

# Ignore whitespace changes (so reformatting doesn't show as blame)
git blame -w src/auth/login.js

# See the full commit for any blame line
git show a3f9c21
```

**Important:** `git blame` is a debugging tool, not a blame-assignment tool. The goal is to find context — "why was this written this way?" — not to point fingers.

---

**Q8. You ran `git blame` and the entire file shows the same person who did a "formatting" commit — so the real authors are hidden. How do you fix this?**

**Answer:**
Use `-C` (detect code moved/copied) or `--ignore-rev` to skip cosmetic commits:

```bash
# Ignore a specific commit (e.g., the bulk formatting commit)
git blame --ignore-rev d84f321 src/auth/login.js

# Or create a file listing all bulk commits to always ignore
echo "d84f321" >> .git-blame-ignore-revs
echo "7bc4120" >> .git-blame-ignore-revs

git blame --ignore-revs-file .git-blame-ignore-revs src/auth/login.js

# Make it permanent for the repo (commit this file)
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

GitHub and GitLab also honor `.git-blame-ignore-revs` automatically if you commit it to the repo root.

---

## Section 4 — git commit --amend

---

**Q9. You just committed with the message "wip" by mistake. The commit hasn't been pushed yet. How do you fix the message?**

**Answer:**

```bash
git commit --amend -m "feat: add user authentication flow"
```

`--amend` rewrites the last commit. Since it rewrites history (new commit hash), it's only safe on commits you haven't pushed yet.

```bash
# Amend message AND open editor for more control
git commit --amend
# Opens your default editor — edit the message, save and close
```

---

**Q10. You committed, then realized you forgot to include one file. How do you add it to the previous commit without creating a new commit?**

**Answer:**

```bash
# Stage the forgotten file
git add src/forgot-this-file.js

# Amend the last commit — adds the staged file to it
git commit --amend --no-edit
# --no-edit keeps the existing commit message unchanged
```

The result is one clean commit with all the right files — not two commits where one says "oops, forgot file."

---

**Q11. You amended a commit that was already pushed to a feature branch (not `main`). Now `git push` fails. What do you do and why?**

**Answer:**
After amend, your local branch and remote branch have **diverged** (different commit hashes for the same logical change). Git refuses a normal push.

```bash
# Force push with the safety net
git push origin feature/auth --force-with-lease
```

`--force-with-lease` checks that nobody else pushed to the branch since you last fetched. If someone did, it refuses — protecting their work.

**Rule:** Amending + force-push is acceptable on your own feature branch. Never amend commits on `main`, `develop`, or any shared branch.

---

## Section 5 — Merge Conflict Resolution (Hands-On)

---

**Q12. You ran `git merge feature/dark-mode` and Git says there's a conflict in `src/app.js`. Walk me through exactly what you do, step by step.**

**Answer:**

**Step 1 — Understand what Git shows you:**
```bash
git status
# both modified: src/app.js
```

**Step 2 — Open the conflicted file. You'll see conflict markers:**
```javascript
<<<<<<< HEAD
const theme = 'light';        // ← your current branch's version
=======
const theme = 'dark';         // ← incoming branch's version
>>>>>>> feature/dark-mode
```

**Step 3 — Decide what the file SHOULD look like. Edit it:**
```javascript
// Option A: Keep yours
const theme = 'light';

// Option B: Keep theirs
const theme = 'dark';

// Option C: Keep both (often the right answer)
const theme = userPreference || 'light';
```

Remove ALL the `<<<<<<<`, `=======`, `>>>>>>>` markers. The file must be clean valid code.

**Step 4 — Mark as resolved and complete the merge:**
```bash
git add src/app.js
git commit
# Git auto-fills a merge commit message — save and close
```

**Step 5 — Verify:**
```bash
git log --oneline --graph
# You should see the merge commit joining the two branches
```

---

**Q13. You're mid-merge and things are going very wrong — conflicts everywhere and you don't understand what's happening. What's the safest move?**

**Answer:**

```bash
git merge --abort
```

This cancels the merge entirely and restores your branch to exactly where it was before you ran `git merge`. No damage done.

Same escape hatches exist for rebase and cherry-pick:
```bash
git rebase --abort
git cherry-pick --abort
```

**The lesson:** Always know your abort command before starting a complex merge. It's your emergency exit.

---

**Q14. What is `git mergetool` and when would you use it over manually editing conflict markers?**

**Answer:**
`git mergetool` launches a visual 3-panel diff editor to resolve conflicts — showing: YOUR version (left), the ORIGINAL (center), and THEIR version (right).

```bash
# Launch the default merge tool
git mergetool

# Use a specific tool
git mergetool --tool=vimdiff
git mergetool --tool=vscode
```

Configure VS Code as your merge tool permanently:
```bash
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

Use `mergetool` when:
- There are many conflicted files
- The conflict is complex and context from both sides matters
- You want a side-by-side view rather than reading raw markers

Use manual editing when:
- There are only 1–2 simple conflicts
- You know exactly which version to keep

---

**Q15. After resolving merge conflicts and committing, a teammate says "the conflict was resolved wrong — you kept the wrong version." How do you undo the merge commit?**

**Answer:**

```bash
# Undo the merge commit but keep the changes staged
git reset --soft HEAD~1

# OR — undo the merge commit completely (nuclear option)
git reset --hard HEAD~1
```

If the merge was already pushed:
```bash
# Safe for shared branches — creates a new "undo" commit
git revert -m 1 HEAD
# -m 1 tells Git which parent to revert to (1 = the branch you merged INTO)
git push origin main
```

`revert` is always safer than `reset` on shared branches because it preserves history.

---

## Section 6 — Commit Message Conventions

---

**Q16. Why does a commit message like "fixed stuff" make a Principal Architect wince? What's the right way to write commit messages?**

**Answer:**
Bad commit messages make `git log` useless. When debugging at 2 AM, "fixed stuff" tells you nothing. You have to open each commit and read the diff to understand what changed.

**The standard: Conventional Commits format**

```
<type>(<scope>): <short summary>

[optional body — explain WHY, not WHAT]

[optional footer — issue references, breaking changes]
```

**Types:**

| Type | When to use |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `chore` | Maintenance (deps, config) — no production code change |
| `docs` | Documentation only |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Code restructure — no feature or fix |
| `test` | Adding or fixing tests |
| `perf` | Performance improvement |
| `ci` | CI/CD pipeline changes |

**Good examples:**
```
feat(auth): add JWT refresh token support
fix(payment): resolve null pointer on failed transactions
chore(deps): upgrade lodash to 4.17.21
docs(readme): update local setup instructions
```

**Why it matters beyond readability:** Tools like `semantic-release` and `standard-version` auto-generate changelogs and bump version numbers (major/minor/patch) based on these prefixes. `feat` → minor bump, `fix` → patch bump, `feat!` or `BREAKING CHANGE:` in footer → major bump.

---

**Q17. What is `BREAKING CHANGE` in a commit message and when do you use it?**

**Answer:**
`BREAKING CHANGE` in the commit footer signals that this commit changes a public API in a way that is not backward compatible — existing consumers of your code WILL break.

```
feat(api)!: rename /user endpoint to /users

BREAKING CHANGE: The /user endpoint has been renamed to /users.
All clients must update their API calls. The old endpoint returns 410 Gone.

Closes #142
```

The `!` after the type is a shorthand marker for breaking changes. This tells automated tools to trigger a **major version bump** (e.g., v2.0.0 → v3.0.0).

As an intern, you likely won't introduce breaking changes — but you must recognize the pattern so you don't accidentally rename public APIs without flagging it.

---

## Section 7 — git submodules

---

**Q18. What is a Git submodule? When would a company use it?**

**Answer:**
A submodule is a **Git repo nested inside another Git repo**. The outer repo stores a pointer (a specific commit hash) to the inner repo — not the inner repo's actual files.

**Real-world use cases:**
- A shared `design-system` component library used by 5 different product repos
- A `common-utils` library shared between frontend and backend repos
- Including a third-party library you need to track at a specific version

```
my-app/               ← outer repo
├── src/
├── .gitmodules       ← config file listing submodules
└── libs/
    └── design-system/  ← inner repo (submodule)
```

The outer repo doesn't store `design-system`'s files — it stores "use commit `a3f9c21` of design-system."

---

**Q19. How do you add a submodule to a repo? And how does a new team member get the submodule content after cloning?**

**Answer:**

**Adding a submodule:**
```bash
# Add the submodule
git submodule add https://github.com/org/design-system.git libs/design-system

# This creates a .gitmodules file and a submodule entry
git commit -m "chore: add design-system as submodule"
```

**New member clones the repo — submodule folder is EMPTY by default:**
```bash
# Option A: Clone with submodules in one command
git clone --recurse-submodules https://github.com/org/my-app.git

# Option B: Already cloned but submodule is empty
git submodule init
git submodule update
# OR in one step:
git submodule update --init --recursive
```

**Updating a submodule to the latest version:**
```bash
cd libs/design-system
git pull origin main
cd ../..
git add libs/design-system
git commit -m "chore: update design-system to latest"
```

---

**Q20. What's the most common submodule mistake interns make?**

**Answer:**
Forgetting to initialize and update submodules after cloning — then wondering why a folder is empty or the build is failing.

```bash
# The repo clones fine but this folder is empty:
ls libs/design-system/
# (nothing)

# Fix:
git submodule update --init --recursive
```

The second most common mistake: making changes INSIDE the submodule folder and committing them to the outer repo. Changes inside a submodule must be committed and pushed from within the submodule repo itself, then the outer repo's pointer updated.

```bash
# WRONG: editing submodule files and committing from outer repo
# RIGHT:
cd libs/design-system
git checkout main
# make changes
git commit -m "fix: button hover state"
git push origin main
cd ../..
git add libs/design-system  # updates the pointer
git commit -m "chore: bump design-system to include button fix"
```

---

## Section 8 — Pre-commit Hooks & Husky

---

**Q21. What is a Git hook? Give me a practical example of one your team should have.**

**Answer:**
A Git hook is a script Git automatically runs at specific points in your workflow — before a commit, after a push, before a merge, etc. They live in `.git/hooks/`.

**Most useful hook for teams: `pre-commit`** — runs before every `git commit` completes.

Example: Automatically run linting before every commit so bad code can never be committed.

```bash
# .git/hooks/pre-commit
#!/bin/sh
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Lint failed. Fix errors before committing."
  exit 1  # Non-zero exit = commit is blocked
fi
```

Other useful hooks:

| Hook | Runs when | Common use |
|---|---|---|
| `pre-commit` | Before commit is created | Run linter, formatter |
| `commit-msg` | After you write the message | Enforce Conventional Commits format |
| `pre-push` | Before `git push` | Run test suite |
| `post-merge` | After a merge completes | Run `npm install` if package.json changed |

---

**Q22. The problem with `.git/hooks/` is it's not committed to the repo — so every developer must manually set up hooks. How do teams solve this?**

**Answer:**
**Husky** — a popular npm package that manages Git hooks and commits them to the repo so every developer gets them automatically.

```bash
# Install
npm install husky --save-dev
npx husky init

# Add a pre-commit hook
echo "npm run lint" > .husky/pre-commit

# Add a commit-msg hook (enforce Conventional Commits)
npm install --save-dev @commitlint/cli @commitlint/config-conventional
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

The `.husky/` folder **is committed to the repo** — so when a new developer runs `npm install`, Husky sets up all hooks automatically. No manual steps.

```
my-app/
├── .husky/
│   ├── pre-commit     ← runs lint before every commit
│   └── commit-msg     ← validates commit message format
└── package.json
```

**Why a Principal Architect cares:** Hooks enforce code quality standards at the source — before code reaches CI/CD. It's the first line of defense.

---

## Section 9 — .gitattributes

---

**Q23. Your team has Windows and Mac developers. Some files keep showing up as "modified" in `git status` even though nobody touched them. What's probably happening and how do you fix it?**

**Answer:**
**Line ending mismatch.** Windows uses `CRLF` (`\r\n`) line endings. Mac/Linux use `LF` (`\n`). When a Windows developer checks out a file, Git may convert `LF` → `CRLF`. When they commit, Git sees every line as "changed."

**Fix with `.gitattributes`:**

```bash
# .gitattributes — commit this to the repo root
# Normalize all text files to LF in the repo
* text=auto eol=lf

# Explicitly handle specific types
*.js    text eol=lf
*.ts    text eol=lf
*.json  text eol=lf
*.md    text eol=lf
*.sh    text eol=lf

# Binary files — never touch line endings
*.png   binary
*.jpg   binary
*.pdf   binary
*.zip   binary
```

`text=auto` lets Git detect text vs binary automatically. `eol=lf` normalizes to LF when committed. Commit `.gitattributes` to the repo and ALL developers get consistent behavior regardless of OS.

---

**Q24. Beyond line endings — what else can `.gitattributes` control?**

**Answer:**

```bash
# 1. Tell Git how to diff a specific file type
# e.g., show word-level diff for Markdown
*.md diff=markdown

# 2. Mark files as binary so Git never shows a diff for them
# (stops Git from showing garbage diff output on compiled files)
*.min.js binary
dist/**  binary

# 3. Set merge strategy per file
# "ours" = in conflicts, always keep our version (useful for generated files)
package-lock.json merge=ours

# 4. Export-ignore — exclude files when running git archive
# (don't include test files in a release zip)
tests/    export-ignore
.husky/   export-ignore
*.test.js export-ignore
```

`.gitattributes` is committed to the repo so the rules apply to every developer and every CI environment — not just one machine's Git config.

---

## Section 10 — The .git Folder (Internals)

---

**Q25. A junior dev accidentally deleted the `.git` folder. What just happened to the project?**

**Answer:**
The entire Git history is gone. The `.git` folder IS the repository. Without it, the directory is just a plain folder of files — no history, no branches, no commits, no remotes.

```
.git/
├── HEAD          ← points to current branch ("ref: refs/heads/main")
├── config        ← repo-level git config (remotes, tracking branches)
├── index         ← the staging area (what's in "git add")
├── objects/      ← ALL commits, trees, blobs stored here (the real data)
│   ├── pack/     ← compressed pack files (efficient storage)
│   └── ab/cd...  ← loose objects (one file per object)
├── refs/
│   ├── heads/    ← local branch pointers (e.g., refs/heads/main)
│   └── tags/     ← tag pointers
└── logs/
    └── HEAD      ← reflog data
```

**Recovery:** If the remote still exists, just re-clone. If it was local-only with no remote — it's gone. This is why `git push` regularly matters.

---

**Q26. What are `ORIG_HEAD`, `MERGE_HEAD`, and `CHERRY_PICK_HEAD`? When do these files appear?**

**Answer:**
These are special files Git creates temporarily inside `.git/` during complex operations:

| File | Created when | Purpose |
|---|---|---|
| `ORIG_HEAD` | Before a merge, rebase, or reset | Saves where HEAD was BEFORE the operation, so you can undo it |
| `MERGE_HEAD` | During an in-progress merge | Points to the commit being merged in |
| `CHERRY_PICK_HEAD` | During an in-progress cherry-pick | Points to the commit being cherry-picked |
| `REBASE_HEAD` | During an in-progress rebase | Points to the commit being replayed |

**Practical use of `ORIG_HEAD`:**
```bash
# You ran a rebase and want to undo it completely
git reset --hard ORIG_HEAD

# You did git merge and want to undo it
git reset --hard ORIG_HEAD
```

`ORIG_HEAD` is your one-step undo for operations that move HEAD significantly.

---

## Section 11 — Rapid Fire (Scenario Judgment)

---

**Q27. A teammate opens a PR with 47 commits — every `console.log`, save, and experiment they did over 2 weeks. As the reviewer, what do you ask them to do before you review?**

**Answer:**
Ask them to **squash** the commits into logical, meaningful groups before the PR is reviewed.

```bash
# Interactive rebase to squash last 47 commits
git rebase -i HEAD~47
# In the editor, change "pick" to "squash" (or "s") for commits
# to combine into the one above them

# OR — squash merge when merging the PR
# (GitHub/GitLab "Squash and Merge" button does this automatically)
```

The goal: the final merged history should tell a clear story. Each commit should be a logical unit — "add dark mode toggle", "add dark mode persistence", not "wip", "more wip", "fix", "fix2", "FINALLY WORKS".

---

**Q28. You're onboarding to a new company. It's your first day. What are the first 5 Git-related things you check or set up?**

**Answer:**
This tests whether an intern thinks systematically:

```bash
# 1. Set your identity correctly
git config --global user.name "Your Name"
git config --global user.email "you@company.com"

# 2. Check which branching strategy the team uses
# (read CONTRIBUTING.md, ask the tech lead — Git Flow? Trunk-based?)

# 3. Set up SSH key for GitHub/GitLab
ssh-keygen -t ed25519 -C "you@company.com"
# Add public key to GitHub Settings → SSH Keys

# 4. Clone the repo and check its remote setup
git clone git@github.com:org/project.git
git remote -v
git branch -a  # understand the branch structure

# 5. Check for .gitattributes and .husky setup
cat .gitattributes
ls .husky/
npm install  # sets up Husky hooks if present
```

Bonus: check if `git lfs` is needed (`cat .gitattributes | grep lfs`).

---

**Q29. What is `git shortlog` and when is it useful?**

**Answer:**

```bash
git shortlog -sn
# Output:
#   142  Riya Sharma
#    89  Arjun Mehta
#    34  Priya Patel
#    12  You (intern)
```

`-s` = summary (just counts), `-n` = sorted by number of commits.

Useful for:
- Generating contributor lists for release notes
- Understanding who owns which parts of the codebase (combine with `git log -- path/`)
- A quick team contribution overview

```bash
# See full commit messages grouped by author
git shortlog

# Shortlog for only the last 3 months
git shortlog --since="3 months ago" -sn
```

---

**Q30. Final Wrap-Up: You're about to push code that goes to production. List your personal 5-step pre-push checklist using Git commands.**

**Answer:**
A mature answer shows process discipline — something a Principal Architect looks for even in interns:

```bash
# 1. Check you're on the right branch
git branch
git status

# 2. Self-review everything your branch changed vs main
git diff main..HEAD --stat
git diff main..HEAD

# 3. Check your commit history reads clearly and follows conventions
git log main..HEAD --oneline
# All messages should be: feat/fix/chore: description

# 4. Make sure your branch is up to date with main (no surprises)
git fetch origin
git log HEAD..origin/main --oneline
# If there are new commits on main, rebase or merge first

# 5. Run tests one final time before pushing
npm test   # or whatever the test command is
git push origin feature/your-branch --force-with-lease
```

This shows you're not just someone who knows commands — you're someone who thinks about quality and consequence before acting. That's what separates a good engineer from someone who just writes code.

---

## Master Cheat Sheet — All 3 Parts Combined

| Topic | Key Commands | Part |
|---|---|---|
| Stash | `git stash`, `stash list`, `stash apply`, `stash pop`, `stash drop` | 1 |
| Search code | `git grep "pattern"` | 1 |
| Rebase | `git rebase main`, `--continue`, `--abort` | 1 |
| Cherry-pick | `git cherry-pick <hash>` | 1 |
| Find bad commit | `git bisect start/good/bad/run` | 1 |
| Recover lost work | `git reflog`, `git reset --hard <hash>` | 1 |
| Undo safely | `git revert <hash>` | 1 |
| Remove untracked | `git clean -fd` | 1 |
| Tags | `git tag -a v1.0.0 -m "..."`, `git push --tags` | 1 |
| PR workflow | branch → commit → push → open PR → review → merge | 2 |
| Git Flow | `feature/*`→`develop`→`release/*`→`main`, `hotfix/*`→`main`+`develop` | 2 |
| Remote setup | `git remote add origin <url>`, `git push -u origin main` | 2 |
| Remote manage | `git remote -v`, `rename`, `set-url`, `remove` | 2 |
| Fork + upstream | `git remote add upstream <url>`, `git fetch upstream` | 2 |
| Clone fast | `git clone --depth 1 --single-branch` | 2 |
| Garbage collect | `git gc`, `git fsck --lost-found` | 2 |
| Large files | `git lfs install`, `lfs track`, `lfs pull` | 2 |
| Diff variants | `git diff`, `--staged`, `main..HEAD`, `--stat`, `--name-only` | 3 |
| Log advanced | `--grep`, `--graph`, `--author`, `--since`, `-- file` | 3 |
| Blame | `git blame -L`, `--ignore-rev` | 3 |
| Amend | `git commit --amend`, `--no-edit` + `push --force-with-lease` | 3 |
| Conflict resolve | edit markers → `git add` → `git commit` / `merge --abort` | 3 |
| Commit format | `feat/fix/chore(scope): message` + `BREAKING CHANGE:` | 3 |
| Submodules | `git submodule add`, `update --init --recursive` | 3 |
| Hooks | `.git/hooks/pre-commit`, Husky + commitlint | 3 |
| Line endings | `.gitattributes` — `* text=auto eol=lf` | 3 |
| Internals | `.git/` structure, `ORIG_HEAD`, `MERGE_HEAD` | 3 |

---

*Prepared by: Principal Architect | Internal Intern Evaluation — Git Complete Series (Part 3 of 3)*
*Parts 1 + 2 + 3 together = comprehensive Git coverage for 0–1 year experience engineers.*
