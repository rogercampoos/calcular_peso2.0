# Sistema de Cálculo de Descarte - COPAT

Sistema web para cálculo e gerenciamento de itens descartáveis da COPAT, permitindo o cálculo preciso de materiais a serem descartados e gerando relatórios detalhados.

## 🌐 Acesso ao Sistema

O sistema está disponível online em:
[https://rogercampoos.pythonanywhere.com/](https://rogercampoos.pythonanywhere.com/)

## 📋 Sobre o Projeto

O Sistema de Cálculo de Descarte é uma aplicação web desenvolvida para auxiliar no processo de gestão de descarte de móveis e equipamentos. O sistema:

- Calcula automaticamente o peso dos materiais (metal, madeira e plástico)
- Permite múltiplos itens por cálculo
- Gera relatórios em Excel para download
- Interface amigável e responsiva
- Validação em tempo real dos dados inseridos

## 🚀 Tecnologias Utilizadas

- Frontend:
  - HTML5
  - CSS3 (Design responsivo)
  - JavaScript (Vanilla JS)
  - Fetch API para requisições

- Backend:
  - Python
  - Flask
  - Pandas (processamento de dados)
  - OpenPyXL (geração de planilhas Excel)

- Hospedagem:
  - PythonAnywhere (servidor de produção)

## 💻 Funcionalidades

- ✅ Seleção dinâmica de móveis
- ✅ Cálculo automático de peso por material
- ✅ Adição/remoção dinâmica de itens
- ✅ Geração de relatórios em Excel
- ✅ Validação de dados em tempo real
- ✅ Interface responsiva e intuitiva

## 🔧 Desenvolvimento Local

Se você deseja executar o sistema localmente para desenvolvimento, siga estas instruções:

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-descarte-copat.git
```

2. Instale as dependências Python:
```bash
pip install flask pandas openpyxl odfpy
```

3. Certifique-se que o arquivo `dados.ods` está na raiz do projeto

4. Execute o servidor de desenvolvimento:
```bash
python server.py
```

5. Acesse a aplicação em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
sistema-descarte-copat/
├── server.py           # Servidor Flask e lógica de backend
├── index.html         # Interface do usuário
├── dados.ods          # Planilha com dados dos móveis
└── README.md          # Documentação
```

## 📊 Formato do Arquivo de Dados

O arquivo `dados.ods` deve seguir a seguinte estrutura:

| Móvel | Metal (kg) | Madeira (kg) | Plástico (kg) |
|-------|------------|--------------|---------------|
| Item 1|    10.5    |     15.0     |     2.0      |
| Item 2|    8.0     |     12.0     |     1.5      |

## 🔍 Requisitos do Sistema

Para desenvolvimento local:
- Python 3.6 ou superior
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexão com internet para carregar fontes
- Mínimo de 512MB de RAM

Para uso em produção:
- Apenas um navegador web moderno com acesso à internet

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## ⚠️ Notas Importantes

- Mantenha o arquivo `dados.ods` atualizado com os dados corretos dos móveis
- Não modifique a estrutura da planilha de dados
- Faça backup regular dos dados
- Para desenvolvimento local, o sistema requer permissões de leitura/escrita na pasta do projeto

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

Para suporte e dúvidas:
- Acesse a aplicação em produção: [https://rogercampoos.pythonanywhere.com/](https://rogercampoos.pythonanywhere.com/)
- Abra uma issue no GitHub
- Contate a equipe de TI da COPAT
