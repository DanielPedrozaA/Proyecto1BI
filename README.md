# Proyecto1BI

curl -X POST http://127.0.0.1:5000/api/retrain -F 'file=@../ODScat_345_SMALL.xlsx'

curl -X POST http://127.0.0.1:5000/api/predict -H "Content-Type: application/json" -d '{"sentences": ["Esta es una oración para clasificar.", "Otra oración más."]}'