Título: Star Wars Advanced API Gateway

Tecnologias: Google Cloud Functions, API Gateway, Python, HATEOAS.

Funcionalidades: * Autenticação via API Key.

Interface de navegação dinâmica (HATEOAS).

Métricas de performance no JSON.

Arquitetura: 

graph LR
    subgraph Client_Side [Lado do Cliente]
        A[Navegador / App]
    end

    subgraph GCP [Google Cloud Platform]
        B[API Gateway]
        C[Cloud Function Gen2]
    end

    subgraph External [Provedor de Dados]
        D[SWAPI.dev]
    end

    A -- "1. Request + API Key" --> B
    B -- "2. Validação & Segurança" --> C
    C -- "3. Requisição HTTP" --> D
    D -- "4. JSON Bruto" --> C
    C -- "5. Lógica de Negócio & HATEOAS" --> B
    B -- "6. Resposta Final (v9)" --> A

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#eee,stroke:#333,stroke-style:dashed