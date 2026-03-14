---
name: Equipes_agentes-dev
description: "Equipes_agentes development checklist â€” verifies templates sync, package integrity, and distribution correctness."
---

# Equipes_agentes Development Checklist

You are running the Equipes_agentes-dev verification skill inside the Equipes_agentes repository.
Your job is to detect and report distribution issues before they reach users.

## How Equipes_agentes Distribution Works

Understand this before checking anything:

- **`templates/`** â†’ Copied by `src/init.js:copyCommonTemplates()` during `npx Equipes_agentes init`
  and by `src/update.js` during `npx Equipes_agentes update`. Everything in `templates/` except
  `ide-templates/` is copied recursively to the user's project. This is the PRIMARY
  distribution mechanism â€” if a file isn't in templates, users don't get it on init.

- **`templates/ide-templates/`** â†’ IDE-specific files. Copied selectively based on user's
  IDE selection during init. Each subfolder (`claude-code/`, `opencode/`, `codex/`,
  `antigravity/`) maps to one IDE choice.

- **`agents/`** (project root) â†’ Predefined agent catalog, distributed via npm
  (`package.json files[]`). Auto-installed during `npx Equipes_agentes init` and new agents
  added during `npx Equipes_agentes update`. Protected from overwrites in
  `src/update.js:PROTECTED_PATHS`. Users can also install manually via
  `npx Equipes_agentes agents install`.

- **`skills/`** (project root) â†’ Bundled skills catalog, distributed via npm
  (`package.json files[]`). Non-MCP skills are auto-installed during init.
  MCP skills (type: mcp/hybrid or with env vars) are offered interactively
  during init. Users can also install manually via `npx Equipes_agentes skills install`.

- **`_Equipes_agentes/core/*`** â†’ Framework core files. MUST have a mirror copy in
  `templates/_Equipes_agentes/core/*`. Any change to a core file that isn't synced to templates
  means `npx Equipes_agentes init` delivers STALE content to new users.

- **`skills/*`** â†’ Bundled skills catalog. Two distribution sub-types:
  - **Multi-file skills** (have scripts/assets/agents dirs alongside SKILL.md, e.g. `Equipes_agentes-skill-creator`):
    also have a mirror in `templates/skills/*` so the full directory structure is copied during init.
    Check B verifies this sync.
  - **Single-file skills** (only `SKILL.md`, no subdirs, e.g. `Equipes_agentes-agent-creator`):
    distributed via `installSkill()` â€” no template copy needed. Check B does NOT apply to these.

- **`package.json files[]`** â†’ Controls what enters the npm package.
  Currently: `bin/`, `src/`, `agents/`, `skills/`, `templates/`.

- **`src/update.js:PROTECTED_PATHS`** â†’ Directories NEVER overwritten during update:
  `_Equipes_agentes/_memory`, `_Equipes_agentes/_investigations`, `agents`, `squads`.

## Multi-IDE Architecture

Equipes_agentes supports multiple IDEs. When a user runs `npx Equipes_agentes init`, they choose which IDE(s) to install for. Files are copied from two places:

1. **Common templates** (`templates/`, excluding `ide-templates/`) â€” copied to every project regardless of IDE
2. **IDE-specific templates** (`templates/ide-templates/{ide}/`) â€” copied only for the selected IDE(s)

### File Classification

| Type | Definition | Location |
|------|-----------|----------|
| SHARED | Applies to all IDEs equally | `_Equipes_agentes/core/`, `templates/` (excluding `ide-templates/`) |
| IDE-SPECIFIC | Applies to one IDE only | `templates/ide-templates/{ide}/` |

### Supported IDEs and Their Template Folders

