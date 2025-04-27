import os
import json
import logging
import random
import cirq
import numpy as np
import matplotlib.pyplot as plt
from iointel import Agent, Workflow
os.environ["IOINTEL_API_KEY"] = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImU0MTNlYTcwLTc2ZDMtNGViYi05ZjRlLTU0OTJkYzhlZjM5MCIsImV4cCI6NDg5OTI2MjQ5Nn0.ka9Nog3-HHDxowTRRpns3Y3O5y_K4z-GxZXUxlc-qeY4j__ZD8hy0ufDzh4Ykj1BGyqoNZ0Ho0IsPPpxSPGNbg"

# --------------------------------------------------
# Proje: Nested Quantum Simülasyon + Multi-Agent Analiz
# Dosya: Prototype_V7.py
# Yazar: Hasan Fatih Öztürk
# Tarih: 2025-04-23
# --------------------------------------------------

# 1. Logging kurulumu
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def save_text(filename: str, text: str):
    """
    Verilen metni bir .txt dosyasına kaydeder.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"Metin dosyası kaydedildi: {filename}")
    except Exception as e:
        logger.error(f"Dosya kaydederken hata: {e}")


def save_json(filename: str, data):
    """
    Verilen veriyi JSON formatında kaydeder.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"JSON dosyası kaydedildi: {filename}")
    except Exception as e:
        logger.error(f"JSON kaydederken hata: {e}")


def setup_qubits(n: int):
    """
    n adet LineQubit düğümü olusturur.
    """
    logger.debug(f"{n} qubit olusturuluyor...")
    return [cirq.LineQubit(i) for i in range(n)]


def build_initial_circuit(qubits):
    """
    Rastgele kapılarla basit bir devre kurar.
    """
    logger.debug("Initial circuit olusturuluyor...")
    circuit = cirq.Circuit()
    # Tek-qubit kapilar
    single = [cirq.X, cirq.Y, cirq.Z, cirq.H, cirq.rx, cirq.ry, cirq.rz]
    # Cift-qubit kapilar
    two = [cirq.CNOT, cirq.CZ, cirq.ISWAP]
    
    # Her qubit icin rastgele 2-3 kapı
    for q in qubits:
        ops_count = random.randint(2, 3)
        for _ in range(ops_count):
            gate = random.choice(single)
            if gate in [cirq.rx, cirq.ry, cirq.rz]:
                angle = np.random.uniform(0, np.pi)
                circuit.append(gate(angle).on(q))
            else:
                circuit.append(gate.on(q))
    # 5 tane rastgele cift-qubit kapisi ekle
    for _ in range(5):
        q1, q2 = random.sample(qubits, 2)
        gate = random.choice(two)
        circuit.append(gate(q1, q2))
    # Olcum
    circuit.append(cirq.measure(*qubits, key='result'))
    logger.debug("Initial circuit hazir.")
    return circuit


def measure_circuit(circuit, simulator, repetitions=1000, key='result'):
    """
    Devreyi simule eder ve sonuc histogramini döner.
    """
    logger.info(f"Devre simule ediliyor, tekrar: {repetitions}")
    result = simulator.run(circuit, repetitions=repetitions)
    hist = result.histogram(key=key)
    logger.info("Simulasyon tamamlandi.")
    return hist


def format_histogram(hist):
    """
    Histogrami okunur hale getirir.
    """
    lines = []
    for bits, count in hist.items():
        bstr = format(bits, f'0{len(bin(bits))-2}b')
        lines.append(f"{bstr} -> {count} kez")
    return "\n".join(lines)


def build_nested_circuit(qubits):
    """
    Initial sonuclarına gore dinamik nested devre kurar.
    """
    logger.debug("Nested circuit olusturuluyor...")
    circuit = cirq.Circuit()
    # GHZ-like entanglement
    circuit.append(cirq.H.on_each(*qubits))
    for i in range(len(qubits)-1):
        circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
    # Parametrik kapilar
    for q in qubits:
        ax = np.random.uniform(0, np.pi)
        ay = np.random.uniform(0, np.pi)
        circuit.append(cirq.rx(ax).on(q))
        circuit.append(cirq.ry(ay).on(q))
    circuit.append(cirq.measure(*qubits, key='nested_result'))
    logger.debug("Nested circuit hazir.")
    return circuit


