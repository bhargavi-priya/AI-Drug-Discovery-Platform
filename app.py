from flask import Flask, render_template, request, send_file
from Bio import SeqIO
from collections import Counter
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Descriptors
from pdf_report import generate_pdf
from rdkit.Chem import Draw
import os

app = Flask(__name__)
latest_report = {}

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create required folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static/images", exist_ok=True)

ALLOWED_PROTEIN_EXTENSIONS = {"pdb", "fasta"}
ALLOWED_DRUG_EXTENSIONS = {"sdf", "mol", "mol2", "pdb"}


def allowed_file(filename, allowed_extensions):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/virtual_screening")
def virtual_screening():
    return render_template("virtual_screening.html")


@app.route("/drug_library")
def drug_library():
    return render_template("drug_library.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/predict", methods=["POST"])
def predict():

    protein = request.files["protein_file"]
    drug = request.files["drug_file"]

    if not allowed_file(protein.filename, ALLOWED_PROTEIN_EXTENSIONS):
        return "<h2>❌ Invalid Protein File (.pdb or .fasta only)</h2>"

    if not allowed_file(drug.filename, ALLOWED_DRUG_EXTENSIONS):
        return "<h2>❌ Invalid Drug File (.sdf, .mol, .mol2 or .pdb only)</h2>"

    protein_path = os.path.join(app.config["UPLOAD_FOLDER"], protein.filename)
    drug_path = os.path.join(app.config["UPLOAD_FOLDER"], drug.filename)

    protein.save(protein_path)
    drug.save(drug_path)

    # ---------------- Protein Analysis ----------------

    protein_id = "Not Available"
    sequence_length = "Not Available"
    sequence_preview = "Not Available"

    amino_acid_counts = {}
    chart_image = None

    if protein.filename.lower().endswith(".fasta"):

        record = SeqIO.read(protein_path, "fasta")

        protein_id = record.id

        sequence = str(record.seq)

        sequence_length = len(sequence)

        sequence_preview = sequence[:50]

        amino_order = list("ACDEFGHIKLMNPQRSTVWY")

        amino_acid_counts = Counter(sequence)

        counts = [amino_acid_counts.get(aa, 0) for aa in amino_order]

        plt.figure(figsize=(10, 5))
        plt.bar(amino_order, counts)
        plt.title("Amino Acid Composition")
        plt.xlabel("Amino Acid")
        plt.ylabel("Count")
        plt.tight_layout()

        chart_path = os.path.join(
            "static",
            "images",
            "amino_acid_chart.png"
        )

        plt.savefig(chart_path)
        plt.close()

        chart_image = "images/amino_acid_chart.png"

    # ---------------- Drug Analysis ----------------

    molecular_weight = "Not Available"
    logp = "Not Available"
    tpsa = "Not Available"
    h_donors = "Not Available"
    h_acceptors = "Not Available"

    molecule_image = None
    lipinski_result = "Not Available"
    lipinski_score = 0

    if drug.filename.lower().endswith(".sdf"):

        supplier = Chem.SDMolSupplier(drug_path)
        mol = supplier[0]

        if mol is not None:

            molecular_weight = round(Descriptors.MolWt(mol), 2)
            logp = round(Descriptors.MolLogP(mol), 2)
            tpsa = round(Descriptors.TPSA(mol), 2)
            h_donors = Descriptors.NumHDonors(mol)
            h_acceptors = Descriptors.NumHAcceptors(mol)

            # Generate 2D structure image
            image_path = os.path.join(
                "static",
                "images",
                "molecule.png"
            )

            Draw.MolToFile(mol, image_path)

            molecule_image = "images/molecule.png"

            # ---------------- Lipinski Score ----------------

            if molecular_weight <= 500:
                lipinski_score += 1

            if logp <= 5:
                lipinski_score += 1

            if h_donors <= 5:
                lipinski_score += 1

            if h_acceptors <= 10:
                lipinski_score += 1

            if lipinski_score == 4:
                lipinski_result = "Excellent Drug Candidate ✅"

            elif lipinski_score == 3:
                lipinski_result = "Good Drug Candidate 🟢"

            elif lipinski_score == 2:
                lipinski_result = "Moderate Drug Candidate 🟡"

            else:
                lipinski_result = "Poor Drug Candidate 🔴"

    global latest_report

    latest_report = {
        "protein_name": protein.filename,
        "protein_id": protein_id,
        "sequence_length": sequence_length,
        "drug_name": drug.filename,
        "molecular_weight": molecular_weight,
        "logp": logp,
        "tpsa": tpsa,
        "h_donors": h_donors,
        "h_acceptors": h_acceptors,
        "lipinski_score": lipinski_score,
        "lipinski_result": lipinski_result
    }

            
   
    return render_template(
        "results.html",
        protein_name=protein.filename,
        drug_name=drug.filename,
        protein_id=protein_id,
        sequence_length=sequence_length,
        sequence_preview=sequence_preview,
        amino_acid_counts=amino_acid_counts,
        chart_image=chart_image,
        molecular_weight=molecular_weight,
        logp=logp,
        tpsa=tpsa,
        h_donors=h_donors,
        h_acceptors=h_acceptors,
        molecule_image=molecule_image,
        lipinski_result=lipinski_result,
        lipinski_score=lipinski_score
    )
@app.route("/download_report")
def download_report():

    pdf_file = "AI_Drug_Discovery_Report.pdf"

    generate_pdf(
        pdf_file,
        latest_report["protein_name"],
        latest_report["protein_id"],
        latest_report["sequence_length"],
        latest_report["drug_name"],
        latest_report["molecular_weight"],
        latest_report["logp"],
        latest_report["tpsa"],
        latest_report["h_donors"],
        latest_report["h_acceptors"],
        latest_report["lipinski_score"],
        latest_report["lipinski_result"]
    )

    return send_file(
        pdf_file,
        as_attachment=True
    )
    
   


if __name__ == "__main__":
    app.run(debug=True)