# Relatório de qualidade dos dados

A checagem abrange os nove CSVs da Olist e os 52 campos de origem. As contagens são reproduzíveis no [notebook](../notebooks/01_data_profiling.ipynb). Os testes abaixo podem se sobrepor. Cada taxa usa o denominador indicado.

## Pedidos e ordem dos eventos

| Verificação | Ocorrências | Leitura |
| --- | ---: | --- |
| Pedidos cancelados | 625 de 99.441 | Status observado. Dos cancelados, 619 estão sem data de entrega e 164 estão sem itens |
| Pedidos indisponíveis | 609 de 99.441 | Status observado. Todos estão sem data de entrega e 603 estão sem itens |
| Cancelados com data de entrega | 6 de 625 | Divergência a investigar entre status e eventos gravados |
| Entregues sem data real | 8 de 96.478 | Incompletude para análises de prazo. Outros 14 entregues estão sem aprovação e dois estão sem postagem |
| Entrega anterior à compra | 0 de 96.476 pares válidos | A comparação usa as duas datas gravadas, sem impor restrição de status |
| Postagem anterior à compra | 166 de 97.658 pares válidos | Sequência temporal a investigar |
| Postagem anterior à aprovação | 1.359 de 97.644 pares válidos | Sinal de sequência atípica. A origem pode registrar os eventos em momentos distintos |
| Entrega anterior à postagem | 23 de 96.475 pares válidos | Sequência atípica relevante para análises de prazo e transporte |
| Limite de envio após o dia previsto de entrega | 128 de 112.650 pares válidos | Calendário operacional a investigar |
| Limite de envio em ano posterior à última compra observada | 4 linhas de 3 pedidos | A última compra é de 2018. O maior prazo de envio registrado é 09/04/2020 |
| Pedido com status entregue sem pagamento associado | 1 de 96.478 | Ausência de vínculo relevante para conciliação |

Todos os valores preenchidos nos oito campos de data foram interpretados no formato esperado. A compra vai de 04/09/2016 a 17/10/2018. A data prevista está preenchida em todos os pedidos. A aprovação está ausente em 160 pedidos (0,16%), a postagem em 1.783 (1,79%) e a entrega ao cliente em 2.965 (2,98%). Parte das ausências de datas e itens ocorre em pedidos cancelados ou indisponíveis. O notebook detalha a distribuição dessas ausências por status.

## Chaves, duplicatas e campos ausentes

- A geolocalização tem **261.831 duplicatas exatas excedentes** em 1.000.163 linhas (26,18%). A contagem de excedentes inclui as ocorrências após a primeira de cada grupo. Os outros oito CSVs não têm duplicatas exatas pela leitura adotada.
- Avaliações apresentam 814 repetições excedentes de `review_id`. A combinação com `order_id` é única nesta amostra. Os 547 pedidos com mais de uma avaliação exigem uma regra explícita para métricas por pedido.
- Título e mensagem da avaliação estão ausentes em 87.656 (88,34%) e 58.247 linhas (58,70%), respectivamente. A nota está preenchida nas 99.224 avaliações e sempre dentro da escala de 1 a 5. Comentários são opcionais para a leitura de satisfação.
- Categoria, comprimento do nome, comprimento da descrição e quantidade de fotos têm 610 ausências cada (1,85% dos produtos). Há 1.603 itens de produtos sem categoria. A tradução oficial também deixa duas categorias preenchidas sem par, `portateis_cozinha_e_preparadores_de_alimentos` e `pc_gamer`, que somam 13 produtos e 24 itens.
- Cada campo de peso e dimensão tem duas ausências. Quatro pesos iguais a zero merecem investigação antes de usar peso em comparações de frete ou logística.

As contagens de correspondência nos dois sentidos estão em [Relacionamentos e granularidade](../docs/source_relationships.md).

## Valores monetários

| Campo | Linhas | Nulos | Zeros | Negativos | Máximo |
| --- | ---: | ---: | ---: | ---: | ---: |
| Preço de item | 112.650 | 0 | 0 | 0 | R$ 6.735,00 |
| Frete de item | 112.650 | 0 | 383 | 0 | R$ 409,68 |
| Valor de pagamento | 103.886 | 0 | 9 | 0 | R$ 13.664,08 |

Frete zero pode ser compatível com a operação. A base registra o valor, e o motivo do zero exige contexto adicional. Há ainda duas linhas com zero parcelas. Valores altos foram conservados e documentados por quantis. Um extremo estatístico requer contexto de produto ou pagamento antes de ser classificado como erro.

## Cobertura e consistência geográfica

