from conexao import conectar

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    sql = (
        "SELECT c.id, c.nome, c.telefone, c.cpf, "
        "COALESCE(SUM(CASE WHEN m.tipo = 'compra' THEN m.valor ELSE 0 END), 0) - "
        "COALESCE(SUM(CASE WHEN m.tipo = 'pagamento' THEN m.valor ELSE 0 END), 0) AS saldo "
        "FROM clientes c "
        "LEFT JOIN movimentacoes m ON c.id = m.cliente_id "
        "GROUP BY c.id, c.nome, c.telefone, c.cpf "
        "ORDER BY c.nome"
    )
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


def adicionar_cliente(nome, telefone):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO clientes (nome, telefone) VALUES (%s, %s)"
    cursor.execute(sql, (nome, telefone))
    conn.commit()
    cursor.close()
    conn.close()

def obter_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, cpf FROM clientes WHERE id = %s", (cliente_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def atualizar_cliente(cliente_id, nome, telefone, cpf):
    conn = conectar()
    cursor = conn.cursor()
    sql = "UPDATE clientes SET nome = %s, telefone = %s, cpf = %s WHERE id = %s"
    cursor.execute(sql, (nome, telefone, cpf, cliente_id))
    conn.commit()
    cursor.close()
    conn.close()

def excluir_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    sql = "DELETE FROM clientes WHERE id = %s"
    cursor.execute(sql, (cliente_id,))
    conn.commit()
    cursor.close()
    conn.close()
