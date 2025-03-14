from flask import Flask, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Carrega a planilha ODS
try:
    dados = pd.read_excel('dados.ods', engine='odf')
    
    # Substitui hífens por 0 e converte para números
    colunas_materiais = ['Metal (kg)', 'Madeira (kg)', 'Plástico (kg)']
    dados[colunas_materiais] = dados[colunas_materiais].replace('-', 0).astype(float)
    
except Exception as e:
    print(f"ERRO AO LER PLANILHA: {str(e)}")
    dados = pd.DataFrame()

# Rota principal: exibe o frontend (index.html)
@app.route('/')
def index():
    return send_file('index.html')

# Rota para calcular os totais
@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        itens = request.json['itens']
        total = {'metal': 0, 'madeira': 0, 'plastico': 0}
        
        if dados.empty:
            return jsonify({"error": "Planilha de dados não carregada!"}), 500
        
        for item in itens:
            movel_filtrado = dados[dados['Móvel'] == item['movel']]
            if movel_filtrado.empty:
                return jsonify({"error": f"Móvel '{item['movel']}' não existe!"}), 400
            
            movel = movel_filtrado.iloc[0]
            total['metal'] += movel['Metal (kg)'] * item['quantidade']
            total['madeira'] += movel['Madeira (kg)'] * item['quantidade']
            total['plastico'] += movel['Plástico (kg)'] * item['quantidade']
        
        # Salva o resultado em um arquivo temporário
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

# Rota para baixar a planilha
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