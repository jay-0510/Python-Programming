# 🐧 Linux Commands — Interview Question Bank
### 35 Questions | Practical Usage · Conceptual Understanding · Reasoning
> **Target Level:** Intern → 2–3 Years Industry Experience  
> **Format:** Every question has a plain-language answer, real-world context, and a follow-up probe.

---

## Table of Contents

| Section | Topic | Questions |
|---------|-------|-----------|
| A | File Viewing & Text Processing | Q1 – Q6 |
| B | File & Directory Operations | Q7 – Q12 |
| C | Permissions & Ownership | Q13 – Q17 |
| D | User Management | Q18 – Q21 |
| E | System Information & Monitoring | Q22 – Q26 |
| F | Search & Comparison | Q27 – Q30 |
| G | Editors — nano & vi | Q31 – Q33 |
| H | Archiving & Compression | Q34 – Q35 |

---

## How to Use This Bank

Three things every answer should demonstrate:
- **What** the command does (syntax + flags)
- **Why** you'd use it over alternatives
- **When** it breaks or has a gotcha worth knowing

---

## Section A — File Viewing & Text Processing

---

### Q1. What does `cat` do, and when should you NOT use it?

**Answer:**

`cat` (short for concatenate) reads one or more files and prints their content to the terminal.

```bash
cat file.txt                  # print a single file
cat file1.txt file2.txt       # print two files back to back
cat -n file.txt               # print with line numbers
cat file1.txt file2.txt > combined.txt  # merge two files into one
```

**When NOT to use it:**
- On large files (logs, CSVs with millions of rows) — it dumps everything at once and floods your terminal. Use `less` instead.
- On binary files — you'll get garbage output that can mess up your terminal encoding.

**Practical use case:**  
You're debugging a config file on a server with no GUI. `cat /etc/nginx/nginx.conf` lets you read it instantly without opening an editor.

> **Probe:** What's the difference between `cat file.txt` and `less file.txt`?  
> `cat` dumps everything at once. `less` lets you scroll up and down — much better for large files.

---

### Q2. What is `echo` and how is it used in scripting?

**Answer:**

`echo` prints text or the value of a variable to the terminal (or a file).

```bash
echo "Hello World"             # prints: Hello World
echo $HOME                     # prints: /home/username
echo "text" > file.txt         # writes text to file (overwrites)
echo "more text" >> file.txt   # appends text to file
echo -n "no newline"           # prints without a newline at the end
```

**Why it matters in scripting:**  
`echo` is the main way to write output, debug variables, and create/append to files inside shell scripts.

```bash
# Real example: write a config value to a file
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=5432" >> .env
```

**Common mistake:** Using `>` when you meant `>>` — single `>` overwrites the entire file. Lost many logs this way.

> **Probe:** What's the difference between `>` and `>>`?  
> `>` overwrites. `>>` appends. If you use `>` on a file that already has content, everything in it is gone.

---

### Q3. How does `grep` work? Explain with 3 practical examples.

**Answer:**

`grep` searches for a pattern (text or regex) inside files or command output. It prints every line that matches.

```bash
# Basic usage
grep "error" app.log            # find all lines with "error" in app.log

# Case-insensitive search
grep -i "error" app.log         # matches ERROR, Error, error

# Search recursively in all files under a directory
grep -r "TODO" ./src/           # find all TODOs in source code

# Show line numbers
grep -n "null" main.py          # shows which lines have "null"

# Invert match — show lines that DON'T match
grep -v "DEBUG" app.log         # filter out debug lines, show rest

# Count matches
grep -c "404" access.log        # how many 404 errors today?

# Pipe usage — grep on live output
tail -f app.log | grep "ERROR"  # watch live logs, show only errors
```

**Why it's used daily:**  
Log analysis, finding which file contains a function, debugging — grep is the Swiss Army knife of text search.

> **Probe:** What does `grep -r "password" .` do and why might it be important in a DevOps/security context?  
> It recursively searches every file in the current directory for the word "password" — useful for auditing if credentials were accidentally committed to source code.

---

### Q4. What is `grep -E` and how does it differ from plain `grep`?

**Answer:**

`grep -E` enables **extended regular expressions (ERE)**, letting you use more powerful pattern matching without escaping special characters.

```bash
# Match lines with either "error" OR "warning"
grep -E "error|warning" app.log

# Match lines starting with a number
grep -E "^[0-9]" data.txt

# Find IP addresses (basic pattern)
grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log
```

**Difference:**  
With plain `grep`, you'd need to escape the `|` with a backslash: `grep "error\|warning"`. `-E` makes the syntax cleaner and is what most people use in practice.

`egrep` is the same as `grep -E` — older systems use `egrep`, but `grep -E` is preferred now.

> **Probe:** How would you use grep to find lines that start with the word "FATAL"?  
> `grep -E "^FATAL" app.log` — the `^` anchors the match to the start of each line.

---

### Q5. Explain the `file` command. Why is it more reliable than checking the file extension?

**Answer:**

`file` reads the actual content of a file and tells you what type it is — it does NOT rely on the file name or extension.

```bash
file document.pdf               # output: document.pdf: PDF document, version 1.6
file image.jpg                  # output: image.jpg: JPEG image data
file script.sh                  # output: script.sh: Bourne-Again shell script, ASCII text
file /bin/ls                    # output: /bin/ls: ELF 64-bit LSB executable
file unknown_file               # identifies it even with no extension
```

**Why it's more reliable than extensions:**  
Anyone can rename `malware.exe` to `report.pdf`. The `file` command reads the **magic bytes** (first few bytes of the file) to identify the real format. This matters in:
- Security checks (is this really a PDF or an executable?)
- Debugging scripts that fail because a file isn't what you think it is
- Working with files transferred across systems with no extensions

