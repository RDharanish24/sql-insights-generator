"""
SQL Insights Generator — Streamlit Frontend
Premium dark-themed UI with interactive Plotly visualizations and agent trace panel.
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="SQL Insights Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Backend URL ---
API_URL = "http://localhost:8000"

# --- Custom CSS for Premium Design ---
st.markdown("""
<style>
    /* ===== Import Premium Font ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===== Global Styles ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ===== Hero Header ===== */
    .hero-header {
        text-align: center;
        padding: 2rem 1rem 1.5rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a4e 40%, #24243e 100%);
        border-radius: 20px;
        border: 1px solid rgba(108, 99, 255, 0.2);
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.15);
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(108, 99, 255, 0.05) 0%, transparent 70%);
        animation: pulse-bg 8s ease-in-out infinite;
    }
    @keyframes pulse-bg {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C63FF 0%, #48C6EF 50%, #6C63FF 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-flow 4s ease infinite;
        margin-bottom: 0.3rem;
        position: relative;
    }
    @keyframes gradient-flow {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    .hero-subtitle {
        color: #8B8FA3;
        font-size: 1.05rem;
        font-weight: 400;
        position: relative;
    }

    /* ===== Result Cards ===== */
    .result-card {
        background: linear-gradient(145deg, #1A1D29 0%, #14161E 100%);
        border: 1px solid rgba(108, 99, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .result-card:hover {
        border-color: rgba(108, 99, 255, 0.4);
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.12);
        transform: translateY(-2px);
    }
    .card-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #E0E0E0;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ===== Agent Trace Steps ===== */
    .trace-step {
        background: rgba(108, 99, 255, 0.06);
        border-left: 3px solid #6C63FF;
        border-radius: 0 10px 10px 0;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        transition: all 0.3s ease;
    }
    .trace-step:hover {
        background: rgba(108, 99, 255, 0.12);
        border-left-color: #48C6EF;
    }
    .trace-step-title {
        font-weight: 600;
        color: #6C63FF;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }
    .trace-step-content {
        color: #9CA3AF;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* ===== Sample Query Chips ===== */
    .chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    /* ===== Metric Cards ===== */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        flex: 1;
        background: linear-gradient(145deg, #1E2030 0%, #171925 100%);
        border: 1px solid rgba(108, 99, 255, 0.12);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #6C63FF;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6B7280;
        margin-top: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ===== Status Badge ===== */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-success {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-retry {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* ===== Sidebar Styling ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1A1D29 100%);
        border-right: 1px solid rgba(108, 99, 255, 0.1);
    }

    /* ===== Button Styling ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #5A52E0 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #7B73FF 0%, #6C63FF 100%);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.5);
        transform: translateY(-1px);
    }

    /* ===== Expander Styling ===== */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #6C63FF;
    }

    /* ===== Hide Streamlit Branding ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ===== Smooth scrolling ===== */
    html {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "current_result" not in st.session_state:
    st.session_state.current_result = None
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False


# --- Helper Functions ---
def call_api(question: str) -> dict:
    """Send a question to the FastAPI backend and return the response."""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"question": question},
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ **Cannot connect to the backend server.** Make sure the FastAPI server is running on port 8000.\n\n```bash\ncd backend && uvicorn api:api --host 0.0.0.0 --port 8000 --reload\n```")
        return None
    except requests.exceptions.Timeout:
        st.error("⏰ **Request timed out.** The query took too long to process. Try a simpler question.")
        return None
    except Exception as e:
        st.error(f"❌ **API Error:** {str(e)}")
        return None


def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create a premium horizontal bar chart."""
    # Sort by value for better visual
    df_sorted = df.sort_values(by=y_col, ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted[y_col],
        y=df_sorted[x_col],
        orientation='h',
        marker=dict(
            color=df_sorted[y_col],
            colorscale=[
                [0, '#2D1B69'],
                [0.25, '#4834D4'],
                [0.5, '#6C63FF'],
                [0.75, '#48C6EF'],
                [1, '#00F5A0']
            ],
            line=dict(width=0),
            cornerradius=6
        ),
        text=[f"  {v:,.2f}" if isinstance(v, float) else f"  {v:,}" for v in df_sorted[y_col]],
        textposition='outside',
        textfont=dict(color='#E0E0E0', size=12, family='Inter'),
        hovertemplate='<b>%{y}</b><br>%{x:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color='#E0E0E0', family='Inter'),
            x=0.5, xanchor='center'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9CA3AF', family='Inter'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(108, 99, 255, 0.08)',
            gridwidth=1,
            zeroline=False,
            title=dict(text=y_col.replace('_', ' ').title(), font=dict(size=13))
        ),
        yaxis=dict(
            showgrid=False,
            title=None,
            tickfont=dict(size=13)
        ),
        margin=dict(l=20, r=40, t=60, b=40),
        height=max(350, len(df_sorted) * 45 + 100),
        hoverlabel=dict(
            bgcolor='#1A1D29',
            bordercolor='#6C63FF',
            font=dict(color='#E0E0E0', family='Inter')
        )
    )
    return fig


def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create a premium line chart with area fill."""
    fig = go.Figure()

    # Area fill under the line
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        fill='tozeroy',
        fillcolor='rgba(108, 99, 255, 0.08)',
        line=dict(color='#6C63FF', width=3, shape='spline'),
        mode='lines+markers',
        marker=dict(
            size=8,
            color='#6C63FF',
            line=dict(width=2, color='#0E1117'),
            symbol='circle'
        ),
        hovertemplate='<b>%{x}</b><br>%{y:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color='#E0E0E0', family='Inter'),
            x=0.5, xanchor='center'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9CA3AF', family='Inter'),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(108, 99, 255, 0.06)',
            gridwidth=1,
            zeroline=False,
            title=dict(text=x_col.replace('_', ' ').title(), font=dict(size=13)),
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(108, 99, 255, 0.08)',
            gridwidth=1,
            zeroline=False,
            title=dict(text=y_col.replace('_', ' ').title(), font=dict(size=13))
        ),
        margin=dict(l=20, r=20, t=60, b=60),
        height=400,
        hoverlabel=dict(
            bgcolor='#1A1D29',
            bordercolor='#6C63FF',
            font=dict(color='#E0E0E0', family='Inter')
        )
    )
    return fig


def render_chart(result: dict):
    """Render the appropriate chart based on the chart recommendation."""
    chart_rec = result.get("chart_recommendation", {})
    chart_type = chart_rec.get("type", "none")

    if chart_type == "none" or not result.get("data") or not result.get("columns"):
        return

    try:
        df = pd.DataFrame(result["data"], columns=result["columns"])
        x_col = chart_rec.get("x_column")
        y_col = chart_rec.get("y_column")
        title = chart_rec.get("title", "Query Results")

        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            return

        # Ensure y column is numeric
        df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
        df = df.dropna(subset=[y_col])

        if df.empty:
            return

        st.markdown(f"""
        <div class="result-card">
            <div class="card-header">📈 Data Visualization</div>
        </div>
        """, unsafe_allow_html=True)

        if chart_type == "bar":
            fig = create_bar_chart(df, x_col, y_col, title)
        elif chart_type == "line":
            fig = create_line_chart(df, x_col, y_col, title)
        else:
            return

        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d']
        })

    except Exception as e:
        st.caption(f"⚠️ Could not generate chart: {str(e)}")


def render_agent_trace(result: dict):
    """Render the step-by-step agent execution trace."""
    retries = result.get("retries", 0)

    steps = [
        {
            "icon": "📋",
            "name": "Planner Agent",
            "description": "Decomposed the question into a logical execution plan",
            "content": result.get("plan", "No plan generated"),
            "status": "✅"
        },
        {
            "icon": "🛠️",
            "name": "SQL Generator Agent",
            "description": "Generated an optimized SQL query",
            "content": f"```sql\n{result.get('sql_query', 'No SQL generated')}\n```",
            "status": "✅"
        },
        {
            "icon": "⚡",
            "name": "SQL Executor",
            "description": f"Executed the query against the database — returned {len(result.get('data', []))} rows",
            "content": f"Columns: {', '.join(result.get('columns', []))}",
            "status": "✅" if not result.get("error") else "❌"
        },
    ]

    if retries > 0:
        steps.append({
            "icon": "🔧",
            "name": "SQL Validator Agent",
            "description": f"Auto-corrected the SQL query ({retries} attempt{'s' if retries > 1 else ''})",
            "content": "The initial query had errors and was automatically fixed by the validation agent.",
            "status": "🔄"
        })

    steps.extend([
        {
            "icon": "📊",
            "name": "Analyst Agent",
            "description": "Performed statistical analysis on the results",
            "content": result.get("analysis", "No analysis available"),
            "status": "✅"
        },
        {
            "icon": "💡",
            "name": "Insight Generator Agent",
            "description": "Translated analysis into business insights",
            "content": result.get("insights", "No insights available"),
            "status": "✅"
        }
    ])

    for step in steps:
        st.markdown(f"""
        <div class="trace-step">
            <div class="trace-step-title">{step['status']} {step['icon']} {step['name']}</div>
            <div class="trace-step-content">{step['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander(f"View {step['name']} Output", expanded=False):
            st.markdown(step["content"])


# ==========================================
# MAIN UI LAYOUT
# ==========================================

# --- Hero Header ---
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🧠 SQL Insights Generator</div>
    <div class="hero-subtitle">Ask business questions in plain English • Get AI-powered SQL, data, and insights instantly</div>
</div>
""", unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🚀 Quick Queries")
    st.caption("Click any query below to auto-fill the input")

    sample_queries = [
        "🏆 Top 5 products by revenue",
        "📈 Monthly revenue trend for 2023",
        "🌍 Total revenue by country",
        "📦 Best performing product category",
        "👥 How many orders did each user place?",
        "💰 What is the total revenue?",
        "🏅 Who is the highest spending customer?",
        "📊 Average order value by country",
    ]

    for query in sample_queries:
        # Strip emoji prefix for the actual query
        clean_query = query.split(" ", 1)[1] if query[0] in "🏆📈🌍📦👥💰🏅📊" else query
        if st.button(query, key=f"sample_{clean_query}", use_container_width=True):
            st.session_state.selected_query = clean_query

    st.markdown("---")

    # Query History
    st.markdown("### 📜 Query History")
    if st.session_state.query_history:
        for i, hist in enumerate(reversed(st.session_state.query_history[-10:])):
            with st.expander(f"Q: {hist['question'][:40]}...", expanded=False):
                st.caption(f"**SQL:** `{hist.get('sql_query', 'N/A')[:80]}...`")
                st.caption(f"**Rows:** {len(hist.get('data', []))}")
    else:
        st.caption("No queries yet. Ask your first question!")

    st.markdown("---")

    # Reset button
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.query_history = []
        st.session_state.current_result = None
        try:
            requests.post(f"{API_URL}/reset", timeout=5)
        except Exception:
            pass
        st.rerun()


# --- Main Query Input Area ---
col_input, col_btn = st.columns([5, 1])

with col_input:
    # Use selected query if available
    default_value = st.session_state.pop("selected_query", "")
    user_question = st.text_input(
        "Ask a business question",
        value=default_value,
        placeholder="e.g., What are the top 5 products by revenue?",
        label_visibility="collapsed",
        key="question_input"
    )

with col_btn:
    analyze_clicked = st.button("🔍 Analyze", use_container_width=True, type="primary")


# --- Process Query ---
if analyze_clicked and user_question.strip():
    with st.spinner(""):
        # Custom loading animation
        loading_placeholder = st.empty()
        loading_placeholder.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
            <div style="color: #6C63FF; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">
                Agents are working...
            </div>
            <div style="color: #6B7280; font-size: 0.85rem;">
                Planner → SQL Generator → Executor → Analyst → Insight Generator
            </div>
        </div>
        """, unsafe_allow_html=True)

        result = call_api(user_question)
        loading_placeholder.empty()

        if result:
            st.session_state.current_result = result
            st.session_state.query_history.append(result)


# --- Display Results ---
if st.session_state.current_result:
    result = st.session_state.current_result

    # --- Metrics Row ---
    retries = result.get("retries", 0)
    row_count = len(result.get("data", []))
    col_count = len(result.get("columns", []))
    has_error = bool(result.get("error"))

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{row_count}</div>
            <div class="metric-label">Rows Returned</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{col_count}</div>
            <div class="metric-label">Columns</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        badge_class = "status-success" if not has_error else "status-retry"
        badge_text = "Success" if not has_error else "Error"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value"><span class="status-badge {badge_class}">{'✅' if not has_error else '❌'} {badge_text}</span></div>
            <div class="metric-label">Status</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{retries}</div>
            <div class="metric-label">Auto-Corrections</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Section 1: SQL Query ---
    st.markdown("""
    <div class="result-card">
        <div class="card-header">🛠️ Generated SQL Query</div>
    </div>
    """, unsafe_allow_html=True)
    st.code(result.get("sql_query", "No SQL generated"), language="sql")

    # --- Two Column Layout for Data + Insights ---
    col_data, col_insights = st.columns([1, 1])

    with col_data:
        # --- Section 2: Raw Data ---
        st.markdown("""
        <div class="result-card">
            <div class="card-header">📋 Query Results</div>
        </div>
        """, unsafe_allow_html=True)

        if result.get("data") and result.get("columns"):
            df = pd.DataFrame(result["data"], columns=result["columns"])
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=min(400, len(df) * 40 + 60)
            )
        else:
            st.info("No data returned for this query.")

    with col_insights:
        # --- Section 3: Business Insights ---
        st.markdown("""
        <div class="result-card">
            <div class="card-header">💡 Business Insights</div>
        </div>
        """, unsafe_allow_html=True)

        insights_text = result.get("insights", "No insights available.")
        if insights_text:
            st.markdown(insights_text)
        else:
            st.info("No insights generated.")

    # --- Section 4: Visualization ---
    render_chart(result)

    # --- Section 5: Agent Trace (Collapsible) ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔗 **Agent Execution Trace** — View the step-by-step AI pipeline", expanded=False):
        render_agent_trace(result)

elif not st.session_state.current_result:
    # --- Welcome State ---
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; margin-top: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
        <div style="color: #6B7280; font-size: 1.15rem; font-weight: 500; margin-bottom: 0.5rem;">
            Ask any business question in plain English
        </div>
        <div style="color: #4B5563; font-size: 0.9rem;">
            The AI agents will plan, write SQL, execute it, analyze the results, and generate insights — all automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature highlights
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">📋</div>
            <div style="color: #E0E0E0; font-weight: 600; font-size: 0.9rem;">Smart Planning</div>
            <div style="color: #6B7280; font-size: 0.75rem; margin-top: 0.2rem;">AI decomposes your question into logical steps</div>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">🛠️</div>
            <div style="color: #E0E0E0; font-weight: 600; font-size: 0.9rem;">SQL Generation</div>
            <div style="color: #6B7280; font-size: 0.75rem; margin-top: 0.2rem;">Optimized queries written by AI agents</div>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">📊</div>
            <div style="color: #E0E0E0; font-weight: 600; font-size: 0.9rem;">Auto Visualization</div>
            <div style="color: #6B7280; font-size: 0.75rem; margin-top: 0.2rem;">Charts generated based on data type</div>
        </div>
        """, unsafe_allow_html=True)
    with f4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">💡</div>
            <div style="color: #E0E0E0; font-weight: 600; font-size: 0.9rem;">Business Insights</div>
            <div style="color: #6B7280; font-size: 0.75rem; margin-top: 0.2rem;">Actionable recommendations from your data</div>
        </div>
        """, unsafe_allow_html=True)
