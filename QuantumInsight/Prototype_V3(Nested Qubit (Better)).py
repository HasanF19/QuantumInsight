#bu dosyanın aslında adı nested_quantum_simulation.py olacaktı ama düzen karışmasın aldığımız 5 qubitli 
#sonuçlar sıfıra çok yakındı şimdi nested yapıcaz ve sonuçlar daha ağır dolanık (GHZ-Like yapılı olacak)
import cirq
import numpy as np
import matplotlib.pyplot as plt
import random

# 5 Qubit oluştur
qubits = [cirq.LineQubit(i) for i in range(5)]

# Başta tüm qubit'lere Hadamard
nested_circuit = cirq.Circuit()
nested_circuit.append(cirq.H.on_each(*qubits))

# Dolanıklık kur (GHZ gibi)
for i in range(4):
    nested_circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))

# Her qubit'e random RX ve RY rotasyonu
for q in qubits:
    angle_x = np.random.uniform(0, np.pi)
    angle_y = np.random.uniform(0, np.pi)
    nested_circuit.append(cirq.rx(angle_x).on(q))
    nested_circuit.append(cirq.ry(angle_y).on(q))

# Ölçüm ekle
nested_circuit.append(cirq.measure(*qubits, key='nested_result'))

# Simülatör
simulator = cirq.Simulator()
nested_result = simulator.run(nested_circuit, repetitions=1000)
nested_histogram = nested_result.histogram(key='nested_result')

# Devreyi göster
print("\nNested (Dinamik) Quantum Devre:")
print(nested_circuit)

print("\nNested Ölçüm Sonuçları:")
for bitstring, count in nested_histogram.items():
    bits = format(bitstring, '05b')
    print(f"{bits} -> {count} kez")

# Ölçüm sonuçlarını plot edelim
labels_nested = [format(x, '05b') for x in nested_histogram.keys()]
frequencies_nested = list(nested_histogram.values())

plt.figure(figsize=(12, 6))
plt.bar(labels_nested, frequencies_nested)
plt.xlabel('Bit Dizisi (Nested Ölçüm)')
plt.ylabel('Frekans')
plt.title('Nested Quantum Ölçüm Dağılımı')
plt.xticks(rotation=90)
plt.grid()
plt.show()

# Ölçüm özetini hazırlayalım (Multi-Agent için kullanacağız)
nested_measurement_summary = "\n".join(f"{format(k, '05b')} -> {v} kez" for k, v in nested_histogram.items())
