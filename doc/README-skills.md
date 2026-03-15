# Catálogo de Skills Equipes_agentes

Explore as skills disponíveis para suas squads. Instale qualquer skill com:

```bash
npx Equipes_agentes install <nome-da-skill>
```

## Skills Disponíveis

| Skill | Tipo | Descrição | Variáveis de Amb. | Instalação |
|-------|------|-------------|----------|---------|
_Nenhuma skill disponível no momento._

## Tipos de Skill

- **mcp** -- Conecta a um servidor MCP externo (transporte stdio ou HTTP)
- **script** -- Executa um script local (Node.js, Python, etc.)
- **hybrid** -- Combina acesso a servidor MCP com capacidades de script local

## Estrutura de Diretórios

Cada skill vive em sua própria pasta com um arquivo `SKILL.md`:

```
skills/
```

O arquivo `SKILL.md` contém frontmatter YAML (nome, tipo, versão, configuração de MCP/script, variáveis de ambiente, categorias) e um corpo Markdown com instruções de uso e operações disponíveis.

## Adicionando uma Nova Skill

1. Crie uma nova pasta em `skills/` com o ID da skill como nome
2. Adicione um arquivo `SKILL.md` com frontmatter YAML válido e corpo Markdown
3. Se a skill incluir scripts, coloque-os em uma subpasta `scripts/`
4. Atualize este README para incluir a nova skill na tabela do catálogo