> **Probe:** You receive a file named `data` with no extension. How do you figure out what it is?  
> `file data` — it will read the file's magic bytes and tell you whether it's a gzip archive, a text file, a Python script, etc.

---

### Q6. What does `diff` do and how do you read its output?

**Answer:**

`diff` compares two files line by line and shows you what's different between them.

```bash
diff file1.txt file2.txt
```

**Reading the output:**

```
2c2
< Hello World
---
> Hello Linux
```

- `2c2` means: line 2 in file1 was **c**hanged to line 2 in file2
- `<` lines are from file1
- `>` lines are from file2

**Useful flags:**

```bash
diff -u file1.txt file2.txt    # unified format — easier to read (used in git diffs)
diff -i file1.txt file2.txt    # ignore case differences
diff -r dir1/ dir2/            # compare two entire directories recursively
```

**Real use case:**  
Comparing two versions of a config file after a deployment. `diff prod.conf staging.conf` immediately shows what changed.

> **Probe:** What does `diff -u` output look like and where have you seen that format before?  
> Lines with `-` are removed, lines with `+` are added. This is exactly the format git uses when you run `git diff`.

---

## Section B — File & Directory Operations

---

### Q7. Explain `rm` and its flags. What is the most dangerous command a Linux user can run?

**Answer:**

`rm` deletes files. There is no Recycle Bin — once you run `rm`, the file is gone.

```bash
rm file.txt                    # delete a file
rm -i file.txt                 # ask for confirmation before deleting
rm -r folder/                  # delete a folder and everything inside it (recursive)
rm -f file.txt                 # force delete, no error if file doesn't exist
rm -rf folder/                 # force delete folder and all contents — no confirmation
```

**The most dangerous command:**

```bash
rm -rf /                       # deletes EVERYTHING on the system starting from root
```

Modern Linux systems have a `--no-preserve-root` safeguard for this, but `rm -rf /home/username` is still catastrophic. Always double-check the path before running `rm -rf`.

**Safe habit:** Run `ls` on the path first to see what you're about to delete.

```bash
ls /tmp/old_logs/   # confirm what's there
rm -rf /tmp/old_logs/           # then delete
```

> **Probe:** Is there a way to recover a file deleted with `rm`?  
> Not easily. `rm` doesn't move to trash — it unlinks the file from the filesystem. Recovery tools like `extundelete` or `testdisk` may help on ext4, but they're unreliable. Prevention (backups, `-i` flag) is the real answer.

---

### Q8. What does `mv` do? How is it different from `cp`?

**Answer:**

`mv` moves or renames files and directories.

```bash
mv old_name.txt new_name.txt   # rename a file
mv file.txt /tmp/              # move file to /tmp directory
mv folder/ /var/backups/       # move a whole folder
mv -i file.txt /tmp/           # ask before overwriting if file exists at destination
```

**Difference from `cp`:**
- `cp` creates a copy — the original stays
- `mv` moves the file — the original is gone from the source location

```bash
cp report.txt /backup/report.txt   # now you have TWO copies
mv report.txt /backup/report.txt   # now there's only ONE — at /backup/
```

**Practical use case:**  
Renaming a deployed config file before replacing it with a new one:
```bash
mv /etc/app/config.yml /etc/app/config.yml.bak   # backup
mv /tmp/new_config.yml /etc/app/config.yml        # deploy new one
```

> **Probe:** Does `mv` work across different filesystems (e.g., from `/home` to `/mnt/usb`)?  
> Yes, but it behaves differently — across filesystems, `mv` actually does a `cp` + `rm` internally because you can't just relink the file. On the same filesystem, `mv` is instant (just updates a pointer).

---

### Q9. What does `chmod` do? Explain the numeric and symbolic modes.

**Answer:**

`chmod` changes the **permissions** of a file or directory — who can read, write, or execute it.

Linux permissions have three groups:
- **Owner (u)** — the user who owns the file
- **Group (g)** — users in the file's group
- **Others (o)** — everyone else

And three permission types:
- **r** = read (4)
- **w** = write (2)  
- **x** = execute (1)

**Symbolic mode:**

```bash
chmod u+x script.sh            # give the owner execute permission
chmod g-w file.txt             # remove write permission from group
chmod o+r file.txt             # give others read permission
chmod a+x script.sh            # give everyone execute permission (a = all)
```

**Numeric (octal) mode:**

Each group gets a number: r=4, w=2, x=1, sum them up.

```bash
chmod 755 script.sh    # owner: rwx (7), group: r-x (5), others: r-x (5)
chmod 644 file.txt     # owner: rw- (6), group: r-- (4), others: r-- (4)
chmod 600 id_rsa       # owner: rw- (6), group: --- (0), others: --- (0)
chmod 777 file.txt     # everyone can do everything — usually a bad idea
```

**Common real-world numbers:**
| Permission | Use case |
|------------|----------|
| `755` | Scripts, executables |
| `644` | Config files, text files |
| `600` | SSH private keys, secrets |
| `700` | Personal directories |

> **Probe:** Why is `chmod 777` on a web server file a security risk?  
> It means anyone on the system — including other users and processes — can read, modify, or execute the file. An attacker who gains any system access can modify your app files.

---

### Q10. What does `chown` do and how is it different from `chmod`?

**Answer:**

`chown` changes the **owner** (and optionally the group) of a file. `chmod` changes permissions. They work together — ownership determines which permission row applies to you.

```bash
chown alice file.txt             # change owner to alice
chown alice:developers file.txt  # change owner to alice, group to developers
chown :developers file.txt       # change only the group
chown -R alice /var/www/         # change owner of folder AND everything inside it
```

**Why it matters:**  
If a file is owned by root and you're running your app as `www-data`, the app can't write to it no matter what permissions are set — because the permission check uses the owner identity.

