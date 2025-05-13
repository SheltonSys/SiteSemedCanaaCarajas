import json
import re

entrada = "dados.json"
saida = "dados_filtrados.json"

with open(entrada, "r", encoding="utf-8") as f:
    dados = json.load(f)

modelos_excluir = ["contenttypes.contenttype", "auth.permission"]
cpfs_unicos = set()
emails_unicos = set()
dados_limpos = []

def normalizar_cpf(cpf):
    return re.sub(r'\D', '', cpf or "").strip()

def normalizar_email(email):
    return email.strip().lower() if email else ""

for obj in dados:
    modelo = obj.get("model")
    if modelo in modelos_excluir:
        continue

    if modelo == "semedapp.cadastrocandidato":
        campos = obj.get("fields", {})
        cpf = normalizar_cpf(campos.get("cpf"))
        email = normalizar_email(campos.get("email"))

        if cpf in cpfs_unicos or email in emails_unicos:
            continue

        cpfs_unicos.add(cpf)
        emails_unicos.add(email)

    dados_limpos.append(obj)

with open(saida, "w", encoding="utf-8") as f:
    json.dump(dados_limpos, f, indent=2, ensure_ascii=False)

print(f"Arquivo salvo como {saida} com {len(dados_limpos)} registros.")
