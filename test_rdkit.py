from rdkit import Chem
from rdkit.Chem import Descriptors

file_path = "uploads/Structure2D_COMPOUND_CID_2244.sdf"

supplier = Chem.SDMolSupplier(file_path)
mol = supplier[0]

if mol is None:
    print("❌ Could not read molecule.")
else:
    print("✅ Molecule Loaded Successfully")
    print("Molecular Weight:", Descriptors.MolWt(mol))
    print("LogP:", Descriptors.MolLogP(mol))
    print("TPSA:", Descriptors.TPSA(mol))
    print("H-Bond Donors:", Descriptors.NumHDonors(mol))
    print("H-Bond Acceptors:", Descriptors.NumHAcceptors(mol))