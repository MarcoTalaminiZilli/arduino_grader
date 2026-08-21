import json
import ollama

class CodeEvaluator:
    @staticmethod
    def evaluate(solucao: str, aluno: str, config: dict) -> dict:
        # Prompt padrão de segurança
        default_prompt = (
            "Você é um professor avaliando um código C++/Arduino enviado por um aluno. "
            "Compare a LÓGICA do código do aluno com o GABARITO fornecido.\n\n"
            "Responda EXCLUSIVAMENTE um objeto JSON com esta estrutura exata:\n"
            "{\n"
            '  "nota": <float entre 0.0 e 100.0>,\n'
            '  "estruturas_ok": <boolean true/false>,\n'
            '  "feedback": "<string com 1-2 frases>"\n'
            "}"
        )

        # Lê o prompt do config.json se existir; caso contrário, usa o default
        prompt_sistema = config.get("prompt_sistema", default_prompt)
        # Usa o modelo especificado no config.json ou "llama3" como padrão
        modelo = config.get("modelo_ollama", "llama3")

        user_content = f"--- GABARITO ---\n{solucao}\n\n--- CÓDIGO DO ALUNO ---\n{aluno}"

        try:
            response = ollama.chat(
                model=modelo,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": user_content}
                ],
                options={"temperature": 0.0, "keep_alive": 0},
                format="json"
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