**Real example — fixing a deployment issue:**

```bash
# App deployed files owned by root, but nginx runs as www-data
ls -la /var/www/html/
# -rw-r--r-- 1 root root index.html  <-- www-data can't write this

chown -R www-data:www-data /var/www/html/
# Now nginx can write logs, cache, sessions properly
```

> **Probe:** How do you check who owns a file?  
> `ls -la filename` — the third column is the owner, the fourth is the group.

---

### Q11. What does `locate` do and why is it faster than `find`?

**Answer:**

`locate` finds files by searching a **pre-built database** instead of scanning the entire filesystem in real time.

```bash
locate nginx.conf               # find all files named nginx.conf
locate -i "readme"              # case-insensitive search
locate "*.log"                  # find all .log files on the system
locate -n 10 config.yml         # show only first 10 results
```

**Why it's faster than `find`:**  
`find` scans every directory on the filesystem in real time — slow on large systems. `locate` reads from a database file (`/var/lib/mlocate/mlocate.db`) that was built in advance.

**The catch:**  
The database isn't updated in real time. If you created a file 5 minutes ago, `locate` might not know about it yet.

```bash
sudo updatedb    # manually update the database so locate sees new files
```

The database is usually updated automatically once a day by a cron job.

> **Probe:** You just created a file but `locate` can't find it. What do you do?  
> Run `sudo updatedb` to rebuild the database, then try `locate` again. Or use `find` which is always real-time.

---

### Q12. Explain the `man` command. How do you use it effectively?

**Answer:**

`man` shows the **manual page** for any Linux command — full documentation, all flags, examples, and explanations.

```bash
man ls                         # full manual for ls
man grep                       # all grep options explained
man chmod                      # permissions explained in detail
man 5 passwd                   # section 5 = file formats (the /etc/passwd file format)
```

**Navigating inside man:**
- `Space` or `f` — scroll forward a page
- `b` — scroll backward
- `/keyword` — search for a word (like Ctrl+F)
- `n` — jump to next search match
- `q` — quit

**Man sections:**
| Section | Content |
|---------|---------|
| 1 | User commands (most common) |
| 2 | System calls |
| 3 | Library functions |
| 5 | File formats |
| 8 | Admin commands |

**Quick alternative — `--help`:**  
If you just want a quick flag reference, most commands support `--help`:
```bash
ls --help
grep --help
```

`man` is for deep understanding; `--help` is for quick reminders.

> **Probe:** How would you search for all man pages that mention the word "socket"?  
> `man -k socket` — the `-k` flag searches the short descriptions of all man pages (same as `apropos socket`).

---

## Section C — Permissions & Ownership

---

### Q13. What does `ls -la` show? Break down a real output line.

**Answer:**

`ls -l` shows detailed file info. `-a` includes hidden files (files starting with `.`).

```bash
ls -la /home/user/
```

**Sample output:**
```
drwxr-xr-x  5 alice developers 4096 Jan 15 10:22 projects
-rw-r--r--  1 alice developers 1234 Jan 14 09:00 notes.txt
-rwx------  1 alice alice       512 Jan 10 08:30 secret.sh
```

**Breaking down `-rw-r--r-- 1 alice developers 1234 Jan 14 09:00 notes.txt`:**

| Part | Meaning |
|------|---------|
| `-` | File type: `-` = regular file, `d` = directory, `l` = symlink |
| `rw-` | Owner (alice) can: read ✓, write ✓, execute ✗ |
| `r--` | Group (developers) can: read ✓, write ✗, execute ✗ |
| `r--` | Others can: read ✓, write ✗, execute ✗ |
| `1` | Number of hard links |
| `alice` | Owner |
| `developers` | Group |
| `1234` | Size in bytes |
| `Jan 14 09:00` | Last modified time |
| `notes.txt` | Filename |

> **Probe:** What does the `d` at the start of a permissions string mean, and how do you create something with a `d`?  
> `d` means it's a directory. You create directories with `mkdir`. You can never make a regular file show `d` — the type is set by how the filesystem object was created.

---

### Q14. What is the sticky bit and when do you use it?

**Answer:**

The **sticky bit** on a directory prevents users from deleting files they don't own, even if they have write access to the directory.

```bash
chmod +t /shared/              # set sticky bit
chmod 1777 /shared/            # rwxrwxrwx + sticky bit (1 = sticky)
ls -la /                       # /tmp always has the sticky bit
```

**Real example:** `/tmp` has sticky bit set. Everyone can write to `/tmp`, but you can only delete YOUR OWN files there. Without sticky bit, any user could delete anyone else's temporary files.

```
drwxrwxrwt  20 root root  /tmp
          ^-- the 't' means sticky bit is set
```

> **Probe:** What's the difference between the sticky bit on a directory vs an executable file?  
> On directories (modern usage): prevents deletion by non-owners. On executable files (historical): used to keep the program in swap memory after it exited — this is obsolete on modern systems and mostly ignored.

---

### Q15. What are setuid and setgid bits?

**Answer:**

**Setuid (SUID):** When set on an executable, the program runs with the **owner's permissions**, not the user who launched it.

**Setgid (SGID):** When set on an executable, it runs with the **group's permissions**. On a directory, new files inherit the directory's group.

```bash
chmod u+s /usr/bin/passwd      # set SUID
chmod g+s /shared/             # set SGID on directory
ls -la /usr/bin/passwd
# -rwsr-xr-x  root root  /usr/bin/passwd
#    ^-- 's' instead of 'x' means SUID is set
```

**Real example:** The `passwd` command needs to write to `/etc/shadow` (owned by root). Regular users can run `passwd` to change their own password because SUID makes it temporarily run as root — but the command itself safely limits what it lets you do.

