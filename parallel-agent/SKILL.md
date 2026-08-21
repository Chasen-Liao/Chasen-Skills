---
name: parallel-agent
description: Use when 2 or more genuinely independent tasks can proceed concurrently without shared mutable state.
---

# Parallel Agent

This is a thin local policy layer for Pi. It decides **whether and how to split work**; the installed `pi-subagents` skill is the source of truth for APIs, roles, execution controls, and detailed recipes.

## Before dispatching

1. Read the installed `pi-subagents` skill completely.
2. Follow its router to the relevant reference: prompting/roles, execution controls, multi-lane orchestration, or constraints/recipes.
3. Run `subagent({ action: "list" })` and use only executable, non-disabled, session-allowed agents; capability ceilings or allowlists can still reject a launch.
4. Do not invent or restate runtime behavior when the installed documentation already defines it.

## Decide whether to parallelize

Parallelize only when each lane has a distinct problem domain and can proceed without another lane's result or shared mutable state. Typical cases include unrelated bugs, independent subsystem reconnaissance, separate review angles, or local context plus external research.

Do not parallelize a coupled investigation, dependent sequence, overlapping source seam, or tasks that would edit the same state. Understand the shared root cause first.

## Local invariants

- The parent Agent owns orchestration, synthesis, approval, and final acceptance.
- Use `workflowScript`; use `runs.all` for independent lanes and `runs.run` for dependent stages, following the installed `pi-subagents` documentation.
- Use `fresh` for independent lanes. Use `fork` only when inherited parent decisions are required and its documented session prerequisites are satisfied.
- For cross-repository work, name the repository, explicit `cwd`, authority boundary, and expected output path.
- Before multiple mutation-capable lanes, record a lane board with `repo/cwd`, authority, claimed files or contract, isolation path, validation gate, and handoff. One `repo/cwd` or worktree has one writer; concurrent mutation requires explicit worktree isolation.
- Planning or review output is evidence, not approval. A worker receives only the parent-approved `acceptedScope` and must not infer extra fixes.
- Ordinary child agents do not launch more subagents. Escalate product, architecture, scope, authority, merge, release, or publication decisions to the parent.
- The parent reads every result, checks changed files and conflicts, runs relevant validation (preferably from a fresh context), and reports failures and residual risks honestly.

## Minimal lane guidance

Use the narrowest role described by the installed `pi-subagents` documentation: local reconnaissance, external research, advisory decision review, read-only review, or approved implementation. Do not duplicate that role catalog here; read the official reference when choosing.

Use three standard shapes:

1. **Read-only fanout** — independent scouts/reviewers answer distinct questions; parent synthesizes.
2. **Research fanout** — local repository context and external primary-source research proceed independently; parent decides after comparing evidence.
3. **Staged implementation** — parallel read-only planning → parent-approved `acceptedScope` → one writer → parallel read-only validation.

## Handoff and failure

Ask every child for a concise handoff containing: `status`, `findings`, `changedFiles`, `validation`, and `remainingRisks`. Use the installed `pi-subagents` artifact/output mechanisms for large reports instead of copying them into every prompt.

A partial failure remains a result: preserve successful independent lanes, report failed lanes, and continue only where safe. Do not silently discard failures or retry indefinitely.

This skill is locally maintained for Chasen's Pi setup. Keep it focused on local policy; consult the installed `pi-subagents` documentation rather than copying its API details here.
