# app.py (Streamlit arayüz)
import streamlit as st
import json
import pathlib
import subprocess
import sys

st.set_page_config(page_title="Quantum Dashboard", layout="wide")
st.title("🚀 Quantum Çoklu Agent Simülasyonu")

# Kullanıcı parametreleri
num_qubits = st.sidebar.slider("Qubit Sayısı", 2, 10, 5)
reps = st.sidebar.number_input("Tekrar Sayısı (100,1000,2000...)", 100, 5000, 1000)

# Proje dizini ve Simulation_Interface.py
base = pathlib.Path(__file__).parent
script = base / "Simulation_Interface.py"

# Görseller ve sonuç dosyaları
initial = base / "initial_hist.png"
nested = base / "nested_hist.png"
results_file = base / "agent_results.json"

# Histogram gösterimi
st.subheader("Histogramlar")
col1, col2 = st.columns(2)
with col1:
    if initial.exists():
        st.image(str(initial), use_container_width=True)
    else:
        st.warning("initial_hist.png bulunamadı.(Eğer ilk kez kullanıyorsanız sorun yok normaldir simülasyonu çalıştırın)")
with col2:
    if nested.exists():
        st.image(str(nested), use_container_width=True)
    else:
        st.warning("nested_hist.png bulunamadı.(Eğer ilk kez kullanıyorsanız sorun yok)")

# Agent raporları
st.subheader("Agent Raporları")
if results_file.exists():
    data = json.loads(results_file.read_text(encoding='utf-8'))
    for agent_name, report in data.items():
        with st.expander(agent_name):
            st.write(report)
else:
    st.warning("agent_results.json bulunamadı.(Eğer ilk kez kullanıyorsanız sorun yok)")

# Simülasyonu başlat
if st.sidebar.button("Simülasyonu Çalıştır"):
    cmd = [sys.executable, str(script),
           "--num_qubits", str(num_qubits),
           "--repetitions", str(reps)]
    with st.spinner("Simülasyon çalışıyor…(Ajanları Bekliyoruz Kendileri 3dk içerisinde yorumlarıyla teşrif edeceklerdir.)"):
        try:
            subprocess.run(cmd, check=True)
            st.success("Simülasyon tamamlandı! Lütfen sayfayı yenileyin.")
        except subprocess.CalledProcessError as e:
            st.error(f"Hata oluştu: {e}")
st.markdown("---")
st.markdown("©Hasan Fatih Öztürk")