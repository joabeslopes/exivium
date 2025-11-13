# exivium
O projeto Exivium consiste em um sistema modular de gerenciamento de cameras, expansível através de plugins. 

# Visão Geral

O uso de câmeras de monitoramento se tornou essencial para garantir a segurança em diversos tipos de ambientes — residenciais, comerciais e industriais.  
No entanto, muitos softwares disponíveis atualmente apresentam limitações quanto à flexibilidade, personalização e facilidade de expansão, dificultando a adaptação às necessidades específicas dos usuários.

Com esse cenário em mente, este projeto propõe o desenvolvimento de um sistema de monitoramento modular utilizando a linguagem Python.  
A proposta visa criar uma plataforma personalizável, escalável e de fácil integração, permitindo a incorporação de plugins específicos para o processamento das imagens captadas.

---

## Objetivos

- Desenvolver um sistema modular para monitoramento de vídeo em tempo real.  
- Permitir a integração com diferentes protocolos e dispositivos (RTSP, ONVIF, DVR, NVR).  
- Garantir compatibilidade com câmeras IP e analógicas.  
- Oferecer um ambiente de fácil expansão, onde novos módulos e funções possam ser adicionados dinamicamente.  
- Utilizar o codec H.264 para otimizar o desempenho e a qualidade da transmissão.

---

## Tecnologias e Protocolos

| Tecnologia | Descrição |
|-------------|------------|
| **Python** | Linguagem principal do projeto, escolhida pela sua flexibilidade e ampla gama de bibliotecas. |
| **RTSP (Real-Time Streaming Protocol)** | Protocolo usado para gerenciar transmissões de vídeo em tempo real. |
| **H.264** | Codec de compressão que garante alta qualidade de imagem com baixo uso de banda. |
| **ZeroMQ** | Broker de mensagens para a transmissão eficiente de imagens e logs. |

---

## Estrutura Modular

O sistema foi projetado para suportar módulos independentes, chamados de "Recursos", que podem ser adicionados conforme a necessidade, sendo cada recurso gerenciado por um processo python separado da API principal, se comunicando através da mensageria do ZeroMQ.

---

## Como rodar o sistema no Docker

É recomendado utilizar o Docker para rodar o sistema. Para isso, basta ir na raiz do projeto e rodar **docker compose up -d** que ele já vai construir a imagem do backend, e também rodar o banco de dados e o nginx para servir o frontend.

Na pasta **backend** você deve criar os arquivos **exivium.log** e **.env** e definir nesse arquivo .env algumas variáveis de ambiente que serão usadas pelos containers, como por exemplo:

>FPS=30
>
>FRAME_WIDTH=640
>
>FRAME_HEIGHT=480
>
>JPEG_QUALITY=70
>
>DATABASE_URL=postgresql+psycopg://usuario:senha@db:5432/banco
>
>POSTGRES_DB=banco
>
>POSTGRES_USER=usuario
>
>POSTGRES_PASSWORD=senha
>
>JWT_SECRET_KEY=chavesecretaaleatoria
>
>JWT_EXPIRE_MINUTES=60
>
>JWT_ALGORITHM=HS256
>
>EXIVIUM_ADMIN_EMAIL=admin
>
>EXIVIUM_ADMIN_PASSWORD=admin

---

## Como rodar o sistema localmente

Após instalar o git, python, postgres e clonar esse repositório, você vai abrir no terminal a pasta **backend** e instalar as dependências python descritas no arquivo **requirements.txt**, sendo recomendado para isso criar um ambiente virtual em uma pasta ".venv", que é o padrão do projeto e será ignorada pelo git.

Os comandos para isso variam por sistema operacional. No Windows:

> python -m venv .venv

> .\\.venv\Scripts\activate.ps1

> pip install -r requirements.txt

No linux:

> python3 -m venv .venv

> source ./.venv/bin/activate

> pip install -r requirements.txt

Com isso, todas as dependencias ficam isoladas nessa pasta .venv, que sempre deve ser ativada antes de rodar o projeto. Para isso existem os scripts **run.ps1** e **run.sh**, sendo o primeiro para Windows e o segundo para Linux.

O arquivo **.env** também deve ser criado na pasta **backend** da mesma maneira explicada acima.

Feito isso, basta rodar **python main.py**, e então você vai na pasta **frontend** e abre o arquivo **index.html** para visualizar o frontend.

---

## O que é um Recurso ?

Um recurso é um mini projeto python que vai ser rodado isoladamente, processando imagens de algum lugar e enviando resultados para o sistema principal, podendo esses resultados serem novas imagens, logs, ou até mesmo informações em uma tabela do banco de dados.

Ele pode estar em um repositório no github, ou pode ser criado diretamente na pasta **recursos/cameras** ou **recursos/plugins**, dependendo do propósito dele. O nome da pasta será o nome do recurso.

Um recurso só tem 3 pré-requisitos para funcionar:

- Ter um arquivo **requirements.txt** com as dependências do projeto

- Ter um arquivo **main.py** que será o ponto de partida inicial

- Herdar a classe **RecursoBase** para interagir com o sistema principal de forma padronizada

---

## Como rodar um recurso

Para criar um recurso, você pode passar a url do github para que ele seja clonado e instalado automaticamente, ou pode manualmente criar uma pasta com o nome do recurso e criar lá os arquivos de código, mantendo o padrão mencionado acima.
Se você tem uma webcam, o jeito mais fácil de testar o sistema é criar o recurso **opencvcam** que está nos exemplos, passando como alvo a string **"0"**, que significa a webcam principal.