| IDE | Template Folder | Example Files |
|-----|----------------|---------------|
| Claude Code | `templates/ide-templates/claude-code/` | `SKILL.md`, `CLAUDE.md`, `.mcp.json` |
| Antigravity | `templates/ide-templates/antigravity/` | `.antigravity/rules.md`, `.agent/workflows/Equipes_agentes.md` |
| OpenCode | `templates/ide-templates/opencode/` | `AGENTS.md` |
| Codex | `templates/ide-templates/codex/` | `AGENTS.md` |

### The Golden Rule

> When a change is requested for a specific IDE, modify ONLY files inside `templates/ide-templates/{ide}/`.
> NEVER add conditional logic ("if antigravity, do X") to shared files.

**Violation example:**
- User asks: "Add sequential execution support for Antigravity in the pipeline."
- âŒ Wrong: Edit `_Equipes_agentes/core/runner.pipeline.md` adding `if antigravity: run sequentially`
- âœ… Correct: Edit `templates/ide-templates/antigravity/.antigravity/rules.md` with the sequential execution instructions

**Legitimate shared file edit:**
- User asks: "Add a new researcher agent type to the architect."
- âœ… Fine: Edit `_Equipes_agentes/core/architect.agent.yaml` because the change benefits ALL IDEs equally.

## Verification Process

### Step 1: Detect what changed

Run these commands to identify changed files:

```bash
# Uncommitted changes (staged + unstaged)
git diff --name-only HEAD

# If no uncommitted changes, check recent commits
git log --oneline -5
git diff --name-only HEAD~5..HEAD
```

Collect all changed file paths into a list.

### Step 2: Run applicable checks

For each changed file, apply the matching verification rules below.
Only run checks that are relevant to the actual changes detected.

#### Check A: Core file sync (`_Equipes_agentes/core/**` changed)

For EACH changed file matching `_Equipes_agentes/core/**`:

1. Compute the expected template path: `templates/{same relative path}`
   Example: `_Equipes_agentes/core/runner.pipeline.md` â†’ `templates/_Equipes_agentes/core/runner.pipeline.md`

2. Run diff:
   ```bash
   diff "_Equipes_agentes/core/{file}" "templates/_Equipes_agentes/core/{file}"
   ```

3. If diff shows differences:
   - **FAIL**: Report the file and show the diff summary
   - **Fix**: `cp _Equipes_agentes/core/{file} templates/_Equipes_agentes/core/{file}`

4. If template file doesn't exist:
   - **FAIL**: "Template missing for `_Equipes_agentes/core/{file}`"
   - **Fix**: `mkdir -p templates/_Equipes_agentes/core/{dir} && cp _Equipes_agentes/core/{file} templates/_Equipes_agentes/core/{file}`

#### Check B: Skills sync (`skills/**` changed)

Only applies to **multi-file skills** â€” skills that have subdirectories (scripts/, assets/, agents/, etc.)
alongside their `SKILL.md`. These require a template mirror so the full directory is copied during init.

Single-file skills (only `SKILL.md`, no subdirs) are distributed via `installSkill()` and do NOT need
a `templates/skills/` counterpart. Do not flag them as missing.

For each changed **multi-file** skill:
- Source: `skills/{skill}/SKILL.md`
- Template: `templates/skills/{skill}/SKILL.md`

#### Check C: Agents directory (`agents/**` changed)

1. Read `package.json`, parse the `files` array
2. Verify `"agents/"` is present in the array
3. If missing: **FAIL** â€” `"agents/" not in package.json files[]`

#### Check D: Init logic (`src/init.js` changed)

1. Read `src/init.js`
2. Verify `copyCommonTemplates` function exists and references `TEMPLATES_DIR`
3. Verify `getTemplateEntries` recursively scans the templates directory
4. Flag if any new filtering logic was added that might exclude files

#### Check E: Update logic (`src/update.js` changed)

1. Read `src/update.js`
2. Extract the `PROTECTED_PATHS` array
3. Verify it includes all user-owned directories:
   - `_Equipes_agentes/_memory` (user preferences and company context)
   - `_Equipes_agentes/_investigations` (Sherlock investigation data)
   - `agents` (user-installed/customized agents)
   - `squads` (user-created squads)