- Os prefixos de CEP têm cinco dígitos e todas as UFs observadas pertencem à lista de siglas. Dos 19.015 prefixos da referência, **17.781** têm mais de um par de coordenadas. Há **oito** prefixos com mais de uma UF.
- Há 8.556 prefixos com mais de uma grafia de cidade. Comparar os nomes ignorando caixa, acentos e espaços repetidos reduz o total para 547. São medições sobre os textos observados.
- A referência não cobre o prefixo de 278 clientes e sete vendedores. Entre os que têm par por prefixo, 35 de 3.088 vendedores estão sem correspondência de UF. Nos clientes, foram zero de 99.163. Entre os que têm CEP e UF com par e cidade preenchida, 24 de 99.163 clientes e 87 de 3.053 vendedores ficam sem par para a cidade comparável.
- Todas as coordenadas estão preenchidas e dentro dos limites globais. Há **29 linhas fora da caixa aproximada** de latitude de −35° a 6° e longitude de −74° a −28°. A caixa é uma triagem escolhida para esta análise. Validar limites territoriais ou CEPs exigiria uma referência apropriada.

## Priorização sugerida para a modelagem dimensional

A criticidade é uma proposta para revisão. A prioridade é alta quando o problema pode alterar totais, a granularidade ou um indicador central. É média quando o efeito se concentra em recortes ou usos específicos, e baixa quando a análise prevista pode usar outros campos já disponíveis. Os tratamentos descritos são hipóteses para avaliação na próxima etapa.

| Problema observado | Criticidade sugerida | Impacto analítico | Possível tratamento a avaliar |
| --- | --- | --- | --- |
| Múltiplos itens, pagamentos e avaliações por pedido | Alta | Junções diretas podem repetir linhas e inflar medidas de preço, frete ou pagamento | Validar chaves no nível de detalhe de cada origem e comparar os totais antes e depois das junções |
| Datas ausentes, sequências temporais atípicas e divergências entre status e eventos | Alta | A elegibilidade para calcular atrasos e os intervalos entre eventos podem variar conforme o critério | Preservar datas e status de origem, sinalizar ocorrências e comparar a cobertura sob regras explícitas |
| Pedido entregue sem pagamento associado | Alta para conciliação | A cobertura de pagamentos fica incompleta entre os pedidos entregues | Sinalizar o vínculo ausente e conferir a cobertura por status antes de definir indicadores financeiros |
| Duplicatas e múltiplas coordenadas por prefixo de CEP | Média. Alta para análises que juntem dados por prefixo | A referência pode multiplicar linhas ou atribuir localizações ambíguas | Avaliar a UF de cadastro em agregados por estado e validar uma regra de referência antes de usar coordenadas |
| Identificador de avaliação repetido e pedidos com várias respostas | Média. Alta para indicadores com uma nota por pedido | Pedidos com várias respostas podem receber mais peso | Validar a chave composta e comparar as regras de consolidação por pedido |
| Categoria ausente no produto ou preenchida sem tradução | Média | A cobertura e os totais por categoria dependem de como cada caso é representado | Avaliar um grupo explícito para ausências e preservar as categorias de origem sem tradução |
| Fretes, pagamentos, parcelas e pesos zerados | Média | Zeros afetam comparações e podem inviabilizar razões que usam esses campos como denominador | Sinalizar os casos e avaliar o contexto antes de usá-los em cada indicador |
| Título ou mensagem de avaliação ausente | Baixa para indicadores baseados na nota | A ausência reduz a cobertura de análises de texto. A nota está disponível em todas as avaliações da amostra | Acompanhar a cobertura dos comentários caso haja uma análise textual |

## Alternativas para a próxima etapa

| Tema | Alternativas e efeito esperado |
| --- | --- |
| Atraso | Avaliar dia de calendário ou horário gravado. Entre os mesmos 96.470 pedidos elegíveis, a taxa é 6,77% pelo dia e 8,11% pelo horário. O cenário por dia que exclui as sequências temporais sinalizadas no notebook tem 96.447 pedidos elegíveis. Sinalizar as ocorrências e publicar a cobertura são alternativas para documentar o critério |
| Status e valores monetários | Manter o status original para volumes. Definir separadamente a população para indicadores realizados e investigar pagamento ausente, zeros e status divergentes antes de conciliar valores |
| Categorias | Expor “sem categoria” como grupo analítico temporário. Para categorias preenchidas sem tradução, manter o nome de origem ou aprovar um mapeamento separado e versionado |
| Avaliações | Manter todas as respostas em distribuições por avaliação. Para métricas por pedido, comparar primeira resposta, última resposta e agregação, com regra de desempate explícita |
| Geolocalização | Para agregados por UF, priorizar a UF de cadastro. Para coordenadas, comparar seleção por frequência e ponto representativo após triagem. Validar prefixos ambíguos e coordenadas suspeitas com referência externa antes de definir um padrão |
| Duplicatas e extremos | Registrar sinalizações e preservar a rastreabilidade. Avaliar deduplicação apenas na referência derivada, conforme o uso. Avaliar valores extremos com critérios de negócio e documentar eventual exclusão de um indicador |

As alternativas acima permanecem abertas. Nesta etapa, os cálculos usam os dados de origem e vistas auxiliares em memória.
