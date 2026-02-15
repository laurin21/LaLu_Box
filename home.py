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
            '',  # Leer als Beispiel
            'Marketing-Kampagne für Q1',
            'Schulung neuer Mitarbeiter',
            ''   # Leer als Beispiel
        ],
        'Geld': [
            ['3'],
            ['2', '3'],
            [],  # Leer als Beispiel
            ['1', '2'],
            ['3']
        ],
        'Zeit': [
            ['3'],
            [],  # Leer als Beispiel
            ['2'],
            ['1'],
            ['2', '3']
        ],
        'Kategorie': [
            ['IT', 'Entwicklung'],
            ['IT', 'Datenbank'],
            ['Marketing'],
            [],  # Leer als Beispiel
            ['IT', 'Infrastruktur']
        ]
    }
    
    st.session_state.df = pd.DataFrame(data)
    # Keine Category-Datentypen mehr nötig, da alles Listen sind

# Verfügbare Kategorien aus allen Einträgen sammeln
if 'verfuegbare_kategorien' not in st.session_state:
    # Alle Kategorien aus dem DataFrame extrahieren
    alle_kategorien = set()
    for kategorien_liste in st.session_state.df['Kategorie']:
        if isinstance(kategorien_liste, list) and kategorien_liste:
            alle_kategorien.update(kategorien_liste)
    st.session_state.verfuegbare_kategorien = sorted(list(alle_kategorien))

# Tabs erstellen (vertauscht)
tab1, tab2 = st.tabs(["🎲 Zufälligen Eintrag finden", "📝 Einträge verwalten"])

