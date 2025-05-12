import streamlit as st
import json
import pandas as pd
from datetime import datetime
import base64
import time

# Set page configuration
st.set_page_config(
    page_title="Project Proposal Generator",
    page_icon="📝",
    layout="wide"
)

# Add educational sidebar with explanations and resources
with st.sidebar:
    st.title("Learning Guide")
    
    st.subheader("What is JSON?")
    st.info("""
    **JSON (JavaScript Object Notation)** is a lightweight data interchange format.
    
    It's commonly used for:
    - API communication
    - Configuration files
    - Data storage
    - Cross-language data exchange
    
    JSON represents data as nested objects (dictionaries) and arrays (lists).
    """)
    
    # Collapsible code example
    with st.expander("📚 JSON Example"):
        st.code("""
{
  "person": {
    "name": "John Smith",
    "age": 25,
    "isStudent": true,
    "courses": ["Programming", "Database", "Web Dev"],
    "address": {
      "street": "123 Main St",
      "city": "Boston"
    }
  }
}
        """)
    
    st.subheader("MoSCoW Prioritization")
    st.info("""
    The MoSCoW method is a prioritization technique:
    
    - **M**ust Have: Critical features required for MVP
    - **S**hould Have: Important but not critical features
    - **C**ould Have: Desirable features if time permits
    - **W**on't Have: Features explicitly out of scope
    
    This helps focus development efforts.
    """)
    
    st.subheader("Streamlit Resources")
    st.markdown("""
    * [Streamlit Documentation](https://docs.streamlit.io/)
    * [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
    * [Streamlit Components](https://streamlit.io/components)
    * [Streamlit Gallery](https://streamlit.io/gallery)
    """)
    
    # Execution time metrics (educational)
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
        st.session_state.last_action_time = time.time()
    
    current_time = time.time()
    st.subheader("App Metrics")
    st.text(f"Session duration: {int(current_time - st.session_state.start_time)}s")
    
    # Record interaction times for educational purposes
    if st.button("Record Interaction"):
        elapsed = current_time - st.session_state.last_action_time
        st.session_state.last_action_time = current_time
        st.write(f"Time since last interaction: {elapsed:.2f}s")

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
if 'page_views' not in st.session_state:
    st.session_state.page_views = {
        "basic_info": 0,
        "team_concept": 0,
        "market_analysis": 0,
        "features": 0,
        "export": 0,
        "json_preview": 0
    }
if 'form_completion' not in st.session_state:
    st.session_state.form_completion = {
        "basic_info": 0,
        "team_concept": 0,
        "market_analysis": 0,
        "features": 0,
        "total": 0
    }

# Helper functions
def add_team_member():
    """Add a new empty team member to the session state."""
    st.session_state.team_members.append({"name": "", "primary_role": "", "secondary_role": "", "skills": ""})

def remove_team_member(index):
    """Remove a team member at the given index from the session state."""
    st.session_state.team_members.pop(index)

def add_feature(category):
    """Add a new empty feature to the specified category."""
    st.session_state.features[category].append({"description": "", "rationale": ""})

def remove_feature(category, index):
    """Remove a feature at the given index from the specified category."""
    st.session_state.features[category].pop(index)

def add_competitor():
    """Add a new empty competitor to the session state."""
    st.session_state.competitors.append({"name": "", "core_features": "", "strengths": "", "weaknesses": "", "pricing": "", "target_audience": ""})

def remove_competitor(index):
    """Remove a competitor at the given index from the session state."""
    st.session_state.competitors.pop(index)

def add_swot_item(category):
    """Add a new empty item to the specified SWOT category."""
    st.session_state.swot[category].append("")

def remove_swot_item(category, index):
    """Remove an item at the given index from the specified SWOT category."""
    st.session_state.swot[category].pop(index)

