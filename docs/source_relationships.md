# Relacionamentos e granularidade da fonte

O [notebook de exploração](../notebooks/01_data_profiling.ipynb) valida candidatas a chave e mede correspondência nos dois sentidos. As cardinalidades abaixo descrevem chaves com par na amostra. Uma tabela pode conter linhas sem par mesmo em uma relação observada como 1:1 ou N:1.

## Granularidade e chaves observadas

| Tabela | Linhas | Granularidade e chave candidata |
| --- | ---: | --- |
| `orders` | 99.441 | Um pedido por `order_id` |
| `customers` | 99.441 | Um registro vinculado ao pedido por `customer_id`. O identificador persistente `customer_unique_id` se repete |
| `order_items` | 112.650 | Um item por `(order_id, order_item_id)` |
| `order_payments` | 103.886 | Uma sequência de pagamento por `(order_id, payment_sequential)` |
| `order_reviews` | 99.224 | Uma observação de avaliação por `(order_id, review_id)` na amostra. `review_id` isolado tem 98.410 valores distintos e 814 ocorrências excedentes |
| `products` | 32.951 | Um produto por `product_id` |
| `sellers` | 3.095 | Um vendedor por `seller_id` |
| `geolocation` | 1.000.163 | Uma observação por linha. O prefixo se repete e mesmo a combinação dos cinco campos tem 261.831 ocorrências excedentes |
| `product_category_name_translation` | 71 | Uma tradução por `product_category_name` |

As chaves candidatas descritas como únicas estavam preenchidas. A unicidade de `(order_id, review_id)` é uma evidência local, a verificar a cada nova carga.

## Ligações e cobertura

Cada linha da tabela resume a ligação de A para B pelas colunas indicadas. “Sem par” conta linhas com chave preenchida. Os nulos ficam em uma coluna própria.

| A → B | Chave de ligação | A:B | Chaves em comum | A sem par | A nulos | B sem par |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Pedidos → clientes | `customer_id` | 1:1 | 99.441 | 0 | 0 | 0 |
| Itens → pedidos | `order_id` | N:1 | 98.666 | 0 | 0 | 775 |
| Pagamentos → pedidos | `order_id` | N:1 | 99.440 | 0 | 0 | 1 |
| Avaliações → pedidos | `order_id` | N:1 | 98.673 | 0 | 0 | 768 |
| Itens → produtos | `product_id` | N:1 | 32.951 | 0 | 0 | 0 |
| Itens → vendedores | `seller_id` | N:1 | 3.095 | 0 | 0 | 0 |
| Produtos → tradução | `product_category_name` | N:1 | 71 | 13 | 610 | 0 |
| Clientes → geolocalização | Prefixo de CEP de cliente e de geolocalização | N:N | 14.837 | 278 | 0 | 31.864 |
| Vendedores → geolocalização | Prefixo de CEP de vendedor e de geolocalização | N:N | 2.239 | 7 | 0 | 731.347 |

Nenhuma chave de B estava nula nessas relações. Os 278 registros de cliente sem par geográfico abrangem 157 prefixos. Os sete vendedores sem par correspondem a sete prefixos. O notebook mantém também as contagens de chaves e de linhas com par nos dois sentidos.

### Pedido e identidade do cliente

Para medir pedidos ou vincular o endereço registrado à compra, use `customer_id`. A Olist descreve `customer_unique_id` como o identificador para reconhecer recompras. Dos 96.096 IDs persistentes ligados a pedidos, 2.997 (3,12%) aparecem em dois ou mais pedidos. O maior volume por identidade foi 17. Há 39 identidades com registros em mais de uma UF, então os distintos calculados por UF podem se sobrepor. [Documentação da Olist no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### Múltiplas linhas por pedido

| Relação | Sem linha | Uma linha | Duas ou mais linhas | Máximo |
| --- | ---: | ---: | ---: | ---: |
| Itens | 775 | 88.863 | 9.803 | 21 |
| Pagamentos | 1 | 96.479 | 2.961 | 29 |
| Avaliações | 768 | 98.126 | 547 | 3 |

## Risco de duplicação em JOINs

Partindo dos 99.441 pedidos, um `LEFT JOIN` com itens produz 113.425 linhas. Adicionar pagamentos eleva esse número a 118.434 e adicionar avaliações leva a 119.143. A projeção por multiplicidade foi conferida com SQL no DuckDB.

| Medida | Soma na origem vinculada aos pedidos | Soma após os três `LEFT JOINs` | Aumento |
| --- | ---: | ---: | ---: |
| Preço dos itens | R$ 13.591.643,70 | R$ 14.273.699,65 | 5,02% |
| Frete dos itens | R$ 2.251.909,54 | R$ 2.370.031,65 | 5,25% |
| Valor dos pagamentos | R$ 16.008.872,12 | R$ 20.579.664,01 | 28,55% |

- Para análises por pedido, uma opção é resumir cada origem por `order_id` antes da junção. Para análises por item, outra opção é manter fatos de granularidades distintas. Atribuir o pagamento a categorias ou itens exigiria uma regra de rateio explícita.
- Para avaliações, manter todas as linhas representa a distribuição das respostas. Usar uma nota por pedido exige escolher uma regra, por exemplo primeira resposta, última resposta ou agregação. Cada alternativa muda os pesos relativos de pedidos com várias avaliações.
- Para geolocalização, UF e cidade informadas dão uma visão descritiva sem expansão de linhas. Uma referência com uma coordenada por prefixo exige uma regra de seleção, como um ponto representativo após triagem. A granularidade de prefixo limita a precisão.
