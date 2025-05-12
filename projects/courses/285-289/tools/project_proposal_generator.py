import streamlit as st
import json
import pandas as pd
from datetime import datetime
import base64

st.set_page_config(
    page_title="Project Proposal Generator",
    page_icon="📝",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'team_members' not in st.session_state:
    st.session_state.team_members = [{"name": "", "primary_role": "", "secondary_role": "", "skills": ""}]
if 'features' not in st.session_state:
    st.session_state.features = {
        "must_have": [{"description": "", "rationale": ""}],
        "should_have": [{"description": "", "rationale": ""}],
        "could_have": [{"description": "", "rationale": ""}],
        "wont_have": [{"description": "", "rationale": ""}]
    }
if 'competitors' not in st.session_state:
    st.session_state.competitors = [{"name": "", "core_features": "", "strengths": "", "weaknesses": "", "pricing": "", "target_audience": ""}]
if 'swot' not in st.session_state:
    st.session_state.swot = {
        "strengths": [""],
        "weaknesses": [""],
        "opportunities": [""],
        "threats": [""]
    }

def add_team_member():
    st.session_state.team_members.append({"name": "", "primary_role": "", "secondary_role": "", "skills": ""})

def remove_team_member(index):
    st.session_state.team_members.pop(index)

def add_feature(category):
    st.session_state.features[category].append({"description": "", "rationale": ""})

def remove_feature(category, index):
    st.session_state.features[category].pop(index)

def add_competitor():
    st.session_state.competitors.append({"name": "", "core_features": "", "strengths": "", "weaknesses": "", "pricing": "", "target_audience": ""})

def remove_competitor(index):
    st.session_state.competitors.pop(index)

def add_swot_item(category):
    st.session_state.swot[category].append("")

def remove_swot_item(category, index):
    st.session_state.swot[category].pop(index)

def get_download_link(data, filename, link_text):
    json_str = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

st.title("CTS285/CSC289 Project Proposal Generator")
st.markdown("""
This tool helps you create your project proposal in a structured format.
Fill in the information in each section and export your data as JSON.
""")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Basic Info", "Team & Concept", "Market Analysis", "Features", "Export"])

# Tab 1: Basic Project Information
with tab1:
    st.header("Basic Project Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input("Project Name", key="project_name")
        team_name = st.text_input("Team Name", key="team_name")
        
    with col2:
        submission_date = st.date_input("Submission Date", datetime.now(), key="submission_date")
        concept_choice = st.selectbox(
            "Project Concept",
            [
                "RecipeShare - Recipe Management and Social Platform",
                "ReserveIt - Reservation Management System",
                "SkillSwap - Skill Exchange Marketplace",
                "EventHub - Community Event Planning Platform",
                "StudyBuddy - Collaborative Learning Platform",
                "GearLend - Equipment Rental Exchange",
                "FitTrack - Fitness Goal Tracking Application",
                "ArtisanMarket - Creative Marketplace Platform",
                "SmartPantry - Kitchen Inventory Management",
                "VolunteerConnect - Volunteer Matching Platform",
                "Custom Concept (describe in vision)"
            ],
            key="concept_choice"
        )
    
    vision_statement = st.text_area("Vision Statement (one sentence)", 
                               "Our application will...", 
                               key="vision_statement")
    
    project_summary = st.text_area("Project Summary (250-300 words)", 
                              "Describe your project here...", 
                              height=200,
                              key="project_summary")

# Tab 2: Team and Concept Details
with tab2:
    st.header("Team Members")
    st.info("Add all team members and their roles")
    
    for i, member in enumerate(st.session_state.team_members):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
        
        with col1:
            st.session_state.team_members[i]["name"] = st.text_input(
                "Name", 
                member["name"], 
                key=f"member_name_{i}"
            )
        
        with col2:
            st.session_state.team_members[i]["primary_role"] = st.text_input(
                "Primary Role", 
                member["primary_role"], 
                key=f"member_primary_{i}"
            )
        
        with col3:
            st.session_state.team_members[i]["secondary_role"] = st.text_input(
                "Secondary Role", 
                member["secondary_role"], 
                key=f"member_secondary_{i}"
            )
        
        with col4:
            st.session_state.team_members[i]["skills"] = st.text_input(
                "Key Skills", 
                member["skills"], 
                key=f"member_skills_{i}"
            )
        
        with col5:
            if i > 0:  # Don't allow removing the first member
                st.write("")  # For vertical alignment
                if st.button("Remove", key=f"remove_member_{i}"):
                    remove_team_member(i)
                    st.experimental_rerun()
    
    if st.button("Add Team Member"):
        add_team_member()
        st.experimental_rerun()
    
    st.header("Project Concept Details")
    
    target_audience = st.text_area(
        "Target Audience (Who will use your application?)",
        "Describe your primary and secondary users...",
        key="target_audience"
    )
    
    st.subheader("Key Differentiators")
    st.info("What makes your approach unique compared to existing solutions?")
    
    key_differentiators = st.text_area(
        "List 3-5 key differentiators (one per line)",
        "1. \n2. \n3. ",
        height=150,
        key="key_differentiators"
    )

# Tab 3: Market Analysis
with tab3:
    st.header("Competitor Analysis")
    
    for i, competitor in enumerate(st.session_state.competitors):
        st.subheader(f"Competitor {i+1}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.competitors[i]["name"] = st.text_input(
                "Competitor Name", 
                competitor["name"], 
                key=f"competitor_name_{i}"
            )
            
            st.session_state.competitors[i]["core_features"] = st.text_area(
                "Core Features", 
                competitor["core_features"], 
                key=f"competitor_features_{i}",
                height=100
            )
            
            st.session_state.competitors[i]["strengths"] = st.text_area(
                "Strengths", 
                competitor["strengths"], 
                key=f"competitor_strengths_{i}",
                height=100
            )
        
        with col2:
            st.session_state.competitors[i]["weaknesses"] = st.text_area(
                "Weaknesses", 
                competitor["weaknesses"], 
                key=f"competitor_weaknesses_{i}",
                height=100
            )
            
            st.session_state.competitors[i]["pricing"] = st.text_input(
                "Pricing Model", 
                competitor["pricing"], 
                key=f"competitor_pricing_{i}"
            )
            
            st.session_state.competitors[i]["target_audience"] = st.text_input(
                "Target Audience", 
                competitor["target_audience"], 
                key=f"competitor_audience_{i}"
            )
        
        if i > 0:  # Always keep at least one competitor
            if st.button("Remove Competitor", key=f"remove_competitor_{i}"):
                remove_competitor(i)
                st.experimental_rerun()
        
        st.divider()
    
    if st.button("Add Competitor"):
        add_competitor()
        st.experimental_rerun()
    
    st.header("SWOT Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Strengths")
        for i, strength in enumerate(st.session_state.swot["strengths"]):
            cols = st.columns([5, 1])
            with cols[0]:
                st.session_state.swot["strengths"][i] = st.text_input(
                    f"Strength {i+1}", 
                    strength, 
                    key=f"strength_{i}"
                )
            with cols[1]:
                if i > 0:  # Always keep at least one item
                    if st.button("X", key=f"remove_strength_{i}"):
                        remove_swot_item("strengths", i)
                        st.experimental_rerun()
        
        if st.button("Add Strength"):
            add_swot_item("strengths")
            st.experimental_rerun()
        
        st.subheader("Opportunities")
        for i, opportunity in enumerate(st.session_state.swot["opportunities"]):
            cols = st.columns([5, 1])
            with cols[0]:
                st.session_state.swot["opportunities"][i] = st.text_input(
                    f"Opportunity {i+1}", 
                    opportunity, 
                    key=f"opportunity_{i}"
                )
            with cols[1]:
                if i > 0:  # Always keep at least one item
                    if st.button("X", key=f"remove_opportunity_{i}"):
                        remove_swot_item("opportunities", i)
                        st.experimental_rerun()
        
        if st.button("Add Opportunity"):
            add_swot_item("opportunities")
            st.experimental_rerun()
    
    with col2:
        st.subheader("Weaknesses")
        for i, weakness in enumerate(st.session_state.swot["weaknesses"]):
            cols = st.columns([5, 1])
            with cols[0]:
                st.session_state.swot["weaknesses"][i] = st.text_input(
                    f"Weakness {i+1}", 
                    weakness, 
                    key=f"weakness_{i}"
                )
            with cols[1]:
                if i > 0:  # Always keep at least one item
                    if st.button("X", key=f"remove_weakness_{i}"):
                        remove_swot_item("weaknesses", i)
                        st.experimental_rerun()
        
        if st.button("Add Weakness"):
            add_swot_item("weaknesses")
            st.experimental_rerun()
        
        st.subheader("Threats")
        for i, threat in enumerate(st.session_state.swot["threats"]):
            cols = st.columns([5, 1])
            with cols[0]:
                st.session_state.swot["threats"][i] = st.text_input(
                    f"Threat {i+1}", 
                    threat, 
                    key=f"threat_{i}"
                )
            with cols[1]:
                if i > 0:  # Always keep at least one item
                    if st.button("X", key=f"remove_threat_{i}"):
                        remove_swot_item("threats", i)
                        st.experimental_rerun()
        
        if st.button("Add Threat"):
            add_swot_item("threats")
            st.experimental_rerun()

# Tab 4: Features
with tab4:
    st.header("Feature Prioritization (MoSCoW Method)")
    
    priority_tabs = st.tabs(["Must Have", "Should Have", "Could Have", "Won't Have"])
    
    # Must Have Features
    with priority_tabs[0]:
        st.subheader("Must Have Features")
        st.info("Critical features required for MVP")
        
        for i, feature in enumerate(st.session_state.features["must_have"]):
            col1, col2, col3 = st.columns([4, 5, 1])
            
            with col1:
                st.session_state.features["must_have"][i]["description"] = st.text_input(
                    "Feature Description", 
                    feature["description"], 
                    key=f"must_feature_{i}"
                )
            
            with col2:
                st.session_state.features["must_have"][i]["rationale"] = st.text_input(
                    "Rationale/Justification", 
                    feature["rationale"], 
                    key=f"must_rationale_{i}"
                )
            
            with col3:
                if i > 0:  # Always keep at least one feature
                    st.write("")  # For alignment
                    if st.button("Remove", key=f"remove_must_{i}"):
                        remove_feature("must_have", i)
                        st.experimental_rerun()
        
        if st.button("Add Must Have Feature"):
            add_feature("must_have")
            st.experimental_rerun()
    
    # Should Have Features
    with priority_tabs[1]:
        st.subheader("Should Have Features")
        st.info("Important features that are not critical")
        
        for i, feature in enumerate(st.session_state.features["should_have"]):
            col1, col2, col3 = st.columns([4, 5, 1])
            
            with col1:
                st.session_state.features["should_have"][i]["description"] = st.text_input(
                    "Feature Description", 
                    feature["description"], 
                    key=f"should_feature_{i}"
                )
            
            with col2:
                st.session_state.features["should_have"][i]["rationale"] = st.text_input(
                    "Rationale/Justification", 
                    feature["rationale"], 
                    key=f"should_rationale_{i}"
                )
            
            with col3:
                if i > 0:  # Always keep at least one feature
                    st.write("")  # For alignment
                    if st.button("Remove", key=f"remove_should_{i}"):
                        remove_feature("should_have", i)
                        st.experimental_rerun()
        
        if st.button("Add Should Have Feature"):
            add_feature("should_have")
            st.experimental_rerun()
    
    # Could Have Features
    with priority_tabs[2]:
        st.subheader("Could Have Features")
        st.info("Desirable features if time permits")
        
        for i, feature in enumerate(st.session_state.features["could_have"]):
            col1, col2, col3 = st.columns([4, 5, 1])
            
            with col1:
                st.session_state.features["could_have"][i]["description"] = st.text_input(
                    "Feature Description", 
                    feature["description"], 
                    key=f"could_feature_{i}"
                )
            
            with col2:
                st.session_state.features["could_have"][i]["rationale"] = st.text_input(
                    "Rationale/Justification", 
                    feature["rationale"], 
                    key=f"could_rationale_{i}"
                )
            
            with col3:
                if i > 0:  # Always keep at least one feature
                    st.write("")  # For alignment
                    if st.button("Remove", key=f"remove_could_{i}"):
                        remove_feature("could_have", i)
                        st.experimental_rerun()
        
        if st.button("Add Could Have Feature"):
            add_feature("could_have")
            st.experimental_rerun()
    
    # Won't Have Features
    with priority_tabs[3]:
        st.subheader("Won't Have Features")
        st.info("Features explicitly excluded from current scope")
        
        for i, feature in enumerate(st.session_state.features["wont_have"]):
            col1, col2, col3 = st.columns([4, 5, 1])
            
            with col1:
                st.session_state.features["wont_have"][i]["description"] = st.text_input(
                    "Feature Description", 
                    feature["description"], 
                    key=f"wont_feature_{i}"
                )
            
            with col2:
                st.session_state.features["wont_have"][i]["rationale"] = st.text_input(
                    "Rationale/Justification", 
                    feature["rationale"], 
                    key=f"wont_rationale_{i}"
                )
            
            with col3:
                if i > 0:  # Always keep at least one feature
                    st.write("")  # For alignment
                    if st.button("Remove", key=f"remove_wont_{i}"):
                        remove_feature("wont_have", i)
                        st.experimental_rerun()
        
        if st.button("Add Won't Have Feature"):
            add_feature("wont_have")
            st.experimental_rerun()
    
    st.header("Technology Stack")
    col1, col2 = st.columns(2)
    
    with col1:
        frontend_tech = st.text_input("Frontend Technology", key="frontend_tech")
        backend_tech = st.text_input("Backend Technology", key="backend_tech")
        database_tech = st.text_input("Database Technology", key="database_tech")
    
    with col2:
        hosting_tech = st.text_input("Hosting/Deployment", key="hosting_tech")
        other_tech = st.text_input("Other Technologies", key="other_tech")

# Tab 5: Export
with tab5:
    st.header("Export Your Proposal Data")
    
    # Clean up empty entries from lists
    for category in st.session_state.swot:
        st.session_state.swot[category] = [item for item in st.session_state.swot[category] if item.strip()]
    
    # Prepare the data for export
    export_data = {
        "project_name": project_name,
        "team_name": team_name,
        "submission_date": submission_date.strftime("%Y-%m-%d"),
        "concept_choice": concept_choice,
        "vision_statement": vision_statement,
        "project_summary": project_summary,
        "team_members": st.session_state.team_members,
        "target_audience": target_audience,
        "key_differentiators": key_differentiators.split("\n"),
        "competitors": st.session_state.competitors,
        "swot_analysis": st.session_state.swot,
        "features": st.session_state.features,
        "technology_stack": {
            "frontend": frontend_tech,
            "backend": backend_tech,
            "database": database_tech,
            "hosting": hosting_tech,
            "other": other_tech
        },
        "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Show data preview
    st.subheader("Data Preview")
    with st.expander("View JSON Data"):
        st.json(export_data)
    
    # Download button
    st.subheader("Download JSON")
    filename = f"{team_name}_{project_name}_proposal_data.json".replace(" ", "_")
    st.markdown(get_download_link(export_data, filename, "Download Proposal Data"), unsafe_allow_html=True)
    
    st.info("""
    **What to do with this JSON file:**
    1. Include it as an attachment with your project proposal
    2. Use the data to help fill out the formal proposal document
    3. This structured data might be useful for your project development
    """)
    
    st.warning("""
    **Important Note:**
    This JSON export does not replace the full project proposal document. 
    It should be used as supplementary material and to help you organize your project information.
    """)
    
    st.success("""
    **Next Steps:**
    1. Download your JSON data
    2. Complete any missing information in the proposal template document
    3. Include screenshots, wireframes, and detailed descriptions
    4. Submit both your proposal document and this JSON file
    """)