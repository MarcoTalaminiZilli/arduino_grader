# Arduino Grader - Branch LLM

O **Arduino Grader** nesta branch utiliza uma **LLM local (via Ollama)** para automatizar a correção e avaliação semântica de códigos do Arduino (`.ino`). 

A IA analisa a **lógica** do programa, comparando o código do aluno com o gabarito. Ela ignora variações irrelevantes de sintaxe ou estilo (como nomes de variáveis diferentes) e gera justificativas detalhadas para cada nota.

---

## Funcionalidades

- **Avaliação Semântica por IA:** Entende a intenção do código do aluno em vez de apenas buscar palavras-chave exatas.
- **Prompt Customizável:** As regras de avaliação e o formato de resposta são totalmente configuráveis via `config.json`.
- **Respostas Determinísticas:** Utiliza `temperature=0.0` e formato JSON estrito para garantir notas e formatos consistentes.
- **Feedback Automático:** Gera justificativas explicativas para cada nota obtida.
- **Execução 100% Local:** Sem custos de API e sem envio de dados para servidores externos.
- **Relatório Completo em Excel:** Gera uma planilha `.xlsx` com notas, checagem de estruturas e a coluna de parecer da IA formatada com quebra automática de texto.

---

## Estrutura do Projeto

```text
arduino_grader/
├── config.json           # Configuração de diretórios, modelo e prompt do Ollama
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

Inicialize o serviço do Ollama e baixe o modelo desejado (por exemplo, `llama3`):
```bash
ollama pull llama3
```

### 3. Instalar as dependências Python
```bash
pip install -r requirements.txt
```

---

## Configuração (`config.json`)

Edite o arquivo `config.json` para definir pastas, o modelo do Ollama e as instruções do prompt de avaliação:

```json
{
  "diretorios": {
    "solucoes": "solutions",
    "entregas": "submissions",
    "relatorio_saida": "relatorio_notas.xlsx"
  },
  "modelo_ollama": "llama3",
  "prompt_sistema": "Você é um professor avaliando um código C++/Arduino enviado por um aluno. Compare a LÓGICA do código do aluno com o GABARITO fornecido.\n\nDiretrizes de avaliação:\n1. Ignore diferenças puramente sintáticas ou de estilo (ex: uso de variáveis para pinos, troca de 'for' por 'while', nomes de variáveis diferentes).\n2. Verifique se a funcionalidade esperada pelo gabarito é atingida.\n3. Verifique se as funções essenciais setup() e loop() existem.\n\nRegras de saída:\nResponda EXCLUSIVAMENTE um objeto JSON com esta estrutura exata:\n{\n  \"nota\": <float entre 0.0 e 100.0>,\n  \"estruturas_ok\": <boolean true/false>,\n  \"feedback\": \"<string com 1-2 frases explicando o acerto ou o erro do aluno>\"\n}"
}
```

> **Aviso sobre a Escolha do Modelo (`modelo_ollama`):**
> O modelo pode ser alterado no `config.json` para qualquer opção suportada pelo seu Ollama local (ex: `llama3`, `mistral`, `gemma2`, `codellama`), permitindo adaptar o projeto à capacidade de processamento (GPU/RAM) da sua máquina.
>
> ⚠️ **Atenção:** Modelos muito leves ou compactos (como versões de 1B a 3B de parâmetros) exigem menos hardware, porém **podem comprometer a qualidade das avaliações**. Eles apresentam maior probabilidade de falhar na interpretação da lógica do C++, na geração do JSON estrito ou no cumprimento do prompt. Recomenda-se o uso de modelos de no mínimo 7B ou 8B parâmetros para garantir notas e feedbacks confiáveis.

---

## Passo a Passo para Testar

1. **Gabarito:** Coloque o arquivo de referência na pasta `solutions/` (ex: `E1T1_solution.ino`).
2. **Entregas:** Coloque os arquivos dos alunos na pasta `submissions/` (ex: `aluno01_E1T1.ino`).
3. **Execução:** Certifique-se de que o Ollama está rodando e execute:
   ```bash
   python main.py
   ```
4. **Resultado:** Abra o arquivo `relatorio_notas.xlsx` gerado na raiz do projeto para visualizar o relatório completo.

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.