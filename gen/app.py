import streamlit as st
import random
from models import World
from engine import SimulationEngine
from export import create_world_docx

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Fizzbend World Engine",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the Fizzbend Aesthetic
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .history-card { background-color: #1E1E1E; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #FF4B4B;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR: THE CONTROL PANEL
# ==========================================
with st.sidebar:
    st.image("https://via.placeholder.com/300x100.png?text=Fizzbend+Games", use_container_width=True) 
    st.title("World Parameters")
    
    # 1. Seed & Core Settings
    seed_input = st.text_input("World Seed (Leave blank for random)", value="")
    years_to_sim = st.slider("Years to Simulate per click", 1, 20, 5)
    
    st.markdown("---")
    
    # 2. Demographics
    all_races = ["Humans", "Elves", "Dwarves", "Halflings", "Goblins", "Orcs", "Lizardmen", "Tripki", "Kerra", "Giants", "Trolls", "Undead", "Ratmen", "Plantients", "Mutants", "Fairies", "Pixies"]
    majority_race = st.selectbox("Majority Ancestry", all_races, index=0)
    minority_races = st.multiselect("Active Minorities", all_races, default=["Elves", "Dwarves"])
    
    st.markdown("---")
    
    # 3. Master Variables
    start_stability = st.slider("Starting Stability", 0, 100, 50)
    start_magic = st.slider("Magic Level", 0, 100, 50)
    start_tech = st.slider("Technology Level", 0, 100, 10)
    climate = st.selectbox("Climate", ["Temperate", "Arid", "Tropical", "Glacial"])
    
    # Initialization Button
    if st.button("Initialize New World", use_container_width=True, type="primary"):
        # Set Seed
        final_seed = seed_input if seed_input else str(random.randint(10000, 99999))
        random.seed(final_seed)
        
        # Build World Object
        new_world = World(seed=final_seed, majority_ancestry=majority_race, active_minorities=minority_races)
        new_world.stability = start_stability
        new_world.magic_level = start_magic
        new_world.tech_level = start_tech
        new_world.climate = climate
        
        # --- THE AI SCRIBE INITIALIZATION ---
        my_scribe = None
        try:
            from ai_scribe import AIScribe
            # Securely fetch the API key from Streamlit Secrets
            api_key = st.secrets["GEMINI_API_KEY"]
            my_scribe = AIScribe(api_key=api_key)
            st.toast("AI Historian connected!", icon="✅")
        except Exception as e:
            st.warning("Running in static fallback mode. Could not connect to AI.")
        
        # Save to Session State
        st.session_state['my_world'] = new_world
        st.session_state['engine'] = SimulationEngine(new_world, ai_scribe=my_scribe)
        st.success(f"World '{final_seed}' Born!")

# ==========================================
# MAIN PANEL: THE CHRONICLE
# ==========================================
st.title("The Living Chronicle")

# Check if a world exists in memory
if 'my_world' in st.session_state:
    world = st.session_state['my_world']
    engine = st.session_state['engine']
    
    # Display Top Dashboard
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Current Year", world.year)
    col2.metric("Stability", world.stability)
    col3.metric("Magic Level", world.magic_level)
    col4.metric("Tech Level", world.tech_level)
    col5.metric("Seed", world.seed)
    
    st.markdown("---")
    
    # Action Buttons
    colA, colB = st.columns([1, 1])
    with colA:
        # ---> UPDATED TO USE THE ERA SUMMARIZER <---
        if st.button(f"Advance {years_to_sim} Years", use_container_width=True):
            with st.spinner("The AI is weaving an Era..."):
                engine.advance_era(years_to_sim)
            st.rerun() 
            
    with colB:
        # Generate the Word Doc
        docx_buffer = create_world_docx(world)
        st.download_button(
            label="Download .docx Export",
            data=docx_buffer,
            file_name=f"Fizzbend_History_{world.seed}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    # Display History & Data in Tabs
    tab1, tab2, tab3 = st.tabs(["The Ledger", "Factions", "Relics & Lore"])
    
    with tab1:
        st.markdown("<p class='big-font'>Historical Events</p>", unsafe_allow_html=True)
        if not world.history_log:
            st.info("The world is new. Click 'Advance Years' to begin history.")
        else:
            for event in reversed(world.history_log):
                # Tweak to display the Era Title beautifully 
                st.markdown(f"""
                <div class='history-card'>
                    <h4>{event.title}</h4>
                    <p>{event.description}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<p class='big-font'>Global Demographics</p>", unsafe_allow_html=True)
        for faction in world.factions.values():
            status = "👑 Majority" if faction.is_majority else "Minority"
            st.write(f"**{faction.race_name}** ({status}) | Tech: {faction.local_tech} | Pop: {faction.population}")

    with tab3:
        st.markdown("<p class='big-font'>World Anchors</p>", unsafe_allow_html=True)
        st.info("Relics, Notable People, and Cities will appear here as history progresses.")

else:
    # Landing Screen
    st.markdown("### Welcome to the Fizzbend Games World Engine")
    st.write("Use the Control Panel on the left to set your parameters and birth a new world.")
