
import streamlit as st
from utils.content_score import calculate_content_score
from agents.orchestrator_agent import OrchestratorAgent
from models import OrchestratorInput

st.set_page_config(
    page_title="SocialPilot AI",
    page_icon="🚀",
    layout="wide",
)

st.markdown("""
<style>

.block-container{
    padding-top: 2rem;
}

.agent-card{
    background:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #2d3748;
    text-align:center;
}

.metric-card{
    background:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #2d3748;
}

.success-banner{
    background:#14532d;
    padding:15px;
    border-radius:12px;
    border:1px solid #22c55e;
}

</style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 SocialPilot AI")

st.markdown("""
### AI-Powered Multi-Agent Social Media Assistant

Generate platform-specific content using:

🔥 Trend Agent  
✍️ Writer Agent  
🛡️ Safety Agent  
📅 Scheduler Agent
""")

# Architecture Diagram
st.markdown("## SocialPilot AI")

card1, card2, card3, card4 = st.columns(4)

with card1:
    st.info("🔥 Trend Agent\n\nResearches trends & hashtags")

with card2:
    st.info("✍️ Writer Agent\n\nCreates engaging content")

with card3:
    st.info("🛡️ Safety Agent\n\nReviews content")

with card4:
    st.info("📅 Scheduler Agent\n\nSchedules approved posts")

# Sidebar
st.sidebar.header("Settings")

platform = st.sidebar.selectbox(
    "Platform",
    ["LinkedIn", "X", "Instagram", "YouTube"]
)

goal = st.sidebar.selectbox(
    "Goal",
    [
        "Personal Branding",
        "Lead Generation",
        "Product Marketing",
        "Community Growth",
        "YouTube Growth"
    ]
)

tone = st.sidebar.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Educational",
        "Thought Leadership"
    ]
)

# User Input
topic = st.text_input(
    "What would you like to create content about?"
)

if st.button("Generate Content"):

    # Empty input protection
    if not topic.strip():
        st.error("Please enter a topic.")
        st.stop()

    with st.spinner("Running AI Agents..."):

        orchestrator = OrchestratorAgent()

        result = orchestrator.run(
            OrchestratorInput(
                user_topic=topic,
                goal=goal,
                tone=tone,
                platform=platform.lower(),
            )
        )
        
        # Calculate content score from the first variation
        score = calculate_content_score(
            result.writer_output.post_content
        )

    st.success("Content Generated Successfully!")

    # ==========================
    # Content Quality Score (FIRST)
    # ==========================
    st.subheader("📊 Content Quality Score")

    st.metric(
        "Overall Score",
        f"{score['overall_score']}/100"
    )

    st.success(
        f"🏆 {score['grade']}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🎣 Hook",
            f"{score['hook_strength']}/10"
        )

    with col2:
        st.metric(
            "📈 Engagement",
            f"{score['engagement']}/10"
        )

    with col3:
        st.metric(
            "📚 Readability",
            f"{score['readability']}/10"
        )
        
    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "💼 Platform Fit",
            f"{score['platform_fit']}/10"
        )

    with col5:
        st.metric(
            "🎯 Goal Alignment",
            f"{score['goal_alignment']}/10"
        )

    # ==========================
    # Writer Agent (FIRST)
    # ==========================
    with st.expander("✍️ Writer Agent Output", expanded=True):

        st.write("### Generated Content")
        tab1, tab2, tab3 = st.tabs(
            [
                "📖 Storytelling",
                "📚 Educational",
                "💬 Engagement",
            ]
        )

        with tab1:
            st.write(
                result.writer_output.variations[0]
            )

        with tab2:
            st.write(
                result.writer_output.variations[1]
            )

        with tab3:
            st.write(
                result.writer_output.variations[2]
            )

        st.write("### Call To Action")
        st.info(result.writer_output.call_to_action)

    # ==========================
    # Trend Agent (LAST)
    # ==========================
    with st.expander("🔥 Trend Agent Output"):

        st.write("### Hashtags")

        for tag in result.trend_output.hashtags:
            st.markdown(f"✅ {tag}")

        st.write("### Trends")

        for trend in result.trend_output.trends:
            st.markdown(f"📈 {trend}")

        st.write("### Audience Keywords")

        for keyword in result.trend_output.audience_keywords:
            st.markdown(f"🎯 {keyword}")


    # ==========================
    # Safety Agent
    # ==========================
    with st.expander("🛡️ Safety Agent Output", expanded=True):

        recommendation = (
            result.safety_output.approval_recommendation.value
        )

        if recommendation == "approve":
            st.success("✅ Content Approved")

        elif recommendation == "review":
            st.warning("⚠️ Content Needs Review")

        else:
            st.error("❌ Content Rejected")

        issues = result.safety_output.safety_report.issues

        if issues:
            st.write("### Detected Issues")

            for issue in issues:
                st.warning(
                    f"{issue.issue_type}: {issue.description}"
                )
        else:
            st.success("No safety issues detected.")

    # ==========================
    # Scheduler Agent
    # ==========================
    with st.expander("📅 Scheduler Agent Output", expanded=True):

        if result.schedule_output:

            schedule = result.schedule_output

            st.success("Post Scheduled Successfully")

            st.metric(
                "Scheduled Time",
                schedule["scheduled_time"]
            )

            st.info(
                f"📌 Event Title: {schedule['event_title']}"
            )

            st.success(
                schedule["message"]
            )

        else:
            st.warning("Post was not scheduled")

   