# Star Wars Advanced API Gateway (v9.0)

Este projeto implementa um orquestrador de dados para a API do Star Wars (SWAPI) utilizando uma arquitetura Serverless no Google Cloud Platform (GCP). A solução vai além do simples repasse de dados, oferecendo uma interface inteligente, métricas de performance e segurança avançada.

# Desenho de Arquitetura Técnica
A arquitetura foi desenhada para ser escalável, segura e de baixa latência.

Snippet de código
<pre>
graph LR
    subgraph Client_Side [Lado do Cliente]
        A[Navegador / Postman / App]
    end

    subgraph GCP [Google Cloud Platform]
        B[API Gateway]
        C[Cloud Function Gen2]
    end

    subgraph External [Provedor de Dados]
        D[SWAPI.dev]
    end

    A -- "1. Request + API Key" --> B
    B -- "2. Validação de Segurança" --> C
    C -- "3. Requisição HTTP" --> D
    D -- "4. JSON Bruto" --> C
    C -- "5. Lógica de Negócio & HATEOAS" --> B
    B -- "6. Resposta Final Enriquecida" --> A

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#eee,stroke:#333,stroke-dasharray: 5 5
</pre>

# Componentes Principais:
Google API Gateway: Atua como o único ponto de entrada, gerenciando autenticação e ocultando a infraestrutura backend.

Cloud Function Gen2 (Python 3.10): Motor de processamento que aplica regras de negócio e transforma dados brutos em informação estruturada.

SWAPI: Fonte de dados externa integrada via requisições assíncronas/HTTP.

# Regras de Negócio Aplicadas
Diferente de APIs convencionais, este projeto implementa camadas lógicas que agregam valor ao usuário final:

**Padronização HATEOAS:** O JSON retornado contém uma seção ui_navigation que dita as próximas ações possíveis, permitindo que a API seja auto-descritiva.

**Versionamento por Contrato:** Cada resposta inclui api_version para garantir compatibilidade com frontends legados.

**Monitoramento de SLA:** O campo metadata.execution_time rastreia a latência do backend, permitindo auditoria de performance.

**Abstração de Erros:** IDs inexistentes ou falhas na fonte externa são tratados para retornar mensagens amigáveis em vez de erros de sistema (HTTP 500).

# Segurança e Autenticação
A segurança é implementada de forma multicamada:

**Autenticação:** Exigência de API Key via Query Parameter.

**Autorização:** Configurada no nível do API Gateway via especificação OpenAPI 2.0 (Swagger).

**Isolamento:** A Cloud Function está configurada para aceitar tráfego apenas através do Gateway, evitando exposição direta.

# Testes Unitários

Para garantir a confiabilidade, o projeto conta com testes unitários que validam:

A correta estruturação do JSON.

A presença obrigatória dos campos de navegação.

O comportamento da API sob falta de parâmetros.

Como rodar os testes:

Bash<pre>**pip install pytest**</pre><pre>**python -m pytest tests/test_main.py**</pre>

<pre>

Exemplo de Resposta (v9.0)
JSON
{
  &quot;api_version&quot;: &quot;v9.0-advanced&quot;,
  &quot;metadata&quot;: {
    &quot;execution_time&quot;: &quot;0.799s&quot;,
    &quot;total_results&quot;: 82
  },
  &quot;payload&quot;: {
    &quot;name&quot;: &quot;Luke Skywalker&quot;,
    &quot;height&quot;: &quot;172&quot;,
    &quot;mass&quot;: &quot;77&quot;
  },
  &quot;ui_navigation&quot;: {
    &quot;available_actions&quot;: [
      { 
        &quot;rel&quot;: &quot;list_all&quot;, 
        &quot;method&quot;: &quot;GET&quot;, 
        &quot;href&quot;: &quot;https://.../consultar?key=...&quot; 
      }
    ],
    &quot;quick_explore&quot;: [
      &quot;https://.../consultar?key=...&amp;categoria=planets&quot;
    ]
  }
}
</pre>

# Como Replicar este Projeto

Deploy da Cloud Function: <pre>**gcloud functions deploy swapi-handler --gen2 --runtime=python310 --trigger-http**</pre>
____________________________________________________________________
Atualizar a Cloud Function: <pre>**gcloud functions deploy swapi-handler --gen2 --runtime=python310 --region=us-central1 --source=**</pre>
____________________________________________________________________
Configuração do Gateway: <pre>**gcloud api-gateway api-configs create config-v9 --openapi-spec=config/openapi2-functions.yaml**</pre>
____________________________________________________________________
Update do Gateway: <pre>**gcloud api-gateway gateways update swapi-gateway --api-config=config-v9**</pre>
____________________________________________________________________
Atualizar o API Gateway (Nova Versão): <pre>**gcloud api-gateway api-configs create swapi-config-v9 --api=swapi-api --openapi-spec=config/openapi2-functions.yaml --project=star-wars-api-gateway-lab**</pre><pre>**gcloud api-gateway gateways update swapi-gateway --api=swapi-api --api-config=swapi-config-v9 --location=us-central1**</pre>
____________________________________________________________________

Desenvolvido por Daniel Silva. Tecnologias: Google Cloud, Python, REST, HATEOAS.