def get_download_link(data, filename, link_text):
    """Generate a download link for the data as a JSON file."""
    # This function creates a downloadable link by:
    # 1. Converting the data to a JSON string
    # 2. Encoding it in base64
    # 3. Creating an HTML link that will trigger a download
    json_str = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def calculate_form_completion():
    """Calculate the completion percentage for each section and overall."""
    # Basic info completion (5 fields)
    basic_fields = ["project_name", "team_name", "concept_choice", "vision_statement", "project_summary"]
    basic_completion = sum(1 for field in basic_fields if st.session_state.get(field, "").strip())
    st.session_state.form_completion["basic_info"] = int((basic_completion / len(basic_fields)) * 100)
    
    # Team & concept completion (team members + target audience + differentiators)
    team_has_data = sum(1 for member in st.session_state.team_members 
                         if any(member[key].strip() for key in member))
    team_completion = team_has_data / max(len(st.session_state.team_members), 1)
    target_audience = 1 if st.session_state.get("target_audience", "").strip() else 0
    differentiators = 1 if st.session_state.get("key_differentiators", "").strip() else 0
    st.session_state.form_completion["team_concept"] = int(((team_completion + target_audience + differentiators) / 3) * 100)
    
    # Market analysis completion (competitors + SWOT)
    competitor_has_data = sum(1 for comp in st.session_state.competitors 
                             if any(comp[key].strip() for key in comp))
    competitor_completion = competitor_has_data / max(len(st.session_state.competitors), 1)
    
    swot_has_data = sum(len([item for item in st.session_state.swot[category] if item.strip()]) 
                        for category in st.session_state.swot)
    swot_total = sum(len(st.session_state.swot[category]) for category in st.session_state.swot)
    swot_completion = swot_has_data / max(swot_total, 1)
    
    st.session_state.form_completion["market_analysis"] = int(((competitor_completion + swot_completion) / 2) * 100)
    
    # Features completion
    feature_has_data = sum(sum(1 for feature in st.session_state.features[category] 
                            if any(feature[key].strip() for key in feature))
                         for category in st.session_state.features)
    feature_total = sum(len(st.session_state.features[category]) for category in st.session_state.features)
    
    tech_stack_fields = ["frontend_tech", "backend_tech", "database_tech", "hosting_tech", "other_tech"]
    tech_completion = sum(1 for field in tech_stack_fields if st.session_state.get(field, "").strip())
    
    st.session_state.form_completion["features"] = int(((feature_has_data / max(feature_total, 1) + 
                                                     tech_completion / len(tech_stack_fields)) / 2) * 100)
    
    # Total completion
    st.session_state.form_completion["total"] = int((
        st.session_state.form_completion["basic_info"] +
        st.session_state.form_completion["team_concept"] +
        st.session_state.form_completion["market_analysis"] +
        st.session_state.form_completion["features"]
    ) / 4)

# Title and introduction
st.title("CTS285/CSC289 Project Proposal Generator")
st.markdown("""
This interactive tool helps you create your project proposal in a structured format.
Fill in the information in each section and export your data as JSON.

**Learning Objectives:**
- Structure project information in a systematic way
- Practice using digital forms for data collection
- Learn about JSON data formatting
- Create a comprehensive project proposal
""")

# Display completion meter at the top
calculate_form_completion()
st.progress(st.session_state.form_completion["total"] / 100)
st.caption(f"Form Completion: {st.session_state.form_completion['total']}%")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Basic Info", 
    "Team & Concept", 
    "Market Analysis", 
    "Features",
    "Export",
    "JSON Tutorial"
])

