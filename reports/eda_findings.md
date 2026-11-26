# Descobertas exploratórias da Olist

O relatório reúne evidências sobre a evolução dos pedidos, a concentração de volume por categoria e região e a relação entre pontualidade e experiência de compra. As análises usam os nove CSVs originais e a população observada em cada tabela. [Notebook de exploração](../notebooks/01_data_profiling.ipynb)

## 1. Como evoluíram o volume e os status dos pedidos?

### Evidência

Novembro de 2017 teve o maior volume observado, com **7.544 pedidos**. De janeiro a agosto de 2018, os volumes mensais ficaram entre 6.167 e 7.269. Setembro e outubro de 2018 tiveram 16 e quatro pedidos, respectivamente.

Na extração, 96.478 dos 99.441 pedidos (97,02%) estavam marcados como entregues. Os 625 cancelados e 609 indisponíveis somavam 1.234 pedidos (1,24% dos 99.441 pedidos).

### Interpretação e limitações

Os volumes observados variam ao longo da série. As compras vão de 04/09/2016 a 17/10/2018, com poucos registros nas extremidades e nenhum em novembro de 2016. A cobertura da amostra limita a interpretação das quedas nessas datas. Os status representam a situação registrada na extração. Em um acompanhamento mensal, sinalizar as lacunas de cobertura ajuda a interpretar as quedas antes de atribuí-las a uma mudança de demanda.

### Próxima investigação

Definir uma janela com cobertura comparável e verificar como ela afeta as taxas de cancelamento e indisponibilidade.

## 2. Quais categorias concentram itens e como variam preços e fretes?

### Evidência

Cama, mesa e banho liderou com **11.115 dos 112.650 itens (9,87%)**, seguida por beleza e saúde (9.670) e esporte e lazer (8.641). Do mesmo total de 112.650 itens, 1.603 (1,42%) pertenciam a produtos sem categoria informada.

| Medida por item | Mediana | Percentil 99 | Máximo |
| --- | ---: | ---: | ---: |
| Preço | R$ 74,99 | R$ 890,00 | R$ 6.735,00 |
| Frete | R$ 16,26 | R$ 84,52 | R$ 409,68 |

### Interpretação e limitações

O ranking mede linhas de item e pode orientar o recorte inicial de um painel de volume. Exibir a parcela sem categoria junto ao ranking torna visível a cobertura da comparação. Preço e frete têm cauda à direita, e a mediana ajuda a descrever a região central da distribuição. Os valores registrados de itens, fretes e pagamentos precisam de definições de negócio e, quando aplicável, fontes complementares para compor indicadores de receita, margem, valor líquido ou reembolso.

### Próxima investigação

Comparar os rankings por quantidade e por soma dos preços registrados, explicitando a cobertura de categoria em cada um. Examinar em quais faixas de preço, peso e distância o frete representa uma parcela maior do valor do item.

## 3. Onde se concentram os registros de clientes e com que frequência há recompras?

### Evidência

São Paulo concentrou **41,98% dos 99.441 registros de cliente**, com 41.746 registros vinculados a pedidos. Rio de Janeiro teve 12.852 e Minas Gerais, 11.635. Das 96.096 identidades persistentes na amostra, 2.997 (3,12%) fizeram dois ou mais pedidos no período observado.

### Interpretação e limitações

As contagens por UF usam o cadastro de cliente vinculado a cada pedido. Uma identidade persistente pode aparecer em mais de uma UF, e as contagens de IDs distintos por UF podem se sobrepor. A análise de recompra se limita às compras observadas e usa o identificador persistente `customer_unique_id`. Esse recorte permite descrever a concentração de pedidos por UF e a repetição de compras na amostra. A geolocalização por prefixo de CEP tem lacunas e ambiguidades. [Relatório de qualidade](data_quality_report.md)

### Próxima investigação

Comparar a recompra entre grupos com janelas de observação equivalentes e medir a cobertura geográfica antes de usar regiões para explicar diferenças.

## 4. Qual é a frequência de atraso nas entregas?

### Evidência

Pelo dia de calendário, **6.534 dos 96.470 pedidos elegíveis (6,77%)** chegaram após o dia previsto. Entre os atrasados, a mediana foi de sete dias e o percentil 95 foi de 31 dias. Pelo horário gravado, foram 7.826 atrasos nos mesmos 96.470 pedidos (8,11%), incluindo mais 1.292 entregas feitas no dia previsto.

### Interpretação e limitações

A frequência depende do critério de atraso. A comparação usa a estimativa registrada na extração e a base não informa o fuso horário. São elegíveis os pedidos com status entregue e datas real e prevista válidas. Oito pedidos marcados como entregues ficaram fora desse denominador por falta de data real. Acompanhar a taxa com seu critério e denominador ajuda a comparar grupos e períodos de forma consistente.

### Próxima investigação

Comparar UFs, categorias e vendedores em períodos semelhantes, apresentando o volume elegível de cada grupo e o efeito da escolha entre dia de calendário e horário gravado.

## 5. Como as notas variam entre entregas no prazo e atrasadas?

### Evidência

Das 99.224 avaliações, 57.328 (57,78%) deram nota 5. Entre os pedidos elegíveis para a análise de atraso, a comparação por dia de calendário mostrou **62,41% de notas 1 ou 2 nas entregas atrasadas e 9,28% nas entregas no prazo ou antes**.

| Grupo de entrega | Linhas de avaliação com nota | Notas 1 ou 2 (% das linhas do grupo) | Pedidos com nota / pedidos elegíveis | Cobertura de notas (% dos pedidos elegíveis do grupo) |
| --- | ---: | ---: | ---: | ---: |
| Após o prazo | 6.409 | 62,41% | 6.381 / 6.534 | 97,66% |
| No prazo ou antes | 89.944 | 9,28% | 89.443 / 89.936 | 99,45% |

### Interpretação e limitações

A diferença descreve uma associação na amostra. Categoria, região, época, composição dos vendedores e propensão a responder podem influenciar a comparação. Cada linha de avaliação tem o mesmo peso nesse cálculo, e alguns pedidos têm mais de uma avaliação. Separar os grupos por pontualidade pode ajudar a investigar as notas baixas, desde que a cobertura de avaliações também fique visível.

### Próxima investigação

Repetir a comparação com uma observação por pedido e verificar se a diferença persiste ao segmentar por UF, categoria e época.

## 6. Como a granularidade afeta os totais usados no BI?

### Evidência

Em um teste de junção direta por `order_id`, a soma registrada dos pagamentos dos pedidos passou de R$ 16,01 milhões para R$ 20,58 milhões ao combinar itens, pagamentos e avaliações no mesmo nível. O aumento de **28,55%** é relativo à soma original dos pagamentos vinculados aos pedidos. [Relacionamentos e granularidade](../docs/source_relationships.md)

### Interpretação e limitações

Pedidos com várias linhas em mais de uma tabela geram combinações repetidas na junção. A diferença medida decorre dessa multiplicação. A soma de cada origem serve de referência para validar as medidas do futuro relatório.

### Próxima investigação

Comparar totais antes e depois de cada junção e validar alternativas que preservem a granularidade de cada medida. Qualquer atribuição de valores de pagamento por item ou categoria exige uma regra de rateio definida.
