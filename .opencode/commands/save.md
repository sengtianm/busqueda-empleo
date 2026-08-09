---
description: Updates the current session's entry in session history.md
---

Update (or create if it does not exist) the current session's entry in `docs/history/session history.md`.

Rules:

- The history is managed by **session number**, newest entry first. The session number is the last existing number + 1 (the consolidated Sessions 1–5 entry counts as one).
- Each entry corresponds to **one OpenCode session** (one conversation), not one calendar day.
- Get the current session ID from the OpenCode local database:
  `sqlite3 ~/.local/share/opencode/opencode.db "SELECT id, substr(title,1,60), datetime(time_updated, 'unixepoch', 'localtime') FROM session ORDER BY time_updated DESC LIMIT 1;"`
- The date must use `DD/MM/YYYY` format.
- The fields to record are: **Topics**, **Decisions**, **Status**.
- Write for a new developer: short, useful, clear keyword-style lists, one bullet per line. No commit hashes, file paths, or rule numbers in Topics.
- **Decisions** and **Status** contain only information from the current session, without repeating data from previous sessions. A single line such as *"Decisions from previous sessions remain in effect"* is sufficient to reference continuity.
- The content is inferred from the conversation that just took place.
- If something is unclear, ask before writing.
- After updating the history, also update `docs/history/tracker.md` if any task changed status during the session.

### Git commit

After updating the documentation, record it in a single commit and share it:

- Verify the scope first: `git status` and `git diff` must show only the files expected from this session. Any unrelated untracked file must not be included.
- Exclude what is never committed: secrets, `.env` (but not `.env.template`, which is versioned), `data/*.db`, `temp/`, `logs/`, and any unrelated file.
- Stage explicitly, never `git add -A` by default, and review `git diff --cached` before committing to catch anything unintended.
- Commit in English, conventional format, imperative mood, subject ≤ 72 characters: `<type>(<scope>): <short summary>` (e.g. `docs(history): add session 13 entry`).
- Commit only once per closing, when the documentation is finished and consistent.
- Push the commit: `git push origin <current-branch>`. If the push fails (remote diverged), stop and report; never force-push.
- Report the commit hash and the push result.
- Merges and any branch push beyond this commit remain governed by the Version Control rules in AGENTS.md; they are never performed here.
