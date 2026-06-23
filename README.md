# Evolução do Projeto

Este projeto é a evolução direta do sistema original **Sistema de Métodos Numéricos v5**, desenvolvido inicialmente como uma aplicação monolítica focada na resolução de exercícios de Métodos Numéricos.

A primeira versão cumpria com excelência o objetivo didático, apresentando fórmulas, substituições, tabelas e resultados passo a passo. Entretanto, à medida que novos conteúdos foram sendo adicionados, o crescimento do código em um único arquivo tornou a manutenção mais complexa.

## Principais melhorias implementadas

### Arquitetura Modular

Antes:

```text
sistema_metodos_numericos_v5.py
```

Agora:

```text
src/
└── metodos_numericos/
    ├── representacao_numerica/
    ├── equacoes_nao_lineares/
    ├── sistemas_lineares/
    ├── interpolacao_polinomial/
    ├── integracao_numerica/
    └── derivacao_numerica/
```

Cada assunto possui sua própria estrutura de diretórios, tornando o projeto mais organizado, escalável e fácil de manter.

### Aplicação de Conceitos de Clean Code

Foram aplicados conceitos inspirados em:

* Clean Code (Robert C. Martin)
* Clean Architecture (Robert C. Martin)
* The Clean Coder (Robert C. Martin)

Melhorias realizadas:

* Separação de responsabilidades.
* Redução de acoplamento.
* Organização por domínio de conhecimento.
* Estrutura preparada para expansão futura.
* Reutilização de componentes comuns.

### Evolução da Interface

A versão original possuía uma visualização inicial dos resultados.

Nesta nova versão:

* Interface web reorganizada.
* Estrutura preparada para expansão visual.
* Integração entre módulos numéricos e interface.
* Melhor experiência para estudo e resolução de exercícios.

### Ampliação do Conteúdo

Além dos métodos já existentes, foram adicionados e reorganizados conteúdos como:

#### Representação Numérica

* Conversão entre bases (2 a 36)
* Parte inteira e fracionária
* Overflow e Underflow
* Ponto Flutuante

#### Equações Não Lineares

* Bisseção
* Falsa Posição
* Newton-Raphson
* Secantes
* Ponto Fixo

#### Sistemas Lineares

* Eliminação de Gauss
* Decomposição LU
* Cholesky
* Gauss-Jacobi
* Gauss-Seidel

#### Interpolação e Aproximação

* Lagrange
* Newton por Diferenças Divididas
* Mínimos Quadrados

#### Cálculo Numérico

* Regra dos Trapézios
* Regra de Simpson 1/3
* Diferenças Finitas

## Comparação entre versões

| Característica           | Sistema v2 | Acadêmico Pro |
| ------------------------ | ---------- | ------------- |
| Estrutura modular        | ❌          | ✅             |
| Clean Code               | ❌          | ✅             |
| Clean Architecture       | ❌          | ✅             |
| Organização por domínio  | ❌          | ✅             |
| Interface web integrada  | Parcial    | ✅             |
| Escalabilidade           | Baixa      | Alta          |
| Facilidade de manutenção | Média      | Alta          |
| Reutilização de código   | Baixa      | Alta          |
| Expansão futura          | Limitada   | Preparada     |

## Objetivo Mantido

Apesar da refatoração completa da estrutura, a essência do projeto foi preservada:

**ser uma ferramenta de aprendizado que ensina o desenvolvimento dos cálculos passo a passo, permitindo compreender os métodos numéricos e não apenas obter respostas prontas.**
