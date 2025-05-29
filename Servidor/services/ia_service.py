import tensorflow as tf
import numpy as np
from PIL import Image
import io
import pandas as pd

CSV_PATH = r"C:\SeekMush\Dataset\Fotos + Nomes\translated_names.csv"

# Lê o CSV com verificação de delimitador
try:
    df = pd.read_csv(CSV_PATH)
    if df.shape[1] == 1:
        # Arquivo pode estar separado por ponto-e-vírgula
        df = pd.read_csv(CSV_PATH, sep=';')
except Exception as e:
    raise RuntimeError(f"Erro ao carregar CSV: {e}")

# Remove espaços e valores nulos
df = df.dropna(subset=["scientific_name"])
df["scientific_name"] = df["scientific_name"].str.strip()
df["common_name"] = df["common_name"].str.strip()

# Ordena pela coluna correta
df_sorted = df.sort_values("scientific_name").reset_index(drop=True)

# Verifica número total
print(f">>> CSV carregado: {len(df_sorted)} classes científicas")

CLASSES = df_sorted["scientific_name"].tolist()
COMMON_NAMES = dict(zip(df_sorted["scientific_name"], df_sorted["common_name"]))


# Carrega o modelo treinado
MODEL_PATH = r"C:\SeekMush\models\V2.1TF.keras"
model = tf.keras.models.load_model(MODEL_PATH)


def prever_imagem(imagem_bytes: bytes):
    image = Image.open(io.BytesIO(imagem_bytes)).convert("RGB").resize((256, 256))
    array = np.expand_dims(np.array(image) / 255.0, axis=0)
    pred = model.predict(array)[0]


    print("Shape da predição:", pred.shape)
    print("Número de classes carregadas:", len(CLASSES))


    idx = int(np.argmax(pred))
    if idx >= len(CLASSES):
        raise ValueError(f"Índice {idx} excede a quantidade de classes.")

    scientific = CLASSES[idx]
    common = COMMON_NAMES.get(scientific, "Unknown")
    accuracy = float(pred[idx])

    return scientific, common, accuracy
