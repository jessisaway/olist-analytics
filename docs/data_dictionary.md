# Dicionário de dados da Olist

Este dicionário descreve os 52 campos nos nove arquivos CSV do [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). A amostra histórica foi anonimizada pela Olist e abrange pedidos de diferentes marketplaces.

Os tipos abaixo descrevem o significado dos campos. Uma coluna numérica inteira com ausências pode aparecer como `float64` na leitura do Pandas. Os prefixos de CEP e identificadores textuais são lidos como texto. Os campos temporais são convertidos em uma representação auxiliar sem fuso horário informado pela fonte. Os valores monetários são em reais. Nulos, tipos carregados e frequências por coluna podem ser consultados no [notebook](../notebooks/01_data_profiling.ipynb).

## Clientes — `olist_customers_dataset.csv`

Uma linha por `customer_id` na amostra. A mesma identidade persistente pode aparecer em mais de um pedido e localidade.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `customer_id` | Texto | Identificador do registro de cliente usado pelo pedido |
| `customer_unique_id` | Texto | Identificador persistente usado para reconhecer compras repetidas na amostra |
| `customer_zip_code_prefix` | Texto | Primeiros cinco dígitos do CEP registrado para o cliente |
| `customer_city` | Texto | Cidade do cliente no registro |
| `customer_state` | Texto | Sigla da UF registrada para o cliente |

## Geolocalização — `olist_geolocation_dataset.csv`

Uma observação geográfica por linha, com várias ocorrências por prefixo e linhas idênticas. O arquivo não fornece um identificador de linha.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `geolocation_zip_code_prefix` | Texto | Primeiros cinco dígitos do CEP da observação |
| `geolocation_lat` | Decimal | Latitude em graus decimais |
| `geolocation_lng` | Decimal | Longitude em graus decimais |
| `geolocation_city` | Texto | Cidade associada à observação |
| `geolocation_state` | Texto | Sigla da UF associada à observação |

## Itens de pedidos — `olist_order_items_dataset.csv`

Uma linha por item identificado pela combinação de pedido e sequência do item.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `order_id` | Texto | Pedido ao qual o item pertence |
| `order_item_id` | Inteiro | Sequência do item dentro do pedido |
| `product_id` | Texto | Produto do item |
| `seller_id` | Texto | Vendedor responsável pelo item |
| `shipping_limit_date` | Data e hora | Prazo registrado para o envio do item |
| `price` | Decimal | Preço do item em R$ |
| `freight_value` | Decimal | Valor de frete associado ao item em R$ |

## Pagamentos — `olist_order_payments_dataset.csv`

Uma linha por sequência de pagamento de um pedido. Um pedido pode ter múltiplas linhas de pagamento.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `order_id` | Texto | Pedido ao qual o pagamento está associado |
| `payment_sequential` | Inteiro | Sequência do registro de pagamento no pedido |
| `payment_type` | Texto | Modalidade registrada, como cartão, boleto ou voucher |
| `payment_installments` | Inteiro | Quantidade de parcelas registrada na linha |
| `payment_value` | Decimal | Valor associado à linha de pagamento em R$ |

## Avaliações — `olist_order_reviews_dataset.csv`

Uma observação de avaliação por linha. Existem pedidos com mais de uma avaliação e identificadores de avaliação repetidos. Consulte a [verificação de chaves](source_relationships.md) antes de definir uma regra de consolidação.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `review_id` | Texto | Identificador fornecido para a avaliação |
| `order_id` | Texto | Pedido associado à avaliação |
| `review_score` | Inteiro | Nota na escala de 1 a 5 |
| `review_comment_title` | Texto | Título opcional do comentário |
| `review_comment_message` | Texto | Mensagem opcional do comentário |
| `review_creation_date` | Data e hora | Data de criação do registro da pesquisa |
| `review_answer_timestamp` | Data e hora | Momento registrado da resposta à pesquisa |

## Pedidos — `olist_orders_dataset.csv`

Uma linha por `order_id`, com o status do pedido na amostra e os eventos disponíveis.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `order_id` | Texto | Identificador do pedido |
| `customer_id` | Texto | Identificador do registro de cliente associado ao pedido |
| `order_status` | Texto | Status observado, incluindo `delivered`, `canceled` e `unavailable` |
| `order_purchase_timestamp` | Data e hora | Momento da compra |
| `order_approved_at` | Data e hora | Momento de aprovação registrado |
| `order_delivered_carrier_date` | Data e hora | Momento registrado da entrega à transportadora |
| `order_delivered_customer_date` | Data e hora | Momento registrado da entrega ao cliente |
| `order_estimated_delivery_date` | Data e hora | Data de entrega prevista no registro do pedido |

## Produtos — `olist_products_dataset.csv`

Uma linha por `product_id`. A grafia original de `product_name_lenght` e `product_description_lenght` foi preservada.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `product_id` | Texto | Identificador do produto |
| `product_category_name` | Texto | Nome original da categoria em português |
| `product_name_lenght` | Inteiro | Comprimento do nome do produto em caracteres |
| `product_description_lenght` | Inteiro | Comprimento da descrição em caracteres |
| `product_photos_qty` | Inteiro | Quantidade registrada de fotos |
| `product_weight_g` | Decimal | Peso registrado em gramas |
| `product_length_cm` | Decimal | Comprimento registrado em centímetros |
| `product_height_cm` | Decimal | Altura registrada em centímetros |
| `product_width_cm` | Decimal | Largura registrada em centímetros |

## Vendedores — `olist_sellers_dataset.csv`

Uma linha por `seller_id` na amostra.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `seller_id` | Texto | Identificador do vendedor |
| `seller_zip_code_prefix` | Texto | Primeiros cinco dígitos do CEP registrado para o vendedor |
| `seller_city` | Texto | Cidade registrada para o vendedor |
| `seller_state` | Texto | Sigla da UF registrada para o vendedor |

## Tradução de categorias — `product_category_name_translation.csv`

Uma linha por categoria original mapeada.

| Campo | Tipo lógico | Significado |
| --- | --- | --- |
| `product_category_name` | Texto | Nome original da categoria em português |
| `product_category_name_english` | Texto | Tradução disponível em inglês |

Para contagens, cobertura e exceções observadas, consulte os [relacionamentos](source_relationships.md) e o [relatório de qualidade](../reports/data_quality_report.md).
