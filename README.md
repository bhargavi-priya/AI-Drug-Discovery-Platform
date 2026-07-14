# AI Drug Discovery Platform

A Flask-based Bioinformatics web application for analyzing protein and drug files.

## Features

- Upload Protein (.fasta/.pdb)
- Upload Drug (.sdf/.mol/.mol2/.pdb)
- Protein sequence analysis
- Amino acid composition chart
- Drug property calculation using RDKit
- Molecular weight
- LogP
- TPSA
- Hydrogen bond donors
- Hydrogen bond acceptors
- Lipinski Rule of Five evaluation
- 2D chemical structure visualization
- Download PDF analysis report

## Technologies Used

- Python
- Flask
- RDKit
- Biopython
- Matplotlib
- ReportLab
- HTML
- CSS

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

## Project Structure

```
AI-Drug-Discovery-Platform/
│
├── app.py
├── pdf_report.py
├── requirements.txt
├── README.md
├── uploads/
├── static/
│   ├── css/
│   └── images/
├── templates/
│   ├── index.html
│   ├── virtual_screening.html
│   ├── drug_library.html
│   ├── about.html
│   └── results.html
└── sample_data/
```

## Author

Bhargavi Priya
B.Tech Bioinformatics
VFSTR University