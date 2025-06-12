import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Roland Garros Finals Explorer",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Amazing Custom CSS for Professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500;600&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Custom CSS Variables */
    :root {
        --primary-color: #D2691E;
        --secondary-color: #FF8C42;
        --accent-color: #FFB347;
        --dark-bg: #1a1a1a;
        --light-bg: #f8f9fa;
        --text-primary: #2c3e50;
        --text-light: #7f8c8d;
        --success-color: #27ae60;
        --warning-color: #f39c12;
        --danger-color: #e74c3c;
        --gradient-1: linear-gradient(135deg, #D2691E 0%, #FF8C42 50%, #FFB347 100%);
        --gradient-2: linear-gradient(135deg, #FF8C42 0%, #D2691E 100%);
        --clay-gradient: linear-gradient(135deg, #8B4513 0%, #D2691E 30%, #FF8C42 70%, #FFB347 100%);
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Stunning Header Design */
    .main-header {
        background: var(--clay-gradient);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 15px 35px rgba(210, 105, 30, 0.3);
        position: relative;
        overflow: hidden;
        text-align: center;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
        animation: float 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes float {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .header-title {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
        position: relative;
        z-index: 2;
    }
    
    .header-subtitle {
        font-size: 1.4rem;
        color: rgba(255,255,255,0.95);
        font-weight: 300;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
    }
    
    .header-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1.5rem;
        position: relative;
        z-index: 2;
    }
    
    .header-stat {
        background: rgba(255,255,255,0.2);
        padding: 1rem 1.5rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        text-align: center;
        min-width: 120px;
    }
    
    .header-stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        display: block;
    }
    
    .header-stat-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        margin-top: 0.2rem;
    }
    
    /* Section Headers */
    .section-header {
        background: var(--gradient-2);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin: 2rem 0 1rem 0;
        font-size: 1.8rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 8px 25px rgba(210, 105, 30, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Cards and Containers */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        transition: all 0.3s ease;
        margin: 1rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(210, 105, 30, 0.2);
        border-color: var(--primary-color);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-1);
        border-radius: 20px 20px 0 0;
    }
    
    .player-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .champion-badge {
        background: var(--gradient-1);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Stats Display */
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid #eee;
    }
    
    .stat-row:last-child {
        border-bottom: none;
    }
    
    .stat-label {
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .stat-value {
        font-weight: 700;
        color: var(--primary-color);
        font-size: 1.1rem;
    }
    
    /* Tennis Score Styling */
    .stat-value.tennis-score {
        font-family: 'Roboto Mono', monospace !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        color: var(--primary-color) !important;
        background: rgba(210, 105, 30, 0.1) !important;
        padding: 0.3rem 0.8rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(210, 105, 30, 0.2) !important;
        display: inline-block !important;
        white-space: nowrap !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--gradient-1);
    }
    
    .css-1lcbmhc {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Buttons and Inputs */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid var(--primary-color);
        border-radius: 10px;
        font-weight: 500;
    }
    
    .stSlider > div > div > div {
        background: var(--gradient-1);
    }
    
    /* Simulation Section */
    .simulation-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid var(--accent-color);
        margin: 2rem 0;
        position: relative;
    }
    
    .simulation-container::before {
        content: '🔮';
        position: absolute;
        top: -15px;
        left: 30px;
        background: white;
        padding: 0.5rem;
        border-radius: 50%;
        font-size: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Footer Styling */
    .app-footer {
        background: var(--dark-bg);
        color: white;
        padding: 3rem 2rem 2rem 2rem;
        margin: 3rem -1rem -1rem -1rem;
        border-radius: 20px 20px 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .app-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-1);
    }
    
    .footer-content {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-section h3 {
        color: var(--accent-color);
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .footer-section p, .footer-section li {
        color: #bbb;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .footer-section ul {
        list-style: none;
        padding: 0;
    }
    
    .footer-section ul li::before {
        content: '🎾';
        margin-right: 0.5rem;
    }
    
    .footer-bottom {
        text-align: center;
        padding-top: 2rem;
        border-top: 1px solid #333;
        color: var(--text-light);
    }
    
    .footer-logo {
        font-size: 2rem;
        font-weight: 700;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Fun Facts Cards */
    .fun-fact-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-top: 4px solid var(--primary-color);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .fun-fact-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(210, 105, 30, 0.15);
    }
    
    .fun-fact-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .fun-fact-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .fun-fact-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .fun-fact-subtitle {
        font-size: 0.9rem;
        color: var(--text-light);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.5rem;
        }
        
        .header-stats {
            flex-direction: column;
            gap: 1rem;
        }
        
        .footer-content {
            grid-template-columns: 1fr;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Enhanced Prediction Badge */
    .prediction-badge {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
        animation: pulse 2s infinite;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    @keyframes pulse {
        0% { 
            box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 8px 30px rgba(231, 76, 60, 0.6);
            transform: scale(1.02);
        }
        100% { 
            box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
            transform: scale(1);
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the tennis data"""
    df = pd.read_csv('roland_garros_finals_2000_2025.csv')
    
    # Clean and process data - handle mixed date formats
    def extract_year(date_str):
        if pd.isna(date_str):
            return None
        date_str = str(date_str)
        if date_str.startswith('2025'):
            return 2025
        try:
            return pd.to_datetime(date_str).year
        except:
            # Extract year from string like "2025-06-08"
            return int(date_str.split('-')[0]) if '-' in date_str else int(date_str[:4])
    
    df['year'] = df['date'].apply(extract_year)
    
    df['duration_minutes'] = df['duration'].apply(lambda x: 
        int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if pd.notna(x) and ':' in str(x) else 0)
    
    # Calculate additional metrics
    df['total_aces'] = df['aces_champion'] + df['aces_runner_up']
    df['total_winners'] = df['winners_champion'] + df['winners_runner_up']
    df['total_errors'] = df['uf_errors_champion'] + df['uf_errors_runner_up']
    df['serve_diff'] = df['first_serve_pct_champion'] - df['first_serve_pct_runner_up']
    df['winner_efficiency'] = df['winners_champion'] / (df['winners_champion'] + df['uf_errors_champion'])
    df['is_prediction'] = df['date'].str.contains('2025', na=False)
    
    return df

def create_stunning_header():
    """Create an amazing header section"""
    df = load_data()
    
    st.markdown(f"""
    <div class="main-header">
        <div class="header-title">🎾 Roland Garros Finals Explorer</div>
        <div class="header-subtitle">
            Advanced Analytics • Machine Learning Predictions • Interactive Simulations
        </div>
        <div class="header-stats">
            <div class="header-stat">
                <span class="header-stat-number">{len(df)}</span>
                <div class="header-stat-label">Finals Analyzed</div>
            </div>
            <div class="header-stat">
                <span class="header-stat-number">25+</span>
                <div class="header-stat-label">Years of Data</div>
            </div>
            <div class="header-stat">
                <span class="header-stat-number">{len(df['champion'].unique())}</span>
                <div class="header-stat-label">Champions</div>
            </div>
            <div class="header-stat">
                <span class="header-stat-number">14</span>
                <div class="header-stat-label">Nadal Titles</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_amazing_footer():
    """Create a professional footer"""
    st.markdown("""
    <div class="app-footer">
        <div class="footer-content">
            <div class="footer-section">
                <div class="footer-logo">🎾 Roland Garros Explorer</div>
                <p>The most comprehensive interactive analysis of Roland Garros Finals from 2000-2025, featuring advanced analytics, machine learning predictions, and counterfactual simulations.</p>
            </div>
            
            <div class="footer-section">
                <h3>🔥 Key Features</h3>
                <ul>
                    <li>25+ years of comprehensive data</li>
                    <li>AI-powered match predictions</li>
                    <li>Interactive counterfactual analysis</li>
                    <li>Advanced performance metrics</li>
                    <li>Historical trend visualization</li>
                </ul>
            </div>
            
            <div class="footer-section">
                <h3>🛠️ Built With</h3>
                <ul>
                    <li>Python & Streamlit</li>
                    <li>Pandas & NumPy</li>
                    <li>Plotly & Matplotlib</li>
                    <li>Advanced Data Science</li>
                    <li>Machine Learning</li>
                </ul>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>© 2025 Roland Garros Finals Explorer | Built with ❤️ for Tennis Analytics Enthusiasts</p>
            <p>🚀 <strong>Ready for LinkedIn?</strong> Share this interactive experience and showcase your data science skills!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_match_comparison_radar(champion_stats, runner_up_stats, champion_name, runner_up_name):
    """Create radar chart comparing two players"""
    categories = ['Aces', 'First Serve %', 'Winners', 'Break Points Saved', 'Total Points']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=champion_stats,
        theta=categories,
        fill='toself',
        name=champion_name,
        line_color='#D2691E',
        fillcolor='rgba(210, 105, 30, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=runner_up_stats,
        theta=categories,
        fill='toself',
        name=runner_up_name,
        line_color='#3498db',
        fillcolor='rgba(52, 152, 219, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Player Performance Comparison",
        height=500,
        font=dict(family="Poppins, sans-serif")
    )
    
    return fig

def create_historical_trends(df):
    """Create historical trends visualization"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Match Duration Over Time', 'Total Aces Per Final', 
                       'Average First Serve %', 'Total Winners Per Match'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Match duration trend
    fig.add_trace(
        go.Scatter(x=df['year'], y=df['duration_minutes'], 
                  mode='lines+markers', name='Duration (min)',
                  line=dict(color='#D2691E', width=3)),
        row=1, col=1
    )
    
    # Total aces trend
    fig.add_trace(
        go.Scatter(x=df['year'], y=df['total_aces'], 
                  mode='lines+markers', name='Total Aces',
                  line=dict(color='#FF8C42', width=3)),
        row=1, col=2
    )
    
    # Average first serve percentage
    avg_serve = (df['first_serve_pct_champion'] + df['first_serve_pct_runner_up']) / 2
    fig.add_trace(
        go.Scatter(x=df['year'], y=avg_serve, 
                  mode='lines+markers', name='Avg First Serve %',
                  line=dict(color='#27ae60', width=3)),
        row=2, col=1
    )
    
    # Total winners
    fig.add_trace(
        go.Scatter(x=df['year'], y=df['total_winners'], 
                  mode='lines+markers', name='Total Winners',
                  line=dict(color='#e74c3c', width=3)),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600, 
        showlegend=False,
        font=dict(family="Poppins, sans-serif")
    )
    fig.update_xaxes(title_text="Year")
    
    return fig

def calculate_player_dominance_score(row):
    """Calculate a dominance score based on various metrics"""
    serve_advantage = (row['first_serve_pct_champion'] - row['first_serve_pct_runner_up']) / 100
    ace_advantage = (row['aces_champion'] - row['aces_runner_up']) / max(row['aces_champion'] + row['aces_runner_up'], 1)
    winner_advantage = (row['winners_champion'] - row['winners_runner_up']) / max(row['winners_champion'] + row['winners_runner_up'], 1)
    points_advantage = (row['tot_points_champion'] - row['tot_points_runner_up']) / max(row['tot_points_champion'] + row['tot_points_runner_up'], 1)
    
    return (serve_advantage + ace_advantage + winner_advantage + points_advantage) * 100

def format_score(score_str):
    """Format tennis score for better readability"""
    if pd.isna(score_str) or not score_str:
        return "Score not available"
    
    score = str(score_str)
    
    # Replace commas with proper spacing for set separation
    # Tennis scores are typically separated by commas for each set
    formatted_score = score.replace(',', '  ')
    
    # Add proper spacing around tiebreak scores for better readability
    # Handle tiebreak formatting: 6-7(4-7) becomes 6-7 (4-7)
    formatted_score = formatted_score.replace('(', ' (').replace(')', ')')
    
    # Clean up multiple spaces and ensure consistent spacing
    formatted_score = ' '.join(formatted_score.split())
    
    # Add a bit more spacing between sets for better visual separation
    formatted_score = formatted_score.replace('  ', '   ')
    
    return formatted_score

def format_duration(duration_str):
    """Format match duration for better display"""
    if pd.isna(duration_str) or not duration_str:
        return "Duration not available"
    return str(duration_str)

def format_umpire(umpire_str):
    """Format umpire name"""
    if pd.isna(umpire_str) or not umpire_str:
        return "Umpire not available"
    return str(umpire_str).strip()

def main():
    # Create stunning header
    create_stunning_header()
    
    # Load data
    df = load_data()
    
    # Sidebar with amazing styling
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #D2691E, #FF8C42); border-radius: 15px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0; font-family: 'Poppins', sans-serif;">🎯 Control Panel</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Year selection
    available_years = sorted(df['year'].unique())
    selected_year = st.sidebar.selectbox(
        "🏆 Select Final Year",
        available_years,
        index=len(available_years)-1  # Default to most recent
    )
    
    # Get selected match data
    selected_match = df[df['year'] == selected_year].iloc[0]
    
    # Match Overview Section
    st.markdown('<div class="section-header">🏆 Match Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced prediction badge logic
        if selected_match['is_prediction']:
            prediction_badge = '<div style="text-align: center; margin: 1rem 0;"><span class="prediction-badge">🔮 AI PREDICTION FOR 2025</span></div>'
        else:
            prediction_badge = ''
        
        # Enhanced match display with better formatting
        champion_name = selected_match['champion'] if pd.notna(selected_match['champion']) else "Unknown Champion"
        runner_up_name = selected_match['runner_up'] if pd.notna(selected_match['runner_up']) else "Unknown Runner-up"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="player-name">
                🥇 {champion_name}
                <span class="champion-badge">CHAMPION</span>
            </div>
            <div class="player-name" style="margin-bottom: 1.5rem;">
                🥈 {runner_up_name}
            </div>
            
            <div class="stat-row">
                <span class="stat-label">📊 Final Score</span>
                <span class="stat-value tennis-score">
                    {format_score(selected_match['score'])}
                </span>
            </div>
            <div class="stat-row">
                <span class="stat-label">⏱️ Duration</span>
                <span class="stat-value">{format_duration(selected_match['duration'])}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">📅 Year</span>
                <span class="stat-value">{selected_match['year']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">👨‍⚖️ Umpire</span>
                <span class="stat-value">{format_umpire(selected_match['umpire'])}</span>
            </div>
            
            {prediction_badge}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        dominance_score = calculate_player_dominance_score(selected_match)
        
        # Enhanced dominance score display
        dominance_level = "Dominant" if dominance_score > 15 else "Competitive" if dominance_score > 5 else "Very Close"
        dominance_color = "#27ae60" if dominance_score > 15 else "#f39c12" if dominance_score > 5 else "#e74c3c"
        dominance_icon = "🔥" if dominance_score > 15 else "⚔️" if dominance_score > 5 else "🤝"
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 3rem; color: {dominance_color};">{dominance_icon}</div>
                <div style="font-size: 2.5rem; font-weight: 700; color: {dominance_color}; margin: 1rem 0;">
                    {dominance_score:.1f}%
                </div>
                <div style="font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem;">Dominance Score</div>
                <div style="background: {dominance_color}; color: white; padding: 0.3rem 1rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem;">
                    {dominance_level}
                </div>
                <div style="font-size: 0.8rem; color: #7f8c8d; line-height: 1.4;">
                    Based on serve %, aces, winners, and total points differential
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Head-to-Head Comparison
    st.markdown('<div class="section-header">⚔️ Head-to-Head Statistical Comparison</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="player-name">🥇 {selected_match['champion']}</div>
            <div class="stat-row">
                <span class="stat-label">🎾 Aces</span>
                <span class="stat-value">{selected_match['aces_champion']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">🎯 First Serve %</span>
                <span class="stat-value">{selected_match['first_serve_pct_champion']}%</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">🔥 Winners</span>
                <span class="stat-value">{selected_match['winners_champion']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">❌ Errors</span>
                <span class="stat-value">{selected_match['uf_errors_champion']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">📊 Total Points</span>
                <span class="stat-value">{selected_match['tot_points_champion']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="player-name">🥈 {selected_match['runner_up']}</div>
            <div class="stat-row">
                <span class="stat-label">🎾 Aces</span>
                <span class="stat-value">{selected_match['aces_runner_up']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">🎯 First Serve %</span>
                <span class="stat-value">{selected_match['first_serve_pct_runner_up']}%</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">🔥 Winners</span>
                <span class="stat-value">{selected_match['winners_runner_up']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">❌ Errors</span>
                <span class="stat-value">{selected_match['uf_errors_runner_up']}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">📊 Total Points</span>
                <span class="stat-value">{selected_match['tot_points_runner_up']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Radar chart
        champion_stats = [
            selected_match['aces_champion'],
            selected_match['first_serve_pct_champion'],
            selected_match['winners_champion'],
            float(selected_match['break_saved_champion'].split('/')[0]) / float(selected_match['break_saved_champion'].split('/')[1]) * 100 if '/' in str(selected_match['break_saved_champion']) else 0,
            selected_match['tot_points_champion'] / (selected_match['tot_points_champion'] + selected_match['tot_points_runner_up']) * 100
        ]
        
        runner_up_stats = [
            selected_match['aces_runner_up'],
            selected_match['first_serve_pct_runner_up'],
            selected_match['winners_runner_up'],
            float(selected_match['break_saved_runner_up'].split('/')[0]) / float(selected_match['break_saved_runner_up'].split('/')[1]) * 100 if '/' in str(selected_match['break_saved_runner_up']) else 0,
            selected_match['tot_points_runner_up'] / (selected_match['tot_points_champion'] + selected_match['tot_points_runner_up']) * 100
        ]
        
        radar_chart = create_match_comparison_radar(
            champion_stats, runner_up_stats,
            selected_match['champion'], selected_match['runner_up']
        )
        st.plotly_chart(radar_chart, use_container_width=True)
    
    # Counterfactual simulation section
    st.markdown('<div class="section-header">🔮 Interactive Counterfactual Simulation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="simulation-container">
        <h3 style="margin-top: 0; color: #2c3e50; font-family: 'Poppins', sans-serif;">
            What if the match statistics were different? 
        </h3>
        <p style="color: #7f8c8d; margin-bottom: 2rem;">
            Adjust the sliders below to see how different performance levels might have changed the match outcome!
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🥇 Adjust Champion's Performance")
        new_serve_pct_champ = st.slider(
            "Champion First Serve %",
            40, 90,
            int(selected_match['first_serve_pct_champion']),
            key="champ_serve"
        )
        new_winners_champ = st.slider(
            "Champion Winners",
            10, 80,
            int(selected_match['winners_champion']),
            key="champ_winners"
        )
        new_errors_champ = st.slider(
            "Champion Unforced Errors",
            5, 60,
            int(selected_match['uf_errors_champion']),
            key="champ_errors"
        )
    
    with col2:
        st.markdown("#### 🥈 Adjust Runner-up's Performance")
        new_serve_pct_runner = st.slider(
            "Runner-up First Serve %",
            40, 90,
            int(selected_match['first_serve_pct_runner_up']),
            key="runner_serve"
        )
        new_winners_runner = st.slider(
            "Runner-up Winners",
            10, 80,
            int(selected_match['winners_runner_up']),
            key="runner_winners"
        )
        new_errors_runner = st.slider(
            "Runner-up Unforced Errors",
            5, 60,
            int(selected_match['uf_errors_runner_up']),
            key="runner_errors"
        )
    
    # Calculate simulated outcome
    original_dominance = calculate_player_dominance_score(selected_match)
    
    # Create modified match data for simulation
    modified_match = selected_match.copy()
    modified_match['first_serve_pct_champion'] = new_serve_pct_champ
    modified_match['first_serve_pct_runner_up'] = new_serve_pct_runner
    modified_match['winners_champion'] = new_winners_champ
    modified_match['winners_runner_up'] = new_winners_runner
    modified_match['uf_errors_champion'] = new_errors_champ
    modified_match['uf_errors_runner_up'] = new_errors_runner
    
    new_dominance = calculate_player_dominance_score(modified_match)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">📊</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #2c3e50;">
                    {original_dominance:.1f}%
                </div>
                <div style="font-weight: 600; color: #7f8c8d;">Original Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        diff_color = "#27ae60" if new_dominance > original_dominance else "#e74c3c" if new_dominance < original_dominance else "#f39c12"
        diff_icon = "📈" if new_dominance > original_dominance else "📉" if new_dominance < original_dominance else "➡️"
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">{diff_icon}</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {diff_color};">
                    {new_dominance:.1f}%
                </div>
                <div style="font-weight: 600; color: #7f8c8d;">Simulated Score</div>
                <div style="color: {diff_color}; font-weight: 600; margin-top: 0.5rem;">
                    {new_dominance - original_dominance:+.1f}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        outcome_change = "More Dominant" if new_dominance > original_dominance else "Less Dominant" if new_dominance < original_dominance else "Same"
        outcome_icon = "🔥" if new_dominance > original_dominance else "❄️" if new_dominance < original_dominance else "⚖️"
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">{outcome_icon}</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #2c3e50;">
                    {outcome_change}
                </div>
                <div style="font-weight: 600; color: #7f8c8d;">Predicted Impact</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Historical trends
    st.markdown('<div class="section-header">📈 Historical Trends Analysis (2000-2025)</div>', unsafe_allow_html=True)
    
    trends_chart = create_historical_trends(df)
    st.plotly_chart(trends_chart, use_container_width=True)
    
    # Player statistics over the years
    st.markdown('<div class="section-header">🎾 Player Performance Analytics</div>', unsafe_allow_html=True)
    
    # Champion frequency
    champion_counts = df['champion'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            x=champion_counts.values,
            y=champion_counts.index,
            orientation='h',
            title="Most Successful Champions",
            color=champion_counts.values,
            color_continuous_scale=['#FFB347', '#FF8C42', '#D2691E']
        )
        fig.update_layout(height=400, showlegend=False, font=dict(family="Poppins, sans-serif"))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average match duration by decade
        df['decade'] = (df['year'] // 10) * 10
        decade_duration = df.groupby('decade')['duration_minutes'].mean()
        
        fig = px.line(
            x=decade_duration.index,
            y=decade_duration.values,
            title="Average Match Duration by Decade",
            markers=True
        )
        fig.update_traces(line_color='#D2691E', line_width=4, marker_size=10)
        fig.update_layout(height=400, font=dict(family="Poppins, sans-serif"))
        st.plotly_chart(fig, use_container_width=True)
    
    # Fun facts section
    st.markdown('<div class="section-header">🎯 Fascinating Tennis Facts</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        longest_match = df.loc[df['duration_minutes'].idxmax()]
        st.markdown(f"""
        <div class="fun-fact-card">
            <span class="fun-fact-icon">⏰</span>
            <div class="fun-fact-title">Longest Final</div>
            <div class="fun-fact-value">{longest_match['duration']}</div>
            <div class="fun-fact-subtitle">{longest_match['champion']} vs {longest_match['runner_up']} ({longest_match['year']})</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        most_aces_match = df.loc[df['total_aces'].idxmax()]
        st.markdown(f"""
        <div class="fun-fact-card">
            <span class="fun-fact-icon">🎾</span>
            <div class="fun-fact-title">Most Aces</div>
            <div class="fun-fact-value">{most_aces_match['total_aces']}</div>
            <div class="fun-fact-subtitle">{most_aces_match['champion']} vs {most_aces_match['runner_up']} ({most_aces_match['year']})</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        most_winners_match = df.loc[df['total_winners'].idxmax()]
        st.markdown(f"""
        <div class="fun-fact-card">
            <span class="fun-fact-icon">🔥</span>
            <div class="fun-fact-title">Most Winners</div>
            <div class="fun-fact-value">{most_winners_match['total_winners']}</div>
            <div class="fun-fact-subtitle">{most_winners_match['champion']} vs {most_winners_match['runner_up']} ({most_winners_match['year']})</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        nadal_titles = len(df[df['champion'] == 'Rafael Nadal'])
        st.markdown(f"""
        <div class="fun-fact-card">
            <span class="fun-fact-icon">👑</span>
            <div class="fun-fact-title">Nadal's Titles</div>
            <div class="fun-fact-value">{nadal_titles}</div>
            <div class="fun-fact-subtitle">King of Clay</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create amazing footer
    create_amazing_footer()

if __name__ == "__main__":
    main() 