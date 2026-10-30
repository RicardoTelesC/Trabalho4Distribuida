# Sistemas Distribuídos — Entrega (Git)

Repositório limpo para envio dos **Trabalhos 2, 3 e 4**.

**Equipe**

- Francisco Ricardo Teles — 2317443  
- Silvio Bruno Do Nascimento Lima — 2313199  

## Estrutura

```
entrega-git/
├── README.md
├── .gitignore
├── trabalhos-2-3/                 # WordPress + Nginx + Locust
│   ├── atv2-wordpress-nginx/      # código Docker, scripts, gráficos
│   ├── apresentacao-trabalhos-2-3.tex
│   └── apresentacao-trabalhos-2-3.pdf
└── trabalho-4/                    # Link Extractor + Locust
    ├── linkextractor-master/      # app (steps 0–6)
    ├── desempenho/                # testes Python/Ruby × cache
    ├── apresentacao-trabalho4.tex
    └── apresentacao-trabalho4.pdf
```

## Trabalhos 2 e 3

Pasta: `trabalhos-2-3/atv2-wordpress-nginx/`

- Guia do código: `GUIA-CODIGO.md`
- Trabalho 2: `README.md`
- Trabalho 3: `README-TRABALHO3.md`
- Slides: `apresentacao-trabalhos-2-3.pdf`

```powershell
cd trabalhos-2-3\atv2-wordpress-nginx
docker compose --profile wp2 --profile wp3 up -d
.\scripts\run_locust_headless.ps1 -Cenario cenario1 -Usuarios 75 -Instancias 3
```

## Trabalho 4

Pasta: `trabalho-4/desempenho/`

- Guia: `README.md`
- Slides: `apresentacao-trabalho4.pdf`

```powershell
cd trabalho-4\desempenho
.\scripts\set_cenario.ps1 -Cenario python-com-cache
.\scripts\run_locust_headless.ps1 -Cenario python-com-cache -Usuarios 15
```

## Compilar slides (opcional)

```powershell
cd trabalhos-2-3
pdflatex apresentacao-trabalhos-2-3.tex

cd ..\trabalho-4
pdflatex apresentacao-trabalho4.tex
```

## Enviar ao Git

```powershell
cd entrega-git
git init
git add .
git commit -m "Entrega Trabalhos 2, 3 e 4 - Sistemas Distribuidos"
git branch -M main
git remote add origin <URL_DO_SEU_REPOSITORIO>
git push -u origin main
```
