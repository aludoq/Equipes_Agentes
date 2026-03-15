# Equipes_agentes — Instruções do Projeto

Este projeto utiliza o **Equipes_agentes**, um framework de orquestração multi-agentes.

## Início Rápido

Digite `/Equipes_agentes` para abrir o menu principal, ou use qualquer um destes comandos:
- `/Equipes_agentes create` — Criar um novo squad
- `/Equipes_agentes run <nome>` — Executar um squad
- `/Equipes_agentes help` — Ver todos os comandos

## Estrutura de Diretórios

- `_Equipes_agentes/` — Arquivos principais do Equipes_agentes (não modifique manualmente)
- `_Equipes_agentes/_memory/` — Memória persistente (contexto da empresa, preferências)
- `skills/` — Skills instaladas (integrações, scripts, prompts)
- `squads/` — Squads criadas pelo usuário
- `squads/{nome}/_investigations/` — Investigações de conteúdo do Sherlock (análises de perfil)
- `squads/{nome}/output/` — Conteúdo e arquivos gerados
- `_Equipes_agentes/_browser_profile/` — Sessões persistentes do navegador (cookies de login, localStorage)

## Como Funciona

1. A skill `/Equipes_agentes` é o ponto de entrada para todas as interações
2. O agente **Arquiteto** cria e modifica squads
3. Durante a criação do squad, o investigador **Sherlock** pode analisar perfis de referência (Instagram, YouTube, Twitter/X, LinkedIn) para extrair padrões reais de conteúdo
4. O **Pipeline Runner** executa os squads automaticamente
5. Os agentes se comunicam via troca de persona (inline) ou subagentes (segundo plano)
6. Checkpoints pausam a execução para entrada/aprovação do usuário

## Regras

- Sempre use comandos `/Equipes_agentes` para interagir com o sistema
- Não edite manualmente os arquivos em `_Equipes_agentes/core/` a menos que saiba o que está fazendo
- Arquivos YAML de squad podem ser editados manualmente se necessário, mas prefira usar `/Equipes_agentes edit`
- O contexto da empresa em `_Equipes_agentes/_memory/company.md` é carregado para toda execução de squad

## Sessões de Navegador

O Equipes_agentes utiliza um perfil de navegador Playwright persistente para manter você logado em plataformas de redes sociais.
- As sessões são armazenadas em `_Equipes_agentes/_browser_profile/` (ignorado pelo git, privado para você)
- Na primeira vez que acessar uma plataforma, você fará login manualmente uma vez
- Execuções subsequentes reutilizarão sua sessão salva
- **Importante:** O plugin nativo Playwright do Claude Code deve ser desativado. O Equipes_agentes utiliza seu próprio servidor `@playwright/mcp` configurado em `.mcp.json`.
