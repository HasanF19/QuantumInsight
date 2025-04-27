# Nested Quantum Simulation + Multi-Agent Analyst

**Turkish explanations are given after English explanations.**

---

## 0. About Me and Project Motivation

I’m Hasan Fatih Öztürk, a third-year Artificial Intelligence Engineering student at Ostim Technical University. I’ve completed many projects involving machine learning and agent-based systems. When a friend studying physics needed help with quantum simulations, I decided to build a quantum-physics simulation interpretation framework. I used the custom-agent structure from the IOIntel infrastructure as a template. To keep the system fast, it runs two simple—but random—quantum measurements and then sequentially interprets them with six agents. To date, no agent has been specifically designed to provide quantum-interpretation in the field of quantum physics. I plan to develop my project by integrating it into more powerful quantum simulations with more advanced agents and turn it into a product.

---

## 0. Hakkımda ve Proje Motivasyonum

Ben Hasan Fatih Öztürk, Ostim Teknik Üniversitesi’nde üçüncü sınıf Yapay Zeka Mühendisliği öğrencisiyim. Makine öğrenmesi ve ajan tabanlı sistemler üzerine birçok proje tamamladım. Fizik okuyan bir arkadaşım kuantum simülasyonları konusunda yardım isteyince, bir kuantum fiziği simülasyon yorumlama çerçevesi geliştirmeye karar verdim. IOIntel altyapısındaki custom-agent yapısını bir şablon olarak kullandım. Sistemin hızlı çalışmasını sağlamak için iki basit — fakat rastgele — kuantum ölçümü gerçekleştiriliyor ve ardından bu ölçümler altı ajan tarafından sırasıyla yorumlanıyor. Şu ana kadar, kuantum fiziği alanında özellikle kuantum yorumlaması sağlamak üzere tasarlanmış bir ajan bulunmamaktadır. Projemi daha güçlü kuantum simülasyonlarına entegre ederek ve daha gelişmiş ajanlar kullanarak geliştirmeyi, sonrasında da bunu bir ürüne dönüştürmeyi planlıyorum.

---

## 1. The Need for Simulation in Quantum Computing and Measurements

Quantum computers stand out for their potential to solve problems that classical computers struggle with. However, because real quantum hardware is still limited in accessibility and prone to noise, we rely on software-based simulations to analyze experimental results and optimize new circuit designs. This project aims to simulate both random (Prototype_V1/V2) and nested (Prototype_V3/V7) quantum circuits and interpret the measurement distributions using statistical and multi-agent approaches.

---

## 1. Kuantum ve Ölçümlerde Simülasyon İhtiyacı

Kuantum bilgisayarlar, klasik bilgisayarların zorlandığı problemleri çözme potansiyeliyle dikkat çeker. Ancak gerçek kuantum donanımlar hâlâ erişim kısıtlı ve gürültülü olduğundan, deneysel sonuçları analiz etmek ve yeni devre tasarımlarını optimize etmek için yazılımsal simülasyonlar kullanırız. Bu proje, hem **rastgele** (Prototype_V1/V2) hem de **nested** (Prototype_V3/V7) kuantum devrelerini simüle ederek, ölçüm dağılımlarını istatistiksel ve çok-ajan yaklaşımıyla yorumlamayı hedefler.

---

## 2. Folder Structure and File Descriptions

- **Prototype_V1.py**  
  - Simulates a single quantum circuit and interprets it with an agent like “Measurement Analyst.”  
- **Prototype_V2.py**  
  - Performs a 5-qubit measurement; since the resulting histogram was heavily skewed, we needed to improve its distribution.  
- **Prototype_V3.py**  
  - Builds a “nested” circuit to achieve a broader, more distributed measurement outcome.  
- **Prototype_V4.py**  
  - Contains no quantum simulation; it only demonstrates the multi-agent framework and how prompts are defined (updated in V7).  
- **Prototype_V7.py**  
  - The project’s “finished,” most powerful version. Combines the nested circuit and multi-agent workflow in a single file.  
- **Simulation_Interface.py**  
  - A Streamlit-optimized, UTF-8-compatible, simplified version of Prototype_V7.py. Used by the interface.  
- **app.py**  
  - Streamlit-based web interface. Select the number of qubits and repetitions in the sidebar, then click “Run Simulation” to launch the entire system.  
- **README.txt**  
  - Project description and usage steps (this file).  

---

## 2. Klasör Yapısı ve Dosya Açıklamaları

- **Prototype_V1.py**  
  - Tek bir kuantum devresi ve “Measurement Analyst” benzeri bir ajanla yorumlama. Sistemi tanımak için inceleyin.  
- **Prototype_V2.py**  
  - 5-qubit ölçümü yapar; sonuç histogramı tek taraflı yoğunlaştığından dağılımı iyileştirmeye ihtiyaç duyduk.  
- **Prototype_V3.py**  
  - “Nested” (iç içe) devre kurarak daha geniş ve dağıtık bir ölçüm dağılımı elde eder.  
- **Prototype_V4.py**  
  - Kuantum simülasyonu yok; yalnızca multi-agent altyapısını ve prompt’ların tanımını gösterir (V7’de promptlar güncellendi).  
- **Prototype_V7.py**  
  - Projenin “bitmiş,” en güçlü versiyonu. Nested devre ve multi-agent akışını tek bir dosyada birleştirir.  
- **Simulation_Interface.py**  
  - `Prototype_V7.py`’nin Streamlit için optimize edilmiş, UTF-8 uyumlu ve sadeleştirilmiş versiyonu. Arayüz tarafından kullanılır.  
- **app.py**  
  - Streamlit tabanlı web arayüzü. Yan panelden qubit sayısı ve tekrar sayısını seçip “Simülasyonu Çalıştır” butonuyla komple sistemi çalıştırır.  
- **README.txt**  
  - Proje açıklamaları ve kullanım adımları (bu dosya).  

---

## 3. Technologies Used

- **Python 3.8+**  
- **Cirq** (Google): Building and simulating quantum circuits.  
- **NumPy**: Generating random parameters and performing numerical operations.  
- **Matplotlib**: Plotting measurement histograms.  
- **IOIntel SDK** (`iointel`): Configuring and analyzing with a multi-agent setup.  
- **Streamlit**: Web-based interactive interface.  
- **logging, os, json, random**: Standard Python libraries.

---

## 3. Kullanılan Teknolojiler

- **Python 3.8+**  
- **Cirq** (Google): Kuantum devresi oluşturma ve simülasyon.  
- **NumPy**: Rastgele parametre üretimi, sayısal işlemler.  
- **Matplotlib**: Ölçüm histogramlarını çizme.  
- **IOIntel SDK** (`iointel`): Multi-agent yapılandırma ve analiz.  
- **Streamlit**: Web tabanlı, etkileşimli arayüz.  
- **logging, os, json, random**: Python standart kütüphaneleri.

---

## 4. Installation and Running

Install the required packages:
pip install cirq numpy matplotlib streamlit iointel
To run the advanced algorithm from the command line:
python Prototype_V7.py
To access the interface and view simplified agent analyses:
python -m streamlit run app.py

## 4. Kurulum ve Yükleme

Gerekli kütüphanelerin yüklenmesi
pip install cirq numpy matplotlib streamlit iointel
Terminal üzerinde Gelişmiş prototipi çalıştırmak için
python Prototype_V7.py
daha basit ve sade haline gelişmiş arayüz ile çalıştırmak için bu kodu kullanın
python -m streamlit run app.py

for any question
ozturkhasanfatih@gmail.com
Herhangi bir sorunuz için
ozturkhasanfatih@gmail.com
