from bio.sequence import Sequence


class FastaOrganism:

    def __init__(self, id, name, sequence):
        self.id = id
        self.name = name
        self.sequence = Sequence(sequence)

    def __repr__(self):
        return f'FastaOrganism(id="{self.id}", name="{self.name}")'
