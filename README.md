# Conversor de Áudio — Freq • Onda • Delay

Aplicação web em Flask para conversão entre frequência e comprimento de onda, cálculo da velocidade do som em função da temperatura e estimativa de atrasos (delay) por distância.

## Funcionalidades

- Conversão entre **frequência (Hz)** e **comprimento de onda (λ)**
- Velocidade do som baseada na **temperatura do ar** (°C): `v ≈ 331,3 + 0,606·T`
- **Atraso por metro** e **atraso total** para uma distância
- **Calculadora rápida** de delay com atualização instantânea
- **Frações de λ** (λ/4, λ/2, λ) úteis para posicionamento e alinhamento
- **Tabela rápida** de delays para 1–30 m
- **Links compartilháveis** via parâmetros de URL (GET)
- **Validação apenas ao enviar** (evita erro na tela inicial)
- **Persistência local** (últimos valores via `localStorage`)
- Acessibilidade básica (`aria-live`) e **clique para copiar** valores dos cards

## Estrutura do projeto

```
.
├── app.py
├── index.py
├── requirements.txt
├── vercel.json
├── functions
│   ├── __init__.py
│   ├── physics.py
│   ├── formatters.py
│   └── parsers.py
├── templates
│   └── index.html
└── static
    ├── css
    │   └── styles.css
    └── js
        └── app.js
```

## Requisitos

- Python 3.10+
- Pip

## Instalação

```bash
pip install -r requirements.txt
```

## Executar localmente

```bash
python app.py
```
Acesse `http://localhost:8000`.

## Deploy (Vercel)

O projeto está preparado para deploy na Vercel usando `@vercel/python`. Arquivo `vercel.json` já incluso.

## Como usar

1. Escolha o **tipo de entrada** (Frequência ou Compr. de onda)
2. Informe o **valor** (aceita vírgula decimal)
3. Defina a **temperatura do ar** (°C)
4. Opcional: informe uma **distância** para calcular o delay
5. Clique em **Calcular**

## Formatos aceitos

- Frequência: `500`, `1k`, `1khz`, `1200`
- Comprimento de onda: `3,4`, `34cm`, `120mm`, `2m`
- Distância: `10`, `250cm`, `120mm`
- Decimais: aceita vírgula ou ponto

## Parâmetros via URL (links compartilháveis)

Você pode abrir a página já com os resultados preenchidos:

```
/?input_type=frequency&frequency=1000&temperature=20&distance=10
```

Ou a partir do comprimento de onda:

```
/?input_type=wavelength&wavelength=0,34&temperature=20
```

## Arquitetura

- `functions/physics.py`: funções de cálculo físico (velocidade do som)
- `functions/formatters.py`: formatação humanizada (unidades e casas decimais)
- `functions/parsers.py`: parsers tolerantes a vírgula decimal, k/khz, cm/mm
- `templates/index.html`: template Jinja2
- `static/css/styles.css`: estilos
- `static/js/app.js`: comportamento do front-end

## Testes manuais rápidos

- Tela inicial não exibe erro até clicar em **Calcular**
- Alternar entre **Frequência** e **Compr. de onda** habilita/desabilita inputs
- Testar formatos: `1k`, `500`, `3,4`, `34cm`, `120mm`
- Usar chips de distância e conferir cálculo do delay
- Conferir **Frações de λ** e **Tabela 1–30 m**
- Recarregar a página e confirmar persistência via `localStorage`

## Próximos passos sugeridos

- Modo precisão opcional: `v = 331.3 * sqrt(1 + T/273.15)`
- Exportar CSV da tabela de delays
- PWA simples (manifest + service worker) para uso offline