# Tab 1: Basic Project Information
with tab1:
    st.session_state.page_views["basic_info"] += 1
    
    st.header("Basic Project Information")
    st.info("""
    This section captures the fundamental details about your project. 
    The vision statement should be concise (one sentence) but impactful, 
    clearly expressing the core purpose of your application.
    """)
    
    # Show section completion
    st.caption(f"Section completion: {st.session_state.form_completion['basic_info']}%")
    
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
    
    # Vision statement with character count
    vision_statement = st.text_area(
        "Vision Statement (one sentence)", 
        "Our application will...", 
        key="vision_statement",
        help="A clear, concise statement of what your application aims to achieve"
    )
    st.caption(f"Character count: {len(vision_statement)}/150 (recommended: keep under 150 characters)")
    
    # Project summary with word count
    project_summary = st.text_area(
        "Project Summary (250-300 words)", 
        "Describe your project here...", 
        height=200,
        key="project_summary"
    )
    word_count = len(project_summary.split())
    st.caption(f"Word count: {word_count}/300 (target: 250-300 words)")
    
    # Educational note about project summaries
    with st.expander("Tips for writing an effective project summary"):
        st.markdown("""
        A strong project summary should:
        
        1. **State the problem** your application solves
        2. **Describe your solution** and its key components
        3. **Identify target users** and their needs
        4. **Highlight key features** that make your application valuable
        5. **Mention the technology** approach briefly
        6. **Explain the benefits** to users
        
        Use clear, concise language and avoid technical jargon.
        """)

# Tab 2: Team and Concept Details
with tab2:
    st.session_state.page_views["team_concept"] += 1
    
    st.header("Team Members")
    st.info("Add all team members and their roles")
    
    # Show section completion
    st.caption(f"Section completion: {st.session_state.form_completion['team_concept']}%")
    
    # Educational explanation of team roles
    with st.expander("Common Team Roles in Software Development"):
        role_col1, role_col2 = st.columns(2)
        
        with role_col1:
            st.markdown("""
            **Technical Roles:**
            - **Frontend Developer**: Creates user interfaces and interactions
            - **Backend Developer**: Implements server-side logic and databases
            - **Full-Stack Developer**: Works on both frontend and backend
            - **UI/UX Designer**: Designs the look and feel of the application
            - **Database Administrator**: Manages data storage and access
            """)
        
        with role_col2:
            st.markdown("""
            **Project Roles:**
            - **Project Manager/Scrum Master**: Coordinates the team and process
            - **Product Owner**: Defines features and prioritizes backlog
            - **QA/Tester**: Ensures quality through testing
            - **Technical Writer**: Creates documentation
            - **DevOps Engineer**: Manages deployment and infrastructure
            """)
    
    # Team member form
    for i, member in enumerate(st.session_state.team_members):
        st.subheader(f"Team Member {i+1}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.team_members[i]["name"] = st.text_input(
                "Name", 
                member["name"], 
                key=f"member_name_{i}"
            )
            
            st.session_state.team_members[i]["primary_role"] = st.text_input(
                "Primary Role", 
                member["primary_role"], 
                key=f"member_primary_{i}",
                help="The main responsibility this person will have"
            )
        
        with col2:
            st.session_state.team_members[i]["secondary_role"] = st.text_input(
                "Secondary Role", 
                member["secondary_role"], 
                key=f"member_secondary_{i}",
                help="Additional responsibilities this person can handle"
            )
            
            st.session_state.team_members[i]["skills"] = st.text_input(
                "Key Skills", 
                member["skills"], 
                key=f"member_skills_{i}",
                help="Technical and soft skills this person brings to the team"
            )
        
        if i > 0:  # Don't allow removing the first member
            if st.button("Remove Member", key=f"remove_member_{i}"):
                remove_team_member(i)
                st.experimental_rerun()
    
    if st.button("Add Team Member"):
        add_team_member()
        st.experimental_rerun()
    
    st.header("Project Concept Details")
    
    # Target audience with examples
    st.subheader("Target Audience")
    with st.expander("Examples of well-defined target audiences"):
        st.markdown("""
        **Good Example:**
        "Our primary users are college students ages 18-24 who are looking for affordable housing near campus. They have limited budgets, are comfortable with technology, and need temporary housing solutions that accommodate academic year timing."
        
        **Weak Example:**
        "Anyone who needs housing."
        
        The good example specifies demographics, needs, constraints, and behaviors.
        """)
    
    target_audience = st.text_area(
        "Who will use your application?",
        "Describe your primary and secondary users...",
        help="Be specific about demographics, needs, and technical proficiency",
        key="target_audience"
    )
    
    st.subheader("Key Differentiators")
    st.info("What makes your approach unique compared to existing solutions?")
    
    with st.expander("Tips for strong differentiators"):
        st.markdown("""
        Good differentiators should be:
        
        1. **Specific and measurable** - Not "better UX" but "simplified 3-step booking process"
        2. **Meaningful to users** - Address actual pain points
        3. **Defensible** - Not easily copied by competitors
        4. **Realistic** - Within your capability to deliver
        
        Focus on unique combinations of features or novel approaches to problems.
        """)
    
    key_differentiators = st.text_area(
        "List 3-5 key differentiators (one per line)",
        "1. \n2. \n3. ",
        height=150,
        key="key_differentiators"
    )