4. If a new user-owned top-level directory was added to the project,
   check if it should be in PROTECTED_PATHS

#### Check F: Package manifest (`package.json` changed)

1. Read `package.json`, parse `files` array
2. Verify these directories are present: `bin/`, `src/`, `agents/`, `skills/`, `templates/`
3. If any distributable directory exists at project root but is NOT in `files[]`: **FAIL**

#### Check G: New top-level directory (any new directory at root)

1. Run `ls -d */` at project root
2. For each directory, check:
   - Is it in `package.json files[]`? (if it should be distributed)
   - Is it in `PROTECTED_PATHS`? (if it's user-owned content)
   - Is it in `templates/`? (if it should be copied during init)
3. Flag any directory that seems like it should be distributed but isn't configured

#### Check H: Init auto-installs agents and skills (`src/init.js` changed)

1. Read `src/init.js`
2. Verify it imports from `./agents.js`: `listAvailable` (aliased as `listAvailableAgents`) and `installAgent`
3. Verify `installAllAgents` function exists and is called in `init()`
4. Verify `installNonMcpSkills` function exists and is called in `init()`
5. Verify `installNonMcpSkills` filters out: `Equipes_agentes-skill-creator`, type `mcp`, type `hybrid`, skills with `env`
6. If any of these are missing: **FAIL** â€” "Init does not auto-install agents/skills"

#### Check I: Update installs new agents/skills (`src/update.js` changed)

1. Read `src/update.js`
2. Verify it imports from `./agents.js`: `listAvailable`, `listInstalled`, `installAgent`
3. Verify it imports from `./skills.js`: `listAvailable`, `listInstalled`, `installSkill`, `getSkillMeta`
4. Verify the update function installs missing agents (compares available vs installed)
5. Verify it installs missing non-MCP skills with same filtering as init
6. If any of these are missing: **FAIL** â€” "Update does not install new agents/skills"

#### Check J: IDE contamination in shared files (any `_Equipes_agentes/core/**` or `templates/**` changed, excluding `templates/ide-templates/**`)

Scan shared files for IDE-specific conditional logic that should live in `templates/ide-templates/{ide}/` instead.

**Files to scan:**
- All files in `_Equipes_agentes/core/`
- All files in `templates/` EXCEPT those under `templates/ide-templates/`

**What to look for:** Content that says "do X for IDE Y" or "if using IDE Y, behave differently."

**Contamination keywords** (IDE names used as conditional subjects):
- `antigravity` or `.antigravity`
- `cursorrules` or `.cursor/`
- `windsurf` or `windsurfrules`
- `opencode` or `open-code`
- `codex`
- Conditional patterns: "se antigravity", "if antigravity", "for antigravity", "if cursor", "if windsurf", "if codex"

**Exclusions:** Mentions inside this Equipes_agentes-dev SKILL.md itself (documentation), and any comment explicitly labeled as a cross-reference.

**Pass:** No IDE-specific conditional logic found in shared files.
**Fail:** Report the file path, relevant line, and the correct location where the change should go instead (i.e., which `templates/ide-templates/{ide}/` file).

### Step 3: Report results

Present a clear summary:

```
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
ðŸ”§ Equipes_agentes Dev Checklist
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”

Files changed: {N}
Checks run: {N}

âœ… Check A: Core file sync â€” {N}/{N} files in sync
âŒ Check B: Skills sync â€” {file} out of sync
   Fix: cp skills/{x}/SKILL.md templates/skills/{x}/SKILL.md
âœ… Check F: Package manifest â€” all directories present
âœ… Check J: IDE contamination â€” no IDE-specific logic in shared files

â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
Result: {N} issues found
â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”
```

If ALL checks pass, report clean:
```
âœ… All {N} checks passed â€” distribution is consistent.
```

If any check fails, list the fix commands at the end so the user
can approve them in batch.

