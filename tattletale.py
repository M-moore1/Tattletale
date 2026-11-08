from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

sim = AerSimulator()

def alice_prepare(bit: int, basis: int) -> QuantumCircuit:
    """Encode one bit in basis 0 (Z) or basis 1 (X)."""
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)       # |0> -> |1>
    if basis == 1:
        qc.h(0)       # rotate into the X basis
    return qc

def bob_measure(qc: QuantumCircuit, basis: int) -> int:
    """Measure one qubit in basis 0 (Z) or basis 1 (X)."""
    qc = qc.copy()
    if basis == 1:
        qc.h(0)       # rotate back before measuring
    qc.measure(0, 0)
    result = sim.run(qc, shots=1, memory=True).result()
    return int(result.get_memory()[0])

if __name__ == "__main__":
    # Matching bases: Bob should always recover Alice's bit
    for bit in (0, 1):
        for basis in (0, 1):
            got = bob_measure(alice_prepare(bit, basis), basis)
            print(f"bit={bit} basis={basis} -> Bob got {got}")

    # Mismatched bases: Bob's result should be a coin flip
    results = [bob_measure(alice_prepare(1, 0), 1) for _ in range(200)]
    print("mismatched bases, fraction of 1s:", sum(results) / len(results))