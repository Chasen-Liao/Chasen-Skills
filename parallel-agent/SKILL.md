---
name: parallel-agent
description: Use when facing 2 or more independent tasks that can be investigated or validated concurrently without shared mutable state.
---

# Parallel Agent

A Pi-native playbook for coordinating independent subagents. The parent agent remains the orchestrator and final decision-maker.

## When to use

Use this skill when there are two or more genuinely independent problem domains, such as:

- unrelated test failures or bugs;
- separate subsystems that need reconnaissance or review;
- local code context and external research that can proceed together;
- independent validation angles after an implementation.

Do not parallelize when tasks share mutable state, depend on one another's conclusions, or are still one coupled investigation. Understand the shared root cause first.

## Role routing

Choose the narrowest builtin role for each lane:

| Need | Agent |
| --- | --- |
| Codebase reconnaissance | `scout` |
| External or current-source research | `researcher` |
| Architecture or decision consistency advice | `oracle` |
| Read-only code, plan, or diff review | `reviewer` |
| Approved implementation | `worker` |
| Small generic delegation | `delegate` |

Use `context: "fresh"` for independent lanes. Use `context: "fork"` only when the child must inherit the parent session's decisions or history, typically for an oracle consultation.

## Parent orchestration rules

- Launch coordinated work through `workflowScript`.
- Use `runs.all([...])` for parallel lanes and `runs.run(key, {...})` for one lane or a dependent sequential step.
- Prefer `async: true` for the overall workflow; do not block merely because a task is short.
- Keep normal fanouts small, usually 2–5 lanes. Do not create a swarm without a distinct decision for every lane.
- Compare prompts before launch. Each lane needs a distinct scope, evidence, authority boundary, success criteria, and output.
- Ordinary child agents must not launch more subagents. Only an explicitly assigned fanout child with the required tool permission may do so.
- Treat child output as evidence. The parent must synthesize it, inspect the resulting diff, resolve conflicts, and own final acceptance.

## Write safety

Never launch multiple mutation-capable workers into the same active worktree.

For implementation work, use this default sequence:

```text
parallel read-only planning or reconnaissance
    -> one worker applies approved changes
    -> parallel read-only review and validation
```

Use isolated worktrees only when multiple writers are explicitly required and each lane has a non-overlapping authority boundary. Do not let a child silently decide product scope, architecture, release, merge, publication, or other authority-sensitive questions.

## Child task contract

Give every child a compact, self-contained contract:

- **Goal** — the concrete result required;
- **Target** — repository, cwd, files, symbols, diff, or source seam;
- **Authority** — read-only or allowed edits; no commit, push, merge, release, or publication unless explicitly approved;
- **Context** — relevant evidence and approved decisions;
- **Success** — what must be true before stopping;
- **Validation** — focused commands or checks;
- **Output** — the required handoff fields;
- **Stop rule** — when to escalate instead of guessing.

Require each child to return:

```text
status
findings
changedFiles
validation
remainingRisks
```

For large reports, use a distinct durable `output` path with `outputMode: "file-only"` and pass the path to dependent steps rather than copying the entire report into every prompt.

## Standard workflows

### 1. Parallel reconnaissance or review

Use distinct roles and distinct questions:

```typescript
subagent({
  workflowScript: `
    const results = await runs.all([
      {
        key: "correctness",
        agent: "reviewer",
        context: "fresh",
        task: "Review the current diff for correctness and regressions. Do not edit files. Return status, findings, changedFiles, validation, and remainingRisks."
      },
      {
        key: "tests",
        agent: "reviewer",
        context: "fresh",
        task: "Review the current diff against the validation contract and identify missing tests or checks. Do not edit files. Return status, findings, changedFiles, validation, and remainingRisks."
      }
    ]);
    return results.map(result => result.output);
  `,
  context: "fresh",
  async: true
})
```

### 2. Parallel local context and external research

Use `scout` for repository facts and `researcher` for external evidence. Keep their questions independent, then synthesize before making a decision:

```typescript
subagent({
  workflowScript: `
    const results = await runs.all([
      { key: "local", agent: "scout", context: "fresh", task: "Inspect the named repository files and return relevant code paths and constraints." },
      { key: "external", agent: "researcher", context: "fresh", task: "Find high-trust current sources for the named API or behavior and return links, evidence, and gaps." }
    ]);
    return results.map(result => result.output);
  `,
  context: "fresh",
  async: true
})
```

### 3. Staged implementation

Use this when independent findings will eventually affect one worktree. Planning and validation fan out; writing stays single-threaded:

```typescript
subagent({
  workflowScript: `
    const plans = await runs.all([
      {
        key: "domain-a",
        agent: "reviewer",
        context: "fresh",
        task: "Inspect the current diff for domain A. Do not edit. Propose only in-scope fixes with file references and focused validation."
      },
      {
        key: "domain-b",
        agent: "reviewer",
        context: "fresh",
        task: "Inspect the current diff for domain B. Do not edit. Propose only in-scope fixes with file references and focused validation."
      }
    ]);

    const worker = await runs.run("implementation", {
      agent: "worker",
      context: "fresh",
      task: "Apply only the accepted fixes from these planning results. You are the sole writer for the active worktree. Run focused validation and return status, findings, changedFiles, validation, and remainingRisks.\n\nPlanning results:\n" + plans.map(result => result.output).join("\n\n")
    });

    const validation = await runs.all([
      {
        key: "post-correctness",
        agent: "reviewer",
        context: "fresh",
        task: "Validate the post-worker diff for correctness and regressions. Do not edit. Return status, findings, changedFiles, validation, and remainingRisks."
      },
      {
        key: "post-tests",
        agent: "reviewer",
        context: "fresh",
        task: "Validate the post-worker diff and focused tests against the accepted scope. Do not edit. Return status, findings, changedFiles, validation, and remainingRisks."
      }
    ]);

    return {
      plans: plans.map(result => result.output),
      worker: worker.output,
      validation: validation.map(result => result.output)
    };
  `,
  context: "fresh",
  async: true
})
```

## Failure and completion

A partial failure is still a result. Preserve successful lanes, report failed lanes explicitly, and continue only with work that remains independent. Do not silently discard failures or retry indefinitely. Retry only when the failure is clearly transient and the retry remains within the approved scope.

Before completion, the parent must:

1. read or aggregate every child result;
2. inspect changed files and resolve conflicts;
3. run the relevant tests, checks, or gates;
4. distinguish blockers, deferred improvements, and residual risks;
5. report the evidence and any failed validation honestly.

This skill is locally maintained for the Chasen Pi setup. Its runtime API follows the installed `pi-subagents` package; this file does not replace the package's own execution or safety documentation.
