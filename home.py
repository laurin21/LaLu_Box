import streamlit as st
import pandas as pd

# Streamlit App
st.title('📊 Projekt-Übersicht')

# Session State initialisieren
if 'df' not in st.session_state:
    # Initiales DataFrame erstellen
    data = {
        'Titel': [
            'Projekt Alpha',
            'Projekt Beta',
            'Projekt Gamma',
            'Projekt Delta',
            'Projekt Epsilon'
        ],
        'Beschreibung': [
            'Entwicklung einer neuen Webapplikation',
            'Optimierung der bestehenden Datenbank',
            'Marketing-Kampagne für Q1',
            'Schulung neuer Mitarbeiter',
            'Infrastruktur-Upgrade'
        ],
        'Geld': [
            '3',
            '2',
            '1',
            '2',
            '3'
        ],
        'Zeit': [
            '3',
            '1',
            '2',
            '1',
            '3'
        ],
        'Kategorie': [
            'IT',
            'IT',
            'Marketing',
            'HR',
            'IT'
        ]
    }
    
    st.session_state.df = pd.DataFrame(data)
    # Spalten in Category-Datentyp konvertieren
    st.session_state.df['Geld'] = st.session_state.df['Geld'].astype('category')
    st.session_state.df['Zeit'] = st.session_state.df['Zeit'].astype('category')
    st.session_state.df['Kategorie'] = st.session_state.df['Kategorie'].astype('category')

# Tabs erstellen
tab1, tab2 = st.tabs(["➕ Neuen Eintrag hinzufügen", "🎲 Zufälligen Eintrag finden"])

# Tab 1: Neuen Eintrag hinzufügen
with tab1:
    st.header("Neuen Eintrag erstellen")
    
    with st.form("neuer_eintrag"):
        titel = st.text_input("Titel", placeholder="z.B. Projekt Omega")
        beschreibung = st.text_area("Beschreibung", placeholder="Beschreibe das Projekt...")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            geld = st.selectbox("Geld", options=["1", "2", "3"])
        
        with col2:
            zeit = st.selectbox("Zeit", options=["1", "2", "3"])
        
        with col3:
            # Dynamisch alle vorhandenen Kategorien + Option für neue
            vorhandene_kategorien = sorted(st.session_state.df['Kategorie'].unique().tolist())
            kategorie_auswahl = st.selectbox(
                "Kategorie", 
                options=vorhandene_kategorien + ["Neue Kategorie..."]
            )
        
        # Wenn "Neue Kategorie" gewählt wurde
        neue_kategorie = None
        if kategorie_auswahl == "Neue Kategorie...":
            neue_kategorie = st.text_input("Neue Kategorie eingeben")
            kategorie = neue_kategorie
        else:
            kategorie = kategorie_auswahl
        
        submitted = st.form_submit_button("Eintrag hinzufügen")
        
        if submitted:
            if not titel or not beschreibung:
                st.error("Bitte fülle Titel und Beschreibung aus!")
            elif kategorie_auswahl == "Neue Kategorie..." and not neue_kategorie:
                st.error("Bitte gib eine neue Kategorie ein!")
            else:
                # Neuen Eintrag erstellen
                neuer_eintrag = pd.DataFrame({
                    'Titel': [titel],
                    'Beschreibung': [beschreibung],
                    'Geld': [geld],
                    'Zeit': [zeit],
                    'Kategorie': [kategorie]
                })
                
                # Zum DataFrame hinzufügen
                st.session_state.df = pd.concat(
                    [st.session_state.df, neuer_eintrag], 
                    ignore_index=True
                )
                
                # Category-Datentypen beibehalten
                st.session_state.df['Geld'] = st.session_state.df['Geld'].astype('category')
                st.session_state.df['Zeit'] = st.session_state.df['Zeit'].astype('category')
                st.session_state.df['Kategorie'] = st.session_state.df['Kategorie'].astype('category')
                
                st.success(f"✅ '{titel}' wurde erfolgreich hinzugefügt!")
    
    # Alle vorhandenen Einträge anzeigen
    st.subheader(f"Alle Einträge ({len(st.session_state.df)})")
    st.dataframe(st.session_state.df, use_container_width=True)

# Tab 2: Zufälligen Eintrag finden
with tab2:
    st.header("Zufälligen Eintrag finden")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        geld_filter = st.multiselect(
            "Geld filtern:",
            options=sorted(st.session_state.df['Geld'].unique()),
            default=None
        )
    
    with col2:
        zeit_filter = st.multiselect(
            "Zeit filtern:",
            options=sorted(st.session_state.df['Zeit'].unique()),
            default=None
        )
    
    with col3:
        kategorie_filter = st.multiselect(
            "Kategorie filtern:",
            options=sorted(st.session_state.df['Kategorie'].unique()),
            default=None
        )
    
    # DataFrame filtern
    filtered_df = st.session_state.df.copy()
    
    if geld_filter:
        filtered_df = filtered_df[filtered_df['Geld'].isin(geld_filter)]
    
    if zeit_filter:
        filtered_df = filtered_df[filtered_df['Zeit'].isin(zeit_filter)]
    
    if kategorie_filter:
        filtered_df = filtered_df[filtered_df['Kategorie'].isin(kategorie_filter)]
    
    st.write(f"**{len(filtered_df)}** Einträge entsprechen den Filtern")
    
    if len(filtered_df) > 0:
        if st.button("🎲 Zufälligen Eintrag anzeigen", type="primary"):
            # Zufälligen Eintrag auswählen
            zufalls_eintrag = filtered_df.sample(n=1).iloc[0]
            
            # Schön formatiert anzeigen
            st.divider()
            st.subheader(f"🎯 {zufalls_eintrag['Titel']}")
            st.write(zufalls_eintrag['Beschreibung'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Geld", zufalls_eintrag['Geld'])
            with col2:
                st.metric("⏱️ Zeit", zufalls_eintrag['Zeit'])
            with col3:
                st.metric("📁 Kategorie", zufalls_eintrag['Kategorie'])
    else:
        st.warning("⚠️ Keine Einträge gefunden, die den Filtern entsprechen.")