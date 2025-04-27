# nested_quantum_multiagent_pro_final.py
import os
import json
import logging
import random
import argparse
import cirq
import numpy as np
import matplotlib.pyplot as plt
from iointel import Agent, Workflow

# API anahtarı
os.environ["IOINTEL_API_KEY"] = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImU0MTNlYTcwLTc2ZDMtNGViYi05ZjRlLTU0OTJkYzhlZjM5MCIsImV4cCI6NDg5OTI2MjQ5Nn0.ka9Nog3-HHDxowTRRpns3Y3O5y_K4z-GxZXUxlc-qeY4j__ZD8hy0ufDzh4Ykj1BGyqoNZ0Ho0IsPPpxSPGNbg"
# --------------------------------------------------
# Proje: Nested Quantum Simülasyon + Multi-Agent Analiz+ Kullanıcı dostu bir arayüz
# Dosya: Simulation_Interface.py
# Yazar: Hasan Fatih Öztürk
# Tarih: 2025-04-26
# --------------------------------------------------
# Komut satırı argümanları
type_parser = argparse.ArgumentParser(description="Nested Quantum Simülasyon ve Multi-Agent Analiz için parametreler")
type_parser.add_argument("--num_qubits", type=int, default=5, help="Kullanılacak qubit sayısı (2-10 arası önerilir)")
type_parser.add_argument("--repetitions", type=int, default=1000, help="Simülasyon tekrar sayısı")
args = type_parser.parse_args()

# Logging kurulumu
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def save_text(filename: str, text: str):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"Metin dosyası kaydedildi: {filename}")
    except Exception as e:
        logger.error(f"Dosya kaydederken hata: {e}")


def save_json(filename: str, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"JSON dosyası kaydedildi: {filename}")
    except Exception as e:
        logger.error(f"JSON kaydederken hata: {e}")


def setup_qubits(n: int):
    logger.debug(f"{n} qubit olusturuluyor...")
    return [cirq.LineQubit(i) for i in range(n)]


def build_initial_circuit(qubits):
    logger.debug("Initial circuit olusturuluyor...")
    circuit = cirq.Circuit()
    single = [cirq.X, cirq.Y, cirq.Z, cirq.H, cirq.rx, cirq.ry, cirq.rz]
    two = [cirq.CNOT, cirq.CZ, cirq.ISWAP]
    for q in qubits:
        ops_count = random.randint(2, 3)
        for _ in range(ops_count):
            gate = random.choice(single)
            if gate in [cirq.rx, cirq.ry, cirq.rz]:
                angle = np.random.uniform(0, np.pi)
                circuit.append(gate(angle).on(q))
            else:
                circuit.append(gate.on(q))
    for _ in range(5):
        q1, q2 = random.sample(qubits, 2)
        circuit.append(random.choice(two)(q1, q2))
    circuit.append(cirq.measure(*qubits, key='result'))
    logger.debug("Initial circuit hazir.")
    return circuit


def measure_circuit(circuit, simulator, repetitions=1000, key='result'):
    logger.info(f"Devre simule ediliyor ({repetitions} tekrar)")
    result = simulator.run(circuit, repetitions=repetitions)
    hist = result.histogram(key=key)
    logger.info("Simulasyon tamamlandi.")
    return hist


def format_histogram(hist):
    lines = []
    bitlen = len(bin(next(iter(hist.keys())))) - 2
    for bits, count in hist.items():
        bstr = format(bits, f'0{bitlen}b')
        lines.append(f"{bstr} -> {count} kez")
    return "\n".join(lines)


def build_nested_circuit(qubits):
    logger.debug("Nested circuit olusturuluyor...")
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(*qubits))
    for i in range(len(qubits)-1):
        circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
    for q in qubits:
        circuit.append(cirq.rx(np.random.uniform(0, np.pi)).on(q))
        circuit.append(cirq.ry(np.random.uniform(0, np.pi)).on(q))
    circuit.append(cirq.measure(*qubits, key='nested_result'))
    logger.debug("Nested circuit hazir.")
    return circuit


def plot_histogram(hist, title, filename=None):
    labels = [format(x, f'0{len(bin(x))-2}b') for x in hist.keys()]
    vals = list(hist.values())
    plt.figure(figsize=(10,5))
    plt.bar(labels, vals)
    plt.title(title)
    plt.xlabel('Bit Dizisi')
    plt.ylabel('Frekans')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    if filename:
        plt.savefig(filename, bbox_inches='tight', dpi=150)
        logger.info(f"Grafik kaydedildi: {filename}")
    plt.show()


