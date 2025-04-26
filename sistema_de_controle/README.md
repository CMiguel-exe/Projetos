# Client Management and Financial Transaction System

A Flask-based web application that provides comprehensive client management and financial transaction tracking capabilities. The system enables businesses to manage customer information, track purchases and payments, and generate reports on outstanding balances.

This application serves as a robust solution for small businesses needing to track customer transactions and manage accounts receivable. It features a user-friendly interface for managing client records, recording financial transactions, and monitoring payment histories. The system maintains detailed transaction logs and provides real-time balance calculations, making it particularly useful for businesses that extend credit to their customers.

## Repository Structure
```
.
├── app.py                 # Main Flask application entry point with route definitions
├── cliente.py            # Client management operations (CRUD operations)
├── conexao.py           # Database connection configuration
├── movimentacao.py      # Financial transaction handling logic
└── templates/           # HTML templates for the web interface
    ├── clientes.html              # Client listing and search interface
    ├── editar_cliente.html        # Client information editing form
    ├── historico.html             # Transaction history display
    ├── nova_compra_livre.html     # New purchase registration form
    ├── novo_cliente.html          # New client registration form
    ├── novo_pagamento_livre.html  # New payment registration form
    ├── pagina_inicial.html        # Application homepage
    └── relatorio_devedores.html   # Debtors report display
```

## Usage Instructions
### Prerequisites
- Python 3.6 or higher
- MySQL Server
- pip (Python package installer)

Required Python packages:
```bash
Flask
mysql-connector-python
```

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment:
```bash
# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install Flask mysql-connector-python
```

4. Configure the database:
```sql
CREATE DATABASE padaria;
USE padaria;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    cpf VARCHAR(14)
);

CREATE TABLE movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    tipo VARCHAR(20),
    valor DECIMAL(10,2),
    descricao TEXT,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
```

5. Update database connection settings in `conexao.py` with your credentials.

### Quick Start

1. Start the application:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

3. Basic operations:
- Add a new client through "Novo Cliente"
- Record purchases using "Nova Compra"
- Register payments via "Novo Pagamento"
- View client history by clicking on the history link next to each client

### More Detailed Examples

1. Managing Clients:
```python
# Add a new client
POST /clientes/novo
{
    "nome": "John Doe",
    "telefone": "123-456-7890",
    "cpf": "123.456.789-00"
}

# Update client information
POST /clientes/<id>/editar
{
    "nome": "John Doe Updated",
    "telefone": "098-765-4321",
    "cpf": "123.456.789-00"
}
```

2. Recording Transactions:
```python
# Record a purchase
POST /compras/nova
{
    "cliente_id": "1",
    "valor": "100.50",
    "descricao": "Monthly purchase"
}

# Record a payment
POST /pagamentos/novo
{
    "cliente_id": "1",
    "valor": "50.25",
    "descricao": "Partial payment"
}
```

### Troubleshooting

Common Issues:

1. Database Connection Errors
```
Error: Cannot connect to MySQL server
Solution: 
- Verify MySQL is running
- Check credentials in conexao.py
- Ensure database 'padaria' exists
```

2. Client Search Not Working
```
Issue: Search returns no results
Debug steps:
1. Check if the search term is being properly passed
2. Verify database connection
3. Check SQL query in listar_clientes()
```

## Data Flow
The system processes client and transaction data through a structured flow from user input to database storage and retrieval.

```ascii
User Input → Flask Routes → Business Logic → Database
     ↑                                          |
     |__________ Template Rendering ____________|
```

Key Component Interactions:
1. Flask routes handle HTTP requests and direct traffic
2. Client operations manage customer data through cliente.py
3. Transaction operations process financial data via movimentacao.py
4. Database connections are managed through conexao.py
5. Templates render data for user interface
6. API endpoints provide real-time client information
7. Search functionality filters client records
8. Transaction history maintains chronological record