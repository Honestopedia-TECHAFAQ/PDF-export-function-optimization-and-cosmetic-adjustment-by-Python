import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate
import tempfile
import os

def format_dataframe_for_pdf(dataframe):
    dataframe = dataframe.astype(str)
    return dataframe

def create_pdf_from_dataframe(dataframe, pdf_file_path):
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = 1

    formatted_df = format_dataframe_for_pdf(dataframe)

    data = [list(formatted_df.columns)] + formatted_df.values.tolist()
    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    elements.append(Paragraph('Exported Results', styles['Title']))
    elements.append(table)

    doc.build(elements)

def main():
    st.title('Data to PDF Exporter')
    st.write('Please input your data below:')

    num_columns = st.number_input('Number of columns', min_value=1, max_value=10, value=3)
    column_names = []
    data = []

    for i in range(num_columns):
        column_name = st.text_input(f'Column {i+1} name', f'Column{i+1}')
        column_names.append(column_name)

    num_rows = st.number_input('Number of rows', min_value=1, max_value=100, value=4)
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            row.append(st.text_input(f'Row {i+1}, Column {j+1}', ''))
        data.append(row)

    if st.button('Generate PDF'):
        if any('' in row for row in data):
            st.error('All fields must be filled out.')
        else:
            df = pd.DataFrame(data, columns=column_names)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                output_pdf_path = tmp_file.name
                create_pdf_from_dataframe(df, output_pdf_path)
                tmp_file.close()
                with open(output_pdf_path, 'rb') as pdf_file:
                    st.download_button('Download PDF', data=pdf_file, file_name='output.pdf')
                os.remove(output_pdf_path)

if __name__ == "__main__":
    main()
