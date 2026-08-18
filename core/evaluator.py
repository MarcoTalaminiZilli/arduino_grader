import json
import ollama

class CodeEvaluator:
    @staticmethod
    def evaluate(solucao: str, aluno: str, config: dict) -> dict:
        prompt_sistema = (
            "Você é um professor avaliando um código C++/Arduino enviado por um aluno. "
            "Compare a LÓGICA do código do aluno com o GABARITO fornecido.\n\n"
            "Diretrizes de avaliação:\n"
            "1. Ignore diferenças puramente sintáticas ou de estilo (ex: uso de variáveis para pinos, "
            "troca de 'for' por 'while', nomes de variáveis diferentes).\n"
            "2. Verifique se a funcionalidade esperada pelo gabarito é atingida.\n"
            "3. Verifique se as funções essenciais setup() e loop() existem.\n\n"
            "Regras de saída:\n"
            "Responda EXCLUSIVAMENTE um objeto JSON com esta estrutura exata:\n"
            "{\n"
            '  "nota": <float entre 0.0 e 100.0>,\n'
            '  "estruturas_ok": <boolean true/false>,\n'
            '  "feedback": "<string com 1-2 frases explicando o acerto ou o erro do aluno>"\n'
            "}"
        )

        user_content = f"--- GABARITO ---\n{solucao}\n\n--- CÓDIGO DO ALUNO ---\n{aluno}"

        # Modelo padrão pode ser sobrescrito pelo config.json
        modelo = config.get("modelo_ollama", "llama3")

        try:
            response = ollama.chat(
                model=modelo,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": user_content}
                ],
                options={"temperature": 0.0},  # Garante respostas determinísticas
                format="json"                   # Força a LLM a retornar JSON estrito
            )

            dados = json.loads(response["message"]["content"])

            return {
                "final_score": float(dados.get("nota", 0.0)),
                "has_essential": bool(dados.get("estruturas_ok", False)),
                "feedback": str(dados.get("feedback", "Sem observações."))
            }

        except Exception as e:
            return {
                "final_score": 0.0,
                "has_essential": False,
                "feedback": f"Erro na avaliação via IA: {str(e)}"
            }