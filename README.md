# Elgol Lexer

Este projeto é um interpretador para a linguagem **Elgol**, que possui um conjunto de regras léxicas para identificar identificadores, palavras reservadas, operadores e outras estruturas essenciais dessa linguagem. Ele foi implementado utilizando a biblioteca `ply` (Python Lex-Yacc) para analisar e tokenizar o código-fonte da linguagem Elgol.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Uso no Linux](#instalação-e-uso-no-linux)

## Sobre o Projeto

O **Elgol Lexer** é um projeto que visa a implementação de um analisador léxico para a linguagem Elgol. Ele identifica e classifica tokens do código-fonte com base nas regras da linguagem.

### Funcionalidades:
- Reconhecimento de identificadores (nomes de variáveis e funções).
- Detecção de palavras reservadas específicas do Elgol.
- Suporte a operações matemáticas: soma (+), subtração (-), multiplicação (x) e divisão (/).
- Análise de números inteiros sem zeros à esquerda.
- Suporte a declarações e estruturas da linguagem Elgol.

---

## Pré-requisitos

- Python 3 instalado (recomendado 3.7 ou superior)
- Git instalado
- `pip` instalado (gerenciador de pacotes Python)

Verifique a instalação com:

```bash
python3 --version
git --version
pip3 --version
```
## Instalação e Uso no Linux
git clone https://github.com/ErnestoTSantos/Elgolinterpreter

python3 -m venv venv

source venv/bin/activate

pip install ply

python3 main.py

