# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

# Função para classificar o consumo
def classificar_consumo(consumo):
    if consumo <= 500:
        return "Consumo Baixo (≤ 500 kWh)"
    elif consumo <= 1500:
        return "Consumo Médio (501–1500 kWh)"
    else:
        return "Consumo Alto (> 1500 kWh)"

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    classificacao = None
    consumo_total = None

    if request.method == "POST":
        try:
            servidores = int(request.form["servidores"])
            custo_kwh = float(request.form["custo_kwh"])
            consumo_mensal = float(request.form["consumo_mensal"])
            usar_solar = request.form.get("usar_solar")

            # Cálculo do consumo total
            consumo_total = servidores * consumo_mensal
            if usar_solar:
                consumo_total *= 0.7  # Redução de 30% com energia solar

            # Cálculo do custo total
            custo_total = consumo_total * custo_kwh
            resultado = f"R$ {custo_total:.2f}"

            # Classificação do consumo
            classificacao = classificar_consumo(consumo_total)

        except ValueError:
            resultado = "Erro: Verifique se todos os campos foram preenchidos corretamente."

    return render_template("index.html", resultado=resultado, classificacao=classificacao, consumo=consumo_total)

if __name__ == "__main__":
    app.run(debug=True)