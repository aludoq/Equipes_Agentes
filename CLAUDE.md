# Equipes_agentes â€” Project Instructions

This project uses **Equipes_agentes**, a multi-agent orchestration framework.

## Quick Start

Type `/Equipes_agentes` to open the main menu, or use any of these commands:
- `/Equipes_agentes create` â€” Create a new squad
- `/Equipes_agentes run <name>` â€” Run a squad
- `/Equipes_agentes help` â€” See all commands

## Directory Structure

- `_Equipes_agentes/` â€” Equipes_agentes core files (do not modify manually)
- `_Equipes_agentes/_memory/` â€” Persistent memory (company context, preferences)
- `skills/` â€” Installed skills (integrations, scripts, prompts)
- `squads/` â€” User-created squads
- `squads/{name}/_investigations/` â€” Sherlock content investigations (profile analyses)
- `squads/{name}/output/` â€” Generated content and files
- `_Equipes_agentes/_browser_profile/` â€” Persistent browser sessions (login cookies, localStorage)

## How It Works

1. The `/Equipes_agentes` skill is the entry point for all interactions
2. The **Architect** agent creates and modifies squads
3. During squad creation, the **Sherlock** investigator can analyze reference profiles (Instagram, YouTube, Twitter/X, LinkedIn) to extract real content patterns
4. The **Pipeline Runner** executes squads automatically
5. Agents communicate via persona switching (inline) or subagents (background)
6. Checkpoints pause execution for user input/approval

## Rules

- Always use `/Equipes_agentes` commands to interact with the system
- Do not manually edit files in `_Equipes_agentes/core/` unless you know what you're doing
- Squad YAML files can be edited manually if needed, but prefer using `/Equipes_agentes edit`
- Company context in `_Equipes_agentes/_memory/company.md` is loaded for every squad run

## Browser Sessions

Equipes_agentes uses a persistent Playwright browser profile to keep you logged into social media platforms.
- Sessions are stored in `_Equipes_agentes/_browser_profile/` (gitignored, private to you)
- First time accessing a platform, you'll log in manually once
- Subsequent runs will reuse your saved session
- **Important:** The native Claude Code Playwright plugin must be disabled. Equipes_agentes uses its own `@playwright/mcp` server configured in `.mcp.json`.

