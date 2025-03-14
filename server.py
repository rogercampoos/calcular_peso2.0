from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Carrega a planilha ODS com tratamento de erros
try:
    dados = pd.read_excel('dados.ods', engine='odf')  # Engine 'odf' é obrigatório
    
    # Verifica colunas necessárias
    colunas_necessarias = ['Móvel', 'Metal (kg)', 'Madeira (kg)', 'Plástico (kg)']
    if not all(col in dados.columns for col in colunas_necessarias):
        raise ValueError("Colunas ausentes na planilha!")
    
    # Substitui '-' por 0 e converte para float
    dados[colunas_necessarias[1:]] = dados[colunas_necessarias[1:]].replace('-', 0).astype(float)
    
except Exception as e:
    print(f"ERRO AO LER PLANILHA: {str(e)}")
    dados = pd.DataFrame()

# Rota principal: exibe o frontend
@app.route('/')
def index():
    return send_file('index.html')

# Rota para listar móveis
@app.route('/api/moveis')
def listar_moveis():
    try:
        if dados.empty:
            return jsonify({"error": "Planilha não carregada!"}), 500
        
        moveis = dados['Móvel'].tolist()
        return jsonify(moveis)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para calcular os totais
@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        itens = request.json['itens']
        total = {'metal': 0, 'madeira': 0, 'plastico': 0}
        
        if dados.empty:
            return jsonify({"error": "Planilha não carregada!"}), 500
        
        for item in itens:
            movel_filtrado = dados[dados['Móvel'] == item['movel']]
            if movel_filtrado.empty:
                return jsonify({"error": f"Móvel '{item['movel']}' não encontrado!"}), 400
            
            movel = movel_filtrado.iloc[0]
            total['metal'] += movel['Metal (kg)'] * item['quantidade']
            total['madeira'] += movel['Madeira (kg)'] * item['quantidade']
            total['plastico'] += movel['Plástico (kg)'] * item['quantidade']
        
        # Salva resultado em arquivo temporário
        df_resultado = pd.DataFrame([total])
        df_resultado.to_excel('resultado_temp.xlsx', index=False)
        
        return jsonify({
            "metal": total['metal'],
            "madeira": total['madeira'],
            "plastico": total['plastico'],
            "planilha": "/download"
        })
    
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# Rota para download da planilha
@app.route('/download')
def download():
    try:
        return send_file(
            'resultado_temp.xlsx',
            as_attachment=True,
            download_name='resultado_descarte.xlsx'
        )
    except Exception as e:
        return jsonify({"error": "Arquivo não encontrado!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
