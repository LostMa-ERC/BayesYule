import numpy as np

def compute_stat_witness(witness_nb, additional_stats = True):
    """
    Compute stats on witness distribution.
    """
    nb_stats = 13 if additional_stats else 6

    if not witness_nb:
        return np.zeros(nb_stats)
    elif witness_nb == "BREAK":
        return np.ones(nb_stats)
    
    witness_nb = np.array(witness_nb, dtype=np.float64)
    nb_oeuvre = witness_nb.size
    nb_temoins = np.sum(witness_nb)
    
    stats = []

    # Calcul de chaque statistique
    stats.append(nb_temoins.item()/1e6)
    stats.append(nb_oeuvre/1e6)
    stats.append(nb_oeuvre/nb_temoins.item())
    stats.append(np.max(witness_nb).item()/nb_temoins.item())
    stats.append(np.median(witness_nb).item()/np.max(witness_nb).item())
    stats.append(np.sum(witness_nb == 1).item()/nb_oeuvre)

    if additional_stats:
        stats.append(np.sum(witness_nb == 2).item()/nb_oeuvre)
        stats.append(np.sum(witness_nb == 3).item()/nb_oeuvre)
        stats.append(np.sum(witness_nb == 4).item()/nb_oeuvre)
        stats.append(np.quantile(witness_nb, 0.75).item()/np.max(witness_nb).item())
        stats.append(np.quantile(witness_nb, 0.85).item()/np.max(witness_nb).item())
        stats.append(np.partition(witness_nb, -2)[-2].item()/nb_temoins.item() if len(witness_nb) > 1 else 0)
        stats.append(np.partition(witness_nb, -2)[-2].item()/np.max(witness_nb).item() if len(witness_nb) > 1 else 0)

    
    # Construction du tableau avec des valeurs scalaires
    stats = np.array(stats, dtype=np.float64)
    
    return stats

def inverse_compute_stat_witness(stats):
    """Inverse les statistiques pour retrouver les valeurs d'origine"""

    nb_temoins = int(stats[0]*1e6)
    nb_oeuvre = int(stats[1]*1e6)
    max_wit = int(stats[3]*stats[0]*1e6)
    med_wit = int(stats[4]*stats[3]*stats[0]*1e6)
    nb_one = int(stats[5]*stats[1]*1e6)
    
    return [nb_temoins, nb_oeuvre, max_wit, med_wit, nb_one]

