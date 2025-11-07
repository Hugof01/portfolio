# vigenere_tool_precis.py
import string
import random
import math
import time

# fréquences françaises approximatives (monogrammes)
FREQ_FR = {
    'A': 0.081, 'B': 0.009, 'C': 0.034, 'D': 0.037, 'E': 0.173, 'F': 0.011,
    'G': 0.009, 'H': 0.007, 'I': 0.075, 'J': 0.006, 'K': 0.001, 'L': 0.054,
    'M': 0.030, 'N': 0.071, 'O': 0.053, 'P': 0.030, 'Q': 0.009, 'R': 0.066,
    'S': 0.079, 'T': 0.073, 'U': 0.063, 'V': 0.018, 'W': 0.001, 'X': 0.004,
    'Y': 0.003, 'Z': 0.001
}

COMMON_FR_WORDS = ["LE", "LA", "LES", "DE", "DES", "ET", "EN", "UNE", "QUE", "QUI", "POUR", "DANS", "EST", "SUR"]

# ------------------------------
# FONCTIONS VIGENERE (unchanged)
# ------------------------------
def chiffrement_vigenere(texte, cle):
    texte = texte.upper()
    cle = cle.upper()
    texte_chiffre = ""
    index_cle = 0
    for caractere in texte:
        if caractere.isalpha():
            decalage = ord(cle[index_cle]) - ord('A')
            caractere_chiffre = chr((ord(caractere) - ord('A') + decalage) % 26 + ord('A'))
            texte_chiffre += caractere_chiffre
            index_cle = (index_cle + 1) % len(cle)
        else:
            texte_chiffre += caractere
    return texte_chiffre

def dechiffrement_vigenere(texte_chiffre, cle):
    texte_chiffre = texte_chiffre.upper()
    cle = cle.upper()
    texte_dechiffre = ""
    index_cle = 0
    for caractere in texte_chiffre:
        if caractere.isalpha():
            decalage = ord(cle[index_cle]) - ord('A')
            caractere_dechiffre = chr((ord(caractere) - ord('A') - decalage) % 26 + ord('A'))
            texte_dechiffre += caractere_dechiffre
            index_cle = (index_cle + 1) % len(cle)
        else:
            texte_dechiffre += caractere
    return texte_dechiffre

# ------------------------------
# UTILS STATISTIQUES
# ------------------------------
def chi_square_score(texte):
    texte_alpha = [c for c in texte if c.isalpha()]
    if not texte_alpha:
        return float("inf")
    n = len(texte_alpha)
    freq_obs = {c: texte_alpha.count(c) / n for c in string.ascii_uppercase}
    chi2 = sum(((freq_obs.get(c, 0) - FREQ_FR.get(c, 0)) ** 2) / (FREQ_FR.get(c, 0) or 1e-9)
               for c in FREQ_FR)
    return chi2

def word_score_fr(texte):
    """Score simple basé sur la présence de mots fréquents français."""
    T = texte.upper()
    score = 0
    # compte occurrences non chevauchantes (approximatif)
    for w in COMMON_FR_WORDS:
        score += T.count(w) * len(w)
    # penalise si texte contient très peu d'espaces (signe de mauvais découpage)
    spaces = T.count(' ')
    score += spaces * 2
    return score

def combined_score_improved(texte):
    """
    Score à maximiser.
    - On garde chi² (plus bas = meilleur), on l'inverse et on le normalise.
    - On favorise la présence d'espaces (indice de mots).
    - On ajoute un petit bonus pour digrammes fréquents (approx) via chi² rapide.
    """
    texte_up = texte.upper()
    # composantes
    c = chi_square_score(texte)         # plus petit = meilleur
    spaces = texte_up.count(' ')
    # composante digramme très légère : on pénalise rareté d'AG,LE,RE,... (approx)
    common_digrams = ["LE", "DE", "ES", "EN", "RE", "ER", "ON", "TE"]
    digram_score = sum(texte_up.count(dg) for dg in common_digrams)

    # normalisation empirique / pondérations
    # On veut un score croissant avec qualité
    score = (digram_score * 8) + (spaces * 3) - (c * 5)
    return score

# ------------------------------
# KASISKI / FRIEDMAN-LIKE : estimation longueur via IC moyenne par colonne
# ------------------------------
def index_of_coincidence(seq):
    seq = [c for c in seq if c.isalpha()]
    n = len(seq)
    if n <= 1:
        return 0.0
    freqs = {c: seq.count(c) for c in string.ascii_uppercase}
    ic = sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))
    return ic