**Security note:** SUID files are high-value targets in privilege escalation attacks. In a security audit, `find / -perm -4000` finds all SUID files on the system — unexpected ones are a red flag.

> **Probe:** How do you find all SUID files on a Linux system?  
> `find / -perm -4000 -type f 2>/dev/null` — lists all files with SUID bit set, discarding permission errors.

---

### Q16. What does `umask` do?

**Answer:**

`umask` sets the **default permissions** that are REMOVED when new files and directories are created. It's a mask that subtracts permissions from the maximum.

```bash
umask              # show current umask (e.g., 022)
umask 027          # set new umask for this session
```

**How it works:**
- Default max permissions: files = 666, directories = 777
- With `umask 022`: files get `666 - 022 = 644`, dirs get `777 - 022 = 755`
- With `umask 027`: files get `640`, dirs get `750` (others get nothing)

```bash
umask 022
touch newfile.txt
ls -la newfile.txt
# -rw-r--r-- (644) — others can read, no write
```

**Why it matters:**  
In production environments, `umask 027` is often set so that new files aren't world-readable by default — important for config files and logs containing sensitive data.

> **Probe:** If you set `umask 000`, what permissions will new files get?  
> `666 - 000 = 666 (rw-rw-rw-)` — everyone can read and write. This is rarely appropriate and a security risk.

---

### Q17. What is a symbolic link (symlink) and how do you create one?

**Answer:**

A symbolic link is a pointer (shortcut) to another file or directory. It's like an alias — accessing the symlink accesses the original file.

```bash
ln -s /var/log/nginx/access.log ~/logs/nginx_access.log
# Now you can read ~/logs/nginx_access.log instead of the long path

ls -la ~/logs/
# lrwxrwxrwx nginx_access.log -> /var/log/nginx/access.log
# 'l' at start means it's a symlink
```

**Symlink vs Hard link:**

| | Symlink | Hard Link |
|--|---------|-----------|
| Created with | `ln -s` | `ln` (no -s) |
| Points to | Path | Actual data (inode) |
| If original deleted | Symlink breaks | Data still accessible |
| Cross filesystem | Yes | No |

**Real use case:**  
Multiple app versions installed, but you want `/usr/local/bin/python` to point to whichever version is "current":
```bash
ln -s /usr/local/bin/python3.11 /usr/local/bin/python
# Switch version later:
ln -sf /usr/local/bin/python3.12 /usr/local/bin/python
```

> **Probe:** How do you tell if a file is a symlink without `ls`?  
> `file symlink_name` will say "symbolic link to ..." or use `test -L filename && echo "is symlink"`.

---

## Section D — User Management

---

### Q18. How do you create a new user in Linux? Walk through the full process.

**Answer:**

```bash
# Step 1: Create the user
sudo useradd -m -s /bin/bash alice
# -m: create home directory at /home/alice
# -s /bin/bash: set bash as their shell

# Step 2: Set their password
sudo passwd alice
# It will prompt you to enter and confirm the new password

# Step 3: (Optional) Add user to a group
sudo usermod -aG sudo alice     # give alice sudo access
sudo usermod -aG developers alice  # add to developers group

# Verify the user was created
id alice
# uid=1001(alice) gid=1001(alice) groups=1001(alice),27(sudo)
```

**What `useradd` creates:**
- Entry in `/etc/passwd` (user info)
- Entry in `/etc/shadow` (hashed password)
- Home directory at `/home/alice`
- Default shell configuration files

> **Probe:** What's the difference between `useradd` and `adduser`?  
> `useradd` is the low-level command — you control every option manually. `adduser` (Debian/Ubuntu) is a higher-level script that's more interactive and sets sensible defaults automatically. In production scripts, `useradd` is preferred because it's predictable and non-interactive.

---

### Q19. How do you delete a user? What is the risk of not using the right flags?

**Answer:**

```bash
sudo userdel alice              # delete user but KEEP home directory
sudo userdel -r alice           # delete user AND their home directory + mail spool
```

**The risk of forgetting `-r`:**  
Without `-r`, `/home/alice` stays on disk. The directory now has a dangling UID (no username maps to it anymore). If you later create a new user who happens to get the same UID, they automatically own alice's old files — a security issue.

**Best practice before deleting:**
```bash
# Back up their files first
tar -czf /backup/alice_home.tar.gz /home/alice/

# Lock the account first (disables login without deleting)
sudo usermod -L alice           # lock
sudo usermod -U alice           # unlock later if needed

# Then delete
sudo userdel -r alice
```

> **Probe:** How do you disable a user account without deleting it?  
> `sudo usermod -L alice` — this puts a `!` in front of their hashed password in `/etc/shadow`, making it impossible to log in. The account and files still exist.

---

### Q20. Explain the `passwd` command and where passwords are actually stored.

**Answer:**

`passwd` sets or changes a user's password.

```bash
passwd                         # change YOUR OWN password (prompts for current + new)
sudo passwd alice              # change alice's password (as root, no old password needed)
sudo passwd -l alice           # lock alice's account
sudo passwd -u alice           # unlock alice's account
sudo passwd -e alice           # expire alice's password (force change on next login)
```

**Where passwords are stored:**
- `/etc/passwd` — user info (username, UID, GID, home dir, shell) — world-readable, NO passwords
- `/etc/shadow` — actual hashed passwords — readable only by root

```bash
sudo cat /etc/shadow
# alice:$6$rounds=5000$salt$hashedpassword:19000:0:99999:7:::
# $6$ means SHA-512 hashing
```

**Why the split into two files?**  
In older Linux, passwords were in `/etc/passwd` which is world-readable. Anyone could grab the file and crack the hashes offline. Moving hashed passwords to `/etc/shadow` (root-only) fixed this.

