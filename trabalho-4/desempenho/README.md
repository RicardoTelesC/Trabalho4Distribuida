# Trabalho 4 — Testes de desempenho: Link Extractor

Testes de carga com **Locust** sobre as versões **Python** (step5) e **Ruby** (step6) do [Link Extractor](../linkextractor-master), **com e sem cache Redis**.

Guia teórico do app: tutorial [Application Containerization and Microservice Orchestration](https://training.play-with-docker.com/microservice-orchestration/) (cópia local em `../Application Containerization and Microservice Orchestration.html`).

## Requisitos do enunciado

| Requisito | Como foi atendido |
|-----------|-------------------|
| Ferramenta configurável via script | Locust (`locust/locustfile.py`) |
| 10 invocações com URLs diferentes por usuário | loop sobre lista de 10 URLs no `@task` |
| Variar nº de usuários virtuais | 5, 15 e 40 |
| Variar linguagem (Python / Ruby) | compose `python-*` e `ruby-*` |
| Variar cache (com / sem) | Redis ligado ou API sem Redis |
| Métricas armazenadas | CSV Locust + `resultados/manifest.json` + gráficos PNG |

## Arquitetura sob teste

```
Locust  →  API (/api/<url>)  →  [Redis?]  →  fetch HTML + parse links
              ↑
           Web PHP (opcional, porta 80)
```

- **Python + cache:** `linkextractor-master/step5`
- **Python sem cache:** API do `step4` (sem Redis)
- **Ruby + cache:** `linkextractor-master/step6`
- **Ruby sem cache:** `api-ruby-sem-cache/` (Sinatra sem Redis)

## Como executar

### 1. Subir um cenário

```powershell
cd Trabalho4\desempenho
.\scripts\set_cenario.ps1 -Cenario python-com-cache
```

Cenários válidos: `python-com-cache`, `python-sem-cache`, `ruby-com-cache`, `ruby-sem-cache`.

- Web: http://localhost/?url=http%3A%2F%2Fexample.com%2F  
- API Python: http://localhost:5000/api/http://example.com/  
- API Ruby: http://localhost:4567/api/http://example.com/  
- Locust UI: http://localhost:8089  

### 2. Um teste headless

```powershell
.\scripts\run_locust_headless.ps1 -Cenario python-com-cache -Usuarios 15
```

### 3. Matriz completa (12 execuções)

```powershell
.\scripts\run_matriz_testes.ps1
```

### 4. Gráficos (ou dados simulados para a apresentação)

```powershell
python scripts\gerar_dados_simulados.py
python scripts\gerar_graficos.py
```

## Script Locust (comportamento do usuário)

Cada usuário virtual, a cada tarefa:

1. Faz **10 GETs** em sequência  
2. Cada GET usa uma **URL alvo diferente**  
3. O path chamado é `/api/<url_alvo>` no serviço de extração  

Intervalo entre tarefas: `between(0.5, 1.5)` segundos.

## Apresentação

Slides LaTeX: [`../apresentacao-trabalho4.tex`](../apresentacao-trabalho4.tex)

```powershell
cd Trabalho4
pdflatex apresentacao-trabalho4.tex
pdflatex apresentacao-trabalho4.tex
```
