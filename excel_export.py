import xlsxwriter
import pandas as pd
import math
import os

def get_final_excel(original_df, state_name):
    df = pd.DataFrame({
        'Proposal title': original_df['Label'],
        'State': state_name,
        'Solicitation #': original_df['Code'],
        'RFx Type': '???',
        'Due Date': original_df['End (UTC-7)'],
        'Decision Date': '???',
        'Keyword Hits': original_df['Keyword Hits']
    })
    return df

def export(df, state_name):
    df = get_final_excel(df, state_name)
    with pd.ExcelWriter("./output/rfq_scraping_output.xlsx", engine='xlsxwriter') as writer:
        sheet_name = f"{state_name} RFP Sheet"
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        format_header = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'vcenter',
            'align': 'center',
            'fg_color': '#83cceb',
            'font_color': 'black',
            'border': 5,
            'font_size': 14,
            'font_name': 'Aptos Narrow Bold'
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, format_header)
        worksheet.set_row(0, 66)
        worksheet.set_column('A:A', 41)
        worksheet.set_column('B:B', 14.5)
        worksheet.set_column('C:C', 30.5)
        worksheet.set_column('E:E', 24)
        worksheet.set_column('F:F', 20)
        wrap_format_A = workbook.add_format({
            'font_name': 'Aptos Narrow',
            'font_size': 11,
            'font_color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#dae9f8',
            'underline': True,
            'text_wrap': True,
            'border': 5
        })
        default_format = workbook.add_format({
            'font_name': 'Aptos Narrow',
            'font_size': 11,
            'font_color': 'black',
            'align': 'center',
            'valign': 'vcenter',
            'border': 2
        })
        italic_format = workbook.add_format({
            'font_name': 'Aptos Narrow',
            'font_size': 11,
            'font_color': 'black',
            'italic': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 2
        })
        for i, row in enumerate(df.itertuples(index=False), start=1):
            for j, value in enumerate(row):
                if j == 0:
                    worksheet.write(i, j, value, wrap_format_A)
                else:
                    if j in [2, 4, 5]:
                        worksheet.write(i, j, value, italic_format)
                    else:
                        worksheet.write(i, j, value, default_format)
            title = row[0]
            lines = math.ceil(len(str(title)) / 41)
            height = max(lines * 15, 40)
            worksheet.set_row(i, height)
    os.startfile("C:/Users/jason/vscode/rfp-scraper-demo/output/rfq_scraping_output.xlsx")
