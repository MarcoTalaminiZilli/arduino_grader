# Arduino Grader

O **Arduino Grader** é uma ferramenta em Python desenvolvida para automatizar a correção e avaliação estática de códigos de Arduino (`.ino`) submetidos por alunos.

O projeto analisa a estrutura do código C++/Arduino utilizando expressões regulares e heurísticas leves, validando a presença de funções essenciais (`setup` e `loop`) e comparando o uso de instruções com um código de gabarito oficial. Os resultados são exportados diretamente para um relatório formatado em Excel.

---

## Funcionalidades

- **Análise Estática Leve:** Não depende de parsers de C rígidos, sendo imune a erros comuns de compilação ou macros específicas do ecossistema Arduino.
- **Pré-processamento de Código:** Remove comentários de bloco (`/* */`) e de linha (`//`) antes da avaliação para evitar falsos positivos.
- **Detecção de Estruturas:** Verifica se o código possui a estrutura básica de funcionamento (`setup()` e `loop()`).
- **Mapeamento de Funções:** Compara o conjunto de chamadas de função (`pinMode`, `digitalWrite`, `delay`, etc.) presentes no arquivo do aluno com o gabarito.
- **Configuração Flexível:** Pesos de notas, pastas de entrada e nomes de relatórios são totalmente customizáveis via `config.json`.
- **Relatório em Excel:** Gera uma planilha `.xlsx` com formatação visual, notas finais calculadas e status detalhado por entrega.

---

## Estrutura do Projeto

```text
arduino_grader/
├── config.json           # Arquivo de configuração de pesos e diretórios
├── main.py               # Script principal de execução
├── requirements.txt      # Dependências do projeto
├── core/
│   ├── __init__.py
│   ├── loader.py         # Leitura, varredura e limpeza de arquivos .ino
│   ├── evaluator.py      # Lógica de avaliação e cálculo de pontuação
│   └── reporter.py       # Exportação e formatação do relatório Excel
├── solutions/            # Pasta reservada para os arquivos de gabarito (.ino)
└── submissions/          # Pasta reservada para os arquivos dos alunos (.ino)
```

---

## Pré-requisitos e Instalação

### 1. Clonar o repositório
```bash
git clone [https://github.com/SEU_USUARIO/arduino-grader.git](https://github.com/SEU_USUARIO/arduino-grader.git)
cd arduino-grader
```

### 2. Instalar as dependências
Certifique-se de ter o Python 3.8+ instalado. Instale os pacotes necessários rodando:
```bash
pip install -r requirements.txt
```

---

## Configuração (`config.json`)

Você pode ajustar os pesos e caminhos das pastas alterando o arquivo `config.json` na raiz do projeto:

```json
{
  "diretorios": {
    "solucoes": "solutions",
    "entregas": "submissions",
    "relatorio_saida": "relatorio_notas.xlsx"
  },
  "pesos_avaliacao": {
    "estrutura_basica": 50.0,
    "chamadas_funcao": 50.0
  }
}
```

---

## Como Usar

1. **Adicionar o Gabarito:**
   Coloque o arquivo `.ino` de referência na pasta `solutions/` (Exemplo: `E1T1_solution.ino`).

2. **Adicionar os Trabalhos dos Alunos:**
   Coloque os arquivos dos alunos na pasta `submissions/`. O padrão esperado de nome de arquivo é `IDALUNO_EXERCICIO.ino` (Exemplo: `joao123_E1T1.ino`).

3. **Executar a Avaliação:**
   No terminal, rode o script principal:
   ```bash
   python main.py
   ```

4. **Visualizar os Resultados:**
   Um relatório formatado será gerado na raiz do projeto com o nome definido no `config.json` (padrão: `relatorio_notas.xlsx`).

---
