# Descobertas exploratórias da Olist

A análise cobre os nove CSVs originais e usa a população observada em cada tabela. Os resultados são reproduzíveis no [notebook](../notebooks/01_data_profiling.ipynb). Evidências de qualidade e detalhes de junção estão no [relatório de qualidade](data_quality_report.md) e na [documentação de relacionamentos](../docs/source_relationships.md).

## Oito descobertas

1. **O pico mensal observado foi novembro de 2017, com 7.544 pedidos.** O volume ficou entre 6.167 e 7.269 por mês de janeiro a agosto de 2018. Setembro e outubro de 2018 têm apenas 16 e quatro pedidos, respectivamente. A cobertura rarefeita na borda limita comparações com os meses anteriores.
2. **97,02% dos pedidos estavam marcados como entregues.** São 96.478 dos 99.441 pedidos. Os 625 cancelados e 609 indisponíveis somam 1.234 pedidos (1,24% da base). O status é o observado na extração.
3. **Os preços e fretes têm cauda à direita.** As medianas por item são R$ 74,99 para preço e R$ 16,26 para frete. O P99 é R$ 890,00 e R$ 84,52, respectivamente. Os máximos chegam a R$ 6.735,00 e R$ 409,68.
4. **Cama, mesa e banho lidera em volume.** A categoria tem 11.115 dos 112.650 itens (9,87%), seguida por beleza e saúde (9.670) e esporte e lazer (8.641). Outros 1.603 itens (1,42%) correspondem a produtos sem categoria informada. O ranking mede linhas de item.
5. **São Paulo concentra 41,98% dos registros de cliente.** São 41.746 registros, seguidos por Rio de Janeiro (12.852) e Minas Gerais (11.635). A amostra tem 96.096 identidades persistentes, das quais 2.997 (3,12%) tiveram pelo menos dois pedidos no período observado.
6. **Atrasos afetam 6,77% dos pedidos entregues com datas válidas pelo critério de dia.** Foram 6.534 de 96.470. Entre os atrasados, a mediana foi de sete dias e o P95 de 31 dias. Comparar pelos horários gravados dá 8,11%, pois inclui mais 1.292 entregas feitas no dia previsto.
7. **As notas se concentram em cinco, e as notas baixas são mais frequentes nas entregas atrasadas.** Das 99.224 avaliações, 57.328 (57,78%) deram nota 5. Entre as linhas com nota vinculadas a entregas elegíveis, 62,41% deram nota 1 ou 2 após o prazo, ante 9,28% no prazo ou antes. A cobertura de notas por pedido também difere entre os grupos (97,66% e 99,45%), e alguns pedidos têm várias avaliações.
8. **Uma junção direta das três tabelas filhas inflaria medidas comerciais.** A soma registrada dos pagamentos dos pedidos passa de R$ 16,01 milhões para R$ 20,58 milhões (+28,55%) quando itens, pagamentos e avaliações são unidos por `order_id` no mesmo nível, sem resumir cada origem.

## Limitações de interpretação

- As compras observadas vão de 04/09/2016 a 17/10/2018. Nas extremidades e em novembro de 2016, os volumes escassos ou ausentes podem refletir cobertura da amostra. Para comparações mensais, vale explicitar a janela escolhida.
- A taxa de atraso depende do status e da disponibilidade das datas. O denominador por dia deixa de fora oito pedidos marcados como entregues sem data real. A estimativa gravada representa a data disponível na extração e a fonte não informa fuso horário.
- A comparação de notas é descritiva. Região, categoria, época, composição dos vendedores e propensão a responder podem influenciar a diferença. As duas populações de notas incluem todas as linhas vinculadas.
- Os valores financeiros são registros de itens, fretes e pagamentos. Indicadores de receita, margem, valor líquido ou reembolso precisam de definições de negócio e, quando aplicável, fontes complementares.
- CEP é um prefixo, e a cobertura de geolocalização tem ambiguidades. As contagens por UF usam o cadastro do cliente vinculado ao pedido. IDs persistentes que aparecem em várias UFs podem contribuir para mais de uma contagem estadual.

## Perguntas para aprofundar

- Quais UFs, categorias e vendedores concentram atrasos quando se comparam grupos com volumes e períodos semelhantes?
- A diferença nas notas se mantém com uma única observação por pedido e após segmentar por UF, categoria e época?
- Em quais faixas de preço, peso e distância o frete representa maior parcela do valor do item?
- As categorias que mais vendem em volume também lideram em valor dos itens? Qual é a cobertura da categorização em cada ranking?
- Como mudam as taxas de cancelamento, indisponibilidade e recompra ao escolher uma janela de observação comparável?
