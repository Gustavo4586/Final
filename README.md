# EduCollab - Plataforma de Aprendizado Colaborativo

## 📋 Descrição do Projeto

EduCollab é uma plataforma fullstack de aprendizado colaborativo desenvolvida para facilitar o compartilhamento de conhecimento entre estudantes e instrutores. A plataforma oferece um ambiente militar-inspirado com funcionalidades robustas para gerenciamento de cursos, anotações colaborativas, fóruns de discussão e acompanhamento de progresso.

A plataforma combina o melhor dos bancos de dados relacionais e não-relacionais, utilizando SQLite para dados estruturados principais e MongoDB para analytics e atividades em tempo real, proporcionando uma experiência rica e escalável para todos os usuários.


### Visão Geral da Arquitetura

A EduCollab utiliza uma arquitetura híbrida que combina o melhor dos bancos de dados relacionais e não-relacionais. Esta abordagem permite otimizar tanto a consistência dos dados críticos quanto a flexibilidade e performance para analytics e atividades em tempo real.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Databases     │
│   (React)       │◄──►│    (Flask)      │◄──►│                 │
│                 │    │                 │    │  ┌─────────────┐│
│ • Components    │    │ • REST API      │    │  │   SQLite    ││
│ • Routing       │    │ • Authentication│    │  │ (Principal) ││
│ • State Mgmt    │    │ • Business Logic│    │  └─────────────┘│
│ • UI/UX         │    │ • Data Access   │    │  ┌─────────────┐│
└─────────────────┘    └─────────────────┘    │  │  MongoDB    ││
                                              │  │ (Analytics) ││
                                              │  └─────────────┘│
                                              └─────────────────┘
```

### Estrutura de Diretórios Detalhada

```
plataforma_aprendizado_colaborativo/
├── frontend/
│   └── plataforma-frontend/
│       ├── src/
│       │   ├── components/          # Componentes React reutilizáveis
│       │   │   └── ui/             # Componentes de interface (Shadcn/ui)
│       │   ├── hooks/              # React Hooks customizados
│       │   ├── lib/                # Utilitários e configurações
│       │   ├── assets/             # Recursos estáticos
│       │   ├── App.jsx             # Componente principal
│       │   └── main.jsx            # Ponto de entrada da aplicação
│       ├── public/                 # Arquivos públicos
│       ├── index.html              # Template HTML
│       ├── package.json            # Dependências e scripts
│       ├── vite.config.js          # Configuração do Vite
│       ├── vercel.json             # Configuração para deploy no Vercel
│       └── .env.example            # Exemplo de variáveis de ambiente
├── backend/
│   └── educollab-api/
│       ├── src/
│       │   ├── models/             # Modelos de dados
│       │   │   ├── user.py         # Modelos SQLAlchemy (SQL)
│       │   │   └── mongo_models.py # Modelos MongoDB (NoSQL)
│       │   ├── routes/             # Rotas da API
│       │   │   ├── user.py         # Rotas principais (CRUD)
│       │   │   └── analytics.py    # Rotas de analytics (MongoDB)
│       │   ├── database/           # Banco de dados SQLite
│       │   │   └── app.db          # Arquivo do banco SQLite
│       │   ├── static/             # Arquivos estáticos do backend
│       │   └── main.py             # Aplicação Flask principal
│       ├── venv/                   # Ambiente virtual Python
│       ├── requirements.txt        # Dependências Python
│       ├── Procfile               # Configuração para deploy
│       ├── gunicorn.conf.py       # Configuração do Gunicorn
│       ├── runtime.txt            # Versão do Python
│       └── .env.example           # Exemplo de variáveis de ambiente
├── docs/                          # Documentação técnica
│   ├── api-documentation.yaml     # Documentação da API (OpenAPI)
│   ├── er-diagram.mmd            # Diagrama ER (Mermaid)
│   ├── class-diagram.mmd         # Diagrama de classes
│   └── use-case-diagram.mmd      # Diagrama de casos de uso
├── README.md                      # Documentação principal
└── INSTALL.md                     # Guia de instalação
```

