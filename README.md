# 🍄 **SeekMush - Sistema de Identificação de Cogumelos com IA**

---

## 📦 **Arquivos Necessários**

🔗 **Link para os arquivos pesados demais para colocar no GitHub:**

[https://drive.google.com/drive/folders/1ZxPsswSgVYVr4KDplHpVL1oYeZGdU4HM?usp=drive_link](https://drive.google.com/drive/folders/1ZxPsswSgVYVr4KDplHpVL1oYeZGdU4HM?usp=drive_link)

📁 **Apenas baixe o `.zip` e descompacte-o no diretório raiz do projeto**  
*(Recomenda-se criar uma pasta dentro do diretório `C:\` chamada "SeekMush" e descompactar tudo lá)*

📂 **Mova o arquivo `best_model.keras` para o caminho:**  
`C:\SeekMush\Tensorflow\Treinamento\Versões\V2.1 (Optimized Pipeline)`

---

## ⚙️ **Requirements**

### 📌 **1 - PostgreSQL**  
### 🐍 **2 - Python**

#### 📚 **2.1 - Bibliotecas necessárias para a execução**
- `SQLalchemy`
- `Tensorflow`
- `FastAPI`
- `Traceback`
- `PIL`
- `Numpy`
- `Pandas`
- `Pydantic`
- `Csv`
- `Shutil`
- `Requests`

#### 💻 **2.2 - Instale-as via linha de comando:**
```bash
pip install sqlalchemy tensorflow fastapi traceback pil numpy pandas pydantic csv shutil requests
```
> ⚠️ **Para isso, será necessário instalar o Python e o PostgreSQL antes.**

---

## 🧪 **Instruções**

1️⃣ - Baixe o repositório todo  
2️⃣ - Crie um database no **PostgreSQL** chamado **SeekMushBD**  
3️⃣ - Crie um usuário no **PostgreSQL** chamado **"rocha"** com a senha **"rocha123"** e garanta todas as permissões dentro do banco **"SeekMush"**  
4️⃣ - Execute o arquivo **"create_tabels.py"** localizado dentro da pasta **"db"** no diretório raiz  
5️⃣ - Verifique se as tabelas **"imagens_dos_usuarios"** e **"usuarios"** foram criadas  
6️⃣ - Execute o arquivo **"populate.py"** localizado dentro da pasta **"db"** no diretório raiz  
7️⃣ - Verifique se a tabela **"mushrroms"** foi adicionada e se está populada com o dataset presente nos arquivos baixados  
8️⃣ - No terminal do seu editor de código (presumivelmente **VS Code**), acesse a pasta **"Servidor"** e digite o comando:  
```bash
uvicorn main:app --reload
```
9️⃣ - Para verificar se a conexão com a API deu certo, acesse o endereço:  
```
localhost:8000
```
> 🧭 Ele deve te enviar para a página de controle e visualização da **FastAPI**

🔟 - Também no navegador, abra os arquivos HTML **"login"** e **"register"**  
> ✅ Eles devem estar funcionando corretamente, logando o usuário no sistema e registrando no banco de dados

---

## 🛠️ **Para Fazer**

1️⃣ - Consertar/desenvolver todos os sistemas inerentes ao arquivo **profile.html**  
> *(Por enquanto apenas o nome de usuário e email são mostrados de maneira dinâmica)*

2️⃣ - Testar o upload de imagens e resposta da IA  

3️⃣ - Implementar uma pesquisa por nome da espécie retornada pela IA para que as informações da espécie apareçam ao usuário  
> *(Um resumo de uma página da Wikipedia já serve)*

4️⃣ - Adicionar um histórico de uploads dos usuários, contendo imagens, nome científico e acurácia do modelo  

5️⃣ - Exportação desse mesmo histórico para um arquivo `.pdf`  

6️⃣ - Busca manual no banco de dados  
> *O BD deve retornar nome comum, nome científico e foto, e utilizar as mesmas técnicas do processo da IA para retornar informações sobre as espécies*

7️⃣ - Adicionar uma versão em **Inglês** do Frontend  
> *(Opcional, mas está na lista de Requisitos Não Funcionais)*

---

## 📝 **Observação**

🛠️ No **Frontend** que você me mandou, eu mudei o nome do arquivo **`scripts.js`** para **`maria.js`** pois não estava o utilizando.  
👨‍🔧 Eu também dei uma modificada em alguns elementos do **Front**, nada visual, mas **operacional**.