def create_agents():
    logger.debug("Agent'lar olusturuluyor...")
    api_key = os.environ.get("IOINTEL_API_KEY")
    base = "https://api.intelligence.io.solutions/api/v1"
    specs = [
    (
        "Measurement Analyst",
        """– With English Take the raw quantum measurement histogram and:
1. Compute key statistics (mean, variance, entropy).
2. Identify most frequent and least frequent measurement results.
3. Provide examples with visual and numerical comparisons.
4. Provide decision support recommendations with a brief, bulleted summary."""
    ),
    (
        "Noise Detector",
        """– With English Analyze measurement data for anomalies:
1. Outlier detection (with statistical thresholds).
2. Noise spectrum analysis (Fourier based).
3. Calculate signal-to-noise ratio.
4. Algorithmic correction or filtering suggestions."""
    ),
    (
        "Pattern Recognizer",
        """– With English Discover recurring patterns in data:
1. Analyze patterns with clustering or PCA.
2. Find correlations among time-series-like measurements.
3. Explain phenomena with examples.
4. List statistically significant patterns, item by item."""
    ),
    (
        "Circuit Optimizer",
        """–Examine the existing quantum circuit:
1. We propose depth (depth) and width (width) strategies.
2. Equivalent transformations to reduce the amount of gates sun.
3. Evaluate the best fit to the target hardware (hardware).
4. Show with an example "before/after" circuit diagram."""
    ),
    (
        "Final Report Writer",
        """– With English Combine all analyses into a single scientific report:
1. Introduction (purpose and methodology).
2. 3–5 highlights of the findings for each agent.
3. Conclusions supported by graphs and tables.
4. Next steps and recommendations section."""
    ),
    (
        "Türkçe Yorumcu",
        """Siz “Türkçe Yorumcu” rolündesiniz. Aşağıdaki kuantum ölçüm histogramını ve proje amacını **madde madde**, net bir biçimde açıklayın.  
**İstediğim yapı:**  
1. “Kuantum nedir?” başlığıyla **en az iki cümle** açıklama yapın, basit bir benzetme ekleyin.  
2. Ölçüm histogramını **günlük hayat örnekleri** (en az 2 farklı) ile sadeleştirin.  
3. Tamamen kuantum bilmeyen birinin anlayacağı, akıcı ve samimi bir dille yazın.  
4. Bu sonuçların projenin hangi aşamasında ne işe yarayacağını, nasıl daha iyi sonuçlar elde edebileceğinizi ve diğer agent’ların bulgularını **kısa bir özet halinde** anlatın.  
"""
    ),
]
    agents = []
    for name, instr in specs:
        agents.append(Agent(name=name, instructions=instr, model="meta-llama/Llama-3.3-70B-Instruct", api_key=api_key, base_url=base))
    return agents


def analyze_with_agents(text, agents):
    logger.info("Multi-Agent workflow basladi.")
    results = {}
    for ag in agents:
        wf = Workflow(text=text, client_mode=False)
        out = wf.custom(name=ag.name, objective=f"{ag.name} görevini gerçekleştir", instructions=ag.instructions, agents=[ag]).run_tasks()
        results[ag.name] = out["results"].get(ag.name)
    logger.info("Tüm agent çıktıları toplandı.")
    return results


def main(seed_circuits=True):
    logger.info("Proje basladi.")
    num_qubits = args.num_qubits
    reps = args.repetitions
    simulator = cirq.Simulator()
    qubits = setup_qubits(num_qubits)

    # Initial
    init_circ = build_initial_circuit(qubits)
    hist1 = measure_circuit(init_circ, simulator, repetitions=reps)
    save_text("initial_measurements.txt", format_histogram(hist1))
    plot_histogram(hist1, f"BAŞLANGIÇ ({num_qubits} qubit, {reps} tekrar)", "initial_hist.png")

    # Nested
    nested_circ = build_nested_circuit(qubits)
    hist2 = measure_circuit(nested_circ, simulator, repetitions=reps, key='nested_result')
    save_text("nested_measurements.txt", format_histogram(hist2))
    plot_histogram(hist2, f"NESTED ({num_qubits} qubit, {reps} tekrar)", "nested_hist.png")

    summary = f"Baslangic Sonuclari:\n{format_histogram(hist1)}\n\nNested Sonuclari:\n{format_histogram(hist2)}"
    agents = create_agents()
    results = analyze_with_agents(summary, agents)
    save_json("agent_results.json", results)

    logger.info("Proje tamamlandi.")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
