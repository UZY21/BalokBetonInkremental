#Membuat Interface Lebih Menarik
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import math
import plotly.express as px


#Sidebar Radio
Awal = st.sidebar.radio ("",['Home','Mind Map','Optimasi Desain 1','Optimasi Desain 2','Cek Kapasitas'])
#Laman AWAL
if Awal == "Home":
    st.header("TUGAS AKHIR")
    st.subheader("OPTIMASI DESAIN PENAMPANG BALOK BETON BERTULANG METODE INKREMENTAL")
    image = Image.open('ITENAS.png')
    st.image (image)
#Laman MidMap
if Awal == "Mind Map":
    st.header ("Bagan Alir Perhitungan")
    st.subheader("Perhitungan Perencanaan Balok Beton Bertulang Tulangan Tunggal")
    image5 = Image.open('flowchart1.png')
    st.image(image5)
    image6 = Image.open('flowchart2.png')
    st.image(image6)
    st.subheader("Perhitungan Harga")
    image7 = Image.open('flowchart3.png')
    st.image(image7)
#Optimasi Desain 1
if Awal == "Optimasi Desain 1":
    options = st.sidebar.selectbox("", ["Asumsi Tulangan Satu Lapis", "Asumsi Tulangan Dua Lapis"])
    if options == "Asumsi Tulangan Satu Lapis":
        st.header("ANALISIS PENAMPANG BALOK BETON BERTULANG METODE INKREMENTAL")
        tab1, tab2, tab3, tab4, tab5, tab6,tab7= st.tabs(["List Input","Input Angka","Analisis Awal", "Inkremental", "Harga Material","Grafik1","Grafik2"])
        with tab1:
            st.header ("NILAI - NILAI YANG DIBUTUHKAN")
            st.subheader ("Jenis Tulangan")
            image8 = Image.open ('BetonPolos.png')
            st.image(image8)
            image9 = Image.open('BetonUlir.png')
            st.image(image9)
            st.subheader ("Harga Mutu Beton Per Meter Kubik")
            image10 = Image.open('HARGABETON.PNG')
            st.image(image10)
            st.subheader("Harga Baja Per Meter")
            image12 = Image.open('BajaHarga.PNG')
            st.image(image12)
        with tab2:
            st.header ("DENAH PERANCANGAN")
            image11 = Image.open('Denah.png')
            st.image(image11)
            st.subheader ("INPUT DATA PERANCANGAN")
            #Input Pembagian kolom
            col3, col4 = st.columns(2)
            with col3 :
                L1 = st.number_input("Panjang Bentang Balok (m) =", value=7)
                selimut = st.number_input ("Nilai Tebal Selimut (mm) = ",value=40)
                sengkang =st.number_input ("Nilai diameter sengkang (Dsengkang mm) = ",value=10)
                D = st.number_input ("Nilai Diameter Longitudinal (D (mm)) = ",value=19)
                sni = st.number_input ("Nilai Beban hidup Struktur (LL (kN/m^2)) = ",value = 6)
                fc = st.number_input ("Nilai Mutu beton (Fc' (Mpa)) = ",value = 30)
                fy = st.number_input("Nilai Mutu Baja (Fy) = ", value=420)


            with col4:
                tebalplat = st.number_input("Tebal Pelat Beton (mm) = ", value=120)
                beratbeton = st.number_input("Berat Beton (kN/m^3) = ", value=24)
                beratbajalongitudinal = (st.number_input(" Berat Baja (Berat Nominal Per meter)= ", value=2.226))
                hargabeton = st.number_input ("Masukan Harga Beton (per - m^3)",value=995000)
                hargabesi = st.number_input("Masukan Harga Baja (per-kg) = ", value=9477)
                lebartributaryatas = st.number_input("Lebartributary Atas = ", value=5)
                lebartributarybawah = st.number_input("Lebartributary Bawah = ", value=5)
                #Asumsi
                Es = 200000
                hitung = st.button ("EXECUTE")
                with tab3:
                    st.header("Analisis Awal Tulangan Satu Lapis")
                    if hitung:
                        # Perhitungan Tributary Area
                        tributaryarea = (lebartributaryatas/2)+(lebartributarybawah/2)
                        #Preliminary Desain
                        L = 1*L1
                        h = math.ceil((L / 16) * 1000)
                        b = (1 / 2 * h)
                        # Hitung Beban
                        qLL = ((sni * tributaryarea))
                        qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                        qdL2 = ((tebalplat/1000) * beratbeton * tributaryarea)
                        qdL = qdL1 + qdL2
                        qu = (1.2 * qdL + 1.6 * qLL)
                        Mu = round(((1 / 8) * (qu * (L ** 2))), 3)
                        # Tulangan
                        if 17 <= fc <= 28:
                            beta_1 = 0.85
                        elif 28 <= fc < 55:
                            beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                        else:
                            beta_1 = 0.65
                        d = round (h - selimut - sengkang - (D / 2),3)
                        jd = (0.925 * d)
                        As8 = round((Mu * 1000000) / (0.9 * 420 * jd),3)
                        Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                        Asmin2 = round((1.4 / fy) * b * d, 3)
                        Asmax = round(max(As8, Asmin1, Asmin2), 3)
                        # Desain Tulangan
                        n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                        Asterpasang = round(n * ((1 / 4) * 3.1416 * ((D) ** 2)), 3)
                        if Asterpasang > Asmax:
                            As = "Memenuhi"
                        else:
                            As = "TidakMemenuhi"
                        # RasioTulangan
                        Aefektif = b * d
                        rho9 = round((Asterpasang / Aefektif), 3)
                        if rho9 < 0.025:
                            rho = "Memenuhi"
                        else:
                            rho = "TidakMemenuhi"
                        a = ((Asterpasang * fy) / (0.85 * fc * b))
                        c = ((a / beta_1))
                        ey = fy / Es
                        et1 = round((((d - c) / c) * 0.003), 4)
                        if et1 > ey:
                            et = "Under Reinfoce (Keruntuhan Tarik)"
                        elif et1 < ey:
                            et = "Over Reinforce (Keruntuhan Tekan)"
                        else:
                            et = "Balance"
                        # FaktorReduksiKekuatan
                        if et1 > 0.005:
                            phi = 0.9
                        elif 0.002 < et1 < 0.005:
                            phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                        else:
                            phi = 0.65
                        # Hitung Momen Nominal
                        Mn = round((Asterpasang * fy * (d - a / 2))/1000000, 4)
                        phiMn1 = round (phi * Mn ,4)
                        if phiMn1 > Mu:
                            phiMn = "Memenuhi"
                        else:
                            phiMn = "TidakMemenuhi"
                        rasiodesain = round(Mu / phiMn1, 3)
                        df = {"L (m)": L, "h (mm)": h, "b (mm)": b, "Mu": Mu, "d (mm)": d, "Asmax (mm^2)": Asmax, "n(buah)": n, "Asterpasang(mm^2)": Asterpasang, "As": As, "rho": rho9,"SyaratRasio": rho ,"ey": ey, "et": et1, "Jenis Keruntuhan": et, "phi": phi, "Mn": Mn, "phiMn":phiMn1 ,"PerBandingan": phiMn,"Rasio Desain":rasiodesain}
                        st.dataframe(df, 950, 700)
                with tab4:
                    st.header("Analisis Tulangan Tunggal Satu Lapis")
                    image9 = Image.open('Tulangan1Lapis.png')
                    st.image(image9)
                    df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)", "Mu", "d (mm)", "Asmax (mm^2)", "n(buah)",
                                               "Asterpasang(mm^2)", "As", "rho", "SyaratRasio", "ey", "et",
                                               "Jenis Keruntuhan", "phi", "Mn", "phiMn", "Perbandingan",
                                               "rasiodesain"])

                    #inputColom Ingkrement
                    U1 = st.number_input("Nilai Batas Bawah =")
                    U2 = st.number_input("Nilai Batas Atas=")
                    U3 = st.number_input("Ingkremental=")
                    hitungulang1 = st.button ("EXCECUTE")
                    if hitungulang1:
                        awal = np.arange(U1,U2,U3)
                        for H1 in awal :
                            # Perhitungan Tributary Area
                            tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                            #PrliminaryDesain
                            L = 1*L1
                            h = H1
                            b = (1 / 2 * h)
                            # Hitung Beban
                            qLL = round((sni * tributaryarea), 3)
                            qdL1 = round((b / 1000) * (h / 1000) * beratbeton, 3)
                            qdL2 = round((tebalplat / 1000) * beratbeton * tributaryarea, 3)
                            qdL = qdL1 + qdL2
                            qu = round(1.2 * qdL + 1.6 * qLL, 3)
                            Mu = round(((1 / 8) * (qu * (L ** 2))), 4)
                            # Tulangan
                            if 17 <= fc <= 28:
                                beta_1 = 0.85
                            elif 28 <= fc < 55:
                                beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                            else:
                                beta_1 = 0.65
                            d = h - selimut - sengkang - (D / 2)
                            jd = 0.925 * d
                            As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                            Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                            Asmin2 = round((1.4 / fy) * b * d, 3)
                            Asmax = round(max(As8, Asmin1, Asmin2), 3)
                            # Desain Tulangan
                            n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                            Asterpasang = round(n * (1 / 4 * 3.1416 * ((D) ** 2)), 3)
                            if Asterpasang > Asmax:
                                As = "Memenuhi"
                            else:
                                As = "TidakMemenuhi"
                            # RasioTulangan
                            Aefektif = b * d
                            rho9 = round((Asterpasang / Aefektif), 3)
                            if rho9 < 0.025:
                                rho = "Memenuhi"
                            else:
                                rho = "TidakMemenuhi"
                            a = ((Asterpasang * fy) / (0.85 * fc * b))
                            c = (a / beta_1)
                            ey = fy / Es
                            et1 = round((((d - c) / c) * 0.003), 4)
                            if et1 > ey:
                                et = "Under Reinfoce (Keruntuhan Tarik)"
                            elif et1 < ey:
                                et = "Over Reinforce (Keruntuhan Tekan)"
                            else:
                                et = "Balance"
                            # FaktorReduksiKekuatan
                            if et1 > 0.005:
                                phi = 0.9
                            elif 0.002 < et1 < 0.005:
                                phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                            else:
                                phi = 0.65
                            # Hitung Momen Nominal
                            Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 4)
                            phiMn1 = round(phi * Mn, 4)
                            if phiMn1 > Mu:
                                phiMn = "Memenuhi"
                            else:
                                phiMn = "TidakMemenuhi"
                            rasiodesain = round(Mu / phiMn1, 3)
                            data = [L, h, b, Mu, d, Asmax, n, Asterpasang, As, rho9, rho, ey, et1, et, phi, Mn, phiMn1, phiMn,rasiodesain]
                            df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                    st.dataframe(df.loc[df["Perbandingan"] == "Memenuhi"])
                    excel = df.to_excel("data.xlsx", index=False)

                    with open("data.xlsx", "rb") as f:
                        excel_bytes = f.read()

                    st.download_button(
                        "Download Excel",
                        excel_bytes,
                        "Inkremental.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key='download-excel'
                    )
                with tab5 :
                    st.header("Analisis Harga")
                    df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)",
                                               "Perbandingan","Harga Beton Rp.","Harga Besi Rp.","Harga Balok Beton Bertulang Rp."])
                    if hitungulang1:
                        awal = np.arange(U1, U2, U3)
                        for H1 in awal:
                            # Perhitungan Tributary Area
                            tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                            # PrliminaryDesain
                            L = 1 * L1
                            h = H1
                            b = (1 / 2 * h)
                            # Hitung Beban
                            qLL = ((sni * tributaryarea))
                            qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                            qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                            qdL = qdL1 + qdL2
                            qu = (1.2 * qdL + 1.6 * qLL)
                            Mu = round(((1 / 8) * (qu * (L ** 2))), 4)
                            # Tulangan
                            if 17 <= fc <= 28:
                                beta_1 = 0.85
                            elif 28 <= fc < 55:
                                beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                            else:
                                beta_1 = 0.65
                            d = h - selimut - sengkang - (D / 2)
                            jd = 0.925 * d
                            As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                            Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                            Asmin2 = round((1.4 / fy) * b * d, 3)
                            Asmax = round(max(As8, Asmin1, Asmin2), 3)
                            # Desain Tulangan
                            n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                            Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                            if Asterpasang > Asmax:
                                As = "Memenuhi"
                            else:
                                As = "TidakMemenuhi"
                            # RasioTulangan
                            Aefektif = b * d
                            rho9 = round((Asterpasang / Aefektif), 3)
                            if rho9 < 0.025:
                                rho = "Memenuhi"
                            else:
                                rho = "TidakMemenuhi"
                            a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                            c = round((a / beta_1), 3)
                            ey = fy / Es
                            et1 = round((((d - c) / c) * 0.003), 4)
                            if et1 > ey:
                                et = "Under Reinfoce (Keruntuhan Tarik)"
                            elif et1 < ey:
                                et = "Over Reinforce (Keruntuhan Tekan)"
                            else:
                                et = "Balance"
                            # FaktorReduksiKekuatan
                            if et1 > 0.005:
                                phi = 0.9
                            elif 0.002 < et1 < 0.005:
                                phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                            else:
                                phi = 0.65
                            # Hitung Momen Nominal
                            Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 4)
                            phiMn1 = round(phi * Mn, 4)
                            if phiMn1 > Mu:
                                phiMn = "Memenuhi"
                            else:
                                phiMn = "TidakMemenuhi"
                            rasiodesain = round(Mu / phiMn1, 3)
                            #AnalisisHargaSatuan
                            #Balok
                            Volume = ((b / 1000) * (h / 1000) * L)
                            BetonperMeter = Volume
                            HargaB = round(BetonperMeter * hargabeton, 0)
                            # TulanganLongitudinal
                            BesiBawah = (beratbajalongitudinal * L * n)
                            HargaD = round(hargabesi * BesiBawah, 0)
                            Jumlah = round(HargaB + HargaD, 0)
                            data = [L, h, b, phiMn, HargaB,  HargaD, Jumlah ]
                            df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                        st.dataframe(df.loc[df["Perbandingan"] == "Memenuhi"])
                        excel = df.to_excel("data.xlsx", index=False)

                        with open("data.xlsx", "rb") as f:
                            excel_bytes = f.read()

                        st.download_button(
                            "Download Excel 2",
                            excel_bytes,
                            "Inkremental 2.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key='download-excel 2'
                        )

                with tab6 :
                    st.header("Tampilan Grafik")
                    df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)","LuasPenampang","n",
                                               "rasiodesain", "Harga Beton Rp.", "Harga Besi Rp.",
                                               "Harga Balok Beton Bertulang Rp."])
                    if hitungulang1:
                        awal = np.arange(U1, U2, U3)
                        for H1 in awal:
                            # Perhitungan Tributary Area
                            tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                            # PrliminaryDesain
                            L = 1 * L1
                            h = H1
                            b = (1 / 2 * h)
                            Luas = h*b
                            # Hitung Beban
                            qLL = ((sni * tributaryarea))
                            qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                            qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                            qdL = qdL1 + qdL2
                            qu = (1.2 * qdL + 1.6 * qLL)
                            Mu = round(((1 / 8) * (qu * (L ** 2))), 4)
                            # Tulangan
                            if 17 <= fc <= 28:
                                beta_1 = 0.85
                            elif 28 <= fc < 55:
                                beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                            else:
                                beta_1 = 0.65
                            d = h - selimut - sengkang - (D / 2)
                            jd = 0.925 * d
                            As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                            Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                            Asmin2 = round((1.4 / fy) * b * d, 3)
                            Asmax = round(max(As8, Asmin1, Asmin2), 3)
                            # Desain Tulangan
                            n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                            Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                            if Asterpasang > Asmax:
                                As = "Memenuhi"
                            else:
                                As = "TidakMemenuhi"
                            # RasioTulangan
                            Aefektif = b * d
                            rho9 = round((Asterpasang / Aefektif), 3)
                            if rho9 < 0.025:
                                rho = "Memenuhi"
                            else:
                                rho = "TidakMemenuhi"
                            a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                            c = round((a / beta_1), 3)
                            ey = fy / Es
                            et1 = round((((d - c) / c) * 0.003), 4)
                            if et1 > ey:
                                et = "Under Reinfoce (Keruntuhan Tarik)"
                            elif et1 < ey:
                                et = "Over Reinforce (Keruntuhan Tekan)"
                            else:
                                et = "Balance"
                            # FaktorReduksiKekuatan
                            if et1 > 0.005:
                                phi = 0.9
                            elif 0.002 < et1 < 0.005:
                                phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                            else:
                                phi = 0.65
                            # Hitung Momen Nominal
                            Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 4)
                            phiMn1 = round(phi * Mn, 4)
                            if phiMn1 > Mu:
                                phiMn = "Memenuhi"
                            else:
                                phiMn = "TidakMemenuhi"
                            rasiodesain = round(Mu / phiMn1, 3)
                            # AnalisisHargaSatuan
                            # Balok
                            Volume = ((b / 1000) * (h / 1000) * L)
                            BetonperMeter = Volume
                            HargaB = round(BetonperMeter * hargabeton, 0)
                            # TulanganLongitudinal
                            BesiBawah = (beratbajalongitudinal * L * n)
                            HargaD = round(hargabesi * BesiBawah, 0)
                            Jumlah = round(HargaB + HargaD, 0)
                            data = [L, h, b, Luas,n,rasiodesain, HargaB, HargaD, Jumlah]
                            df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                            fig = px.scatter(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain",
                                             title="Harga Balok Beton Bertulang vs. Rasio Desain")
                            fig.add_trace(px.line(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain").data[0])
                            fig2 = px.scatter(df, x="LuasPenampang", y="rasiodesain",
                                              title="LuasPenampang vs. Rasio Desain")
                            fig2.add_trace(px.line(df, x="LuasPenampang", y="rasiodesain").data[0])
                            fig3 = px.scatter(df, x="Harga Balok Beton Bertulang Rp.", y="LuasPenampang",
                                              title="Harga Balok Beton Bertulang Rp. vs. LuasPenampang")
                            fig3.add_trace(px.line(df, x="Harga Balok Beton Bertulang Rp.", y="LuasPenampang").data[0])
                        st.plotly_chart(fig)
                        st.plotly_chart(fig2)
                        st.plotly_chart(fig3)
                        with pd.ExcelWriter('graph_data.xlsx') as writer:
                            df.to_excel(writer, index=False)
                        st.download_button("Download Graph Data", open('graph_data.xlsx', 'rb').read(),
                                           file_name='graph_data.xlsx',
                                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                with tab7 :
                    st.header("Tampilan Grafik Nilai Jumlah Tulangan Tidak Di Bulatkan Ke Atas")
                    df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)","LuasPenampang","n",
                                               "rasiodesain", "Harga Beton Rp.", "Harga Besi Rp.",
                                               "Harga Balok Beton Bertulang Rp."])
                    if hitungulang1:
                        awal = np.arange(U1, U2, U3)
                        for H1 in awal:
                            # Perhitungan Tributary Area
                            tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                            # PrliminaryDesain
                            L = 1 * L1
                            h = H1
                            b = (1 / 2 * h)
                            Luas = h*b
                            # Hitung Beban
                            qLL = ((sni * tributaryarea))
                            qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                            qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                            qdL = qdL1 + qdL2
                            qu = (1.2 * qdL + 1.6 * qLL)
                            Mu = round(((1 / 8) * (qu * (L ** 2))), 4)
                            # Tulangan
                            if 17 <= fc <= 28:
                                beta_1 = 0.85
                            elif 28 <= fc < 55:
                                beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                            else:
                                beta_1 = 0.65
                            d = h - selimut - sengkang - (D / 2)
                            jd = 0.925 * d
                            As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                            Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                            Asmin2 = round((1.4 / fy) * b * d, 3)
                            Asmax = round(max(As8, Asmin1, Asmin2), 3)
                            # Desain Tulangan
                            n = ((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                            Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                            if Asterpasang > Asmax:
                                As = "Memenuhi"
                            else:
                                As = "TidakMemenuhi"
                            # RasioTulangan
                            Aefektif = b * d
                            rho9 = round((Asterpasang / Aefektif), 3)
                            if rho9 < 0.025:
                                rho = "Memenuhi"
                            else:
                                rho = "TidakMemenuhi"
                            a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                            c = round((a / beta_1), 3)
                            ey = fy / Es
                            et1 = round((((d - c) / c) * 0.003), 4)
                            if et1 > ey:
                                et = "Under Reinfoce (Keruntuhan Tarik)"
                            elif et1 < ey:
                                et = "Over Reinforce (Keruntuhan Tekan)"
                            else:
                                et = "Balance"
                            # FaktorReduksiKekuatan
                            if et1 > 0.005:
                                phi = 0.9
                            elif 0.002 < et1 < 0.005:
                                phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                            else:
                                phi = 0.65
                            # Hitung Momen Nominal
                            Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 4)
                            phiMn1 = round(phi * Mn, 4)
                            if phiMn1 > Mu:
                                phiMn = "Memenuhi"
                            else:
                                phiMn = "TidakMemenuhi"
                            rasiodesain = round(Mu / phiMn1, 3)
                            # AnalisisHargaSatuan
                            # Balok
                            Volume = ((b / 1000) * (h / 1000) * L)
                            BetonperMeter = Volume
                            HargaB = round(BetonperMeter * hargabeton, 0)
                            # TulanganLongitudinal
                            BesiBawah = (beratbajalongitudinal * L * n)
                            HargaD = round(hargabesi * BesiBawah, 0)
                            Jumlah = round(HargaB + HargaD, 0)
                            data = [L, h, b, Luas,n,rasiodesain, HargaB, HargaD, Jumlah]
                            df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                            fig = px.scatter(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain",
                                             title="Harga Balok Beton Bertulang vs. Rasio Desain")
                            fig.add_trace(px.line(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain").data[0])
                            fig2 = px.scatter(df, x="LuasPenampang", y="rasiodesain",
                                              title="LuasPenampang vs. Rasio Desain")
                            fig2.add_trace(px.line(df, x="LuasPenampang", y="rasiodesain").data[0])
                            fig3 = px.scatter(df, x="Harga Balok Beton Bertulang Rp.", y="LuasPenampang",
                                              title="Harga Balok Beton Bertulang Rp. vs. LuasPenampang")
                            fig3.add_trace(px.line(df, x="Harga Balok Beton Bertulang Rp.", y="LuasPenampang").data[0])
                        st.plotly_chart(fig)
                        st.plotly_chart(fig2)
                        st.plotly_chart(fig3)
                        with pd.ExcelWriter('graph_data.xlsx') as writer:
                            df.to_excel(writer, index=False)
                        st.download_button("Download Graph Data", open('graph_data.xlsx', 'rb').read(),
                                           file_name='graph_data.xlsx',
                                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#MU PAKE LEBAR TRIBUTARY
if Awal == "Optimasi Desain 1":
        if options == "Asumsi Tulangan Dua Lapis":
            st.header("ANALISIS PENAMPANG BALOK BETON BERTULANG METODE INKREMENTAL")
            tab6, tab7, tab8, tab9, tab10,tab11, tab12= st.tabs(["List Input", "Input Angka", "Analisis Awal", "Inkremental","Harga Material","Grafik1","Grafik2"])
            with tab6:
                st.header("NILAI - NILAI YANG DIBUTUHKAN")
                st.subheader("Jenis Tulangan")
                image8 = Image.open('BetonPolos.png')
                st.image(image8)
                image9 = Image.open('BetonUlir.png')
                st.image(image9)
                st.subheader("Harga Mutu Beton Per Meter Kubik")
                image10 = Image.open('HARGABETON.PNG')
                st.image(image10)
                st.subheader("Harga Baja Per Meter")
                image12 = Image.open('BajaHarga.PNG')
                st.image(image12)
                with tab7:
                    st.header("DENAH PERANCANGAN")
                    image11 = Image.open('Denah.png')
                    st.image(image11)
                    st.subheader("INPUT DATA PERANCANGAN")
                    # Input Pembagian kolom
                    col7, col8 = st.columns(2)
                    with col7:
                        L1 = st.number_input("Panjang Bentang Balok (m) ", value=7)
                        D = st.number_input("Nilai Diameter Longitudinal (D) (mm) = ", value=19)
                        selimut = st.number_input("Nilai Tebal Selimut (mm) = ", value=40)
                        sengkang = st.number_input("Nilai diameter sengkang (Dsengkang) (mm) = ", value=10)
                        sni = st.number_input("Nilai Beban hidup Struktur (LL) (kN/m^2) = ", value=6)
                        fc = st.number_input("Nilai Mutu beton (Fc') (Mpa) = ", value=30)
                        fy = st.number_input("Nilai Mutu Baja (Fy) (Mpa) = ", value=420)
                        tebalplat = st.number_input("Tebal Pelat Beton (mm) =", value=120)

                    with col8:
                        beratbeton = st.number_input("Berat Beton (kN/m^3) =", value=24)
                        jarakantartulangan = st.number_input("Jarak Antar Tulangan (mm) =", value=25)
                        beratbajalongitudinal = (st.number_input(" Berat Baja (Berat Nominal Per meter)= ", value=2.226))
                        hargabeton = st.number_input("Masukan Harga Beton (per - m^3) =", value=995000)
                        hargabesi = st.number_input("Masukan Harga Baja (per-kg) = ", value=9477)
                        lebartributaryatas = st.number_input("Lebartributary Atas (m) = ", value=5)
                        lebartributarybawah = st.number_input("Lebartributary Bawah (m) = ", value=5)

                    # Asumsi
                    Es = 200000
                    hitung = st.button("EXECUTE")

                    with tab8:
                        st.header("Analisis Awal Tulangan Dua Lapis")
                        if hitung:
                            # Perhitungan Tributary Area
                            tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                            # Preliminary Desain
                            L = 1 * L1
                            h = math.ceil((L / 16) * 1000)
                            b = (1 / 2 * h)
                            # Hitung Beban
                            qLL = ((sni * tributaryarea))
                            qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                            qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                            qdL = qdL1 + qdL2
                            qu = (1.2 * qdL + 1.6 * qLL)
                            Mu = round(((1 / 8) * (qu * (L ** 2))), 4)
                            # Tulangan
                            if 17 <= fc <= 28:
                                beta_1 = 0.85
                            elif 28 <= fc < 55:
                                beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                            else:
                                beta_1 = 0.65
                            dt = h - selimut - sengkang - D - (jarakantartulangan/2)
                            jd = 0.925 * dt
                            As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                            Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * dt, 3)
                            Asmin2 = round((1.4 / fy) * b * dt, 3)
                            Asmax = round(max(As8, Asmin1, Asmin2), 3)
                            # Desain Tulangan
                            n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                            Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 4)
                            if Asterpasang > Asmax:
                                As = "Memenuhi"
                            else:
                                As = "TidakMemenuhi"
                            # RasioTulangan
                            Aefektif = b * dt
                            rho9 = round((Asterpasang / Aefektif), 3)
                            if rho9 < 0.025:
                                rho = "Memenuhi"
                            else:
                                rho = "TidakMemenuhi"
                            a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                            c = round((a / beta_1), 3)
                            ey = fy / Es
                            et1 = round((((dt - c) / c) * 0.003), 4)
                            if et1 > ey:
                                et = "Under Reinfoce (Keruntuhan Tarik)"
                            elif et1 < ey:
                                et = "Over Reinforce (Keruntuhan Tekan)"
                            else:
                                et = "Balance"
                            # FaktorReduksiKekuatan
                            if et1 > 0.005:
                                phi = 0.9
                            elif 0.002 < et1 < 0.005:
                                phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                            else:
                                phi = 0.65
                            # Hitung Momen Nominal
                            Mn = round((Asterpasang * fy * (dt - a / 2)) / 1000000, 4)
                            phiMn1 = round(phi * Mn, 4)
                            if phiMn1 > Mu:
                                phiMn = "Memenuhi"
                            else:
                                phiMn = "TidakMemenuhi"
                            rasiodesain = round(Mu / phiMn1, 3)
                            df = {"L (m)": L, "h (mm)": h, "b (mm)": b, "Mu": Mu, "d (mm)": dt, "Asmax (mm^2)": Asmax,
                                  "n(buah)": n, "Asterpasang(mm^2)": Asterpasang, "As": As, "rho": rho9,
                                  "SyaratRasio": rho, "ey": ey, "et": et1, "Jenis Keruntuhan": et, "phi": phi, "Mn": Mn,
                                  "phiMn": phiMn1, "PerBandingan": phiMn, "Rasio Desain": rasiodesain}
                            st.dataframe(df, 950, 700)
                    with tab9:
                        st.header("Analisis Tulangan Tunggal Dua Lapis")
                        image9 = Image.open('Tulangan2Lapis.png')
                        st.image(image9)
                        df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)", "Mu", "dt (mm)", "Asmax (mm^2)", "n(buah)",
                                               "Asterpasang(mm^2)", "As", "rho", "SyaratRasio", "ey", "et",
                                               "Jenis Keruntuhan", "phi", "Mn", "phiMn", "Perbandingan",
                                               "rasiodesain"])
                        U1 = st.number_input("Nilai Batas Bawah =")
                        U2 = st.number_input("Nilai Batas Atas=")
                        U3 = st.number_input("Ingkremental=")
                        hitungulang1 = st.button("EXCECUTE")
                        if hitungulang1:
                            awal = np.arange(U1, U2, U3)
                            for H1 in awal:
                                # Perhitungan Tributary Area
                                tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                                # PrliminaryDesain
                                L = 1 * L1
                                h = H1
                                b = (1 / 2 * h)
                                # Hitung Beban
                                qLL = ((sni * tributaryarea))
                                qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                                qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                                qdL = qdL1 + qdL2
                                qu = (1.2 * qdL + 1.6 * qLL)
                                Mu = round(((1 / 8) * (qu * (L ** 2))), 4)
                                # Tulangan
                                if 17 <= fc <= 28:
                                    beta_1 = 0.85
                                elif 28 <= fc < 55:
                                    beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                                else:
                                    beta_1 = 0.65
                                dt = h - selimut - sengkang - D - (jarakantartulangan/2)
                                jd = 0.925 * dt
                                As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                                Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * dt, 3)
                                Asmin2 = round((1.4 / fy) * b * dt, 3)
                                Asmax = round(max(As8, Asmin1, Asmin2), 3)
                                # Desain Tulangan
                                n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                                Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 4)
                                if Asterpasang > Asmax:
                                    As = "Memenuhi"
                                else:
                                    As = "TidakMemenuhi"
                                # RasioTulangan
                                Aefektif = b * dt
                                rho9 = round((Asterpasang / Aefektif), 3)
                                if rho9 < 0.025:
                                    rho = "Memenuhi"
                                else:
                                    rho = "TidakMemenuhi"
                                a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                                c = round((a / beta_1), 3)
                                ey = fy / Es
                                et1 = round((((dt - c) / c) * 0.003), 4)
                                if et1 > ey:
                                    et = "Under Reinfoce (Keruntuhan Tarik)"
                                elif et1 < ey:
                                    et = "Over Reinforce (Keruntuhan Tekan)"
                                else :
                                    et = "Balance"
                                # FaktorReduksiKekuatan
                                if et1 > 0.005:
                                    phi = 0.9
                                elif 0.002 < et1 < 0.005:
                                    phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                                else:
                                    phi = 0.65
                                # Hitung Momen Nominal
                                Mn = round((Asterpasang * fy * (dt - a / 2)) / 1000000, 3)
                                phiMn1 = round(phi * Mn, 3)
                                if phiMn1 > Mu:
                                    phiMn = "Memenuhi"
                                else:
                                    phiMn = "TidakMemenuhi"
                                rasiodesain = round(Mu / phiMn1, 3)
                                data = [L, h, b, Mu, dt, Asmax, n, Asterpasang, As, rho9, rho, ey, et1, et, phi, Mn,
                                        phiMn1, phiMn, rasiodesain]
                                df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                        st.dataframe(df.loc[df["Perbandingan"] == "Memenuhi"])
                        excel = df.to_excel("data.xlsx", index=False)

                        with open("data.xlsx", "rb") as f:
                            excel_bytes = f.read()

                        st.download_button(
                            "Download Excel",
                            excel_bytes,
                            "Inkremental.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key='download-excel'
                        )
                    with tab10:
                        st.header("Analisis Harga")
                        df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)",
                                                   "Perbandingan", "Harga Beton Rp.", "Harga Besi Rp.",
                                                   "Harga Balok Beton Bertulang Rp."])
                        if hitungulang1:
                            awal = np.arange(U1, U2, U3)
                            for H1 in awal:
                                # Perhitungan Tributary Area
                                tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                                # PrliminaryDesain
                                L = 1 * L1
                                h = H1
                                b = (1 / 2 * h)
                                # Hitung Beban
                                qLL = ((sni * tributaryarea))
                                qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                                qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                                qdL = qdL1 + qdL2
                                qu = (1.2 * qdL + 1.6 * qLL)
                                Mu = round(((1 / 8) * (qu * (L ** 2))), 3)
                                # Tulangan
                                if 17 <= fc <= 28:
                                    beta_1 = 0.85
                                elif 28 <= fc < 55:
                                    beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                                else:
                                    beta_1 = 0.65
                                dt = h - selimut - sengkang - D - (jarakantartulangan/2)
                                jd = 0.925 * dt
                                As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                                Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * dt, 3)
                                Asmin2 = round((1.4 / fy) * b * dt, 3)
                                Asmax = round(max(As8, Asmin1, Asmin2), 3)
                                # Desain Tulangan
                                n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                                Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                                if Asterpasang > Asmax:
                                    As = "Memenuhi"
                                else:
                                    As = "TidakMemenuhi"
                                # RasioTulangan
                                Aefektif = b * dt
                                rho9 = round((Asterpasang / Aefektif), 3)
                                if rho9 < 0.025:
                                    rho = "Memenuhi"
                                else:
                                    rho = "TidakMemenuhi"
                                a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                                c = round((a / beta_1), 3)
                                ey = fy / Es
                                et1 = round((((dt - c) / c) * 0.003), 3)
                                if et1 > ey:
                                    et = "Under Reinfoce (Keruntuhan Tarik)"
                                elif et1 < ey:
                                    et = "Over Reinforce (Keruntuhan Tekan)"
                                else:
                                    et = "Balance"
                                # FaktorReduksiKekuatan
                                if et1 > 0.005:
                                    phi = 0.9
                                elif 0.002 < et1 < 0.005:
                                    phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                                else:
                                    phi = 0.65
                                # Hitung Momen Nominal
                                Mn = round((Asterpasang * fy * (dt - a / 2))/1000000, 0)
                                phiMn1 = phi * Mn
                                if phiMn1 > Mu:
                                    phiMn = "Memenuhi"
                                else:
                                    phiMn = "TidakMemenuhi"
                                rasiodesain = round(Mu / phiMn1, 3)
                                # AnalisisHargaSatuan
                                # Balok
                                Volume = round((b / 1000) * (h / 1000) * L, 3)
                                BetonperMeter = Volume
                                HargaB = round (BetonperMeter * hargabeton,0)
                                # TulanganLongitudinal
                                BesiBawah = (beratbajalongitudinal * L * n)
                                HargaD = round (hargabesi * BesiBawah,0)
                                Jumlah = round(HargaB + HargaD,0)
                                data = [L, h, b, phiMn, HargaB, HargaD, Jumlah]
                                df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                        st.dataframe(df.loc[df["Perbandingan"] == "Memenuhi"])
                        excel = df.to_excel("data.xlsx", index=False)

                        with open("data.xlsx", "rb") as f:
                            excel_bytes = f.read()

                        st.download_button(
                            "Download Excel 2",
                            excel_bytes,
                            "Inkremental 2.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key='download-excel 2'
                        )
                    with tab11:
                        st.header("Tampilan Grafik")

                        df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)", "LuasPenampang","n",
                                                   "rasiodesain", "Harga Beton Rp.", "Harga Besi Rp.",
                                                   "Harga Balok Beton Bertulang Rp."])
                        if hitungulang1:
                            awal = np.arange(U1, U2, U3)
                            for H1 in awal:
                                # Perhitungan Tributary Area
                                tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                                # PrliminaryDesain
                                L = 1 * L1
                                h = H1
                                b = (1 / 2 * h)
                                Luas = h*b
                                # Hitung Beban
                                qLL = ((sni * tributaryarea))
                                qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                                qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                                qdL = qdL1 + qdL2
                                qu = (1.2 * qdL + 1.6 * qLL)
                                Mu = round(((1 / 8) * (qu * (L ** 2))), 3)
                                # Tulangan
                                if 17 <= fc <= 28:
                                    beta_1 = 0.85
                                elif 28 <= fc < 55:
                                    beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                                else:
                                    beta_1 = 0.65
                                dt = h - selimut - sengkang - D - (jarakantartulangan/2)
                                jd = 0.925 * dt
                                As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                                Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * dt, 3)
                                Asmin2 = round((1.4 / fy) * b * dt, 3)
                                Asmax = round(max(As8, Asmin1, Asmin2), 3)
                                # Desain Tulangan
                                n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                                Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                                if Asterpasang > Asmax:
                                    As = "Memenuhi"
                                else:
                                    As = "TidakMemenuhi"
                                # RasioTulangan
                                Aefektif = b * dt
                                rho9 = round((Asterpasang / Aefektif), 3)
                                if rho9 < 0.025:
                                    rho = "Memenuhi"
                                else:
                                    rho = "TidakMemenuhi"
                                a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                                c = round((a / beta_1), 3)
                                ey = fy / Es
                                et1 = round((((dt - c) / c) * 0.003), 3)
                                if et1 > ey:
                                    et = "Under Reinfoce (Keruntuhan Tarik)"
                                elif et1 < ey:
                                    et = "Over Reinforce (Keruntuhan Tekan)"
                                else:
                                    et = "Balance"
                                # FaktorReduksiKekuatan
                                if et1 > 0.005:
                                    phi = 0.9
                                elif 0.002 < et1 < 0.005:
                                    phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                                else:
                                    phi = 0.65
                                # Hitung Momen Nominal
                                Mn = round((Asterpasang * fy * (dt - a / 2))/1000000, 0)
                                phiMn1 = phi * Mn
                                if phiMn1 > Mu:
                                    phiMn = "Memenuhi"
                                else:
                                    phiMn = "TidakMemenuhi"
                                rasiodesain = round(Mu / phiMn1, 3)
                                # AnalisisHargaSatuan
                                # Balok
                                Volume = round((b / 1000) * (h / 1000) * L, 3)
                                BetonperMeter = Volume
                                HargaB = round (BetonperMeter * hargabeton,0)
                                # TulanganLongitudinal
                                BesiBawah = (beratbajalongitudinal * L * n)
                                HargaD = round (hargabesi * BesiBawah,0)
                                Jumlah = round(HargaB + HargaD,0)
                                data = [L, h, b,Luas,n, rasiodesain, HargaB, HargaD, Jumlah]
                                df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                                fig = px.scatter(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain",
                                                 title="Harga Balok Beton Bertulang vs. Rasio Desain")
                                fig.add_trace(px.line(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain").data[0])
                                fig2 = px.scatter(df, x="LuasPenampang", y="rasiodesain",
                                                  title="LuasPenampang vs. Rasio Desain")
                                fig2.add_trace(px.line(df, x="LuasPenampang", y="rasiodesain").data[0])
                                fig3 = px.scatter(df, x="Harga Balok Beton Bertulang Rp.", y="LuasPenampang",
                                                  title="Harga Balok Beton Bertulang Rp. vs. LuasPenampang")
                                fig3.add_trace(px.line(df, x="Harga Balok Beton Bertulang Rp.", y="LuasPenampang").data[0])
                            st.plotly_chart(fig)
                            st.plotly_chart(fig2)
                            st.plotly_chart(fig3)
                            with pd.ExcelWriter('graph_data.xlsx') as writer:
                                df.to_excel(writer, index=False)
                            st.download_button("Download Graph Data", open('graph_data.xlsx', 'rb').read(),
                                               file_name='graph_data.xlsx',
                                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    with tab11:
                        st.header("Tampilan Grafik Nilai Jumlah Tulangan Tidak Di Bulatkan Ke Atas")

                        df = pd.DataFrame(columns=["L (m)", "h (mm)", "b (mm)", "LuasPenampang","n",
                                                   "rasiodesain", "Harga Beton Rp.", "Harga Besi Rp.",
                                                   "Harga Balok Beton Bertulang Rp."])
                        if hitungulang1:
                            awal = np.arange(U1, U2, U3)
                            for H1 in awal:
                                # Perhitungan Tributary Area
                                tributaryarea = (lebartributaryatas / 2) + (lebartributarybawah / 2)
                                # PrliminaryDesain
                                L = 1 * L1
                                h = H1
                                b = (1 / 2 * h)
                                Luas = h*b
                                # Hitung Beban
                                qLL = ((sni * tributaryarea))
                                qdL1 = ((b / 1000) * (h / 1000) * beratbeton)
                                qdL2 = ((tebalplat / 1000) * beratbeton * tributaryarea)
                                qdL = qdL1 + qdL2
                                qu = (1.2 * qdL + 1.6 * qLL)
                                Mu = round(((1 / 8) * (qu * (L ** 2))), 3)
                                # Tulangan
                                if 17 <= fc <= 28:
                                    beta_1 = 0.85
                                elif 28 <= fc < 55:
                                    beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                                else:
                                    beta_1 = 0.65
                                dt = h - selimut - sengkang - D - (jarakantartulangan/2)
                                jd = 0.925 * dt
                                As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                                Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * dt, 3)
                                Asmin2 = round((1.4 / fy) * b * dt, 3)
                                Asmax = round(max(As8, Asmin1, Asmin2), 3)
                                # Desain Tulangan
                                n = ((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                                Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                                if Asterpasang > Asmax:
                                    As = "Memenuhi"
                                else:
                                    As = "TidakMemenuhi"
                                # RasioTulangan
                                Aefektif = b * dt
                                rho9 = round((Asterpasang / Aefektif), 3)
                                if rho9 < 0.025:
                                    rho = "Memenuhi"
                                else:
                                    rho = "TidakMemenuhi"
                                a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                                c = round((a / beta_1), 3)
                                ey = fy / Es
                                et1 = round((((dt - c) / c) * 0.003), 3)
                                if et1 > ey:
                                    et = "Under Reinfoce (Keruntuhan Tarik)"
                                elif et1 < ey:
                                    et = "Over Reinforce (Keruntuhan Tekan)"
                                else:
                                    et = "Balance"
                                # FaktorReduksiKekuatan
                                if et1 > 0.005:
                                    phi = 0.9
                                elif 0.002 < et1 < 0.005:
                                    phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                                else:
                                    phi = 0.65
                                # Hitung Momen Nominal
                                Mn = round((Asterpasang * fy * (dt - a / 2))/1000000, 0)
                                phiMn1 = phi * Mn
                                if phiMn1 > Mu:
                                    phiMn = "Memenuhi"
                                else:
                                    phiMn = "TidakMemenuhi"
                                rasiodesain = round(Mu / phiMn1, 3)
                                # AnalisisHargaSatuan
                                # Balok
                                Volume = round((b / 1000) * (h / 1000) * L, 3)
                                BetonperMeter = Volume
                                HargaB = round (BetonperMeter * hargabeton,0)
                                # TulanganLongitudinal
                                BesiBawah = (beratbajalongitudinal * L * n)
                                HargaD = round (hargabesi * BesiBawah,0)
                                Jumlah = round(HargaB + HargaD,0)
                                data = [L, h, b,Luas,n, rasiodesain, HargaB, HargaD, Jumlah]
                                df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                                fig = px.scatter(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain",
                                                 title="Harga Balok Beton Bertulang vs. Rasio Desain")
                                fig.add_trace(px.line(df, x="Harga Balok Beton Bertulang Rp.", y="rasiodesain").data[0])
                                fig2 = px.scatter(df, x="LuasPenampang", y="rasiodesain",
                                                  title="LuasPenampang vs. Rasio Desain")
                                fig2.add_trace(px.line(df, x="LuasPenampang", y="rasiodesain").data[0])
                            st.plotly_chart(fig)
                            st.plotly_chart(fig2)
                            with pd.ExcelWriter('graph_data.xlsx') as writer:
                                df.to_excel(writer, index=False)
                            st.download_button("Download Graph Data", open('graph_data.xlsx', 'rb').read(),
                                               file_name='graph_data.xlsx',
                                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#Optimasi Desain 2
if Awal == "Optimasi Desain 2":
    options = st.sidebar.selectbox("", ["Asumsi Tulangan Satu Lapis"])
    if options == "Asumsi Tulangan Satu Lapis":
        st.header("ANALISIS PENAMPANG BETON BERTULANG METODE INKREMENTAL")
        tab1, tab2, tab3, tab4, tab5= st.tabs(["List Input","Input Angka", "Inkremental", "Grafik1", "Grafik2"])
        with tab1:
            st.header("NILAI - NILAI YANG DIBUTUHKAN")
            st.subheader("Jenis Tulangan")
            image8 = Image.open('BetonPolos.png')
            st.image(image8)
            image9 = Image.open('BetonUlir.png')
            st.image(image9)
            with tab2:
                st.header("Analisis Tulangan Tunggal Satu Lapis")
                image9 = Image.open('Tulangan1Lapis.png')
                st.image(image9)
                st.subheader("INPUT DATA PERANCANGAN")
                #Input Pembagian kolom
                col3, col4 = st.columns(2)
                with col3 :
                    U1 = st.number_input("Nilai Batas Bawah =",value=600)
                    U2 = st.number_input("Nilai Batas Atas=",value =1050)
                    U3 = st.number_input("Ingkremental=",value=50 )
                    selimut = st.number_input("Nilai Tebal Selimut (mm) = ", value=40)
                    sengkang = st.number_input("Nilai diameter sengkang (Dsengkang) (mm) = ", value=10)

                with col4:
                    D = st.number_input("Nilai Diameter Longitudinal ((D) mm) = ", value=19)
                    Mu = st.number_input("Nilai Momen Ultimate (kNm') = ", value=800)
                    fc = st.number_input("Nilai Mutu beton (Fc') (Mpa) = ", value=30)
                    fy = st.number_input("Nilai Mutu Baja (Fy) = ", value=420)
                #Asumsi
                Es = 200000
                hitung = st.button ("EXECUTE")
                with tab3:
                    df = pd.DataFrame(columns=[ "h (mm)", "b (mm)", "Mu", "d (mm)", "Asmax (mm^2)", "n(buah)",
                                               "Asterpasang(mm^2)", "As", "rho", "SyaratRasio", "ey", "et",
                                               "Jenis Keruntuhan", "phi", "Mn", "phiMn", "PerBandingan",
                                               "Rasio Desain"])
                #inputColom Ingkrement
                    if hitung:
                        awal = np.arange(U1,U2,U3)
                        for H1 in awal :
                            #PrliminaryDesain
                            h = H1
                            b = (1 / 2 * h)
                            # Tulangan
                            if 17 <= fc <= 28:
                                beta_1 = 0.85
                            elif 28 <= fc < 55:
                                beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                            else:
                                beta_1 = 0.65
                            d = h - selimut - sengkang - (D / 2)
                            jd = 0.925 * d
                            As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                            Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                            Asmin2 = round((1.4 / fy) * b * d, 3)
                            Asmax = round(max(As8, Asmin1, Asmin2), 3)
                            # Desain Tulangan
                            n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                            Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 4)
                            if Asterpasang > Asmax:
                                As = "Memenuhi"
                            else:
                                As = "TidakMemenuhi"
                            # RasioTulangan
                            Aefektif = b * d
                            rho9 = round((Asterpasang / Aefektif), 3)
                            if rho9 < 0.025:
                                rho = "Memenuhi"
                            else:
                                rho = "TidakMemenuhi"
                            a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                            c = round((a / beta_1), 3)
                            ey = fy / Es
                            et1 = round((((d - c) / c) * 0.003), 4)
                            if et1 > ey:
                                et = "Under Reinfoce (Keruntuhan Tarik)"
                            elif et1 < ey:
                                et = "Over Reinforce (Keruntuhan Tekan)"
                            else:
                                et = "Balance"
                            # FaktorReduksiKekuatan
                            if et1 > 0.005:
                                phi = 0.9
                            elif 0.002< et1 < 0.005:
                                phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                            else :
                                phi = 0.65
                            # Hitung Momen Nominal
                            Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 4)
                            phiMn1 = round(phi * Mn, 4)
                            if phiMn1 > Mu:
                                phiMn = "Memenuhi"
                            else:
                                phiMn = "TidakMemenuhi"
                            rasiodesain = round(Mu / phiMn1, 3)
                            data = [h, b, Mu, d, Asmax, n, Asterpasang, As, rho9, rho, ey, et1, et, phi, Mn, phiMn1,
                                    phiMn, rasiodesain]
                            df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                    st.dataframe(df.loc[df["PerBandingan"] == "Memenuhi"])
                    excel = df.to_excel("data.xlsx", index=False)

                    with open("data.xlsx", "rb") as f:
                        excel_bytes = f.read()

                    st.download_button(
                        "Download Excel",
                        excel_bytes,
                        "Inkremental.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key='download-excel'
                    )

                    with tab4:
                        st.header("Tampilan Grafik")
                        df = pd.DataFrame(columns=[ "h (mm)", "b (mm)","LuasPenampang","n",
                                                   "rasiodesain"])
                        if hitung:
                            awal = np.arange(U1, U2, U3)
                            for H1 in awal:
                                #PrliminaryDesain
                                h = H1
                                b = (1 / 2 * h)
                                Luas = h*b
                                # Tulangan
                                if 17 <= fc <= 28:
                                    beta_1 = 0.85
                                elif 28 <= fc < 55:
                                    beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                                else:
                                    beta_1 = 0.65
                                d = h - selimut - sengkang - (D / 2)
                                jd = 0.925 * d
                                As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                                Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                                Asmin2 = round((1.4 / fy) * b * d, 3)
                                Asmax = round(max(As8, Asmin1, Asmin2), 3)
                                # Desain Tulangan
                                n = math.ceil((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                                Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                                if Asterpasang > Asmax:
                                    As = "Memenuhi"
                                else:
                                    As = "TidakMemenuhi"
                                # RasioTulangan
                                Aefektif = b * d
                                rho9 = round((Asterpasang / Aefektif), 3)
                                if rho9 < 0.025:
                                    rho = "Memenuhi"
                                else:
                                    rho = "TidakMemenuhi"
                                a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                                c = round((a / beta_1), 3)
                                ey = fy / Es
                                et1 = round((((d - c) / c) * 0.003), 4)
                                if et1 > ey:
                                    et = "Under Reinfoce (Keruntuhan Tarik)"
                                elif et1 < ey:
                                    et = "Over Reinforce (Keruntuhan Tekan)"
                                else:
                                    et = "Balance"
                                # FaktorReduksiKekuatan
                                if et1 > 0.005:
                                    phi = 0.9
                                elif 0.002 < et1 < 0.005:
                                    phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                                else:
                                    phi = 0.65
                                # Hitung Momen Nominal
                                Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 3)
                                phiMn1 = phi * Mn
                                if phiMn1 > Mu:
                                    phiMn = "Memenuhi"
                                else:
                                    phiMn = "TidakMemenuhi"
                                rasiodesain = round(Mu / phiMn1, 3)

                                data = [h, b,Luas,n, rasiodesain]
                                df = df.append(pd.Series(data, index=df.columns), ignore_index=True)

                                fig2 = px.scatter(df, x="LuasPenampang", y="rasiodesain",
                                                 title="LuasPenampang vs. Rasio Desain")
                                fig2.add_trace(px.line(df, x="LuasPenampang", y="rasiodesain").data[0])


                            st.plotly_chart(fig2)
                            with pd.ExcelWriter('graph_data.xlsx') as writer:
                                df.to_excel(writer, index=False)
                            st.download_button("Download Graph Data", open('graph_data.xlsx', 'rb').read(),
                                               file_name='graph_data.xlsx',
                                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    with tab5:
                        st.header("Tampilan Grafik Nilai Jumlah Tulangan Tidak Di Bulatkan Ke Atas")
                        df = pd.DataFrame(columns=[ "h (mm)", "b (mm)","LuasPenampang","n",
                                                   "rasiodesain"])
                        if hitung:
                            awal = np.arange(U1, U2, U3)
                            for H1 in awal:
                                #PrliminaryDesain
                                h = H1
                                b = (1 / 2 * h)
                                Luas = h*b
                                # Tulangan
                                if 17 <= fc <= 28:
                                    beta_1 = 0.85
                                elif 28 <= fc < 55:
                                    beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                                else:
                                    beta_1 = 0.65
                                d = h - selimut - sengkang - (D / 2)
                                jd = 0.925 * d
                                As8 = (Mu * 1000000) / (0.9 * 420 * jd)
                                Asmin1 = round(((0.25 * (fc ** 0.5)) / fy) * b * d, 3)
                                Asmin2 = round((1.4 / fy) * b * d, 3)
                                Asmax = round(max(As8, Asmin1, Asmin2), 3)
                                # Desain Tulangan
                                n = ((Asmax / ((1 / 4) * 3.1416 * (D ** 2))))
                                Asterpasang = round(n * 1 / 4 * 3.1416 * ((D) ** 2), 3)
                                if Asterpasang > Asmax:
                                    As = "Memenuhi"
                                else:
                                    As = "TidakMemenuhi"
                                # RasioTulangan
                                Aefektif = b * d
                                rho9 = round((Asterpasang / Aefektif), 3)
                                if rho9 < 0.025:
                                    rho = "Memenuhi"
                                else:
                                    rho = "TidakMemenuhi"
                                a = round((Asterpasang * fy) / (0.85 * fc * b), 3)
                                c = round((a / beta_1), 3)
                                ey = fy / Es
                                et1 = round((((d - c) / c) * 0.003), 4)
                                if et1 > ey:
                                    et = "Under Reinfoce (Keruntuhan Tarik)"
                                elif et1 < ey:
                                    et = "Over Reinforce (Keruntuhan Tekan)"
                                else:
                                    et = "Balance"
                                # FaktorReduksiKekuatan
                                if et1 > 0.005:
                                    phi = 0.9
                                elif 0.002 < et1 < 0.005:
                                    phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                                else:
                                    phi = 0.65
                                # Hitung Momen Nominal
                                Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 3)
                                phiMn1 = phi * Mn
                                if phiMn1 > Mu:
                                    phiMn = "Memenuhi"
                                else:
                                    phiMn = "TidakMemenuhi"
                                rasiodesain = round(Mu / phiMn1, 3)

                                data = [h, b,Luas,n, rasiodesain]
                                df = df.append(pd.Series(data, index=df.columns), ignore_index=True)

                                fig2 = px.scatter(df, x="LuasPenampang", y="rasiodesain",
                                                 title="LuasPenampang vs. Rasio Desain")
                                fig2.add_trace(px.line(df, x="LuasPenampang", y="rasiodesain").data[0])


                            st.plotly_chart(fig2)
                            with pd.ExcelWriter('graph_data.xlsx') as writer:
                                df.to_excel(writer, index=False)
                            st.download_button("Download Graph Data", open('graph_data.xlsx', 'rb').read(),
                                               file_name='graph_data.xlsx',
                                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#CEK KAPASITAS
if Awal == "Cek Kapasitas":
    st.header("ANALISIS PENAMPANG BETON BERTULANG METODE INKREMENTAL")
    tab2, tab3 = st.tabs(["Input Angka", "HASIL"])
    with tab2:
        st.subheader("INPUT DATA")
        # Input Pembagian kolom
        col3, col4 = st.columns(2)
        with col3:
            h2 = st.number_input("Tinggi Penampang Balok =")
            b2 = st.number_input("Lebar Penampang Balok = ")
            D = st.number_input("Nilai Diameter Longitudinal (D) = ")
            d = st.number_input("Nilai Tinggi Efektif Balok (d) = ")
        with col4:
            fc = st.number_input("Nilai Mutu beton (Fc') = ")
            fy = st.number_input("Nilai Mutu Baja (Fy) = ")
            n = st.number_input("Jumlah Tulangan = ")
            # Asumsi
            Es = 200000
            hitung = st.button("EXECUTE")
            with tab3:
                st.header("CEK KAPASITAS")
                df = pd.DataFrame(columns=["h (mm)", "b (mm)", "d (mm)", "n(buah)",
                                            "As", "rho", "SyaratRasio", "ey", "et",
                                           "Jenis Keruntuhan", "phi", "Mn","phiMn"])
                if hitung:
                    # Preliminary Desain
                    h = h2
                    b = b2
                    # Tulangan
                    if 17 <= fc <= 28:
                        beta_1 = 0.85
                    elif 28 <= fc < 55:
                        beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                    else:
                        beta_1 = 0.65
                    # Desain Tulangan
                    Asterpasang = round(n * (1 / 4) * 3.1416 * ((D) ** 2),2)
                    # RasioTulangan
                    Aefektif = b * d
                    rho9 = round((Asterpasang / Aefektif), 3)
                    if rho9 < 0.025:
                        rho = "Memenuhi"
                    else:
                        rho = "TidakMemenuhi"
                    a = ((Asterpasang * fy) / (0.85 * fc * b))
                    c = ((a / beta_1))
                    ey = fy / Es
                    et1 = round((((d - c) / c) * 0.003), 5)
                    if et1 > ey:
                        et = "Under Reinfoce (Keruntuhan Tarik)"
                    elif et1 < ey:
                        et = "Over Reinforce (Keruntuhan Tekan)"
                    else:
                        et = "Balance"
                    # FaktorReduksiKekuatan
                    if et1 >= 0.005:
                        phi = 0.9
                    elif 0.002 < et1 < 0.005:
                        phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                    else:
                        phi = 0.65
                    # Hitung Momen Nominal
                    Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 3)
                    phiMn = round (phi * Mn,3)
                    data = [h, b, d, n, Asterpasang, rho9, rho, ey, et1, et, phi, Mn,
                            phiMn]
                    df = df.append(pd.Series(data, index=df.columns), ignore_index=True)
                st.dataframe(df)
                excel = df.to_excel("data.xlsx", index=False)

                with open("data.xlsx", "rb") as f:
                    excel_bytes = f.read()

                st.download_button(
                    "Download Excel",
                    excel_bytes,
                    "Inkremental.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key='download-excel'
                )
#DONE!