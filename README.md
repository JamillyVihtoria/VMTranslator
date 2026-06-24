# VM Translator - Nand2Tetris

## Integrantes

| Nome Completo | Matrícula |
|--------------|-----------|
| Jamilly Vitoria Ferreira Barbosa | 20250071213 |
| Marcos Vinicius Jansem Oliveira | 20250071278 |

---

## Linguagem Utilizada

- **Linguagem:** Python
- **Versão recomendada:** Python 3.10+

---

## Estrutura do Projeto

```text
VMTRANSLATOR/
├── codewriter.py
├── parser.py
├── main.py
├── test_vmtranslator.py
├── README.md
│
├── 07/
│   ├── BasicTest/
│   ├── SimpleAdd/
│   └── MemoryAccess/
│
└── 08/
    ├── ProgramFlow/
    │   ├── BasicLoop/
    │   └── FibonacciSeries/
    │
    └── FunctionCalls/
        ├── SimpleFunction/
        └── NestedCall/
```

---

## Dependências

Este projeto utiliza apenas bibliotecas da biblioteca padrão do Python.

Não é necessária a instalação de dependências externas.

---

## Build

Não é necessário compilar o projeto.

Verifique apenas se o Python está instalado:

```bash
python --version
```

---

## Execução

### Tradução de um único arquivo `.vm`

```bash
python main.py <arquivo.vm>
```

Exemplo:

```bash
python main.py 07/BasicTest/BasicTest.vm
```

Saída:

```text
BasicTest.asm
```

---

### Tradução de um diretório (Parte 2)

```bash
python main.py <diretorio>
```

Exemplo:

```bash
python main.py 08/FunctionCalls/NestedCall
```

Saída:

```text
NestedCall.asm
```

O arquivo gerado conterá:

- Código de bootstrap
- Tradução de todos os arquivos `.vm` encontrados no diretório

---

## Funcionalidades Implementadas

### Parte 1 – Comandos Aritméticos e Acesso à Memória

#### Arithmetic Commands

- add
- sub
- neg
- eq
- gt
- lt
- and
- or
- not

#### Memory Access

##### Push

- constant
- local
- argument
- this
- that
- temp
- pointer
- static

##### Pop

- local
- argument
- this
- that
- temp
- pointer
- static

---

### Parte 2 – Controle de Fluxo e Sub-rotinas

#### Bootstrap

Implementação do código de inicialização da máquina virtual:

```text
SP = 256
call Sys.init
```

Executado automaticamente ao traduzir diretórios.

---

#### Controle de Fluxo

Suporte aos comandos:

```vm
label
goto
if-goto
```

Esses comandos permitem a criação de laços, desvios condicionais e estruturas de controle.

---

#### Funções e Sub-rotinas

Suporte aos comandos:

```vm
function
call
return
```

Recursos implementados:

- Criação de funções
- Inicialização de variáveis locais
- Salvamento do frame do chamador
- Restauração do contexto durante o retorno
- Geração de endereços de retorno únicos
- Suporte a chamadas aninhadas
- Suporte a recursão

---

#### Suporte a Múltiplos Arquivos VM

O tradutor aceita diretórios contendo vários arquivos `.vm`.

Todos os arquivos encontrados são processados e concatenados em um único arquivo `.asm`, conforme especificado no Projeto 08 do Nand2Tetris.

---

## Exemplo

### Entrada VM

```vm
function Main.main 0
push constant 10
push constant 20
add
return
```

### Saída Assembly (trecho simplificado)

```asm
(Main.main)

@10
D=A
...

@20
D=A
...

M=M+D
```

---

## Validação

Os arquivos gerados foram testados utilizando os scripts oficiais do projeto Nand2Tetris.

### Parte 1

- SimpleAdd
- BasicTest

### Parte 2

#### Program Flow

- BasicLoop
- FibonacciSeries

#### Function Calls

- SimpleFunction
- NestedCall

Os testes foram executados por meio do CPU Emulator utilizando os arquivos `.tst` disponibilizados pelo Nand2Tetris.

---

## Justificativa da Escolha da Linguagem

Python foi escolhido por possuir sintaxe simples e legível, facilitando a implementação do parser e do gerador de código Assembly.

Além disso, oferece excelente suporte para manipulação de arquivos texto, requisito fundamental para o desenvolvimento do VM Translator.

---

## Evolução do Projeto

### Parte 1

- Implementação dos comandos aritméticos
- Implementação dos segmentos de memória
- Tradução de arquivos VM individuais

### Parte 2

- Implementação do Bootstrap
- Implementação de Controle de Fluxo
- Implementação de Funções e Sub-rotinas
- Suporte a múltiplos arquivos `.vm`
- Tradução de diretórios completos

---

## Referências

- Nand2Tetris – The Elements of Computing Systems
- Projeto 07 – VM Translator
- Projeto 08 – Program Flow and Function Calls
- CPU Emulator do Nand2Tetris