def ic_moyen_pour_longueur(texte, L):
    """Sépare en L colonnes et retourne l'IC moyen (utilisé comme indicateur de longueur)."""
    cols = ['' for _ in range(L)]
    chiff = ''.join([c for c in texte.upper() if c.isalpha()])
    if not chiff:
        return 0.0
    for i, c in enumerate(chiff):
        cols[i % L] += c
    ics = [index_of_coincidence(col) for col in cols if col]
    if not ics:
        return 0.0
    return sum(ics) / len(ics)

def candidats_longueurs(texte, max_long=12, top_k=3):
    scores = []
    for L in range(1, max_long + 1):
        scores.append((L, ic_moyen_pour_longueur(texte, L)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [L for L, s in scores[:top_k]]

# ------------------------------
# INITIALISATION PAR CHI² (comme précédemment)
# ------------------------------
def meilleure_lettre_par_colonne(colonne):
    meilleur_score = float("inf")
    meilleure_lettre = 'A'
    for shift in range(26):
        texte_shift = ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in colonne)
        score = chi_square_score(texte_shift)
        if score < meilleur_score:
            meilleur_score = score
            meilleure_lettre = chr(ord('A') + shift)
    return meilleure_lettre

def cle_initiale_chi2(texte_chiffre, longueur):
    texte_chiffre = ''.join([c for c in texte_chiffre.upper() if c.isalpha()])
    colonnes = ['' for _ in range(longueur)]
    for i, c in enumerate(texte_chiffre):
        colonnes[i % longueur] += c
    return ''.join(meilleure_lettre_par_colonne(col) for col in colonnes)

# ------------------------------
# HILL-CLIMBING POUR AFFINER LA CLE
# ------------------------------
def hill_climb_affinage_sa(texte_chiffre, cle_init,
                           iterations=5000, restarts=8,
                           start_temp=1.0, end_temp=0.001, verbose=False):
    """
    Simulated annealing avec plusieurs types de mutation.
    Retourne (best_key, best_text, best_score).
    """
    letters = string.ascii_uppercase
    best_key = cle_init
    best_text = dechiffrement_vigenere(texte_chiffre, best_key)
    best_score = combined_score_improved(best_text)

    rng = random.Random()  # local RNG for reproducibility if needed

    start_time = time.time()
    for r in range(restarts):
        # initialisation (pour diversité : petite perturbation de cle_init)
        if r == 0:
            current_key = cle_init
        else:
            current_key = ''.join(rng.choice(letters) if rng.random() < 0.15 else cle_init[i]
                                   for i in range(len(cle_init)))
        current_text = dechiffrement_vigenere(texte_chiffre, current_key)
        current_score = combined_score_improved(current_text)

        temp = start_temp
        # linear cooling
        for it in range(iterations):
            # temperature schedule
            frac = it / max(1, iterations - 1)
            temp = start_temp * (1 - frac) + end_temp * frac

            # choose mutation type
            m = rng.random()
            if m < 0.45:
                # mutation: remplacer une lettre
                pos = rng.randrange(len(current_key))
                new_letter = rng.choice(letters)
                candidate_key = current_key[:pos] + new_letter + current_key[pos+1:]
            elif m < 0.75:
                # permutation de deux positions
                a, b = rng.randrange(len(current_key)), rng.randrange(len(current_key))
                if a == b:
                    candidate_key = current_key
                else:
                    lst = list(current_key)
                    lst[a], lst[b] = lst[b], lst[a]
                    candidate_key = ''.join(lst)
            else:
                # shift cyclique de la clé (utile si clé est périodiquement décalée)
                shift = rng.choice([-1, 1, 2, -2])
                candidate_key = ''.join(current_key[(i - shift) % len(current_key)] for i in range(len(current_key)))

            candidate_text = dechiffrement_vigenere(texte_chiffre, candidate_key)
            candidate_score = combined_score_improved(candidate_text)

            # acceptance criterion (Metropolis)
            delta = candidate_score - current_score
            if delta > 0 or math.exp(delta / max(1e-12, temp)) > rng.random():
                current_key, current_text, current_score = candidate_key, candidate_text, candidate_score
                # update global best
                if current_score > best_score:
                    best_key, best_text, best_score = current_key, current_text, current_score

            # optional verbose small log
            if verbose and (it % 1000 == 0) and it > 0:
                print(f"[restart {r}] it={it}, temp={temp:.5f}, cur_score={current_score:.2f}, best_score={best_score:.2f}")

        # end of this restart
    if verbose:
        print("SA elapsed:", time.time() - start_time)
    return best_key, best_text, best_score

# ------------------------------
# ASSEMBLAGE : casser_vigenere_precis
# ------------------------------
def casser_vigenere_precis(texte_chiffre, max_longueur=12):
    # conservation du texte original (avec espaces/punctuation) pour affichage final
    texte_orig = texte_chiffre
    # on travaille sur la version alpha pour partition/IC mais dechiffrement garde la ponctuation si on utilise la fonction
    # ici nos fonctions dechiffrement_vigenere retirent ponctuation automatiquement lors du mapping alpha, donc on fournit le texte original
    candidats = candidats_longueurs(texte_chiffre, max_long=max_longueur, top_k=5)
    meilleur = (None, None, float("-inf"))  # key, text, score

    for L in candidats:
        cle_init = cle_initiale_chi2(texte_chiffre, L)
        cle_affinee, texte_affine, score = hill_climb_affinage_sa(texte_chiffre, cle_init,
                                                               iterations=1500, restarts=6)
        if score > meilleur[2]:
            meilleur = (cle_affinee, texte_affine, score)

    # si rien de convaincant, fallback sur les petites longueurs directes
    if meilleur[0] is None:
        for L in range(1, min(6, max_longueur + 1)):
            cle_init = cle_initiale_chi2(texte_chiffre, L)
            cle_affinee, texte_affine, score = hill_climb_affinage_sa(texte_chiffre, cle_init,
                                                                   iterations=1000, restarts=3)
            if score > meilleur[2]:
                meilleur = (cle_affinee, texte_affine, score)

    return meilleur[0], meilleur[1]

# ------------------------------
# INTERFACE PRINCIPALE (1..4)
# ------------------------------
def main():
    print("Choisissez un mode :")
    print("1. Chiffrement (texte clair + clé)")
    print("2. Déchiffrement (texte chiffré + clé)")
    print("3. Casser le texte (méthode rapide chi², 1..10)")
    print("4. Casser le texte (méthode précise : IC + chi² init + hill-climbing)")
    choix = input("Votre choix (1, 2, 3 ou 4) : ").strip()

    if choix == "1":
        texte = input("Entrez le texte à chiffrer : ").strip()
        cle = input("Entrez la clé : ").strip()
        if not texte or not cle:
            print("Texte et clé ne peuvent pas être vides.")
            return
        print("\nTexte chiffré :\n", chiffrement_vigenere(texte, cle))

    elif choix == "2":
        texte_chiffre = input("Entrez le texte chiffré : ").strip()
        cle = input("Entrez la clé : ").strip()
        if not texte_chiffre or not cle:
            print("Texte chiffré et clé ne peuvent pas être vides.")
            return
        print("\nTexte déchiffré :\n", dechiffrement_vigenere(texte_chiffre, cle))

    elif choix == "3":
        from math import inf
        # version rapide (comme fournie précédemment)
        def meilleure_lettre(colonne):
            meilleur_score = inf
            meilleure_lettre = 'A'
            for shift in range(26):
                texte_shift = ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in colonne)
                score = chi_square_score(texte_shift)
                if score < meilleur_score:
                    meilleur_score = score
                    meilleure_lettre = chr(ord('A') + shift)
            return meilleure_lettre

        def casser_vigenere_rapide(texte_chiffre, max_longueur=10):
            texte_chiffre_alpha = ''.join([c for c in texte_chiffre.upper() if c.isalpha()])
            meilleur_score_global = float("inf")
            meilleure_cle = ""
            meilleur_texte = ""
            for longueur_cle in range(1, max_longueur + 1):
                colonnes = ['' for _ in range(longueur_cle)]
                for i, c in enumerate(texte_chiffre_alpha):
                    colonnes[i % longueur_cle] += c
                cle_candidate = ''.join(meilleure_lettre(col) for col in colonnes)
                texte_dechiffre = dechiffrement_vigenere(texte_chiffre, cle_candidate)
                score = chi_square_score(texte_dechiffre)
                if score < meilleur_score_global:
                    meilleur_score_global = score
                    meilleure_cle = cle_candidate
                    meilleur_texte = texte_dechiffre
            return meilleure_cle, meilleur_texte

        texte_chiffre = input("Entrez le texte chiffré à casser : ").strip()
        if not texte_chiffre:
            print("Texte chiffré ne peut pas être vide.")
            return
        print("\nTentative de cassage (rapide) en cours...")
        cle, texte = casser_vigenere_rapide(texte_chiffre)
        print("\n✅ Clé probable :", cle)
        print("\nTexte déchiffré (approx.) :\n", texte)

    elif choix == "4":
        texte_chiffre = input("Entrez le texte chiffré à casser : ").strip()
        if not texte_chiffre:
            print("Texte chiffré ne peut pas être vide.")
            return
        print("\nTentative de cassage (précise) en cours... cela peut prendre quelques secondes.")
        cle, texte = casser_vigenere_precis(texte_chiffre, max_longueur=12)
        print("\n✅ Clé probable :", cle)
        print("\nTexte déchiffré (approx., affiné) :\n", texte)

    else:
        print("Choix invalide.")

if __name__ == "__main__":
    main()