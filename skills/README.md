# Opensquad Skill Catalog

Browse available skills for your squads. Install any skill with:

```bash
npx opensquad install <skill-name>
```

## Available Skills

| Skill | Type | Description | Env Vars | Install |
|-------|------|-------------|----------|---------|
| [image-fetcher](./image-fetcher/) | hybrid | Acquire visual assets via web search, live screenshots (Playwright), and user-provided files. | _(none)_ | `npx opensquad install image-fetcher` |
| [image-creator](./image-creator/) | mcp | Render HTML/CSS into production-ready PNG images via Playwright. | _(none)_ | `npx opensquad install image-creator` |

## Skill Types

- **mcp** -- Connects to an external MCP server (stdio or HTTP transport)
- **script** -- Runs a local script (Node.js, Python, etc.)
- **hybrid** -- Combines MCP server access with local script capabilities

## Directory Structure

Each skill lives in its own folder with a `SKILL.md` file:

```
skills/
  image-fetcher/
    SKILL.md
  image-creator/
    SKILL.md
```

The `SKILL.md` file contains YAML frontmatter (name, type, version, MCP/script config, env vars, categories) and a Markdown body with usage instructions and available operations.

## Adding a New Skill

1. Create a new folder under `skills/` with the skill ID as the name
2. Add a `SKILL.md` file with valid YAML frontmatter and Markdown body
3. If the skill includes scripts, place them in a `scripts/` subfolder
4. Update this README to include the new skill in the catalog table
