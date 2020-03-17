# Processador Harry Potter

O seguinte projeto, inserido no âmbito da U.C. de Scripting no Processamento de Linguagem Natural, tinha o objetivo de processar o livro "Harry Potter e a Pedra Filosofal" na linguagem <em>python</em>. Com o intuito de recolher todas as combinações de nomes próprios na mesma frase, e realizar uma análise sobre esses dados.

## Processamento

Primeiramente, no que concerne ao processamento do ficheiro, temos a função `getTexto()` que realiza a leitura do ficheiro linha a linha e retorna o texto.

Tendo o texto como input, a função `frases()` faz a distinção entre as várias frases. Para identificar cada frase, foram utilizadas duas expressões regulares:

    exp1 = r"(\n\n+\s*)([\“\"A-Z])"
    exp2 = r"([a-z][.?!]+\s*)([\“\"A-Z])"

Utilizando a função `re.sub()`, é feito o <em>pattern matching</em> das frases com as expressões <em>regex</em>, e é colocado um `@` em cada mudança de frase.
Também recorreu-se a outras duas expressões regulares auxiliares para eliminar os marcadores de página, assim como ignorar o caso de ter "Mr." ou "Mrs." como final de frase.

A parte final do processamento, com a função `entidades()`, passa por identificar as diferentes entidades, combinações e calcular o nº de ocorrências dessas combinações.
Como tal, primeiro dividiu-se uma expressão regular em 3 partes:

    s = r"\s+"
    maiusc = r"(?:[A-Z]\w+(?:[-\']\w+)*|[A-Z]\.)"
    ent = f"({maiusc}(?:{s}{maiusc}|{s}{maiusc})*)"

A <em>regex</em> `s` identifica espaços, `maiusc` identifica palavras que iniciam com maiúscula, e a `ent` identifica um ou mais nomes.
Logo para cada frase é aplicada a expressão `ent`e aí obtem-se a lista de entidades por frase. É utilizada a função `combinations()` para fazer as diferentes combinações, e cada uma destas é guardada como **key** num dicionário, sendo o respetivo **value** o nº de ocorrências.

## Estratégia de Limpeza

Como nem sempre é fácil identificar corretamente nomes de pessoas, foi necessário implementar algumas estratégias de limpeza de ruído:

- Reparou-se que muito do "lixo" se tratava de pronomes ou construtores de início de frase, logo foi criada uma lista com estas palavras que seriam filtradas e descartadas.

- Definiu-se um valor mínimo de nº de ocorrências de 10, de modo a obtermos apenas as relações mais relevantes entre personagens. Este filtro é realizado pela função `limpa()`.

## Nº Combinações

Após todo o processamento do texto, armazenamento e limpeza dos dados pretendidos, apenas foi necessário chamar a função `len()` para calcular o tamanho do dicionário. O nº total de combinações diferentes obtido é de **33**.

## Interpretador

Tendo já o dicionário com os dados relevantes, criou-se uma função `interpretador()`. Esta mostra a tabela das diferentes combinações, e consoante um <em>input</em> do utilizador correspondente a um dos nomes da tabela, imprime as respetivas entidades com quem interagiu.

Sendo assim apenas foi necessário percorrer o dicionário e identificar as relações a retornar, preenchendo um outro dicionário `amigos`. No final é feito um <em>sort</em> para ordenar por ordem decrescente de valor, imprimindo para o ecrã as top5 entidades que tiveram maior interação.

## Grafo de Relações

De modo a termos uma melhor visão da rede de relações criada, criou-se um grafo que a demonstra, através da função `graph()`.
Para tal utilizou-se o módulo de grafos do <em>python</em> denominado **graphviz**.

Mais uma vez, foi necessário percorrer o dicionário de dados e criar por cada entrada, dois `node` que representam as duas entidades, e uma `edge` que liga esse par de nós. Essa `edge` tem como valor o nº de interações das respetivas entidades.

No final da execução do programa, este grafo é gravado na diretoria com o nome **grafo.png**:

![Alt text](grafo.png?raw=true "Grafo")

## Executar o Programa

O programa recebe como argumento apenas o ficheiro a processar, tal como:

    python3 processor.py harryPotter.txt

É importante realçar que para a correta execução do programa, é necessário instalar na máquina o módulo do **graphviz**.
