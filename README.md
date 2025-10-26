# exivium
O projeto Exivium consiste em um sistema modular de gerenciamento de cameras, expansível através de plugins. 

# Sistema de Monitoramento Modular em Python

#  Visão Geral

O uso de câmeras de monitoramento se tornou essencial para garantir a segurança em diversos tipos de ambientes — residenciais, comerciais e industriais.  
No entanto, muitos softwares disponíveis atualmente apresentam limitações quanto à flexibilidade, personalização e facilidade de expansão**, dificultando a adaptação às necessidades específicas dos usuários.

Com esse cenário em mente, este projeto propõe o desenvolvimento de um sistema de monitoramento modular utilizando a linguagem Python.  
A proposta visa criar uma plataforma personalizável, escalável e de fácil integração, permitindo a incorporação de plugins específicos** para o processamento das imagens captadas.

---

##  Objetivos

- Desenvolver um sistema modular para monitoramento de vídeo em tempo real.  
- Permitir a integração com diferentes protocolos e dispositivos (RTSP, ONVIF, DVR, NVR).  
- Garantir compatibilidade com câmeras IP e analógicas.  
- Oferecer um ambiente de fácil expansão, onde novos módulos e funções possam ser adicionados dinamicamente.  
- Utilizar o codec H.264 para otimizar o desempenho e a qualidade da transmissão.

---

##  Tecnologias e Protocolos

| Tecnologia | Descrição |
|-------------|------------|
| **Python** | Linguagem principal do projeto, escolhida pela sua flexibilidade e ampla gama de bibliotecas. |
| **RTSP (Real-Time Streaming Protocol)** | Protocolo usado para gerenciar transmissões de vídeo em tempo real. |
| **H.264** | Codec de compressão que garante alta qualidade de imagem com baixo uso de banda. |


---

##  Estrutura Modular

O sistema será projetado para suportar módulos independentes, que podem ser adicionados conforme a necessidade:

