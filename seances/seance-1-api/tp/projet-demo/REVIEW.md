| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Les codes de statut correspondent à la spec (201, 404, 409) |OK||
| `response_model` présent sur les 4 routes |OK | |
| La validation `date_fin > date_debut` est bien dans le schéma Pydantic |OK | |
| Le router n'accède pas au stockage de `items` |OK | |
| Pas d'`async def` sans `await` | | |
| Aucune dépendance ajoutée dans `requirements.txt` (ou justifiée) |OK | |
| Les routes littérales sont déclarées avant les routes paramétrées |OK | |
| Le code renvoie une réponse cohérente pour `POST /reservations/999/annuler` |OK | |
