import cirq
import numpy as np
import matplotlib.pyplot as plt
import random
import os

# 1. 5 Qubit oluştur
qubits = [cirq.LineQubit(i) for i in range(5)]

# 2. Rastgele kapı setleri tanımla
single_qubit_gates = [cirq.X, cirq.Y, cirq.Z, cirq.H, cirq.rx, cirq.ry, cirq.rz]
two_qubit_gates = [cirq.CNOT, cirq.CZ, cirq.ISWAP]

# 3. Devreyi inşa et
circuit = cirq.Circuit()

# Her qubit için rastgele 2-3 gate uygula
for q in qubits:
    for _ in range(random.randint(2, 3)):
        gate = random.choice(single_qubit_gates)
        if gate in [cirq.rx, cirq.ry, cirq.rz]:
            angle = np.random.uniform(0, np.pi)
            circuit.append(gate(angle).on(q))
        else:
            circuit.append(gate.on(q))

# Rastgele 5 tane çift-qubit kapısı ekle
for _ in range(5):
    q1, q2 = random.sample(qubits, 2)
    gate = random.choice(two_qubit_gates)
    circuit.append(gate(q1, q2))

# Tüm qubit'leri ölçelim
circuit.append(cirq.measure(*qubits, key='result'))

# 4. Devreyi göster
print("Başlangıç Quantum Devresi:")
print(circuit)

# 5. Simülasyon
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)
histogram = result.histogram(key='result')

# 6. Sonuçları görelim
print("\nÖlçüm Sonuçları (bit dizisi -> frekans):")
for bitstring, count in histogram.items():
    bits = format(bitstring, '05b')
    print(f"{bits} -> {count} kez")

# 7. Histogram çizelim
labels = [format(x, '05b') for x in histogram.keys()]
frequencies = list(histogram.values())

plt.figure(figsize=(12, 6))
plt.bar(labels, frequencies)
plt.xlabel('Bit Dizisi (5 Qubit Ölçüm)')
plt.ylabel('Frekans')
plt.title('Başlangıç Quantum Ölçüm Dağılımı')
plt.xticks(rotation=90)
plt.grid()
plt.show()

# 8. Ölçüm sonuçlarını döndürelim (sonraki aşama için)
measurement_summary = "\n".join(f"{format(k, '05b')} -> {v} kez" for k, v in histogram.items())
