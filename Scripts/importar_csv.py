import csv
import os
import sys

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import SessionLocal
from db.models import MushroomDataset
from db import mushroom_mapping as mm  # importa os mapeamentos

# Caminho do arquivo CSV
csv_file_path = os.path.join('Dataset', 'mushrooms.csv')

def map_letalidade(class_code):
    return mm.LETALIDADE_MAP.get(class_code, 1)  # padrão: 1 (não letal)

def main():
    session = SessionLocal()

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):
            # Mapeia os códigos
            mushroom = MushroomDataset(
                file_path=f"Dataset/mushroom_{i}.jpg",  # fictício
                especie="Desconhecida",  # até a IA definir
                confidence=0.0,
                informacoes=None,
                letalidade=map_letalidade(row['class']),
                cap_shape=mm.CAP_SHAPE_MAP.get(row['cap-shape']),
                cap_surface=mm.CAP_SURFACE_MAP.get(row['cap-surface']),
                cap_color=mm.CAP_COLOR_MAP.get(row['cap-color']),
                bruises=mm.BRUISES_MAP.get(row['bruises']),
                odor=mm.ODOR_MAP.get(row['odor']),
                gill_attachment=mm.GILL_ATTACHMENT_MAP.get(row['gill-attachment']),
                gill_spacing=mm.GILL_SPACING_MAP.get(row['gill-spacing']),
                gill_size=mm.GILL_SIZE_MAP.get(row['gill-size']),
                gill_color=mm.GILL_COLOR_MAP.get(row['gill-color']),
                stalk_shape=mm.STALK_SHAPE_MAP.get(row['stalk-shape']),
                stalk_root=mm.STALK_ROOT_MAP.get(row['stalk-root']),
                stalk_surface_above_ring=mm.STALK_SURFACE_MAP.get(row['stalk-surface-above-ring']),
                stalk_surface_below_ring=mm.STALK_SURFACE_MAP.get(row['stalk-surface-below-ring']),
                stalk_color_above_ring=mm.STALK_COLOR_MAP.get(row['stalk-color-above-ring']),
                stalk_color_below_ring=mm.STALK_COLOR_MAP.get(row['stalk-color-below-ring']),
                veil_type=mm.VEIL_TYPE_MAP.get(row['veil-type']),
                veil_color=mm.VEIL_COLOR_MAP.get(row['veil-color']),
                ring_number=mm.RING_NUMBER_MAP.get(row['ring-number']),
                ring_type=mm.RING_TYPE_MAP.get(row['ring-type']),
                spore_print_color=mm.SPORE_PRINT_COLOR_MAP.get(row['spore-print-color']),
                population=mm.POPULATION_MAP.get(row['population']),
                habitat=mm.HABITAT_MAP.get(row['habitat'])
            )

            session.add(mushroom)

        session.commit()
        print(f"{i+1} registros importados com sucesso.")

if __name__ == "__main__":
    main()
