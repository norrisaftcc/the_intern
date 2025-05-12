# Project Proposal Generator Tool

This interactive Streamlit application helps students create and organize their project proposal information in a structured format. Students can input project details, team information, market research, and feature plans, then export the data as a JSON file.

## Purpose

This tool serves multiple educational purposes:

1. **Interactive Planning**: Guides students through the project planning process in a structured way
2. **Data Structure Learning**: Introduces students to structured data formats (JSON)
3. **Tool Exposure**: Provides hands-on experience with Streamlit, a tool they might use in their own projects
4. **Consistency**: Ensures all project proposals contain the required information

## Running the Tool

### Setup

1. Ensure you have Python 3.7+ installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Starting the Application

Run the following command in this directory:
```
streamlit run project_proposal_generator.py
```

The application will open in your default web browser at http://localhost:8501.

## Using the Tool

The application is organized into tabs:

1. **Basic Info**: Project name, team name, concept selection, and summary
2. **Team & Concept**: Team member details and concept explanation
3. **Market Analysis**: Competitor analysis and SWOT analysis
4. **Features**: Feature prioritization using the MoSCoW method
5. **Export**: Preview and download the proposal data as JSON

Students should work through each tab, filling in the required information. They can add multiple team members, competitors, features, and SWOT items as needed.

## Teaching Notes

### Classroom Integration

This tool works best when introduced after:
- The Project Concept Guide has been discussed
- SWOT analysis has been explained
- Competitor analysis methodology has been taught
- MoSCoW prioritization has been covered

### Implementation Exercise

Consider having students enhance this tool as a practical exercise:
- Add new fields or categories
- Implement a feature to import previously saved JSON data
- Add visualizations for the SWOT analysis
- Create a report generator that converts JSON to a formatted document

### Assessment Ideas

1. Have students submit both their JSON data and formal proposal document
2. Compare how well students translated their structured data into coherent proposals
3. Check for consistency between the JSON data and proposal document
4. Have students peer review each other's proposals using the JSON data as a reference

## Customization

You can modify this tool by:
- Adding or removing fields
- Changing the project concept options
- Adding validation for specific fields
- Creating a companion tool that reads the JSON and generates a formatted report

## Technical Notes

The application uses:
- Streamlit for the web interface
- Session state to maintain form data between interactions
- Base64 encoding for the download functionality
- JSON for data storage

## Troubleshooting

If students encounter issues:
1. Ensure all requirements are installed
2. Check that the browser allows downloads
3. Verify the JSON file can be opened in a text editor
4. Make sure students save their work (by downloading) before closing the browser