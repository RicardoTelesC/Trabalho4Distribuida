# Trabalho 4 — Link Extractor (testes de desempenho)

- `linkextractor-master/` — aplicação (tutorial Play-with-Docker)
- `desempenho/` — Locust + Compose (Python/Ruby × com/sem cache)
- `apresentacao-trabalho4.pdf` — slides

Detalhes técnicos: [desempenho/README.md](desempenho/README.md)

## Como rodar

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) ligado
- PowerShell
- Python 3 (opcional, só para gerar gráficos): `pip install matplotlib`

### 1. Entrar na pasta de testes

```powershell
cd trabalho-4\desempenho
```

### 2. Subir um cenário

```powershell
.\scripts\set_cenario.ps1 -Cenario python-com-cache
```

Cenários válidos:

| Cenário | API | Cache |
|---------|-----|-------|
| `python-com-cache` | Python (porta 5000) | Redis |
| `python-sem-cache` | Python (porta 5000) | sem |
| `ruby-com-cache` | Ruby (porta 4567) | Redis |
| `ruby-sem-cache` | Ruby (porta 4567) | sem |

Aguarde ~40 s após o `up`. Endereços:

- Web: http://localhost/?url=http%3A%2F%2Fexample.com%2F
- API Python: http://localhost:5000/api/http://example.com/
- API Ruby: http://localhost:4567/api/http://example.com/
- Locust UI: http://localhost:8089

### 3. Rodar um teste de carga (headless)

```powershell
.\scripts\run_locust_headless.ps1 -Cenario python-com-cache -Usuarios 15
```

Cada usuário virtual faz **10 GETs** com URLs diferentes no serviço de extração.  
CSV em `desempenho/resultados/<cenario>/users_<N>/`.

### 4. Matriz completa (12 testes)

Usuários **5 / 15 / 40** × 4 cenários:

```powershell
.\scripts\run_matriz_testes.ps1
```

### 5. Gerar gráficos

Com resultados reais (após a matriz) ou com dados de apoio:

```powershell
python scripts\gerar_dados_simulados.py   # opcional
python scripts\gerar_graficos.py
```

PNG em `desempenho/graficos/`.

### 6. Parar os containers

```powershell
# exemplo para o cenário atual
docker compose -f compose\python-com-cache.yml -p t4_python-com-cache down
```

Ou rode de novo `set_cenario.ps1` com outro cenário (ele derruba os anteriores).

### Compilar os slides (opcional)

```powershell
cd trabalho-4
pdflatex apresentacao-trabalho4.tex
pdflatex apresentacao-trabalho4.tex
```
