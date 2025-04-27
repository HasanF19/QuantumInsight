from iointel import Agent, Workflow
import os

# 1. API anahtarlarını ayarla
os.environ["IOINTEL_API_KEY"] = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImU0MTNlYTcwLTc2ZDMtNGViYi05ZjRlLTU0OTJkYzhlZjM5MCIsImV4cCI6NDg5OTI2MjQ5Nn0.ka9Nog3-HHDxowTRRpns3Y3O5y_K4z-GxZXUxlc-qeY4j__ZD8hy0ufDzh4Ykj1BGyqoNZ0Ho0IsPPpxSPGNbg"  # Buraya kendi io.net key'ini koy

# 2. Başlangıç + Nested Ölçüm Verilerini birleştir
quantum_summary_text = f"""
Başlangıç Quantum Devresi Ölçüm Sonuçları:
00000 -> 467 kez
01100 -> 491 kez
01000 -> 12 kez
00001 -> 4 kez
00100 -> 11 kez
10000 -> 6 kez
11100 -> 4 kez
01101 -> 5 kez

Nested Quantum Devresi Ölçüm Sonuçları:
01110 -> 99 kez
11110 -> 208 kez
11111 -> 296 kez
01011 -> 19 kez
11101 -> 12 kez
11001 -> 3 kez
01111 -> 182 kez
10111 -> 31 kez
11011 -> 36 kez
11010 -> 18 kez
01001 -> 2 kez
01101 -> 9 kez
11100 -> 8 kez
10110 -> 14 kez
00111 -> 19 kez
00110 -> 10 kez
10011 -> 4 kez
01010 -> 19 kez
00011 -> 2 kez
01100 -> 3 kez
00101 -> 1 kez
10010 -> 1 kez
10100 -> 1 kez
10101 -> 1 kez
11000 -> 1 kez
00100 -> 1 kez
"""


##normalde buraya ölçüm sonuçlarını yazıyoruz Her simülasyonda kopyalama bizi yorar
#iki quantım ve bir multiagent sistemi birleştirip son prototipi çıkartıyorum

# 3. 5 Agent Tanımlayalım
agents = [
    
    Agent(
        name="Measurement Analyst",
        instructions="Analyze the initial and nested quantum measurement results. Identify general trends.",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["IOINTEL_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    ),
    Agent(
        name="Noise Detector",
        instructions="Detect noise or inconsistencies in the measurement results. Comment on potential sources of error.",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["IOINTEL_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    ),
    Agent(
        name="Pattern Recognizer",
        instructions="Find recurring patterns or structures in the quantum measurement data.",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["IOINTEL_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    ),
    Agent(
        name="Circuit Optimizer",
        instructions="Suggest possible optimizations to improve the quantum circuit based on measurement distributions.",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["IOINTEL_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    ),
    Agent(
        name="Final Report Writer",
        instructions="Collect all previous agent outputs and write a complete scientific-style final report about the quantum experiment.",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["IOINTEL_API_KEY"],
        base_url="https://api.intelligence.io.solutions/api/v1"
    ),
]

# 4. Workflow Başlat
workflow = Workflow(
    text=quantum_summary_text,
    client_mode=False
)

# 5. Multi-Agent Görev Ver
results = workflow.custom(
    name="nested-simulation-multi-agent",
    objective="Complete full quantum simulation analysis and optimization.",
    instructions="Each agent should perform their specialized role and produce a combined output.",
    agents=agents
).run_tasks()

# 6. Sonuçları yazdır
print("\nMulti-Agent Analysis Result:\n", results)
