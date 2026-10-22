# Métodos Numéricos — Sistema Interativo de Cálculo e Aprendizagem

> Uma ferramenta educacional para explorar métodos numéricos, acompanhar etapas de cálculo e compreender os resultados — no navegador ou pelo terminal.

![Python](https://img.shields.io/badge/Python-CLI-3776AB?logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Web-F7DF1E?logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-Interface-E34F26?logo=html5&logoColor=white)
![Status](https://img.shields.io/badge/Projeto-Acad%C3%AAmico-64748B)

## Sobre o projeto

O **Métodos Numéricos** nasceu do interesse em transformar procedimentos matemáticos, muitas vezes vistos apenas como fórmulas, em experiências que possam ser exploradas na prática.

O repositório reúne **duas implementações independentes**: uma aplicação web construída em HTML, CSS e JavaScript e um programa interativo em Python executado pelo terminal. O objetivo didático é acompanhar o raciocínio por trás dos cálculos, incluindo fórmulas, aproximações, iterações e resultados, conforme o método escolhido.

A proposta não é apenas encontrar uma resposta numérica, mas facilitar o entendimento de **como** ela foi obtida.

## Funcionalidades

| Área | Métodos e operações |
| --- | --- |
| **Análise de erros e aritmética** | Erro absoluto e relativo; máximo erro relativo de arredondamento; proporção de erro; MMC, MDC e fatoração; operações com frações; underflow e overflow |
| **Equações não lineares** | Bisseção; falsa posição; Newton-Raphson; secantes; ponto fixo |
| **Sistemas lineares** | Eliminação de Gauss; decomposição LU; Gauss-Jacobi; Gauss-Seidel; Cholesky |
| **Interpolação** | Lagrange; Newton por diferenças divididas |
| **Integração numérica** | Regra dos trapézios; Simpson 1/3 |
| **Derivação numérica** | Diferenças progressiva, regressiva e central; segunda derivada central |

### Versão web

- Interface organizada por categorias de métodos.
- Formulários para inserir funções, intervalos, matrizes, vetores e tolerâncias.
- Exibição de resultados e, conforme a operação, tabelas, etapas de cálculo e fórmulas.
- Visualização gráfica para a seção de equações não lineares.
- Seção de ajuda com exemplos de escrita de funções matemáticas.
- Layout adaptável a diferentes tamanhos de tela.

### Versão Python

- Menus interativos no terminal, organizados por grupos de métodos.
- Entrada de parâmetros e funções matemáticas pelo teclado.
- Demonstração textual de fórmulas, substituições, iterações e resultados.
- Recursos para normalizar expressões matemáticas comuns.

## Como executar

### Opção 1 — Aplicação web

Não é necessário instalar pacotes para abrir a interface web.

1. Clone o repositório ou baixe os arquivos:

   ```bash
   git clone https://github.com/JhonataFontoura/Metodos-numericos.git
   cd Metodos-numericos
   ```

2. Abra o arquivo `metodos_numericos_web_resultados_melhorados.html` no navegador.
3. Escolha a categoria, informe os dados e execute o cálculo.

> A implementação web está concentrada em um arquivo HTML com estilos CSS e código JavaScript. Não há, na estrutura atual do repositório, um servidor ou etapa de compilação obrigatória para essa interface.

### Opção 2 — Programa Python

**Pré-requisito:** Python 3 instalado.

No terminal, dentro da pasta do projeto, execute:

```bash
python sistema_metodos_numericos_v5_funcoes_verificadas.py
```

Se seu ambiente utilizar `python3`:

```bash
python3 sistema_metodos_numericos_v5_funcoes_verificadas.py
```

A aplicação apresenta menus para selecionar operações e informar os parâmetros necessários.

> O arquivo Python utiliza bibliotecas da própria linguagem, como `math`, `fractions`, `functools` e `re`. Não há arquivo `requirements.txt` na versão consultada.

## Exemplo de utilização

Para explorar um método de busca de raízes:

1. Abra a **versão web** e selecione **Equações Não Lineares**.
2. Escolha **Bisseção**.
3. Informe a função `x^3 - x - 2`.
4. Defina o intervalo `[1, 2]`, as tolerâncias e o limite de iterações.
5. Execute o cálculo para acompanhar o resultado e a tabela de iterações.

A interface aceita formatos como `x^3`, `x³`, `sen(x)`, `raiz(x)` e `2x + 3` em seus campos de funções. Algumas operações exigem condições específicas, como intervalo adequado, matriz compatível ou número par de subintervalos para Simpson 1/3.

## Estrutura do repositório

```text
Metodos-numericos/
├── metodos_numericos_web_resultados_melhorados.html
└── sistema_metodos_numericos_v5_funcoes_verificadas.py
```

| Arquivo | Responsabilidade |
| --- | --- |
| `metodos_numericos_web_resultados_melhorados.html` | Interface web, estilos e cálculos em JavaScript |
| `sistema_metodos_numericos_v5_funcoes_verificadas.py` | Aplicação de terminal, menus e implementações em Python |

**Observação:** as duas versões implementam os métodos em seus próprios códigos. Não existe, na estrutura consultada, uma API que conecte o HTML ao programa Python.

## Tecnologias utilizadas

- **Python:** operações numéricas, funções matemáticas e interface de linha de comando.
- **JavaScript:** cálculos e interatividade da aplicação web.
- **HTML5 e CSS3:** estrutura visual e apresentação dos resultados.
- **Git e GitHub:** versionamento e disponibilização do código.

## Objetivos de aprendizagem

Este projeto foi desenvolvido como uma forma de aproximar teoria e prática. Entre os conhecimentos exercitados estão:

- Implementação de algoritmos matemáticos.
- Representação de aproximações e análise de erros.
- Uso de critérios de parada e tolerâncias em processos iterativos.
- Manipulação de funções, matrizes e vetores.
- Organização de fluxos de entrada, processamento e apresentação de resultados.
- Desenvolvimento de interfaces para apoiar a aprendizagem.

## Limitações e cuidados

O sistema tem **finalidade acadêmica e educacional**. Resultados numéricos dependem dos dados informados, dos critérios de convergência e das limitações de precisão de ponto flutuante. Recomenda-se conferir os resultados em aplicações que exijam elevada confiabilidade.

O repositório atual não inclui uma suíte automatizada de testes, documentação de cobertura ou evidências de validação de todos os cenários possíveis. Portanto, a presença de um método no código não deve ser interpretada como garantia de precisão em qualquer entrada.

## Autor

**Jhonata Fontoura Nunes**  
Estudante de Ciência da Computação — UniCarioca

- [Perfil no GitHub](https://github.com/JhonataFontoura)
- [Repositório do projeto](https://github.com/JhonataFontoura/Metodos-numericos)

---

*Aprender um método é mais do que aplicar uma fórmula: é compreender cada etapa até chegar ao resultado.*
