import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from PIL import Image
from streamlit_javascript import st_javascript

# Load Data
df = pd.read_csv("dummy_kompetensi_pegawai.csv", delimiter=";")
selected_name = st.selectbox("Pilih Pegawai", df["Nama"])
pegawai = df[df["Nama"] == selected_name].iloc[0]

# Layout: 2 Columns (Photo + Biodata)
col1, col2 = st.columns([1, 3])

photo_path = "profile.png"

with col1:
    if os.path.exists(photo_path):
        st.image(photo_path, width=200)
    else:
        st.warning("📸 Foto tidak ditemukan.")

with col2:
    st.markdown("### **Biodata**")
    st.markdown(f"""
    **Nama**: {pegawai['Nama']}  
    **NIP**: {pegawai['NIP']}  
    **Jabatan**: {pegawai['Jabatan']}  
    **Unit Terakhir**: {pegawai['Unit Terakhir']}  
    **Golongan**: {pegawai['Golongan']}  
    **Masa Kerja**: {pegawai['Masa Kerja']}  
    **Pendidikan**:
    - {pegawai['Pendidikan D3']}
    - {pegawai['Pendidikan S1']}
    - {pegawai['Pendidikan S2']}
    """)

# Data Dictionary
kompetensi = {
    "Akuntansi": [pegawai["Kompetensi Akuntansi"], pegawai["Pengalaman Akuntansi"], pegawai["Assessment Akuntansi"]],
    "Penilaian": [pegawai["Kompetensi Penilaian"], pegawai["Pengalaman Penilaian"], pegawai["Assessment Penilaian"]],
    "Aktuaria": [pegawai["Kompetensi Aktuaria"], pegawai["Pengalaman Aktuaria"], pegawai["Assessment Aktuaria"]],
    "Perpajakan": [pegawai["Kompetensi Perpajakan"], pegawai["Pengalaman Perpajakan"], pegawai["Assessment Perpajakan"]]
}
df_plot = pd.DataFrame(kompetensi, index=["Kompetensi", "Pengalaman", "Assessment"]).T.reset_index()
df_plot = df_plot.rename(columns={"index": "Bidang"})

# Layout: Bar Chart for Pengalaman and Assessment
st.markdown("### Keahlian Bidang Profesi Keuangan")

# Auto-detect screen width
width = st_javascript("window.innerWidth")
is_mobile = width is not None and width < 768

if is_mobile:
    for i, row in df_plot.iterrows():
        avg_score = round((row["Kompetensi"] + row["Pengalaman"] + row["Assessment"]) / 3)

        st.subheader(row['Bidang'])
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_score,
            number={'font': {'size': 22}},
            title={'text': f"<b>{row['Bidang']}</b>", 'font': {'size': 12}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1f77b4"},
                'bgcolor': "white",
                'shape': "angular"
            },
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig.update_layout(
        height=110,  # Lebih pendek
            margin=dict(t=5, b=5, l=5, r=5),
            font=dict(size=12),  # Kecilkan semua teks dalam chart
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**Kompetensi: {row['Kompetensi']}**")
        st.progress(row['Kompetensi'] / 100)

        st.markdown(f"**Pengalaman**: {row['Pengalaman']}")
        st.progress(row['Pengalaman'] / 100)

        st.markdown(f"**Assessment**: {row['Assessment']}")
        st.progress(row['Assessment'] / 100)
        st.markdown("---")
else:
    gauge_cols = st.columns(min(len(df_plot), 4))

    for i, row in df_plot.iterrows():
        avg_score = round((row["Kompetensi"] + row["Pengalaman"] + row["Assessment"]) / 3)

        with gauge_cols[i]:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg_score,
                title={'text': f"<b>{row['Bidang']}</b>", 'font': {'size': 14}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1f77b4"},
                    'bgcolor': "white",
                    'shape': "angular"
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            fig.update_layout(
                height=180,
                margin=dict(t=20, b=10, l=5, r=5),
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"**Kompetensi: {row['Kompetensi']}**")
            st.progress(row['Kompetensi'] / 100)

            st.markdown(f"**Pengalaman**: {row['Pengalaman']}")
            st.progress(row['Pengalaman'] / 100)

            st.markdown(f"**Assessment**: {row['Assessment']}")
            st.progress(row['Assessment'] / 100)

st.markdown("<br><br>", unsafe_allow_html=True)
