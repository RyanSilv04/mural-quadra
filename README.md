# Mural Online da Quadra

Site simples para divulgar avisos e eventos sobre o uso da quadra. (foco no MVP)
Stack: Python (Flask) + MySQL + HTML/CSS.

 Guia para testar na sua propria "maquina" (famoso LocalHost), "passo a passo" rs  

## 1. Pré-requisitos
- Python 3.9+ instalado
- MySQL Server instalado e rodando se não me quebra

## 2. Instalar as dependências Python
```bash
pip install flask mysql-connector-python
```

## 3. Criar o banco de dados
Abra o MySQL (terminal ou MySQL Workbench) e rode o arquivo `schema.sql`:
```bash
mysql -u root -p < schema.sql
```
Isso cria o banco `mural_quadra` e a tabela `posts`, já com 2 avisos de exemplo.

## 4. Configurar a senha do banco
Abra `app.py` e troque:
```python
"password": "SUA_SENHA_AQUI",
```
pela senha do seu usuário MySQL.

## 5. Rodar o site
```bash
python app.py
```
O terminal vai mostrar algo como:
```
 * Running on http://127.0.0.1:5000
```
Abra esse endereço no navegador do computador.

## 6. Acessar pelo celular (mesma rede Wi-Fi)
No `app.py`, troque a última linha por:
```python
app.run(debug=True, host='0.0.0.0')
```
Depois, descubra o IP do seu computador na rede (`ipconfig` no Windows ou `ifconfig`/`ip a` no Linux/Mac,
procure algo como 192.168.x.x) e acesse `http://SEU_IP:5000` pelo navegador do celular.

## Estrutura do projeto
```
mural_quadra/
├── app.py              # back-end Flask (rotas e lógica)
├── schema.sql           # criação do banco MySQL
├── templates/           # páginas HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   └── novo_post.html
└── static/
    └── style.css         # estilo visual, responsivo
```

## 7. Hospedando de graça (Render + db4free.net)

### Passo 1 — criar o banco no db4free.net
1. Acesse **https://www.db4free.net/signup.php** e crie uma conta
2. Confirme o e-mail de verificação
3. Anote: nome do banco, usuário e senha que você escolheu — o host de conexão é sempre `db4free.net`, porta `3306`

### Passo 2 — subir o código pro GitHub
1. Crie uma conta em **https://github.com** (se ainda não tiver)
2. Crie um repositório novo e suba a pasta `mural_quadra` (pelo VS Code mesmo, usando a aba "Source Control", ou pelo site do GitHub com "Add file > Upload files")
3. **Não suba o arquivo `.env`** com senhas reais (só o `.env.example`, que já não tem dado sensível)

### Passo 3 — criar o Web Service no Render
1. Acesse **https://render.com** e crie uma conta (dá pra usar login do GitHub)
2. Clique em **New > Web Service**
3. Conecte o repositório que você acabou de subir
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Em **Environment**, adicione as variáveis (com os dados do db4free.net):
   - `DB_HOST` = `db4free.net`
   - `DB_USER` = seu usuário do db4free
   - `DB_PASSWORD` = sua senha do db4free
   - `DB_NAME` = nome do seu banco no db4free
   - `DB_PORT` = `3306`
6. Clique em **Deploy**

Depois de alguns minutos, o Render te dá uma URL tipo `https://mural-quadra.onrender.com` — esse é o link que você entrega no trabalho.

> Lembrete: bom, ao que aparenta, o plano free do Render "dorme" depois de 15 min sem acesso, e demora entre 30s a-60s pra "acordar" no próximo acesso. É normal, não é erro.

## Possíveis melhorias para o "trabalho"...
- Login de administrador para só ele poder publicar/apagar 
- Envio de e-mail/notificação quando um novo evento é postado
- Hospedar...maybe

aceito criticas construtivas ja que to no "inicio" da caminhada e FÉ