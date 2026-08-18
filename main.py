import os
import json
from core.loader import CodeLoader
from core.evaluator import CodeEvaluator
from core.reporter import ExcelReporter

def load_config(config_path="config.json"):
    """Lê o arquivo de configuração JSON."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {config_path} não encontrado!")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {config_path} não é um JSON válido!")
        return None

def run():
    # 1. Carrega as configurações
    config = load_config()
    if not config:
        return

    sol_dir = config["diretorios"]["solucoes"]
    sub_dir = config["diretorios"]["entregas"]
    output_file = config["diretorios"]["relatorio_saida"]
    
    # Verifica se as pastas existem
    if not os.path.exists(sol_dir) or not os.path.exists(sub_dir):
        print(f"Verifique se as pastas '{sol_dir}' e '{sub_dir}' existem.")
        return

    # 2. Carrega o gabarito
    sol_path = os.path.join(sol_dir, "E1T1_solution.ino")
    solution_code = CodeLoader.load_ino_file(sol_path)
    
    if not solution_code:
        print(f"Gabarito '{sol_path}' não encontrado! Crie este arquivo para testar.")
        return

    # 3. Encontra entregas dos alunos
    submissions = CodeLoader.scan_submissions(sub_dir)
    results = []

    # 4. Avalia cada aluno via IA utilizando as configurações do config.json
    for sub in submissions:
        submission_code = CodeLoader.load_ino_file(sub["filepath"])
        
        # Repassa 'config' completo para o Evaluator acessar os parâmetros da IA
        eval_result = CodeEvaluator.evaluate(solution_code, submission_code, config)

        # Monta a estrutura esperada pelo novo ExcelReporter
        entry = {
            "aluno_id": sub["student_id"],
            "exercicio": sub["assignment_id"],
            "has_essential": eval_result.get("has_essential", False),
            "final_score": eval_result.get("final_score", 0.0),
            "feedback": eval_result.get("feedback", "Sem observações.")
        }
        results.append(entry)

    # 5. Gera o relatório em Excel
    ExcelReporter.generate_report(results, output_file)

if __name__ == "__main__":
    run()