# Tab 3: Market Analysis
with tab3:
    st.session_state.page_views["market_analysis"] += 1
    
    st.header("Competitor Analysis")
    st.info("Research existing applications similar to your concept")
    
    # Show section completion
    st.caption(f"Section completion: {st.session_state.form_completion['market_analysis']}%")
    
    # Educational tips
    with st.expander("How to research competitors effectively"):
        st.markdown("""
        **Research Sources:**
        - App stores (Apple App Store, Google Play)
        - Product Hunt and similar platforms
        - Tech blogs and review sites
        - Company websites and pricing pages
        - User reviews and ratings
        
        **What to Look For:**
        - Key features and limitations
        - Pricing models
        - Target audience
        - User interface approach
        - Marketing messaging
        - User complaints and praise
        
        **Tools for Research:**
        - SimilarWeb for website analytics
        - AppAnnie for mobile app intelligence
        - Google Trends for interest over time
        - Social media mentions and sentiment
        """)
    
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
                height=100,
                help="List the main features this competitor offers"
            )
            
            st.session_state.competitors[i]["strengths"] = st.text_area(
                "Strengths", 
                competitor["strengths"], 
                key=f"competitor_strengths_{i}",
                height=100,
                help="What does this competitor do well?"
            )
        
        with col2:
            st.session_state.competitors[i]["weaknesses"] = st.text_area(
                "Weaknesses", 
                competitor["weaknesses"], 
                key=f"competitor_weaknesses_{i}",
                height=100,
                help="Where does this competitor fall short?"
            )
            
            st.session_state.competitors[i]["pricing"] = st.text_input(
                "Pricing Model", 
                competitor["pricing"], 
                key=f"competitor_pricing_{i}",
                help="Free, Freemium, Subscription, One-time purchase, etc."
            )
            
            st.session_state.competitors[i]["target_audience"] = st.text_input(
                "Target Audience", 
                competitor["target_audience"], 
                key=f"competitor_audience_{i}",
                help="Who does this competitor serve?"
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
    
    # SWOT educational content
    with st.expander("Understanding SWOT Analysis"):
        swot_col1, swot_col2 = st.columns(2)
        
        with swot_col1:
            st.markdown("""
            **Strengths & Weaknesses (Internal Factors)**
            
            **Strengths** are internal capabilities that give your project advantages:
            - Team skills and experience
            - Novel technology approach
            - Unique features
            - Access to resources
            
            **Weaknesses** are internal limitations that could hinder success:
            - Skill gaps
            - Resource constraints
            - Technical limitations
            - Time restrictions
            """)
        
        with swot_col2:
            st.markdown("""
            **Opportunities & Threats (External Factors)**
            
            **Opportunities** are external possibilities that your project could exploit:
            - Underserved market segments
            - New technologies becoming available
            - Changes in user behavior
            - Gaps in competitor offerings
            
            **Threats** are external challenges that could cause problems:
            - Established competitors
            - Changing technology landscape
            - Regulatory considerations
            - Market saturation
            """)
    
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
    st.session_state.page_views["features"] += 1
    
    st.header("Feature Prioritization (MoSCoW Method)")
    
    # Show section completion
    st.caption(f"Section completion: {st.session_state.form_completion['features']}%")
    
    # Educational content on MoSCoW
    with st.expander("About MoSCoW Prioritization"):
        st.markdown("""
        The MoSCoW method helps teams prioritize requirements by dividing them into four categories:
        
        **Must Have** 🔴 - Critical features without which the product will not work. These are non-negotiable for the MVP.
        
        **Should Have** 🟠 - Important features that add significant value, but the product is still viable without them.
        
        **Could Have** 🟡 - Desirable features that would be nice to include if time and resources permit.
        
        **Won't Have** ⚪ - Features that are explicitly out of scope for the current version (but might be considered for future versions).
        
        This approach ensures clarity about what's critical vs. what's optional, helping teams focus their efforts.
        """)
    
    priority_tabs = st.tabs(["Must Have 🔴", "Should Have 🟠", "Could Have 🟡", "Won't Have ⚪"])
    
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
                    key=f"must_rationale_{i}",
                    help="Why is this feature critical for your MVP?"
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
                    key=f"should_rationale_{i}",
                    help="Why is this feature important but not critical?"
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
                    key=f"could_rationale_{i}",
                    help="What value would this feature add if included?"
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
                    key=f"wont_rationale_{i}",
                    help="Why is this feature explicitly out of scope?"
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
    
    # Educational content on tech stack
    with st.expander("Understanding Technology Stacks"):
        stack_col1, stack_col2 = st.columns(2)
        
        with stack_col1:
            st.markdown("""
            **Common Frontend Technologies:**
            - **React**: Popular JavaScript library for UIs
            - **Angular**: Full-featured framework by Google
            - **Vue.js**: Progressive JavaScript framework
            - **Bootstrap/Tailwind**: CSS frameworks
            - **Flutter**: UI toolkit for cross-platform apps
            """)
            
            st.markdown("""
            **Common Backend Technologies:**
            - **Node.js**: JavaScript runtime
            - **Django/Flask**: Python web frameworks
            - **Spring Boot**: Java framework
            - **Ruby on Rails**: Ruby framework
            - **ASP.NET**: Microsoft's framework
            """)
        
        with stack_col2:
            st.markdown("""
            **Common Database Technologies:**
            - **PostgreSQL/MySQL**: Relational databases
            - **MongoDB**: Document database
            - **Redis**: Key-value store
            - **Firebase**: Mobile/web app database
            - **SQLite**: Lightweight database
            """)
            
            st.markdown("""
            **Common Hosting Solutions:**
            - **AWS**: Amazon's cloud platform
            - **Azure**: Microsoft's cloud platform
            - **Google Cloud**: Google's cloud platform
            - **Heroku**: PaaS for easy deployment
            - **Vercel/Netlify**: Frontend deployment platforms
            """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        frontend_tech = st.text_input(
            "Frontend Technology", 
            key="frontend_tech",
            help="Technologies for user interface and client-side logic"
        )
        backend_tech = st.text_input(
            "Backend Technology", 
            key="backend_tech",
            help="Technologies for server-side logic and processing"
        )
        database_tech = st.text_input(
            "Database Technology", 
            key="database_tech",
            help="Technologies for data storage and retrieval"
        )
    
    with col2:
        hosting_tech = st.text_input(
            "Hosting/Deployment", 
            key="hosting_tech",
            help="Where and how you'll deploy your application"
        )
        other_tech = st.text_input(
            "Other Technologies", 
            key="other_tech",
            help="Additional technologies, libraries, or frameworks"
        )
        
        # Interactive tech stack visualization
        if any([frontend_tech, backend_tech, database_tech, hosting_tech]):
            st.subheader("Tech Stack Visualization")
            # Simple ASCII art stack visualization
            st.code(f"""
+---------------------+
|    Frontend         |  {frontend_tech if frontend_tech else "[Not specified]"}
+---------------------+
|    Backend          |  {backend_tech if backend_tech else "[Not specified]"}
+---------------------+
|    Database         |  {database_tech if database_tech else "[Not specified]"}
+---------------------+
|    Hosting          |  {hosting_tech if hosting_tech else "[Not specified]"}
+---------------------+
            """)

# Tab 5: Export
with tab5:
    st.session_state.page_views["export"] += 1
    
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
        "metadata": {
            "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completion_percentage": st.session_state.form_completion["total"],
            "form_activity": {
                "page_views": st.session_state.page_views
            }
        }
    }
    
    # Show data preview
    st.subheader("Data Preview")
    with st.expander("View JSON Data"):
        st.session_state.page_views["json_preview"] += 1
        st.json(export_data)
    
    # Download button
    st.subheader("Download JSON")
    filename = f"{team_name}_{project_name}_proposal_data.json".replace(" ", "_")
    st.markdown(get_download_link(export_data, filename, "📥 Download Proposal Data"), unsafe_allow_html=True)
    
    # Educational information about the exported file
    with st.expander("What is this JSON file?"):
        st.markdown("""
        The file you're downloading is a **JSON (JavaScript Object Notation)** file containing all the data you've entered in this form.
        
        **Why JSON?**
        - It's a widely used format for data exchange
        - It's human-readable while still being structured
        - It can be easily processed by various programming languages
        - It's the standard format for many APIs and web services
        
        **What can you do with this file?**
        - Import it into other applications
        - Process it with programming languages like Python, JavaScript, Java, etc.
        - Store it as a backup of your proposal information
        - Share it with team members or instructors
        - Use it as a data source for your application development
        """)
    
    st.info("""
    **What to do with this JSON file:**
    1. Include it as an attachment with your project proposal
    2. Use the data to help fill out the formal proposal document
    3. This structured data will be useful for your project development
    """)
    
    # Usage analytics (educational)
    st.subheader("Form Usage Analytics")
    st.caption("This data is just for demonstration purposes - it helps illustrate how applications track user behavior")
    
    # Display page view metrics
    page_views_df = pd.DataFrame({
        'Section': list(st.session_state.page_views.keys()),
        'Views': list(st.session_state.page_views.values())
    })
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.dataframe(page_views_df)
    
    with col2:
        st.bar_chart(page_views_df.set_index('Section'))
    
    st.caption("These analytics demonstrate how applications can track user behavior and interactions")

# Tab 6: JSON Tutorial
with tab6:
    st.header("JSON Tutorial")
    st.info("This tutorial will help you understand JSON format and how to work with it")
    
    st.subheader("What is JSON?")
    st.markdown("""
    **JSON (JavaScript Object Notation)** is a lightweight data interchange format that's easy for humans to read and write, and easy for machines to parse and generate.
    
    JSON has become the standard format for data exchange in web applications, APIs, configuration files, and many other contexts.
    """)
    
    st.subheader("JSON Structure")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Basic JSON Data Types:**
        
        - **Strings**: Text enclosed in double quotes
          - `"Hello, world!"`
        
        - **Numbers**: Integers or floating point
          - `42` or `3.14159`
        
        - **Booleans**: True or false values
          - `true` or `false`
        
        - **null**: Represents no value
          - `null`
        
        - **Arrays**: Ordered lists of values in square brackets
          - `["apple", "banana", "cherry"]`
        
        - **Objects**: Collections of key/value pairs in curly braces
          - `{"name": "John", "age": 30}`
        """)
    
    with col2:
        st.code("""
{
  "person": {
    "name": "Jane Smith",
    "age": 28,
    "isStudent": false,
    "courses": ["Programming", "Data Structures"],
    "address": {
      "street": "123 Main St",
      "city": "Boston",
      "zipCode": "02108"
    },
    "phoneNumbers": [
      {
        "type": "home",
        "number": "555-1234"
      },
      {
        "type": "work",
        "number": "555-5678"
      }
    ],
    "active": true
  }
}
        """, language="json")
    
    st.subheader("Working with JSON in Programming Languages")
    
    lang_tabs = st.tabs(["Python", "JavaScript", "Java"])
    
    with lang_tabs[0]:
        st.markdown("#### Working with JSON in Python")
        st.code("""
import json

# Parsing JSON (string to Python object)
json_string = '{"name": "Alice", "skills": ["Python", "SQL", "JavaScript"]}'
data = json.loads(json_string)

print(data["name"])                # Output: Alice
print(data["skills"][0])           # Output: Python

# Modifying data
data["age"] = 25
data["skills"].append("HTML")

# Creating JSON (Python object to string)
new_json_string = json.dumps(data, indent=4)
print(new_json_string)

# Reading JSON from a file
with open("data.json", "r") as file:
    data_from_file = json.load(file)

# Writing JSON to a file
with open("output.json", "w") as file:
    json.dump(data, file, indent=4)
        """, language="python")
    
    with lang_tabs[1]:
        st.markdown("#### Working with JSON in JavaScript")
        st.code("""
// Parsing JSON (string to JavaScript object)
const jsonString = '{"name": "Bob", "skills": ["JavaScript", "React", "Node.js"]}';
const data = JSON.parse(jsonString);

console.log(data.name);            // Output: Bob
console.log(data.skills[0]);       // Output: JavaScript

// Modifying data
data.age = 28;
data.skills.push("TypeScript");

// Creating JSON (JavaScript object to string)
const newJsonString = JSON.stringify(data, null, 2);
console.log(newJsonString);

// Working with JSON in fetch requests
fetch('https://api.example.com/data')
  .then(response => response.json())  // Parse JSON response
  .then(data => {
    console.log(data);
  });

// Sending JSON data
fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
});
        """, language="javascript")
    
    with lang_tabs[2]:
        st.markdown("#### Working with JSON in Java")
        st.code("""
