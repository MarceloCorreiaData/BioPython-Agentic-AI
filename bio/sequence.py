class Sequence:

    def __init__(self, sequence):
        self.sequence = sequence

    def __repr__(self):
        return f'Sequence("{self.sequence}")'

    def __iter__(self):
        return iter(self.sequence)

    def __str__(self):
        return self.sequence

    def __len__(self):
        return len(self.sequence)

    def __eq__(self, other_sequence):
        return str(self) == str(other_sequence)

    def __getitem__(self, index):
        return self.sequence.__getitem__(index)

    def complement(self):
        complement_map = {"A": "T", "T": "A", "C": "G", "G": "C"}
        new = "".join(complement_map.get(base, base) for base in self.sequence)
        return Sequence(new)

    def reverse_complement(self):
        return Sequence(self.complement().sequence[::-1])

    def transcribe(self):
        return Sequence(self.sequence.replace("T", "U"))

    def translate(self, stop=False):
        from bio.constants import DNA_TO_AMINO_ACID, DNA_STOP_CODONS

        protein = ""
        for i in range(0, len(self.sequence) - 2, 3):
            codon = self.sequence[i:i+3]
            if codon in DNA_STOP_CODONS:
                if stop:
                    break
                protein += "*"
            elif codon in DNA_TO_AMINO_ACID:
                protein += DNA_TO_AMINO_ACID[codon]
            else:
                protein += "X"
        return protein

    def calculate_percentage(self, bases):
        count = sum(1 for base in self.sequence if base in bases)
        return count / len(self.sequence)
