import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="About — Smart Traffic Violation Pattern Detector",
    layout="wide"
)

# -----------------------------
# Header Section
# -----------------------------
st.title("📘 About — Smart Traffic Violation Pattern Detector")
st.write("")

col1, col2 = st.columns([1, 2])

with col1:
 st.markdown("""
Welcome to the **Smart Traffic Violation Pattern Detector**, an intelligent system designed to enhance road safety through **data-driven insights**.

This project utilizes:  
- 📊 *Advanced Analytics*  
- 🤖 *Machine Learning*  
- 📈 *Smart Dashboards*  

Our aim is to help authorities **identify patterns**, reduce accidents, and improve city-wide traffic management.
    """)
with col2:
 
    st.image("assets/detection.png", width=1000)

st.markdown("---")

# -----------------------------
# Expanders Section
# -----------------------------

# ---- Who We Are ----
with st.expander("👨‍💻 Who We Are", expanded=False):
    st.markdown("""
We are a team of developers and data analysts committed to creating effective, real-world technology solutions.

We specialize in:
- 🐍 **Python Development**
-  🎛 **Streamlit Dashboards**
- 🤖 **Machine Learning**
- 📊 **Data Visualization & Analytics**

Our mission is to make traffic monitoring **smarter, faster, and more reliable**.
    """)

# ---- What We Do ----
with st.expander("🛠️ What We Do", expanded=False):
    st.markdown("""
### ✔ Automated Data Processing  
Cleans, structures and analyzes large-scale traffic violation data automatically.

### ✔ Violation Severity Scoring  
Applies custom severity levels to each violation type.

### ✔ Risk Index Calculation  
Computes risk score per vehicle based on cumulative violations.

### ✔ Pattern & Trend Detection  
Finds:
- Most common violations  
- Violation combinations  
- Peak time for rule-breaking  
- High-risk vehicles & regions  

### ✔ Interactive Visualizations  
Includes:
- Hour-wise violations  
- Severity distribution  
- Vehicle-type trends  
- Fine contribution analytics  

### ✔ Predictive ML Insights *(Optional)*  
Predicts:
- Future violations  
- Risky behavior patterns  
    """)

# ---- Mission ----
with st.expander("🎯 Our Mission"):
    st.markdown("""
To empower traffic authorities with a **data-driven, scalable, and reliable** system that reduces manual work and improves road safety.
    """)

# ---- Vision ----
with st.expander("🌍 Our Vision"):
    st.markdown("""
A future where **technology & analytics** work together to minimize road accidents, ensure better compliance, and build **safer, smarter cities**.
    """)

# ---- Why It Matters ----
with st.expander("🚦 Why This Project Matters"):
    st.markdown("""
- Urban traffic is increasing rapidly  
- Manual monitoring is slow and inefficient  
- Data reveals hidden patterns humans may miss  
- Helps prevent violations and save lives  
- Brings **transparency, accuracy & intelligence** to traffic systems  
    """)
# -----------------------------
# Technologies Used
# -----------------------------
with st.expander("🧩 Technologies & Libraries Used", expanded=False):
    st.markdown("""
### ✔ **Python Libraries**
- **Pandas** – Data cleaning & manipulation  
- **NumPy** – Numerical operations  
- **Matplotlib** – Static charts  
- **Seaborn** – Statistical visualizations  
- **Plotly (Optional)** – Interactive charts  
- **Scikit-learn** – Machine learning  
- **Collections / Counter** – Pattern analysis  
- **Datetime** – Time-based processing  

### ✔ **Frameworks & Tools**
- **Streamlit** – Web dashboards  
- **VS Code** – Development environment  
- **Google Colab** – Exploratory analysis  
- **Jupyter Notebook** – Prototyping  
- **GitHub** – Version control  
    """)
# -----------------------------
# Contributors Section
# -----------------------------
st.header("🤝 Contributors")

st.write("**Ishwari** - Software Developer")
st.write("**Saidul** - ML Engineer")
st.write("**Anshu** - Backend Developer")
st.write("**Mrunali** - ML Engineer")
st.write("**Sanjana** - ML Engineer")
st.write("**Poojitha** - Data Analyst & Streamlit Developer")
st.write("**Divija** - ML Engineer")
st.write("**Amit** - Backend Developer")
st.write("**Rakshitha** - Streamlit Developer")
st.write("**Harika** - ML Engineer")
st.write("**Vijay** - Data Analyst & Streamlit Developer")
st.write("**Mehek** - Streamlit Developer")
st.write("**Darsana** - Backend Developer")
st.write("**Monika** - ML Engineer")
st.write("**Monika** - Streamlit Developer")

st.markdown("---")

st.success("✨ About Page Loaded Successfully!")
