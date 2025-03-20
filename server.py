from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO
import os

app = Flask(__name__)

# Caminho absoluto para arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'dados.ods')
RESULT_PATH = os.path.join(BASE_DIR, 'resultado_temp.xlsx')

try:
    dados = pd.read_excel(DATA_PATH, engine='odf')
    colunas_necessarias = ['Móvel', 'Metal (kg)', 'Madeira (kg)', 'Plástico (kg)']
    
    if not all(col in dados.columns for col in colunas_necessarias):
        raise ValueError("Colunas ausentes na planilha!")
    
    dados[colunas_necessarias[1:]] = dados[colunas_necessarias[1:]].replace('-', 0).astype(float)

except Exception as e:
    print(f"ERRO AO LER PLANILHA: {str(e)}")
    dados = pd.DataFrame()

@app.route('/')
def index():
    return send_file(os.path.join(BASE_DIR, 'index.html'))

@app.route('/api/moveis')
def listar_moveis():
    if dados.empty:
        return jsonify({"error": "Planilha não carregada!"}), 500
    return jsonify(dados['Móvel'].tolist())

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        itens = request.json['itens']
        total_geral = {'metal': 0.0, 'madeira': 0.0, 'plastico': 0.0}
        detalhes = []

        if dados.empty:
            return jsonify({"error": "Planilha não carregada!"}), 500

        for item in itens:
            movel_nome = item['movel']
            quantidade = item['quantidade']
            
            movel_data = dados[dados['Móvel'] == movel_nome].iloc[0]
            
            metal = round(movel_data['Metal (kg)'] * quantidade, 2)
            madeira = round(movel_data['Madeira (kg)'] * quantidade, 2)
            plastico = round(movel_data['Plástico (kg)'] * quantidade, 2)
            
            total_geral['metal'] += metal
            total_geral['madeira'] += madeira
            total_geral['plastico'] += plastico
            
            detalhes.append({
                'Móvel': movel_nome,
                'Quantidade': quantidade,
                'Metal (kg)': metal,
                'Madeira (kg)': madeira,
                'Plástico (kg)': plastico
            })

        df_detalhes = pd.DataFrame(detalhes)
        df_total = pd.DataFrame([total_geral])

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_detalhes.to_excel(writer, sheet_name='Detalhado', index=False)
            df_total.to_excel(writer, sheet_name='Resumo', index=False)
        
        output.seek(0)
        
        # Salva o arquivo temporário
        with open(RESULT_PATH, 'wb') as f:
            f.write(output.getvalue())

        return jsonify({
            "metal": total_geral['metal'],
            "madeira": total_geral['madeira'],
            "plastico": total_geral['plastico'],
            "planilha": "/download"
        })

    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/download')
def download():
    try:
        return send_file(
            RESULT_PATH,
            as_attachment=True,
            download_name='relatorio_descarte.xlsx'
        )
    except Exception as e:
        return jsonify({"error": "Arquivo não encontrado!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
