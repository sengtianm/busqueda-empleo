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
