# 2) Kütüphaneleri import edelim
import cirq
import numpy as np
import matplotlib.pyplot as plt
from iointel import Agent, Workflow
import os

os.environ["IOINTEL_API_KEY"] = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImU0MTNlYTcwLTc2ZDMtNGViYi05ZjRlLTU0OTJkYzhlZjM5MCIsImV4cCI6NDg5OTI2MjQ5Nn0.ka9Nog3-HHDxowTRRpns3Y3O5y_K4z-GxZXUxlc-qeY4j__ZD8hy0ufDzh4Ykj1BGyqoNZ0Ho0IsPPpxSPGNbg"

# 4) Quantum devresi oluşturup ölçüm yapalım
qubits = [cirq.LineQubit(i) for i in range(3)]

circuit = cirq.Circuit()
circuit.append([cirq.H(q) for q in qubits])
circuit.append(cirq.CNOT(qubits[0], qubits[1]))
circuit.append(cirq.CNOT(qubits[1], qubits[2]))
circuit.append(cirq.measure(*qubits, key='result'))

simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)
histogram = result.histogram(key='result')

# Histogramı okunabilir hale getirelim
measurement_summary = "\n".join(
    f"{format(bitstring, '03b')} -> {count} kez"
    for bitstring, count in histogram.items()
)

print("Quantum Ölçüm Özeti:\n", measurement_summary)

# 5) IO.NET Agent tanımlayalım
agent = Agent(
    name="Quantum Analyzer Agent",
    instructions="You are a quantum computing assistant. Analyze the provided quantum measurement results and find patterns.",
    model="meta-llama/Llama-3.3-70B-Instruct",
    api_key=os.environ["IOINTEL_API_KEY"],
    base_url="https://api.intelligence.io.solutions/api/v1"
)

# 6) Workflow tanımlayalım
workflow = Workflow(
    text=f"The following are quantum circuit measurement results:\n{measurement_summary}",
    client_mode=False
)

# 7) Agent'a görev verelim
results = workflow.custom(
    name="quantum-analysis-task",
    objective="Analyze quantum measurement results and suggest possible interpretations.",
    instructions="Interpret the results and suggest why certain bitstrings occur more frequently.",
    agents=[agent]
).run_tasks()

# 8) Sonucu yazdıralım
print("\nAgent Analiz Sonucu:\n", results)