> **Probe:** What does it mean if a user's entry in `/etc/shadow` starts with `!`?  
> The account is locked. The `!` prefix on the hash means authentication will always fail — the user cannot log in.

---

### Q21. What is the `sudo` command and how does it differ from logging in as root?

**Answer:**

`sudo` (Super User DO) lets an authorized user run a single command as root (or another user) without switching to the root account.

```bash
sudo apt update                 # run apt as root
sudo -u postgres psql          # run psql as the postgres user
sudo -i                        # open an interactive root shell
sudo !!                        # run the last command again with sudo
```

**Difference from logging in as root directly:**

| | `sudo command` | `su root` / root login |
|--|----------------|------------------------|
| Scope | One command at a time | Entire session as root |
| Audit trail | Every command logged in `/var/log/auth.log` | Harder to track individual actions |
| Risk | Limited exposure | One mistake damages the whole system |
| Access control | Configured per user in `/etc/sudoers` | Anyone with root password |

**Check who can use sudo:**
```bash
sudo cat /etc/sudoers           # full access control file
sudo -l                        # what can YOU run with sudo?
```

> **Probe:** A developer accidentally ran `sudo rm -rf /var/www/html`. How does `sudo` logging help in a post-incident review?  
> Every `sudo` command is logged with a timestamp, username, and the exact command in `/var/log/auth.log`. You can see exactly what was run, by whom, and when — critical for incident investigation.

---

## Section E — System Information & Monitoring

---

### Q22. What does `df` tell you and how do you use it in production?

**Answer:**

`df` (disk free) shows **disk space usage** for all mounted filesystems.

```bash
df                             # show disk usage (in 512-byte blocks — hard to read)
df -h                          # human-readable: KB, MB, GB
df -h /                        # show only the root filesystem
df -h /var/log                 # show usage for where logs are stored
df -T                          # also show filesystem type (ext4, xfs, etc.)
```

