from bio.fasta_organism import FastaOrganism


def read_fasta(file_path):
    organisms = []

    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            if line[0] == ">":
                organism_id, name = line[1:].rstrip().split("|")
                organisms.append({
                    "id": organism_id.strip(),
                    "name": name.strip(),
                    "sequence": ""
                })
            else:
                organisms[-1]["sequence"] += line.rstrip()

    return [FastaOrganism(
        id=organism["id"],
        name=organism["name"],
        sequence=organism["sequence"],
    ) for organism in organisms]