import org.json.JSONObject;
import org.json.JSONArray;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Paths;

public class JsonExample {
    public static void main(String[] args) {
        // Creating a JSON object
        JSONObject person = new JSONObject();
        person.put("name", "Carol");
        person.put("age", 32);
        
        // Creating a JSON array
        JSONArray skills = new JSONArray();
        skills.put("Java");
        skills.put("Spring");
        skills.put("SQL");
        
        person.put("skills", skills);
        
        // Getting values
        String name = person.getString("name");
        int age = person.getInt("age");
        String firstSkill = person.getJSONArray("skills").getString(0);
        
        System.out.println(name);         // Output: Carol
        System.out.println(firstSkill);   // Output: Java
        
        // Converting to string
        String jsonString = person.toString(2);  // Indented with 2 spaces
        
        try {
            // Writing to a file
            FileWriter file = new FileWriter("person.json");
            file.write(jsonString);
            file.close();
            
            // Reading from a file
            String content = new String(Files.readAllBytes(Paths.get("person.json")));
            JSONObject readPerson = new JSONObject(content);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
        """, language="java")
    
    st.subheader("JSON Best Practices")
    st.markdown("""
    1. **Use Clear Key Names**: Choose descriptive, consistent key names
    2. **Format for Readability**: When sharing JSON with humans, use proper indentation
    3. **Validate Your JSON**: Use tools like JSONLint to check validity
    4. **Be Consistent with Data Types**: Don't mix types for the same key
    5. **Use Arrays for Ordered Data**: When order matters, use arrays
    6. **Use Objects for Key-Value Mappings**: When you need to look up by name
    7. **Consider Security**: Be careful with sensitive data
    8. **Handle Errors**: Always have error handling when parsing JSON
    """)
    
    st.subheader("Tools for Working with JSON")
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.markdown("""
        **Online Tools:**
        - [JSONLint](https://jsonlint.com/) - JSON validator
        - [JSON Formatter & Validator](https://jsonformatter.curiousconcept.com/)
        - [JSON to CSV Converter](https://www.convertcsv.com/json-to-csv.htm)
        - [JSON Path Finder](https://jsonpathfinder.com/)
        """)
    
    with tool_col2:
        st.markdown("""
        **Desktop/IDE Tools:**
        - Visual Studio Code with JSON extensions
        - JetBrains IDEs with JSON tools
        - Notepad++ with JSONViewer plugin
        - Advanced REST clients (Postman, Insomnia)
        """)
    
    st.subheader("Exercise: JSON Transformation")
    st.info("""
    Try the exercise below to practice working with JSON. Transform the given JSON into the target format.
    This simulates a common task in software development: reformatting data between different systems.
    """)
    
    with st.expander("Show Exercise"):
        st.markdown("#### Original JSON:")
        st.code("""
{
  "students": [
    {"id": 1, "firstName": "John", "lastName": "Doe", "grades": [85, 90, 78]},
    {"id": 2, "firstName": "Jane", "lastName": "Smith", "grades": [92, 88, 95]},
    {"id": 3, "firstName": "Bob", "lastName": "Johnson", "grades": [76, 82, 79]}
  ],
  "course": "Data Structures"
}
        """, language="json")
        
        st.markdown("#### Target Format:")
        st.code("""
{
  "course": "Data Structures",
  "studentCount": 3,
  "studentPerformance": [
    {
      "fullName": "John Doe",
      "averageGrade": 84.33,
      "passing": true
    },
    {
      "fullName": "Jane Smith",
      "averageGrade": 91.67,
      "passing": true
    },
    {
      "fullName": "Bob Johnson",
      "averageGrade": 79.0,
      "passing": true
    }
  ],
  "classAverage": 85.0
}
        """, language="json")
        
        st.markdown("#### Solution (Python):")
        solution_visible = st.checkbox("Show Solution")
        
        if solution_visible:
            st.code("""
import json

# Original JSON string
original_json = '''
{
  "students": [
    {"id": 1, "firstName": "John", "lastName": "Doe", "grades": [85, 90, 78]},
    {"id": 2, "firstName": "Jane", "lastName": "Smith", "grades": [92, 88, 95]},
    {"id": 3, "firstName": "Bob", "lastName": "Johnson", "grades": [76, 82, 79]}
  ],
  "course": "Data Structures"
}
'''

# Parse the JSON
data = json.loads(original_json)

# Prepare the new structure
new_data = {
    "course": data["course"],
    "studentCount": len(data["students"]),
    "studentPerformance": [],
    "classAverage": 0
}

# Calculate student performances
total_average = 0

for student in data["students"]:
    # Calculate average grade
    avg_grade = sum(student["grades"]) / len(student["grades"])
    total_average += avg_grade
    
    # Add student performance
    new_data["studentPerformance"].append({
        "fullName": f"{student['firstName']} {student['lastName']}",
        "averageGrade": round(avg_grade, 2),
        "passing": avg_grade >= 60  # Assuming 60 is passing grade
    })

# Calculate class average
new_data["classAverage"] = round(total_average / len(data["students"]), 2)

# Convert to JSON
new_json = json.dumps(new_data, indent=2)
print(new_json)
            """, language="python")

# Main app script conclusion
st.markdown("---")
st.caption("© 2025 CTS285/CSC289 Project Proposal Generator | Educational Tool")
st.caption(f"Total page views: {sum(st.session_state.page_views.values())}")