# Tab 1: Zufälligen Eintrag finden
with tab1:
    st.header("Zufälligen Eintrag finden")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Alle vorhandenen Geld-Werte sammeln
        geld_werte = set()
        for geld_liste in st.session_state.df['Geld']:
            if isinstance(geld_liste, list) and geld_liste:
                geld_werte.update(geld_liste)
        geld_filter = st.multiselect(
            "Geld filtern:",
            options=sorted(list(geld_werte)),
            default=None
        )
    
    with col2:
        # Alle vorhandenen Zeit-Werte sammeln
        zeit_werte = set()
        for zeit_liste in st.session_state.df['Zeit']:
            if isinstance(zeit_liste, list) and zeit_liste:
                zeit_werte.update(zeit_liste)
        zeit_filter = st.multiselect(
            "Zeit filtern:",
            options=sorted(list(zeit_werte)),
            default=None
        )
    
    with col3:
        kategorie_filter = st.multiselect(
            "Kategorie filtern:",
            options=st.session_state.verfuegbare_kategorien,
            default=None
        )
    
    # DataFrame filtern
    filtered_df = st.session_state.df.copy()
    
    if geld_filter:
        filtered_df = filtered_df[filtered_df['Geld'].apply(
            lambda x: any(g in x for g in geld_filter) if isinstance(x, list) else False
        )]
    
    if zeit_filter:
        filtered_df = filtered_df[filtered_df['Zeit'].apply(
            lambda x: any(z in x for z in zeit_filter) if isinstance(x, list) else False
        )]
    
    if kategorie_filter:
        # Filtern nach Kategorien (ein Eintrag muss mindestens eine der ausgewählten Kategorien haben)
        filtered_df = filtered_df[filtered_df['Kategorie'].apply(
            lambda x: any(kat in x for kat in kategorie_filter) if isinstance(x, list) else False
        )]
    
    st.write(f"**{len(filtered_df)}** Einträge entsprechen den Filtern")
    
    if len(filtered_df) > 0:
        if st.button("🎲 Zufälligen Eintrag anzeigen", type="primary"):
            # Zufälligen Eintrag auswählen
            zufalls_eintrag = filtered_df.sample(n=1).iloc[0]
            
            # Schön formatiert anzeigen
            st.divider()
            st.subheader(f"🎯 {zufalls_eintrag['Titel']}")
            
            # Beschreibung nur anzeigen wenn vorhanden
            if zufalls_eintrag['Beschreibung']:
                st.write(zufalls_eintrag['Beschreibung'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if isinstance(zufalls_eintrag['Geld'], list) and zufalls_eintrag['Geld']:
                    geld_text = ", ".join(zufalls_eintrag['Geld'])
                else:
                    geld_text = "-"
                st.metric("💰 Geld", geld_text)
            with col2:
                if isinstance(zufalls_eintrag['Zeit'], list) and zufalls_eintrag['Zeit']:
                    zeit_text = ", ".join(zufalls_eintrag['Zeit'])
                else:
                    zeit_text = "-"
                st.metric("⏱️ Zeit", zeit_text)
            with col3:
                # Kategorien als Liste anzeigen
                if isinstance(zufalls_eintrag['Kategorie'], list) and zufalls_eintrag['Kategorie']:
                    kategorien_text = ", ".join(zufalls_eintrag['Kategorie'])
                else:
                    kategorien_text = "-"
                st.metric("📁 Kategorien", kategorien_text)
    else:
        st.warning("⚠️ Keine Einträge gefunden, die den Filtern entsprechen.")

# Tab 2: Einträge verwalten
with tab2:
    st.header("Einträge verwalten")
    
    # Drei Unterabschnitte: Neu hinzufügen, Bearbeiten und Kategorien verwalten
    action = st.radio(
        "Was möchtest du tun?",
        ["Neuen Eintrag hinzufügen", "Bestehenden Eintrag bearbeiten", "Kategorien verwalten"],
        horizontal=True
    )
    
    if action == "Kategorien verwalten":
        st.subheader("🏷️ Kategorien verwalten")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Vorhandene Kategorien:**")
            if st.session_state.verfuegbare_kategorien:
                for i, kat in enumerate(st.session_state.verfuegbare_kategorien):
                    st.write(f"{i+1}. {kat}")
            else:
                st.info("Noch keine Kategorien vorhanden.")
        
        with col2:
            st.write("**Neue Kategorie hinzufügen:**")
            neue_kat_name = st.text_input("Name der neuen Kategorie:", key="neue_kat_verwaltung")
            if st.button("Kategorie hinzufügen"):
                if neue_kat_name:
                    if neue_kat_name not in st.session_state.verfuegbare_kategorien:
                        st.session_state.verfuegbare_kategorien.append(neue_kat_name)
                        st.session_state.verfuegbare_kategorien = sorted(st.session_state.verfuegbare_kategorien)
                        st.success(f"✅ Kategorie '{neue_kat_name}' wurde hinzugefügt!")
                        st.rerun()
                    else:
                        st.error("Diese Kategorie existiert bereits!")
                else:
                    st.error("Bitte gib einen Namen ein!")
        
        st.divider()
        
        # Kategorie löschen
        st.write("**Kategorie löschen:**")
        if st.session_state.verfuegbare_kategorien:
            zu_loeschende_kat = st.selectbox(
                "Wähle eine Kategorie zum Löschen:",
                options=st.session_state.verfuegbare_kategorien,
                key="kat_loeschen"
            )
            
            if st.button("Kategorie löschen", type="secondary"):
                # Prüfen, ob Kategorie noch verwendet wird
                verwendung = 0
                for kategorien_liste in st.session_state.df['Kategorie']:
                    if isinstance(kategorien_liste, list) and zu_loeschende_kat in kategorien_liste:
                        verwendung += 1
                
                if verwendung > 0:
                    st.warning(f"⚠️ Diese Kategorie wird noch in {verwendung} Einträgen verwendet. Sie wird aus allen Einträgen entfernt.")
                    
                    # Aus allen Einträgen entfernen
                    st.session_state.df['Kategorie'] = st.session_state.df['Kategorie'].apply(
                        lambda x: [k for k in x if k != zu_loeschende_kat] if isinstance(x, list) else x
                    )
                
                # Aus verfügbaren Kategorien entfernen
                st.session_state.verfuegbare_kategorien.remove(zu_loeschende_kat)
                st.success(f"🗑️ Kategorie '{zu_loeschende_kat}' wurde gelöscht!")
                st.rerun()
        else:
            st.info("Keine Kategorien zum Löschen vorhanden.")
    
    elif action == "Neuen Eintrag hinzufügen":
        st.subheader("➕ Neuen Eintrag erstellen")
        
        with st.form("neuer_eintrag"):
            titel = st.text_input("Titel *", placeholder="z.B. Projekt Omega")
            beschreibung = st.text_area("Beschreibung (optional)", placeholder="Beschreibe das Projekt...")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                geld = st.multiselect("Geld (optional):", options=["1", "2", "3"], default=None)
            
            with col2:
                zeit = st.multiselect("Zeit (optional):", options=["1", "2", "3"], default=None)
            
            with col3:
                # Multiselect für Kategorien
                kategorien = st.multiselect(
                    "Kategorien (optional):",
                    options=st.session_state.verfuegbare_kategorien,
                    default=None
                )
            
            submitted = st.form_submit_button("Eintrag hinzufügen")
            
            if submitted:
                if not titel:
                    st.error("Bitte gib einen Titel ein!")
                else:
                    # Neuen Eintrag erstellen
                    neuer_eintrag = pd.DataFrame({
                        'Titel': [titel],
                        'Beschreibung': [beschreibung],
                        'Geld': [geld if geld else []],
                        'Zeit': [zeit if zeit else []],
                        'Kategorie': [kategorien if kategorien else []]
                    })
                    
                    # Zum DataFrame hinzufügen
                    st.session_state.df = pd.concat(
                        [st.session_state.df, neuer_eintrag], 
                        ignore_index=True
                    )
                    
                    st.success(f"✅ '{titel}' wurde erfolgreich hinzugefügt!")
                    st.rerun()
    
    else:  # Bestehenden Eintrag bearbeiten
        st.subheader("✏️ Eintrag bearbeiten")
        
        if len(st.session_state.df) == 0:
            st.info("Noch keine Einträge vorhanden.")
        else:
            # Eintrag zum Bearbeiten auswählen
            titel_liste = st.session_state.df['Titel'].tolist()
            ausgewaehlter_titel = st.selectbox(
                "Wähle einen Eintrag zum Bearbeiten:",
                options=titel_liste
            )
            
            # Index des ausgewählten Eintrags finden
            eintrag_idx = st.session_state.df[st.session_state.df['Titel'] == ausgewaehlter_titel].index[0]
            eintrag = st.session_state.df.iloc[eintrag_idx]
            
            with st.form("eintrag_bearbeiten"):
                titel_neu = st.text_input("Titel *", value=eintrag['Titel'])
                beschreibung_neu = st.text_area("Beschreibung (optional)", value=eintrag['Beschreibung'])
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Multiselect für Geld mit vorausgewählten Werten
                    aktuelle_geld = eintrag['Geld'] if isinstance(eintrag['Geld'], list) else []
                    geld_neu = st.multiselect(
                        "Geld (optional):", 
                        options=["1", "2", "3"],
                        default=aktuelle_geld
                    )
                
                with col2:
                    # Multiselect für Zeit mit vorausgewählten Werten
                    aktuelle_zeit = eintrag['Zeit'] if isinstance(eintrag['Zeit'], list) else []
                    zeit_neu = st.multiselect(
                        "Zeit (optional):", 
                        options=["1", "2", "3"],
                        default=aktuelle_zeit
                    )
                
                with col3:
                    # Multiselect für Kategorien mit vorausgewählten Werten
                    aktuelle_kategorien = eintrag['Kategorie'] if isinstance(eintrag['Kategorie'], list) else []
                    kategorien_neu = st.multiselect(
                        "Kategorien (optional):",
                        options=st.session_state.verfuegbare_kategorien,
                        default=aktuelle_kategorien
                    )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    update_button = st.form_submit_button("💾 Änderungen speichern", type="primary")
                with col_b:
                    delete_button = st.form_submit_button("🗑️ Eintrag löschen", type="secondary")
                
                if update_button:
                    if not titel_neu:
                        st.error("Bitte gib einen Titel ein!")
                    else:
                        # Eintrag aktualisieren
                        st.session_state.df.at[eintrag_idx, 'Titel'] = titel_neu
                        st.session_state.df.at[eintrag_idx, 'Beschreibung'] = beschreibung_neu
                        st.session_state.df.at[eintrag_idx, 'Geld'] = geld_neu if geld_neu else []
                        st.session_state.df.at[eintrag_idx, 'Zeit'] = zeit_neu if zeit_neu else []
                        st.session_state.df.at[eintrag_idx, 'Kategorie'] = kategorien_neu if kategorien_neu else []
                        
                        st.success(f"✅ '{titel_neu}' wurde erfolgreich aktualisiert!")
                        st.rerun()
                
                if delete_button:
                    # Eintrag löschen
                    st.session_state.df = st.session_state.df.drop(eintrag_idx).reset_index(drop=True)
                    
                    st.success(f"🗑️ '{ausgewaehlter_titel}' wurde gelöscht!")
                    st.rerun()
    
    # Alle vorhandenen Einträge anzeigen
    st.divider()
    st.subheader(f"Alle Einträge ({len(st.session_state.df)})")
    # DataFrame für Anzeige vorbereiten (Listen als String)
    df_anzeige = st.session_state.df.copy()
    df_anzeige['Geld'] = df_anzeige['Geld'].apply(
        lambda x: ", ".join(x) if isinstance(x, list) and x else "-"
    )
    df_anzeige['Zeit'] = df_anzeige['Zeit'].apply(
        lambda x: ", ".join(x) if isinstance(x, list) and x else "-"
    )
    df_anzeige['Kategorie'] = df_anzeige['Kategorie'].apply(
        lambda x: ", ".join(x) if isinstance(x, list) and x else "-"
    )
    # Leere Felder mit "-" ersetzen
    df_anzeige['Beschreibung'] = df_anzeige['Beschreibung'].apply(lambda x: x if x else "-")
    st.dataframe(df_anzeige, use_container_width=True)