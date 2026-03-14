# Squad Varejo Insight (LÃ­der: Danilo Dados)

Esta squad Ã© especializada em inteligÃªncia de abastecimento e gestÃ£o de estoque para redes de varejo. Ela orquestra mÃºltiplos agentes para garantir que as lojas tenham o produto certo, na gountidade certa, minimizando rupturas e excessos de estoque.

## ðŸ‘¥ Agentes e Responsabilidades

- **ðŸ¤µ Danilo Dados (Analista de Dados):** O cÃ©rebro analÃ­tico. Processa giros de estoque, calcula o Ponto de Pedido (ROP) com lead time dinÃ¢mico de 2-4 dias e sugere reposiÃ§Ãµes baseadas no saldo do CD.
- **ðŸ¬ Gabi GÃ´ndola (Visual Merchandising):** Garante a estÃ©tica e o "efeito de massa". Suas travas de estoque de apresentaÃ§Ã£o (facing) anulam sugestÃµes baixas de reposiÃ§Ã£o para itens em exposiÃ§Ã£o.
- **ðŸ“¦ Leonardo LogÃ­stica (LogÃ­stica de Loja):** Otimiza o espaÃ§o fÃ­sico. Identifica sobras no depÃ³sito da loja para evitar pedidos desnecessÃ¡rios ao CD.
- **ðŸŒ¤ï¸ Clara Clima (InteligÃªncia Sazonal):** Ajusta o OTB (Open-to-Buy) com base em previsÃµes climÃ¡ticas e histÃ³rico promocional.
- **ðŸ›’ Paulo Pedidos (Gestor do CD):** ResponsÃ¡vel pelo "Estoque PulmÃ£o" no **Centro de DistribuiÃ§Ã£o (Filial 15)**. Garante cobertura de 15 dias para a rede, comprando de fornecedores externos em fardos/caixas.
- **ðŸ“Š Roberta RelatÃ³rios (Relator Executivo):** Consolida os dados em KPIs estratÃ©gicos e alertas de aÃ§Ã£o para a diretoria.

## âš™ï¸ Regras de NegÃ³cio Implementadas

1. **CD Centralizado:** A Filial 15 Ã© o hub oficial de distribuiÃ§Ã£o.
2. **Lead Time DinÃ¢mico:** Ciclo de reposiÃ§Ã£o entre 2 e 4 dias.
3. **PadrÃ£o de SeguranÃ§a CD:** ManutenÃ§Ã£o de 15 dias de giro global no CD.
4. **ConversÃ£o de Embalagem:** Todas as ordens de compra para o CD sÃ£o convertidas automaticamente para a unidade de venda do fornecedor (caixas/fardos).

## ðŸš€ Como Executar

Para iniciar a orquestraÃ§Ã£o desta squad, use o comando:

```
/run-varejo
```

Ou atravÃ©s do menu principal:
1. Digite `/Equipes_agentes`
2. Selecione **Executar squad**
3. Escolha **varejo-insight**

