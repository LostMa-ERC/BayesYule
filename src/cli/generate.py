import json

import numpy as np
import pandas as pd

from src.models import BirthDeath, YuleModel
from src.utils.stats import compute_stat_witness, inverse_compute_stat_witness


def generate(
    data_path: str,
    model: YuleModel | BirthDeath,
    parameters,
    seed: int = 42,
    show_params: bool = False,
):
    rng = np.random.default_rng(seed)

    if show_params:
        print("\nPARAMETERS_JSON_START")
        print(json.dumps(parameters))
        print("PARAMETERS_JSON_END")

    print("Generating population...")

    pop = model.generator.generate(rng, parameters)
    if pop == []:
        print("No survivors in the simulation!")
        return False
    if pop == "BREAK":
        print("The estimation hit the maximum size during simulation...")
        print("Estimation not saved.")
        return False

    text_val = []
    witness_val = []

    for i, num in enumerate(pop):
        for j in range(num):
            text_val.append(f"T{i}")
            witness_val.append(f"W{i}-{j + 1}")

    # Créer le dataframe
    df = pd.DataFrame({"witness_ID": witness_val, "text_ID": text_val})

    df.to_csv(data_path, sep=";", index=False)

    aggregates = df.groupby("text_ID")["witness_ID"]
    witness_counts = list(aggregates.count().sort_values(ascending=False))
    s = inverse_compute_stat_witness(compute_stat_witness(witness_counts))

    print(f"Witness Number: {s[0]}")
    print(f"Works Number: {s[1]}")
    print(f"Max Witnesses: {s[2]}")
    print(f"Number of 1: {s[4]}")

    return True
