---
description: Updates the current day's entry in Session History.md
---

Update (or create if it does not exist) the current day's entry in `Session History.md`.

Rules:

- There is only **one session per calendar day**. If an entry with today's date already exists, update it; otherwise, create a new one.
- The session number increments sequentially: it is the last existing number + 1.
- The date must use `DD/MM/YYYY` format (no time).
- The fields to record are: **Topics Covered**, **Decisions**, **Agreements**, **Closing Status**.
- The content must be **detailed enough** in each field so that a future session can recover the full context without ambiguity.
- Information from past sessions cannot be deleted or summarized. The history is cumulative.
- **Agreements** and **Closing Status** must contain only information from the current session, without repeating data from previous sessions. A single line such as *"Agreements from previous sessions remain in effect"* is sufficient to reference continuity.
- The content is inferred from the conversation that just took place.
- If something is unclear, ask before writing.
- After updating the history, also update `MVP Tracker.md` if any task changed status during the session.
