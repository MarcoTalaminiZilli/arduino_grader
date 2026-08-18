# Arduino Grader - Branch LLM

O **Arduino Grader** nesta branch utiliza uma **LLM local (via Ollama)** para automatizar a correção e avaliação semântica de códigos do Arduino (`.ino`). 

Diferente de corretores baseados apenas em expressões regulares, a IA analisa a **lógica** do programa, ignorando variações de sintaxe ou de estilo (como nomes de variáveis diferentes) e gerando um **feedback explicativo** para cada aluno.

---

## Funcionalidades

- **Avaliação Semântica por IA:** Entende a intenção do código do aluno em vez de apenas buscar palavras-chave exatas.
- **Respostas Determinísticas:** Utiliza `temperature=0.0` e formato de saída JSON estrito para garantir notas consistentes.
- **Feedback Automático:** Gera justificativas curtas para cada nota obtida.
- **Execução 100% Local:** Sem custos de API e sem envio de dados para servidores externos.
- **Relatório Completo em Excel:** Gera uma planilha `.xlsx` com notas, checagem de estruturas e a coluna de parecer da IA formatada com quebra automática de texto.

---

## Estrutura do Projeto

```text
arduino_grader/
├── config.json           # Configuração de diretórios e modelo do Ollama
├── main.py               # Execução principal do pipeline de avaliação
├── requirements.txt      # Dependências do projeto (incluindo ollama)
├── core/
│   ├── __init__.py
│   ├── loader.py         # Leitura e limpeza de comentários do arquivo .ino
│   ├── evaluator.py      # Integração com a API local do Ollama e avaliação
│   └── reporter.py       # Gerador do relatório formatado em Excel
├── solutions/            # Gabaritos de referência (.ino)
└── submissions/          # Entregas dos alunos (.ino)
```

---

## Pré-requisitos e Instalação

### 1. Selecionar a branch `llm`
```bash
git checkout llm
```

### 2. Instalar e iniciar o Ollama
Certifique-se de ter o [Ollama](https://ollama.com/) instalado no seu sistema.

Inicialize o serviço do Ollama e baixe o modelo desejado (por padrão, o `llama3`):
```bash
ollama pull llama3
```

### 3. Instalar as dependências Python
```bash
pip install -r requirements.txt
```

---

## Configuração (`config.json`)

Edite o arquivo `config.json` para definir o modelo do Ollama e as pastas de trabalho:

```json
{
  "diretorios": {
    "solucoes": "solutions",
    "entregas": "submissions",
    "relatorio_saida": "relatorio_notas.xlsx"
  },
  "modelo_ollama": "llama3"
}
```

---

## Passo a Passo para Testar

1. **Gabarito:** Coloque um arquivo de referência em `solutions/` (ex: `E1T1_solution.ino`).
2. **Entregas:** Coloque um ou mais arquivos de teste em `submissions/` (ex: `aluno01_E1T1.ino`).
3. **Execução:** Garanta que o Ollama esteja rodando em segundo plano e execute:
   ```bash
   python main.py
   ```
4. **Resultado:** Abra o arquivo `relatorio_notas.xlsx` gerado na raiz do projeto para verificar as notas e os feedbacks produzidos pela IA.

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.