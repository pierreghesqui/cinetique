import numpy as np
import os
from tkinter import Tk, filedialog
import csv
import matplotlib.pyplot as plt

def Donnees_CSV_Toutes_Colonnes(path):
    """
    Ouvre une boîte de dialogue pour sélectionner un fichier CSV/TXT.
    Extrait toutes les colonnes du fichier, en considérant la première ligne comme les titres.
    Convertit les données en nombres (float) et les organise en une liste de tableaux NumPy.
    Gère les virgules comme séparateurs décimaux et essaie plusieurs encodages.

    Retourne :
        list: Une liste de tableaux NumPy. Chaque tableau correspond à une colonne du CSV.
              Si le fichier a 3 colonnes, la fonction retournera [colonne1_np_array, colonne2_np_array, colonne3_np_array].
        None: Si l'extraction échoue ou est annulée.
    """
    '''
    root = Tk()
    root.withdraw()  # Cache la fenêtre principale de Tkinter

    file_path = filedialog.askopenfilename(
        title="Ouvrir le fichier de Données (CSV ou TXT)",
        initialdir=os.getcwd(),
        filetypes=[("Fichiers CSV/TXT", "*.csv *.txt"), ("Tous les fichiers", "*.*")]
    )
   
    '''
    file_path = path
    if not file_path:
        print("Aucun fichier sélectionné. Annulation de l'extraction.")
        return None
    
    all_extracted_columns_as_lists = [] # Va contenir les données temporairement sous forme de listes Python
    header = [] # Pour stocker les titres des colonnes
    delimiter = ',' # Délimiteur par défaut, sera détecté
    encoding = None # Variable pour stocker l'encodage qui fonctionne

    try:
        # --- Étape 1: Détection du délimiteur et lecture de l'en-tête ---
        # On essaie plusieurs encodages courants pour maximiser les chances d'ouvrir le fichier.
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(file_path, mode='r', newline='', encoding=enc) as file:
                    sample_line = file.readline()
                    # On devine le délimiteur le plus probable en regardant la première ligne.
                    if ';' in sample_line: # Le point-virgule est fréquent dans les CSV français
                        delimiter = ';'
                    elif ',' in sample_line:
                        delimiter = ','
                    elif '\t' in sample_line:
                        delimiter = '\t'
                    else:
                        # Corrected line for Python 3.4.5
                        print("Avertissement : Délimiteur incertain dans '{}'. Essai par défaut avec virgule.".format(os.path.basename(file_path)))
                        delimiter = ','

                    file.seek(0) # On rembobine le fichier au début pour le relire
                    reader = csv.reader(file, delimiter=delimiter)
                    header = next(reader) # La toute première ligne est l'en-tête (les titres de colonnes)
                    encoding = enc # On stocke l'encodage qui a fonctionné
                    break # Si on a réussi à lire l'en-tête, on sort de la boucle d'encodage
            except UnicodeDecodeError:
                continue # Si cet encodage ne marche pas, on essaie le suivant
            except StopIteration:
                print("Le fichier est vide ou n'a pas de première ligne (en-tête).")
                return None # On arrête si le fichier est vide ou sans en-tête

        if not header:
            print("Erreur : Impossible de lire l'en-tête du fichier avec les encodages essayés.")
            return None

        # print(f"Colonnes détectées (en-têtes) : {header}") # Utile pour le débogage

        # --- Étape 2: Initialisation des listes pour chaque colonne ---
        # Pour chaque colonne trouvée dans l'en-tête, on crée une liste vide.
        # all_extracted_columns_as_lists sera une liste de ces listes vides.
        for _ in header: # On utilise '_' car on n'a pas besoin du nom de l'en-tête ici, juste de savoir combien il y a de colonnes
            all_extracted_columns_as_lists.append([])

        # --- Étape 3: Lecture des données ligne par ligne et conversion en nombres ---
        # On rouvre le fichier car 'csv.reader' ne permet pas de revenir en arrière facilement.
        # On utilise le même encodage et délimiteur que ceux qui ont fonctionné pour l'en-tête.
        with open(file_path, mode='r', newline='', encoding=encoding) as file:
            reader = csv.reader(file, delimiter=delimiter)
            next(reader) # On saute la première ligne (l'en-tête) car on l'a déjà traitée.

            for row in reader: # Pour chaque ligne de données dans le fichier
                for col_idx in range(len(header)): # On parcourt les colonnes (de 0 à nombre de colonnes - 1)
                    if col_idx < len(row): # On vérifie que la ligne a bien une valeur pour cette colonne
                        value_str = row[col_idx].strip().replace(",", ".") # On enlève les espaces et on remplace les virgules par des points pour les décimales
                        try:
                            # On essaie de convertir la valeur en nombre à virgule (float)
                            all_extracted_columns_as_lists[col_idx].append(float(value_str))
                        except ValueError:
                            # Si la conversion échoue (par exemple, c'est du texte ou c'est vide), on met un "Not a Number" (NaN)
                            all_extracted_columns_as_lists[col_idx].append(np.nan)
                    else:
                        # Si la ligne est trop courte et qu'il manque des données pour une colonne, on met aussi un NaN
                        all_extracted_columns_as_lists[col_idx].append(np.nan)

    except FileNotFoundError:
        print("Erreur : Le fichier '{}' n'a pas été trouvé.".format(file_path))
        return None
    except Exception as e:
        print("Une erreur inattendue est survenue lors de l'extraction des données : {}".format(e))
        return None

    # --- Étape 4: Conversion finale des listes en tableaux NumPy ---
    # Maintenant que toutes les données sont lues et converties en float (ou NaN),
    # on transforme chaque liste en un tableau NumPy. C'est ce qui te permet de faire facilement des calculs comme la division.
    final_np_arrays = []
    for col_list in all_extracted_columns_as_lists:
        final_np_arrays.append(np.array(col_list))

    print("\nExtraction de toutes les données terminée.")
    print("Nombre de colonnes extraites : {}".format(len(final_np_arrays)))
    print("Aperçu des premières 5 valeurs de chaque colonne :")
    for i, data_array in enumerate(final_np_arrays):
        print("  Colonne {} (En-tête: '{}'): {}...".format(i+1, header[i].strip(), data_array[:5]))

    return final_np_arrays

