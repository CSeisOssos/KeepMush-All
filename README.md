link para os arquivos pesados demais para colocar no github:

https://drive.google.com/drive/folders/1ZxPsswSgVYVr4KDplHpVL1oYeZGdU4HM?usp=drive_link
apenas baixe o .zip e descompacte-o no diretório raiz do projeto (recomenda-se criar uma pasta dentro do diretório C:\ chamada "SeekMush" e descompactar tudo lá)
mova o arquivo "best_model.keras" para o caminho "\SeekMush\Tensorflow\Treinamento\Versões\V2.1 (Optimized Pipeline)"

requirements:
1 - PostgreSQL
2 - Python
2.1 - Bibliotecas necessárias para a execução (SQLalchemy, Tensorflow, FastAPI, Traceback, PIL, Numpy, Pandas, Pydantic, Csv, Shutil, e Requests)
2.2 - instale-as via linha de comando "pip install sqlalchemy tensorflow fastapi traceback pil numpy pandas pydantic csv shutil requests" (para isso terá de instalar Python e o PostgreSQL antes)

instruções:
1 - baixe o repositório todo
2 - crie um database no PostgreSQL chamado de SeekMushBD
3 - crie um usuário no PostgreSQL chamado "rocha" com a senha "rocha123" e garanta todas as permissões dentro do Banco "SeekMush"
4 - execute o arquivo "create_tabels.py" localizado dentro da pasta "db" no diretório raiz
5 - verifique se as tabelas "imagens_dos_usuarios" e "usuarios" foram criadas
6 - execute o arquivo "populate.py" localizado dentro da pasta "db" no diretório raiz
7 - verifique se a tabela "mushrroms" foi adicionada, tente verificar se ela está populada com o dataset presente nos arquivos baixados
8 - no terminal do seu editor de código (presumivelmente VS Code), acesse a pasta "Servidor" e digite o comando "uvicorn main:app --reload"
9 - para verificar se a conexão com a API deu certo, acesse o endereço "localhost:8000" no seu navegador, ele deve te enviar para a página de controle e visualização da Fast API
10 - também no navegador, abra os arquivos HTML "login" e "register", eles devem estar funcionando corretamente, logando o usuário no Sistema e registrando o usuário no Banco de Dados

para fazer:
1 - consertar/desenvolver todo os sistemas inerentes ao arquivo profile.html (por enquanto apenas o nome de usuário e email são mostrados de maneira dinâmica) e ao arquivo index.html
2 - testar o upload de imagens e resposta da IA
3 - implementar uma pesquisa por nome da espécie retornada pela IA para que as informações da espécie apareçam ao usuário (um resumo de uma página da Wikipedia já serve)
4 - adicionar um histórico de uploads dos usuários, contendo imagens, nome científico, e acurácia do modelo
5 - exportação desse mesmo histórico para um arquivo .pdf
6 - busca manual no banco de dados, o BD deve retornar nome comum, nome científico e foto, e utilizar as mesmas técnicas do processo da IA para retornar informações sobre as espécies
7 - adicionar uma versão em Inglês do Frontend (opcional, mas está na lista de Requisitos Não Funcionais)

ps: no Frontend que você me mandou, eu mudei o nome do arquivo "scripts.js" para "maria.js" pois não estava o utilizando, eu também dei uma modificada em alguns elementos do Front, nada visual, mas operacional
