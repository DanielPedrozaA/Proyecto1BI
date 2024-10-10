# Clasificación ODS

API basada en Flask para clasificar oraciones de acuerdo a los Objetivos de Desarrollo Sostenible (ODS). Proporciona tanto endpoints de API como interfaces web para predicción y reentrenamiento del modelo.

## Estructura del Proyecto

```
├── Documento GProy1E1- 1.pdf
├── ODScat_345.xlsx
├── ODScat_345_SMALL.xlsx
├── Pipeline.ipynb
├── Prediccion resultados
│   ├── resultados_lr.xlsx
│   ├── resultados_rf.xlsx
│   └── resultados_svm.xlsx
├── Proyecto_1.ipynb
├── README.md
├── api
│   ├── app.py
│   ├── functions.py
│   ├── model.joblib
│   └── templates
│       ├── base.html
│       ├── home.html
│       ├── predict.html
│       └── retrain.html
└── requirements.txt
```

## Instalación

1. Clona este repositorio
2. Navega al directorio del proyecto
3. Instala los paquetes requeridos:

```
pip install -r requirements.txt
```

## Ejecutar la Aplicación

Para iniciar la aplicación Flask, ejecuta:

```
python api/app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`.

## Endpoints de la API

### 1. Predecir

- **URL**: `/api/predict`
- **Método**: POST
- **Descripción**: Clasifica una o más oraciones de acuerdo a los ODS.
- **Contenido de la solicitud**: 
  - Formato: JSON
  - Estructura:
    ```json
    {
      "sentences": ["oración 1", "oración 2", ...]
    }
    ```
  - El campo "sentences" es una lista que puede contener una o más oraciones para clasificar.
- **Ejemplo**:
  ```
  curl -X POST http://127.0.0.1:5000/api/predict \
       -H "Content-Type: application/json" \
       -d '{"sentences": ["Implementar medidas para reducir la contaminación del aire en las ciudades", "Mejorar el acceso a la educación en zonas rurales"]}'
  ```
- **Explicación**: En este ejemplo, estamos enviando dos oraciones para clasificar. La API analizará cada oración y devolverá la clasificación ODS correspondiente para cada una.
- **Respuesta**:
    ```json
    {
        "predictions": [
            {
            "prediction": 4,
            "probabilities": [
                0.627164295581676,
                0.1687781820183782,
                0.20405752239994573
            ],
            "sentence": "Implementar medidas para reducir la contaminaci\u00f3n del aire en las ciudades"
            },
            {
            "prediction": 4,
            "probabilities": [
                0.5801207297400305,
                0.18749297199697615,
                0.2323862982629931
            ],
            "sentence": "Mejorar el acceso a la educaci\u00f3n en zonas rurales"
            }
        ]   
    }
    ```

### 2. Reentrenar

- **URL**: `/api/retrain`
- **Método**: POST
- **Descripción**: Reentrena el modelo utilizando un nuevo conjunto de datos.
- **Contenido de la solicitud**:
  - Formato: Multipart form-data
  - Campo del archivo: 'file'
  - Tipo de archivo: Excel (.xlsx)
- **Estructura esperada del archivo**:
  El archivo Excel debe contener al menos dos columnas:
  1. Una columna con las oraciones o textos a clasificar.
  2. Una columna con las etiquetas ODS correspondientes.
- **Ejemplo**:
  ```
  curl -X POST http://127.0.0.1:5000/api/retrain \
       -F 'file=@ruta/al/archivo/ODScat_345_SMALL.xlsx'
  ```
- **Explicación**: En este ejemplo, estamos enviando un archivo Excel llamado 'ODScat_345_SMALL.xlsx' para reentrenar el modelo. Este archivo debe contener nuevos ejemplos de oraciones y sus clasificaciones ODS correspondientes. La API utilizará estos datos para actualizar y mejorar el modelo de clasificación.
- **Respuesta**:
    ```json
    {
    "message": "El modelo se ha reentrenado con \u00e9xito.",
        "report": {
            "3": {
            "f1-score": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "support": 6.0
            },
            "4": {
            "f1-score": 0.6086956521739131,
            "precision": 0.4375,
            "recall": 1.0,
            "support": 7.0
            },
            "5": {
            "f1-score": 0.9032258064516129,
            "precision": 1.0,
            "recall": 0.8235294117647058,
            "support": 17.0
            },
            "accuracy": 0.7,
            "macro avg": {
            "f1-score": 0.5039738195418421,
            "precision": 0.4791666666666667,
            "recall": 0.6078431372549019,
            "support": 30.0
            },
            "weighted avg": {
            "f1-score": 0.6538569424964937,
            "precision": 0.66875,
            "recall": 0.7,
            "support": 30.0
            }
        }
    }

    ```


## Interfaces Web

### 1. Predecir

- **URL**: `/predict`
- **Métodos**: GET, POST
- **Descripción**: Interfaz web para clasificar oraciones de acuerdo a los ODS.


### 2. Reentrenar

- **URL**: `/retrain`
- **Métodos**: GET, POST
- **Descripción**: Interfaz web para reentrenar el modelo con un nuevo conjunto de datos.


## Descripción del Proyecto

Esta aplicación Flask proporciona funcionalidad para clasificar oraciones de acuerdo a los Objetivos de Desarrollo Sostenible (ODS). Los usuarios pueden interactuar con el sistema a través de endpoints de API e interfaces web. Las principales características incluyen:

1. Clasificar una o múltiples oraciones y asociarlas con ODS.
2. Reentrenar el modelo de clasificación utilizando nuevos datos.