# --- Section de test (s'exécute seulement si tu lances ce fichier directement) ---
if __name__ == "__main__":
    print("--- Test de la fonction Donnees_CSV_Toutes_Colonnes ---")
    list_of_data_arrays = Donnees_CSV_Toutes_Colonnes()

    if list_of_data_arrays:
        print("\nLa fonction a retourné une liste de tableaux NumPy.")
        print("Le premier élément ({}) correspond à la première colonne de ton CSV.".format(list_of_data_arrays[0].shape))
        print("Le deuxième élément ({}) correspond à la deuxième colonne, etc.".format(list_of_data_arrays[1].shape))

        # Exemple d'utilisation si tu as au moins 2 colonnes (temps et absorbance)
        if len(list_of_data_arrays) >= 2:
            temps_colonne = list_of_data_arrays[0] # La première colonne est le temps
            absorbance_colonne = list_of_data_arrays[1] # La deuxième colonne est l'absorbance

            print("\nPremières valeurs de la colonne Temps : {}".format(temps_colonne[:5]))
            print("Premières valeurs de la colonne Absorbance : {}".format(absorbance_colonne[:5]))

            # Tu peux maintenant facilement diviser une colonne par un scalaire !
            facteur_bidon = 10.0
            nouvelle_colonne = absorbance_colonne / facteur_bidon
            print("\nAbsorbance divisée par {} (premières 5 valeurs) : {}".format(facteur_bidon, nouvelle_colonne[:5]))

            # Pour un tracé simple (si tu as au moins 2 colonnes)
            plt.figure(figsize=(8, 5))
            plt.plot(temps_colonne, absorbance_colonne, 'o-', label='Absorbance vs Temps')
            plt.xlabel("Temps")
            plt.ylabel("Absorbance")
            plt.title("Aperçu des Données Extraites")
            plt.grid(True)
            plt.legend()
            plt.show()

        else:
            print("Moins de 2 colonnes ont été extraites, pas assez pour un exemple de tracé simple.")
    else:
        print("La fonction n'a retourné aucune donnée.")