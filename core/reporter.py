import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

class Reporter:
    @staticmethod
    def export_to_excel(results: list[dict], output_filepath: str):
        """Recebe uma lista de resultados e gera um arquivo Excel formatado."""
        if not results:
            print("Nenhum resultado para exportar.")
            return

        df = pd.DataFrame(results)

        wb = Workbook()
        ws = wb.active
        ws.title = "Notas"

        # Escreve os cabeçalhos
        headers = list(df.columns)
        ws.append(headers)

        # Formatação do cabeçalho
        header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Escreve os dados
        for row in df.itertuples(index=False):
            ws.append(list(row))

        # Ajusta largura das colunas automaticamente
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = col[0].column_letter
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

        wb.save(output_filepath)
        print(f"Relatório gerado com sucesso: {output_filepath}")