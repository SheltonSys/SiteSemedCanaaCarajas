from django.db import connection

def corrigir_codificacao_cargo():
    with connection.cursor() as cursor:
        # Selecionar todos os cargos problemáticos
        cursor.execute("SELECT id, cargo FROM curriculo_antigo WHERE cargo IS NOT NULL")
        rows = cursor.fetchall()

        for row in rows:
            id_curriculo, cargo_corrompido = row
            try:
                # Corrigir a codificação do cargo
                cargo_corrigido = cargo_corrompido.encode("latin-1", "ignore").decode("utf-8")
                
                # Atualizar a coluna no banco
                cursor.execute("UPDATE curriculo_antigo SET cargo = ? WHERE id = ?", (cargo_corrigido, id_curriculo))
                
                print(f"✔️ Corrigido ID {id_curriculo}: {cargo_corrompido} -> {cargo_corrigido}")

            except (UnicodeDecodeError, AttributeError):
                print(f"❌ Erro ao corrigir ID {id_curriculo}: {cargo_corrompido}")

    print("✅ Correção concluída!")

# Execute a função
corrigir_codificacao_cargo()
