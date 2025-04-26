from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from cliente import listar_clientes, adicionar_cliente, obter_cliente, atualizar_cliente, excluir_cliente
from movimentacao import registrar_compra, registrar_pagamento, listar_movimentacoes, registrar_movimentacao
from conexao import conectar 

app = Flask(__name__)

#Rota para a pagina inicial

@app.route ("/")
def pagina_inicial():
    return render_template("pagina_inicial.html")

#Rota para pesquisar clientes

@app.route("/clientes")
def clientes():
    termo = request.args.get("busca", "").strip()
    todos = listar_clientes()
    if termo:
        filtrados = [c for c in todos if termo.lower() in c[1].lower()]
    else:
        filtrados = todos
    return render_template("clientes.html", clientes=filtrados, busca=termo)

#API para buscar cliente por ID

@app.route("/api/cliente/<int:cliente_id>")
def api_cliente(cliente_id):
    cliente = obter_cliente(cliente_id)
    if cliente:
        return jsonify({
            "id": cliente[0],
            "nome": cliente[1],
            "telefone": cliente[2],
            "cpf": cliente[3]
        })
    else:
        return jsonify({"erro": "Cliente não encontrado"}), 404

#Rota para registrar compra livre

@app.route("/compras/nova", methods=["GET", "POST"])
def nova_compra_livre():
    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        valor = request.form["valor"]
        descricao = request.form["descricao"]
        registrar_movimentacao(cliente_id, "compra", valor, descricao)
        return redirect(url_for("clientes"))
    return render_template("nova_compra_livre.html")

#Rota para registrar pagamento livre

@app.route("/pagamentos/novo", methods=["GET", "POST"])
def novo_pagamento_livre():
    if request.method == "POST":
        cliente_id = request.form["cliente_id"]
        valor = request.form["valor"]
        descricao = request.form["descricao"]
        registrar_movimentacao(cliente_id, "pagamento", valor, descricao)
        return redirect(url_for("clientes"))
    return render_template("novo_pagamento_livre.html")

# Rota para editar cliente

@app.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar_cliente(cliente_id):
    cliente = obter_cliente(cliente_id)
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        cpf = request.form["cpf"]
        atualizar_cliente(cliente_id, nome, telefone, cpf)
        flash("Cliente atualizado com sucesso!")
        return redirect(url_for("clientes"))
    return render_template("editar_cliente.html", cliente=cliente)

#Rota para ver historico de movimentacoes

@app.route("/clientes/<int:cliente_id>/historico")
def historico(cliente_id):
    movimentos = listar_movimentacoes(cliente_id)
    return render_template("historico.html", movimentos=movimentos, cliente_id=cliente_id)

#Rota para excluir cliente individual

@app.route("/clientes/<int:cliente_id>/excluir", methods=["GET"])
def excluir_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("clientes"))

#Rota para excluir movimentacao individual

@app.route("/clientes/<int:cliente_id>/movimentacoes/<int:mov_id>/excluir", methods=["GET"])
def excluir_movimentacao(cliente_id, mov_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movimentacoes WHERE id = %s", (mov_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("historico", cliente_id=cliente_id))

#Rota para adicionar cliente

@app.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        adicionar_cliente(nome, telefone)
        return redirect(url_for("clientes"))
    return render_template("novo_cliente.html")

#Rota para relatorios

@app.route("/relatorios/devedores")
def relatorio_devedores():
    todos = listar_clientes()
    devedores = [c for c in todos if c[4] > 0]  # c[4] = saldo
    return render_template("relatorio_devedores.html", clientes=devedores)

if __name__ == "__main__":
    app.run(debug=True)