**Sample output:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   38G  9.2G  81% /
tmpfs           2.0G  1.2M  2.0G   1% /dev/shm
/dev/sdb1       200G   45G  145G  24% /var/log
```

**Why it matters in production:**  
A full disk (`Use% = 100%`) stops your application from writing logs, creating temp files, or accepting uploads. Monitoring `df -h` is a standard part of health checks.

**Practical alert threshold:** Investigate at 80%, escalate at 90%.

```bash
# Quick check — show only filesystems above 80% usage
df -h | awk 'NR>1 && $5+0 > 80'
```

> **Probe:** How is `df` different from `du`?  
> `df` shows space at the filesystem level. `du` (disk usage) shows how much space specific files and directories are consuming. `df -h /` tells you the disk is 80% full. `du -sh /*` tells you WHICH directories are eating the space.

---

### Q23. What does `hostname` do and why does it matter in distributed systems?

**Answer:**

`hostname` shows or sets the computer's name on the network.

```bash
hostname                       # show current hostname: e.g., "web-server-01"
hostname -I                    # show all IP addresses of this machine
hostname -f                    # show fully qualified domain name (FQDN): web-server-01.company.com
sudo hostname new-name         # temporarily change hostname (resets on reboot)
```

**To permanently change hostname (Ubuntu/Debian):**
```bash
sudo hostnamectl set-hostname new-server-name
cat /etc/hostname              # verify
```

**Why it matters in distributed systems:**  
- Kubernetes, Docker Swarm, and cloud providers use hostnames to identify nodes
- Log aggregation tools (like ELK Stack, Datadog) tag logs with hostname — when an error occurs, you need to know WHICH server it came from
- In auto-scaling groups, each new instance gets a unique hostname so you can trace behavior to a specific node

> **Probe:** Your application logs show errors but all servers have the same hostname. Why is that a problem?  
> You can't tell which physical or virtual server is causing the issue. In distributed systems, every node should have a unique, meaningful hostname so logs and metrics are traceable to a specific instance.

---

### Q24. What is `ps` and how do you find a specific running process?

**Answer:**

`ps` (process status) shows currently running processes.

```bash
ps                             # show only YOUR processes in current terminal
ps aux                         # show ALL processes from ALL users with details
ps aux | grep nginx            # find the nginx process
ps -ef                         # alternative format, shows parent process IDs
```

**Understanding `ps aux` output:**
```
USER   PID  %CPU %MEM    VSZ   RSS TTY  STAT  TIME  COMMAND
root   1234   0.0  0.1  72396  4096 ?    Ss   0:00  /usr/sbin/sshd
www    5678   1.2  2.3 256000 45000 ?    S    0:30  nginx: worker process
```

| Column | Meaning |
|--------|---------|
| PID | Process ID (use this to kill it) |
| %CPU | CPU usage |
| %MEM | Memory usage |
| STAT | S=sleeping, R=running, Z=zombie |
| COMMAND | What's actually running |

**Finding and killing a process:**
```bash
ps aux | grep "python app.py"  # find the PID
kill 5678                      # graceful stop (SIGTERM)
kill -9 5678                   # force kill (SIGKILL) — use when graceful fails
```

> **Probe:** What's the difference between `kill` and `kill -9`?  
> `kill` (SIGTERM) asks the process to shut down gracefully — it can clean up, close files, finish requests. `kill -9` (SIGKILL) is immediate — the kernel kills it instantly with no cleanup. Always try `kill` first; use `-9` only if the process ignores the first signal.

---

### Q25. What does `top` show and what are the key things to check?

**Answer:**

`top` is a real-time system monitor — CPU, memory, running processes, all updating live.

```bash
top                            # launch top
top -u alice                   # show only alice's processes
top -p 1234                    # monitor only process with PID 1234
```

**Key sections in top's output:**

```
top - 14:23:01 up 5 days, load average: 0.52, 1.23, 0.89
Tasks: 145 total, 2 running, 143 sleeping
%Cpu(s): 12.3 us, 2.1 sy, 0.0 ni, 84.5 id, 1.1 wa
MiB Mem:  7982.0 total, 1245.2 free, 5431.2 used, 1305.6 buff/cache
```

| Metric | What to watch |
|--------|---------------|
| Load average | 1, 5, 15 min avg — above number of CPU cores = overloaded |
| `%Cpu id` | "idle" — if below 10%, CPU is maxed out |
| `wa` | Wait I/O — high value means disk is the bottleneck |
| Memory `used` | If free memory is near zero + high swap usage = memory pressure |

**Useful keys while inside top:**
- `M` — sort by memory usage
- `P` — sort by CPU usage
- `k` — kill a process (type PID when prompted)
- `q` — quit

> **Probe:** Load average is 4.5 on a 2-core machine. What does that mean?  
> The system has more work queued than it can process — 4.5 processes are competing for 2 CPU cores on average over the last minute. The machine is overloaded. Investigate which process is consuming CPU with `P` in top.

---

### Q26. What does the `time` command do and when is it useful?

**Answer:**

`time` measures how long a command takes to run — useful for benchmarking and performance debugging.

```bash
time ls -la /var/log/
time python3 data_processor.py
time find / -name "*.conf"
```

**Sample output:**
```
real    0m3.451s
user    0m1.230s
sys     0m0.082s
```

| Metric | Meaning |
|--------|---------|
| `real` | **Wall clock time** — total time from start to finish (what you actually waited) |
| `user` | CPU time spent in user-space code (your program) |
| `sys` | CPU time spent in kernel-space (system calls: file I/O, network, etc.) |

**Interpreting results:**
- `user + sys` ≈ `real` → Single-threaded, CPU-bound work
- `user + sys` << `real` → Program was waiting (I/O, network, sleep)
- `user + sys` >> `real` → Multi-threaded work (multiple CPUs running in parallel)

**Real use case:**  
Comparing two versions of a script to see which is faster:
```bash
time python3 old_script.py     # real: 12.3s
time python3 new_script.py     # real: 3.1s — 4x improvement confirmed
```

> **Probe:** Your script shows `real: 30s, user: 0.2s, sys: 0.1s`. What does this tell you?  
> The script spent almost all its time waiting — not computing. Most likely it's doing network requests, database queries, or waiting on disk I/O. This is where async programming or caching would help, not CPU optimisation.

---

## Section F — Search & Comparison

---

### Q27. How is `find` different from `locate`? Write a practical `find` command for a real scenario.

**Answer:**

| | `find` | `locate` |
|--|--------|----------|
| Speed | Slower (real-time filesystem scan) | Faster (reads pre-built database) |
| Freshness | Always current | May be up to 24 hours stale |
| Filtering | Extremely powerful (by size, time, permissions, etc.) | Only by name/path |

```bash
# Find all .log files modified in the last 24 hours
find /var/log -name "*.log" -mtime -1

# Find files larger than 100MB
find /home -size +100M

# Find files owned by a specific user
find /tmp -user alice

# Find and delete files older than 30 days (clean up temp files)
find /tmp -mtime +30 -delete

# Find files with specific permissions (SUID — security audit)
find / -perm -4000 -type f 2>/dev/null

# Find all Python files containing a specific function name
find . -name "*.py" -exec grep -l "def process_data" {} \;
```

**Real scenario:** Your disk is filling up. Find the largest files:
```bash
find / -type f -size +500M 2>/dev/null
```

> **Probe:** What does the `-exec` flag in `find` do?  
> It runs a command on each file found. `{}` is a placeholder for the filename. `\;` marks the end of the command. Example: `find . -name "*.tmp" -exec rm {} \;` deletes every `.tmp` file found.

---

### Q28. How do you use `grep` with pipes? Give 3 real-world pipeline examples.

**Answer:**

Piping (`|`) sends the output of one command as input to `grep`. This is one of the most powerful patterns in Linux.

```bash
# Example 1: Filter running processes
ps aux | grep "python"
# Shows only processes with "python" in the name

# Example 2: Find errors in real-time logs
tail -f /var/log/app.log | grep "ERROR"
# -f follows the file as it grows; grep filters only error lines

# Example 3: Count how many times 404 appears in a web log
cat /var/log/nginx/access.log | grep "404" | wc -l
# wc -l counts lines — gives you the number of 404 errors

# Example 4: Find which lines contain an IP address (basic pattern)
cat access.log | grep -E "192\.168\."

# Example 5: Find all environment variables with "KEY" in the name
env | grep -i "KEY"
```

**Chain as many pipes as you need:**
```bash
cat app.log | grep "ERROR" | grep "database" | tail -20
# From app.log: only error lines, only those mentioning database, show last 20
```

> **Probe:** What's `grep -v` useful for in a pipeline?  
> It inverts the match — shows everything EXCEPT matching lines. Useful for filtering out noise: `ps aux | grep -v "grep"` removes the grep process itself from process search results.

---

### Q29. What is `awk` and when would you reach for it over `grep`?

**Answer:**

`awk` is a text processing tool that works column by column. Where `grep` finds matching lines, `awk` extracts and processes specific fields from each line.

```bash
# Print only the 1st and 5th columns from ps aux output
ps aux | awk '{print $1, $5}'

# Print the filename and size from ls -la (columns 5 and 9)
ls -la | awk '{print $5, $9}'

# Sum up all file sizes in the current directory
ls -la | awk '{sum += $5} END {print "Total:", sum, "bytes"}'

# Show only lines where 5th column (CPU) is above 10
ps aux | awk '$3 > 10 {print $0}'

# Extract IPs from an access log (first field)
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
# Shows top 10 IPs by request count
```

**grep vs awk:**
- Use `grep` when you need to find/filter lines by content
- Use `awk` when you need to extract specific columns or do math on fields

> **Probe:** What does `awk '{print $NF}'` do?  
> `$NF` is a built-in variable meaning "last field." It prints the last column of each line regardless of how many columns there are.

---

### Q30. What does `tail` do and why is `tail -f` one of the most used commands in production?

**Answer:**

`tail` shows the last N lines of a file. Default is 10 lines.

```bash
tail file.txt                  # last 10 lines
tail -n 50 file.txt            # last 50 lines
tail -n +5 file.txt            # all lines STARTING from line 5
tail -f /var/log/app.log       # follow mode — shows new lines as they're added
tail -f /var/log/app.log | grep "ERROR"  # watch live for errors only
```

**Why `tail -f` is indispensable in production:**  
When you deploy code or investigate a live issue, you need to watch logs in real time. `tail -f` follows the file as the application writes to it — you see errors as they happen, not minutes later.

```bash
# Watch two log files simultaneously
tail -f /var/log/nginx/error.log /var/log/app.log
```

**Alternative for complex multi-file following:** `multitail` (if installed) gives you a split-screen view.

> **Probe:** How do you watch a log file for errors but suppress the noise of INFO-level logs?  
> `tail -f app.log | grep -E "ERROR|WARN|FATAL"` — pipe through grep to filter only the severity levels you care about.

---

## Section G — Editors: nano & vi

---

### Q31. How do you use `nano`? Walk through opening, editing, saving, and exiting.

**Answer:**

`nano` is a beginner-friendly terminal text editor. All shortcuts are shown at the bottom of the screen.

```bash
nano filename.txt              # open file (creates if it doesn't exist)
nano /etc/hosts                # open a system file (may need sudo)
sudo nano /etc/nginx/nginx.conf
```

**Essential shortcuts** (^ means Ctrl):

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Save (Write Out) — then press Enter to confirm |
| `Ctrl+X` | Exit (prompts to save if unsaved changes) |
| `Ctrl+W` | Search (find text) |
| `Ctrl+K` | Cut (delete) the current line |
| `Ctrl+U` | Paste the cut line |
| `Ctrl+G` | Help — shows all shortcuts |
| `Alt+U` | Undo |
| `Ctrl+\` | Find and replace |

**Typical workflow:**
```bash
sudo nano /etc/hosts
# Edit the file
# Ctrl+O to save → press Enter
# Ctrl+X to exit
```

> **Probe:** What happens if you press `Ctrl+X` without saving changes?  
> Nano asks: "Save modified buffer? (Y/N/Cancel)". `Y` saves and exits, `N` discards changes and exits, `Ctrl+C` or `Cancel` returns to editing.

---

### Q32. Explain the three modes of `vi/vim`. Why do beginners get stuck?

**Answer:**

`vi` (and its improved version `vim`) is a powerful but modal editor — it has different modes that change what keyboard input does.

**The three modes:**

| Mode | How to enter | What keyboard does |
|------|-------------|-------------------|
| **Normal** | Default mode / press `Esc` | Navigate, delete, copy, commands |
| **Insert** | Press `i`, `a`, `o` | Type text like a normal editor |
| **Command** | Press `:` (from Normal) | Save, quit, search, replace |

**Why beginners get stuck:** They start typing without entering Insert mode, and their keystrokes execute commands (deleting lines, jumping around) instead of typing text. Or they can't exit because they don't know `:q`.

**Basic workflow:**
```bash
vi filename.txt          # open file
# You start in Normal mode
i                        # press i to enter Insert mode
# Type your text
Esc                      # press Esc to go back to Normal mode
:w                       # save
:q                       # quit
:wq                      # save and quit (most common)
:q!                      # quit WITHOUT saving (force)
:wq!                     # force save and quit
```

**Essential Normal mode commands:**
```
h j k l    # move left / down / up / right
dd         # delete current line
yy         # copy (yank) current line
p          # paste after cursor
u          # undo
/word      # search for "word" — press n for next match
gg         # go to top of file
G          # go to bottom of file
:5         # jump to line 5
```

> **Probe:** How do you find and replace all occurrences of "foo" with "bar" in vim?  
> `:%s/foo/bar/g` — `:` enters command mode, `%` means all lines, `s` is substitute, `/foo/bar/` is old/new, `g` means all occurrences on each line.

---

### Q33. When would you choose `vi` over `nano` (or vice versa) on a production server?

**Answer:**

**Choose nano when:**
- Quick config file edits where speed of learning matters
- You're SSH'd into an unfamiliar server and just need to change one line
- The person you're helping doesn't know vi

**Choose vi/vim when:**
- The server might not have nano installed (vi/vim is available on virtually every Unix/Linux system)
- You need to edit large files efficiently (vi's Normal mode commands are much faster for navigation)
- You need search/replace across a file
- You're working over a slow SSH connection (vi uses fewer resources)
- Writing or editing scripts where precise editing matters

**The practical reality:**  
In many minimal server environments and Docker containers, nano isn't installed. `vi` is almost always there. This is why knowing at least enough vi to open, edit, save, and quit (`:wq`) is considered baseline Linux competency for any engineer working with servers.

```bash
which nano    # check if nano exists
which vi      # vi is almost always here
which vim     # vim is the improved version
```

> **Probe:** You SSH into a minimal Alpine Linux container to debug an issue. `nano` isn't installed and `vim` isn't either. What editor do you have?  
> `vi` is almost certainly there. Alpine uses `busybox vi` — a stripped-down vi implementation. The basic Normal/Insert/Command mode workflow still works: `i` to insert, `Esc` to exit insert, `:wq` to save and quit.

---

## Section H — Archiving & Compression

---

### Q34. Explain `zip` and `unzip`. How do you zip a folder and protect it with a password?

**Answer:**

`zip` creates compressed archives. `unzip` extracts them. The format is compatible with Windows — useful when sharing files cross-platform.

```bash
# Zip a single file
zip archive.zip file.txt

# Zip multiple files
zip archive.zip file1.txt file2.txt file3.txt

# Zip an entire folder (recursively)
zip -r project.zip project/
# -r = recursive (includes all subdirectories)

# Zip with password protection
zip -e secure.zip sensitive_file.txt
# It will prompt for a password

# Unzip to current directory
unzip archive.zip

# Unzip to a specific directory
unzip archive.zip -d /tmp/extracted/

# List contents without extracting
unzip -l archive.zip

# Unzip quietly (no output spam)
unzip -q archive.zip
```

**Password protection note:** zip's built-in encryption (`-e`) uses older ZipCrypto which is weak. For real security, use `zip -er` with AES encryption or use GPG instead.

> **Probe:** What's the difference between `zip -r` and `tar -czf`? When do you use each?  
> `zip -r` creates a .zip (cross-platform, works on Windows). `tar -czf` creates a .tar.gz (Linux/Unix native, preserves Linux file permissions, ownership, symlinks). Use zip when sharing with Windows users. Use tar when archiving for Linux systems or servers — it preserves all Unix metadata that zip drops.

---

### Q35. Explain `tar` — the most common archiving tool in Linux. What do the flags mean?

**Answer:**

`tar` (tape archive) bundles files together. Combined with gzip or bzip2, it compresses them. This is the standard backup and deployment archive format on Linux.

**The flags decoded:**

| Flag | Meaning |
|------|---------|
| `c` | **C**reate a new archive |
| `x` | E**x**tract files from archive |
| `t` | Lis**t** contents without extracting |
| `z` | Compress with g**z**ip (.tar.gz) |
| `j` | Compress with b**j**zip2 (.tar.bz2) |
| `v` | **V**erbose — show files being processed |
| `f` | **F**ile — specify the archive filename (always last) |

**Common commands:**

```bash
# CREATE an archive
tar -czf backup.tar.gz /var/www/html/         # compress with gzip
tar -cjf backup.tar.bz2 /var/www/html/        # compress with bzip2 (smaller, slower)
tar -cf archive.tar files/                    # bundle without compression

# EXTRACT an archive
tar -xzf backup.tar.gz                        # extract .tar.gz here
tar -xzf backup.tar.gz -C /var/restore/       # extract to specific directory
tar -xjf backup.tar.bz2                       # extract .tar.bz2

# LIST contents without extracting
tar -tzf backup.tar.gz                        # list contents of .tar.gz

# Extract a single file from the archive
tar -xzf backup.tar.gz var/www/html/index.php
```

**Memory trick:**  
`tar -czf` = **c**reate **z**ipped **f**ile  
`tar -xzf` = e**x**tract **z**ipped **f**ile

**Real use case — deployment backup:**
```bash
# Before deploying, backup current version
tar -czf /backups/app_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/app/

# If deployment goes wrong, restore
tar -xzf /backups/app_20240115_143022.tar.gz -C /var/www/
```

> **Probe:** You need to extract only the `config/` directory from a large tar.gz backup. How do you avoid extracting everything?  
> `tar -xzf backup.tar.gz config/` — specify the path inside the archive as the last argument. Only that directory is extracted, saving time and disk space.

---

## Quick Reference: 25 Commands Every Intern Should Know

| # | Command | One-Line Purpose |
|---|---------|-----------------|
| 1 | `cat` | Print file contents to terminal |
| 2 | `echo` | Print text or variable to terminal or file |
| 3 | `grep` | Search for patterns in files or output |
| 4 | `find` | Search filesystem in real-time with filters |
| 5 | `locate` | Fast file search using pre-built database |
| 6 | `diff` | Compare two files line by line |
| 7 | `file` | Identify file type by reading magic bytes |
| 8 | `ls -la` | List files with permissions, ownership, size |
| 9 | `chmod` | Change file permissions |
| 10 | `chown` | Change file owner and group |
| 11 | `rm` | Delete files and directories |
| 12 | `mv` | Move or rename files |
| 13 | `cp` | Copy files |
| 14 | `mkdir` | Create directories |
| 15 | `man` | Read documentation for any command |
| 16 | `nano` | Beginner-friendly terminal text editor |
| 17 | `vi/vim` | Powerful modal terminal text editor |
| 18 | `zip/unzip` | Cross-platform file compression |
| 19 | `tar` | Archive and compress files (Linux native) |
| 20 | `df -h` | Check disk space usage |
| 21 | `ps aux` | List all running processes |
| 22 | `top` | Real-time system monitor |
| 23 | `tail -f` | Watch log files in real-time |
| 24 | `grep + pipe` | Filter command output |
| 25 | `hostname` | Show or set machine name |
| 26 | `useradd` | Create new user account |
| 27 | `passwd` | Set or change user password |
| 28 | `userdel` | Delete user account |
| 29 | `sudo` | Run command with root privileges |
| 30 | `time` | Measure how long a command takes |

---

## Bonus: 5 Commands You'll Wish You Knew Earlier

```bash
# 1. Watch a command run repeatedly (monitor disk every 2 seconds)
watch -n 2 df -h

# 2. See the last commands you ran
history | tail -20

# 3. Search command history
history | grep "tar"

# 4. Run last command as sudo (you forgot sudo)
sudo !!

# 5. See which process is using a port
sudo lsof -i :8080
# or
sudo ss -tlnp | grep 8080
```

---

*Prepared for interview readiness at intern → 2–3 years experience level.*  
*Every command here is used in real industry workflows daily.*