def plot_histogram(hist, title, filename=None):
    """
    Histogrami grafik olarak cizer.
    """
    labels = [format(x, f'0{len(bin(x))-2}b') for x in hist.keys()]
    vals = list(hist.values())
    plt.figure(figsize=(10, 5))
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
    """
    Multi-Agent sistemini tanimlar ve her bir agent'a detaylı, zengin talimatlar verir.
    """
    logger.debug("Agent'lar olusturuluyor...")
    api_key = os.environ.get("IOINTEL_API_KEY", None)
    if not api_key:
        logger.error("IOINTEL_API_KEY ayarlanmamis!")
    base = "https://api.intelligence.io.solutions/api/v1"


    agent_specs = [
    (
        "Measurement Analyst",
        """– Take the raw quantum measurement histogram and:
  1. Compute key statistics (ortalama, varyans, entropi).
  2. Identify en sık ve en nadir ölçüm sonuçlarını.
  3. Görsel ve sayısal karşılaştırmalarla örnekler ver.
  4. Kısa, madde madde özetiyle karar destek önerileri sun."""
    ),
    (
        "Noise Detector",
        """– Analyze measurement data for anomalies:
  1. Outlier tespiti (istatistiksel eşiklerle).
  2. Gürültü spektrum analizi (Fourier tabanlı).
  3. Sinyal/ gürültü oranı hesapla.
  4. Algoritmik düzeltme veya filtreleme önerileri."""
    ),
    (
        "Pattern Recognizer",
        """– Verideki tekrarlayan desenleri keşfet:
  1. Kümeleme veya PCA ile örüntü analizi.
  2. Zaman-serisi benzeri ölçümler arasında korelasyon bul.
  3. Olguları örneklerle açıkla.
  4. İstatistiksel olarak anlamlı desenleri madde madde sıralar."""
    ),
    (
        "Circuit Optimizer",
        """– Mevcut kuantum devresini incele:
  1. Derinlik (depth) ve genişlik (width) optimizasyonu öner.
  2. Kapı sayısını azaltacak eşdeğer dönüşümler sun.
  3. Hedef donanıma (hardware) en iyi uyumluluğu değerlendir.
  4. Örnek “before/after” devre diyagramı ile göster."""
    ),
    (
        "Final Report Writer",
        """– Tüm analizleri tek bir bilimsel raporda birleştir:
  1. Giriş (amaç ve metodoloji).
  2. Her ajanın bulgularından öne çıkan 3–5 madde.
  3. Grafik ve tablolarla destekli sonuçlar.
  4. Gelecek adımlar ve öneriler bölümü."""
    ),
    (
        "Türkçe Yorumcu",
        """– Bu projedeki kuantum ölçüm sonuçlarını türkçe olarak aşağıdaki maddeler şeklinde anlat:
  1. “Kuantum nedir?” sorusuyla başlayarak temel kavram tanıtımı.
  2. Ölçüm histogramını örnek günlük hayat benzetmeleriyle sadeleştir.
  3. Henüz kuantumla tanışmamış birinin anlayacağı akıcı bir dille yaz.
  """
    ),
]


    agents = []
    for name, instr in agent_specs:
        ag = Agent(
            name=name,
            instructions=instr,
            model="meta-llama/Llama-3.3-70B-Instruct",
            api_key=api_key,
            base_url=base,
        )
        agents.append(ag)
        logger.debug(f"Agent eklendi: {name}")
    return agents

def analyze_with_agents(text, agents):
    """
    Workflow ile Multi-Agent analysesini calistirir.
    Her ajanı custom workflow ile tek tek çalıştırıp çıktılarını döner.
    """
    logger.info("Multi-Agent workflow basladi.")
    results = {}
    for ag in agents:
        # Her ajanı ayrı custom workflow içinde çalıştırıyoruz
        wf = Workflow(text=text, client_mode=False)
        task = wf.custom(
            name=ag.name,                              # workflow adı ajan adı olsun
            objective=f"{ag.name} görevini gerçekleştir",  
            instructions=ag.instructions,
            agents=[ag]
        )
        out = task.run_tasks()                         # run değil, run_tasks
        # out şu formatta dönecektir: {"conversation_id": "...", "results": {ag.name: "..." } }
        results[ag.name] = out["results"].get(ag.name)
        logger.debug(f"{ag.name} çıktısı alındı.")
    logger.info("Tüm agent çıktıları toplandı.")
    return results


def main():
    # Ortam anahtari kontrol
    logger.info("Proje basladi.")
    # API anahtari yoksa uyari
    if not os.environ.get("IOINTEL_API_KEY"):
        logger.warning("IO.NET API anahtari bulunamadi, ayarlayin.")

    # Kuantum qubit hazirla
    qubits = setup_qubits(5)

    # Baslangic devresi
    init_circ = build_initial_circuit(qubits)
    logger.debug("Baslangic devre kodu:\n%s", str(init_circ))

    # Simulasyon
    simulator = cirq.Simulator()
    hist1 = measure_circuit(init_circ, simulator)

    # SonuCLeri kaydet
    init_summary = format_histogram(hist1)
    save_text("initial_measurements.txt", init_summary)
    plot_histogram(hist1, "Baslangic Olcum Dagilimi", "initial_hist.png")

    # Nested devresi
    nested_circ = build_nested_circuit(qubits)
    logger.debug("Nested devre kodu:\n%s", str(nested_circ))
    hist2 = measure_circuit(nested_circ, simulator, key='nested_result')

    # SonuCLeri kaydet
    nested_summary = format_histogram(hist2)
    save_text("nested_measurements.txt", nested_summary)
    plot_histogram(hist2, "Nested Olcum Dagilimi", "nested_hist.png")

    # Tum sonuCLeri birlestir
    quantum_summary_text = (
        "Baslangic Quantum Devresi Olcum Sonuclari:\n" + init_summary +
        "\n\nNested Quantum Devresi Olcum Sonuclari:\n" + nested_summary
    )

    # Agent'lari olustur ve calistir
    agents = create_agents()
    results = analyze_with_agents(quantum_summary_text, agents)

    # Sonuclari kaydet
    save_json("agent_results.json", results)

    # Final log
    logger.info("Proje tamamlandi, cikti dosyalari olusturuldu.")
    print("\n==== Agent Sonuclari ====\n", json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
