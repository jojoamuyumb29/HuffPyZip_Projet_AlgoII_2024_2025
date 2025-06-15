# HuffPyZip

**HuffPyZip** est un logiciel de compression et décompression de fichiers utilisant l’algorithme de Huffman, développé dans le cadre d’un projet universitaire. Il dispose d’une interface graphique moderne inspirée du design macOS.

---

## Fonctionnalités principales

- Compression de fichiers `.txt`, `.doc`, `.docx`, `.xlsx`, `.pdf`, `.xml`
- Décompression des fichiers compressés par HuffPyZip
- Interface moderne (CustomTkinter) avec :
  - Bouton de sélection de fichier
  - Champ d’affichage du fichier sélectionné
  - Barre de progression
  - Journal des opérations
- Sauvegarde automatique des fichiers compressés/décompressés

---

## Installation

1. Assurez-vous d’avoir **Python 3.10+** installé.
2. Installez les dépendances nécessaires :
```bash
pip install customtkinter
```
3. Lancez le logiciel :
```bash
python gui_updated.py
```

---

## Structure des fichiers

- `gui_updated.py` : Interface graphique du logiciel.
- `huffman_binary.py` : Module de compression/décompression utilisant l’algorithme de Huffman (lecture/écriture binaire).
- `output/` : Dossier de sortie pour les fichiers traités.

---

## Compilation en EXE

Pour créer un exécutable Windows :
```bash
pyinstaller --onefile --noconsole gui_updated.py
```

---

## Auteurs

Projet réalisé par le **Groupe 3** dans le cadre d’un cours de programmation à l’université.