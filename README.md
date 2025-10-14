# Automation_for_refactoring_mailing

# 📞 Redistribuição de Campanhas Telefônicas

Este projeto automatiza a redistribuição de registros de campanhas telefônicas com base em dias úteis, regras de negócio e status dos agendamentos. Ele foi desenvolvido para facilitar a gestão de campanhas ativas, vencidas e em execução, garantindo que os contatos sejam redistribuídos de forma proporcional e eficiente.

---

## 🚀 Objetivo

Redistribuir registros de pacientes que estão com agendamentos vencidos, em execução ou ativos, distribuindo-os proporcionalmente entre os dias úteis do mês, com base em um calendário corporativo.

---

## 🧩 Estrutura do Projeto

O código está dividido em **três blocos principais**, cada um com uma função específica:

### 🔹 Bloco 1 — Coleta de Registros
- Conecta ao banco Oracle
- Busca registros com base no status e na data (`Enviar`, `Em Execução`, vencidos, etc.)
- Agrupa os dados por campanha
- Armazena os dados em um dicionário chamado `registros_para_redistribuir`

### 🔹 Bloco 2 — Carregamento de Calendário
- Extrai o calendário corporativo a partir da data atual
- Filtra os dias úteis com peso (`DIAS_TT_MES`)
- Prepara a base para redistribuição proporcional

### 🔹 Bloco 3 — Redistribuição e Atualização
- Redistribui os registros proporcionalmente entre os dias úteis
- Atualiza os campos `STATUS`, `LIGAR_EM` e `CANAIS` no banco
- Garante que todos os registros sejam tratados com segurança e sem perdas

---

## 📦 Requisitos

- Python 3.10+
- Pandas
- cx_Oracle (ou SQLAlchemy, dependendo da conexão)
- Acesso ao banco Oracle com permissões de leitura e escrita

Instale os pacotes com:

```bash
pip install pandas cx_Oracle


🧪 Testes e Validações
O código verifica se os campos essenciais existem

Evita exclusão agressiva de registros

Preenche valores nulos com padrões seguros (FONE = 999999999, CANAIS = 1)

Exibe mensagens claras sobre o progresso e possíveis erros

💡 Dicas para Manutenção
Sempre verifique o calendário antes de redistribuir

Mantenha o dicionário registros_para_redistribuir bem estruturado

Evite limpar os dados se já vieram íntegros do banco

Use commits claros e organizados no Git

👩‍💻 Desenvolvido por
Luci Iara de Souza Abreu  - Analista de Dados, Porto Alegre, RS — Brasil
