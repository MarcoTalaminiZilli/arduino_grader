import os
import re
from typing import List, Dict, Optional

class CodeLoader:
    @staticmethod
    def remove_comments(code: str) -> str:
        """Remove comentários de linha (//) e bloco (/* */) do código C/Arduino."""
        # Remove comentários de bloco /* ... */
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Remove comentários de linha // ...
        code = re.sub(r'//.*', '', code)
        return code

    @classmethod
    def load_ino_file(cls, filepath: str) -> Optional[str]:
        """Lê um arquivo .ino, remove comentários e retorna o código limpo."""
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return cls.remove_comments(content)
        except Exception as e:
            print(f"Erro ao ler arquivo {filepath}: {e}")
            return None

    @classmethod
    def scan_submissions(cls, submissions_folder: str) -> List[Dict[str, str]]:
        """
        Varre a pasta de entregas procurando arquivos .ino.
        Espera nomes no formato: 'IDALUNO_EXERCICIO.ino' ou similar.
        """
        submissions = []
        if not os.path.exists(submissions_folder):
            return submissions

        for filename in os.listdir(submissions_folder):
            if filename.endswith(".ino"):
                filepath = os.path.join(submissions_folder, filename)
                
                # Exemplo de extração por nome de arquivo: "joao123_E1T1.ino"
                parts = filename.replace(".ino", "").split("_")
                student_id = parts[0] if len(parts) > 0 else "desconhecido"
                assignment_id = parts[1] if len(parts) > 1 else "desconhecido"

                submissions.append({
                    "student_id": student_id,
                    "assignment_id": assignment_id,
                    "filename": filename,
                    "filepath": filepath
                })
        return submissions