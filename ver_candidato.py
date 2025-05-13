import json

with open('dados_filtrados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

for obj in dados:
    if obj['model'] == 'semedapp.cadastrocandidato' and obj['pk'] == 809:
        print(json.dumps(obj, indent=4, ensure_ascii=False))
        break
