from decimal import Decimal, ROUND_HALF_UP
from .models import ReceitaDespesa  # Ajuste o nome conforme o modelo correto

def get_saldos_reprogramados(escola_id, programa_nome):
    try:
        # Busca o último registro de ReceitaDespesa filtrando por escola e programa
        dados = ReceitaDespesa.objects.filter(escola_id=escola_id, programa=programa_nome).last()
        
        if dados:
            # Converte os saldos para Decimal com duas casas decimais (R$ XX,XX)
            saldo_custeio = Decimal(str(dados.saldo_reprogramado_es_custeio or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            saldo_capital = Decimal(str(dados.saldo_reprogramado_es_capital or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            return {
                "custeio": saldo_custeio,
                "capital": saldo_capital
            }

    except Exception as e:
        # Loga o erro no console para depuração
        print(f"❌ Erro ao buscar saldos reprogramados: {e}")

    # Caso não encontre dados ou ocorra erro, retorna saldos zerados
    return {
        "custeio": Decimal("0.00").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
        "capital": Decimal("0.00").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    }


from decimal import Decimal
from .models import ReceitaDespesa  # Certifique-se de ajustar o import

def get_saldos_completos(escola_id, programa_nome):
    try:
        receita = ReceitaDespesa.objects.filter(escola_id=escola_id, programa=programa_nome).last()
        if receita:
            return {
                "saldo_anterior_custeio": receita.saldo_anterior_custeio or Decimal("0.00"),
                "saldo_anterior_capital": receita.saldo_anterior_capital or Decimal("0.00"),
                "valor_creditado_custeio": receita.valor_creditado_custeio or Decimal("0.00"),
                "valor_creditado_capital": receita.valor_creditado_capital or Decimal("0.00"),
                "saldo_reprogramar_custeio": receita.saldo_reprogramar_custeio or Decimal("0.00"),
                "saldo_reprogramar_capital": receita.saldo_reprogramar_capital or Decimal("0.00"),
            }
    except Exception as e:
        print(f"❌ Erro ao buscar dados da receita: {e}")

    # Retorna valores zerados se não encontrar
    return {
        "saldo_anterior_custeio": Decimal("0.00"),
        "saldo_anterior_capital": Decimal("0.00"),
        "valor_creditado_custeio": Decimal("0.00"),
        "valor_creditado_capital": Decimal("0.00"),
        "saldo_reprogramar_custeio": Decimal("0.00"),
        "saldo_reprogramar_capital": Decimal("0.00"),
    }
