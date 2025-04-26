from conexao import conectar

def registrar_compra(cliente_id, valor, descricao=""):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO movimentacoes (cliente_id, tipo, valor, descricao) VALUES (%s, 'compra', %s, %s)"
    cursor.execute(sql, (cliente_id, valor, descricao))
    conn.commit()
    cursor.close()
    conn.close()

def registrar_pagamento(cliente_id, valor, descricao=""):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO movimentacoes (cliente_id, tipo, valor, descricao) VALUES (%s, 'pagamento', %s, %s)"
    cursor.execute(sql, (cliente_id, valor, descricao))
    conn.commit()
    cursor.close()
    conn.close()

def listar_movimentacoes(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    sql = "SELECT tipo, valor, descricao, data, id FROM movimentacoes WHERE cliente_id = %s ORDER BY data DESC"
    cursor.execute(sql, (cliente_id,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def registrar_movimentacao(cliente_id, tipo, valor, descricao):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO movimentacoes (cliente_id, tipo, valor, descricao) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (cliente_id, tipo, valor, descricao))
    conn.commit()
    cursor.close()
    conn.close()


def excluir_movimentacao_por_id(mov_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimentacoes WHERE id = %s", (mov_id,))
    conn.commit()
    cursor.close()
    conn.close()
