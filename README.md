# VM Translator - Nand2Tetris

## Integrantes

| Nome Completo                    |  Matrícula     |
| ---------------------------------| -------------- |
| Jamilly Vitoria Ferreira Barbosa | 20250071213    |
| Marcos Vinicius Jansem Oliveira  | 20250071278    |

---

## Linguagem Utilizada

* Linguagem: Python
* Versão: Python 3.10+

---

## Estrutura do Projeto

```text
VMTRANSLATOR/
├── 07/
│   ├── BasicTest/
│   │   ├── BasicTest.vm
│   │   ├── BasicTest.asm
│   │   ├── BasicTest.tst
│   │   └── BasicTest.cmp
│   │
│   ├── SimpleAdd/
│   │   ├── SimpleAdd.vm
│   │   ├── SimpleAdd.asm
│   │   ├── SimpleAdd.tst
│   │   └── SimpleAdd.cmp
│   │
│   ├── MemoryAccess/
│   │   └── BasicTest/
│   │       ├── BasicTest.vm
│   │       ├── BasicTest.asm
│   │       ├── BasicTest.tst
│   │       └── BasicTest.cmp
│
├── codewriter.py
├── parser.py
├── main.py
├── test_vmtranslator.py
├── README.md
└── **pycache**/

```

---

## Dependências

Este projeto utiliza apenas bibliotecas da biblioteca padrão do Python.

Nenhuma dependência externa precisa ser instalada.

---

## Build

Não é necessário compilar o projeto.

Verifique se o Python está instalado:

```bash
python --version
```

---

## Execução

Execute o tradutor informando o arquivo `.vm` de entrada:

```bash
python main.py <arquivo.vm>
```

### Exemplo 1

```bash
python main.py 07/BasicTest/BasicTest.vm
```

### Exemplo 2

```bash
python main.py 07/SimpleAdd/SimpleAdd.vm
```
### Exemplo 3

```bash
python main.py 07/MemoryAccess/BasicTest/BasicTest.vm

```

O programa gera automaticamente um arquivo `.asm` no mesmo diretório do arquivo de entrada.

---

## Funcionalidades Implementadas

### Arithmetic Commands

* add
* sub
* neg

### Memory Access Commands

#### Push

* constant
* local
* argument
* this
* that
* temp
* pointer

#### Pop

* local
* argument
* this
* that
* temp
* pointer

---

## Validação

Os arquivos gerados podem ser testados utilizando os scripts `.tst` fornecidos pelo projeto Nand2Tetris e executados no CPU Emulator.

Exemplos:

* BasicTest.tst
* SimpleAdd.tst

---

## Justificativa da Escolha da Linguagem

Python foi escolhido por possuir sintaxe simples e legível, facilitando a implementação do parser e do gerador de código Assembly. Além disso, a linguagem oferece suporte eficiente para manipulação de arquivos texto, requisito essencial para o desenvolvimento do VM Translator.
