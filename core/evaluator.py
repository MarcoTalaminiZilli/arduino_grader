import re
from typing import Dict, Set, Any, Optional

class CodeEvaluator:
    @staticmethod
    def check_essential_structures(code: str) -> Dict[str, bool]:
        has_setup = bool(re.search(r'\bvoid\s+setup\s*\(\s*\)', code))
        has_loop = bool(re.search(r'\bvoid\s+loop\s*\(\s*\)', code))
        return {"has_setup": has_setup, "has_loop": has_loop}

    @staticmethod
    def extract_function_calls(code: str) -> Set[str]:
        keywords = {"if", "for", "while", "switch", "return", "void", "setup", "loop"}
        matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
        return {fn for fn in matches if fn not in keywords}

    @classmethod
    def evaluate(cls, solution_code: str, submission_code: Optional[str], pesos: dict) -> Dict[str, Any]:
        """Compara o código enviado com o gabarito, usando os pesos definidos no config."""
        
        # Pega os pesos do dicionário, ou usa 50 caso não encontre
        peso_estrutura = pesos.get("estrutura_basica", 50.0)
        peso_chamadas = pesos.get("chamadas_funcao", 50.0)

        if submission_code is None:
            return {
                "valid_code": False,
                "has_setup_loop": False,
                "call_match_score": 0.0,
                "final_score": 0.0,
                "status": "Arquivo Não Encontrado / Erro de Leitura"
            }

        structures = cls.check_essential_structures(submission_code)
        has_setup_loop = structures["has_setup"] and structures["has_loop"]

        sol_calls = cls.extract_function_calls(solution_code)
        sub_calls = cls.extract_function_calls(submission_code)

        if sol_calls:
            matched_calls = sol_calls.intersection(sub_calls)
            call_match_score = (len(matched_calls) / len(sol_calls)) * 100.0
        else:
            call_match_score = 100.0

        # Aplica a nota proporcional aos pesos do config.json
        nota_estrutura = peso_estrutura if has_setup_loop else 0.0
        nota_chamadas = call_match_score * (peso_chamadas / 100.0)
        final_score = nota_estrutura + nota_chamadas

        return {
            "valid_code": True,
            "has_setup_loop": has_setup_loop,
            "call_match_score": round(call_match_score, 2),
            "final_score": round(final_score, 2),
            "status": "OK" if has_setup_loop else "Falta setup() ou loop()"
        }