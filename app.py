import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import re


load_dotenv()
st.set_page_config(page_title="AI Tweet Generator", page_icon="🐦", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f051d,#1b0d2b,#2b0f4a);
color:white;
font-family: 'Inter', sans-serif;
}

.logo{
font-size:26px;
font-weight:700;
color:#d946ef;
}

.hero-title{
font-size:70px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#ff4ecd,#7aa2ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.hero-sub{           
font-size:20px;
text-align:center;
color:#cbd5f5;
margin-bottom:40px;
}

.enter-btn button{
background: linear-gradient(90deg,#9333ea,#d946ef);
color:white;
border:none;
padding:16px 55px;
border-radius:14px;
font-size:20px;
font-weight:600;
}

.feature-card{
background:#111827;
padding:30px;
border-radius:16px;
text-align:center;
border:1px solid rgba(255,255,255,0.1);
}

.input-card{
background:linear-gradient(145deg,#2a0e3a,#3b0f4f);
padding:30px;
border-radius:16px;
margin-top:20px;
border:1px solid rgba(255,255,255,0.08);
box-shadow:0 8px 30px rgba(0,0,0,0.35);
}

.brand-card{
background:#2a0e3a;
padding:20px;
border-radius:14px;
margin-top:25px;
border:1px solid rgba(255,255,255,0.08);
}

.tweet-card{
background:#2a0e3a;
padding:20px;
border-radius:14px;
margin-bottom:18px;
border:1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "tweets" not in st.session_state:
    st.session_state.tweets = []

if "summary" not in st.session_state:
    st.session_state.summary = []

# ---------- HOME PAGE ----------
if st.session_state.page == "home":

    st.markdown('<div class="hero-title">⚡AI Tweet Generator</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-sub">Craft on-brand tweets using AI powered brand voice analysis</div>',
        unsafe_allow_html=True
    )

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("✨ Enter Now"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.write("")
    st.write("")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
        ⚡ <h3>Instant</h3>
        <p>Generate tweets instantly using AI.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
        📈 <h3>Engaging</h3>
        <p>Optimized tweets for maximum reach.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
        🧠 <h3>Smart</h3>
        <p>AI understands brand tone and audience.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- DASHBOARD ----------
elif st.session_state.page == "dashboard":

    st.markdown('<div class="logo">⚡AI Tweet Generator</div>', unsafe_allow_html=True)

    st.markdown("## Dashboard")
    st.write("Generate on-brand tweets with AI.")

    # ---------- BRAND INFORMATION CARD ----------

    with st.form("tweet_form"):
        

        st.markdown("### Brand Information")

        brand = st.text_input("Brand Name")

        col1, col2 = st.columns(2)

        with col1:
            industry = st.radio(
                "Industry",
                ["Technology","Food","Fashion","Marketing","Startup","Finance","Education"],
                horizontal=True
            )

        with col2:
            objective = st.radio(
                "Campaign Objective",
                ["Engagement","Promotion","Brand Awareness","Product Launch","Community Building"],
                horizontal=True
            )

        product = st.text_area(
            "Describe the brand products",
            placeholder="Example: Sustainable sneakers made from recycled materials",
            height=120
        )

        generate = st.form_submit_button("✨ Generate Tweets")

    st.markdown('</div>', unsafe_allow_html=True)

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if generate:

        prompt = f"""
You are an expert social media strategist.

Brand Name: {brand}
Industry: {industry}
Campaign Objective: {objective}
Product Details: {product}

Write EXACTLY 4 bullet points starting with "-" describing the brand voice including:
- tone
- target audience
- communication style
- typical content themes

Then generate 10 tweets.

Rules:
- Tweets should follow current social media trends
- Tweets must all be different
- Max 280 characters
- Include emojis and hashtags
- Mix engaging, promotional, witty and informative tweets
- Return tweets in numbered list format
"""

        with st.spinner("Generating tweets..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"user","content":prompt}]
            )

            output = response.choices[0].message.content
            lines = output.split("\n")

            brand_voice = []
            tweets_start = None

            for i, line in enumerate(lines):

                line = line.strip()

                if line.startswith("-"):
                    brand_voice.append(line.replace("-", "").replace("*","").strip())

                if re.match(r'1\.', line):
                    tweets_start = i
                    break

            tweet_lines = "\n".join(lines[tweets_start:])
            tweets = re.split(r'\d+\.\s', tweet_lines)

            clean_tweets = []

            for t in tweets:
                t = t.strip()
                if t:
                    clean_tweets.append(t)

            st.session_state.summary = brand_voice[:4]
            st.session_state.tweets = clean_tweets[:10]

    # ---------- BRAND VOICE ----------
    if st.session_state.summary:

        brand_html = '<div class="brand-card">'
        brand_html += "<h3>Brand Voice</h3>"

        for point in st.session_state.summary:
            brand_html += f"<p>• {point}</p>"

        brand_html += "</div>"

        st.markdown(brand_html, unsafe_allow_html=True)

    # ---------- TWEETS ----------
    if st.session_state.tweets:

        st.subheader("Generated Tweets 🐦")

        for tweet in st.session_state.tweets:

            st.markdown(
            f"""
            <div class="tweet-card">
            {tweet}
            </div>
            """,
            unsafe_allow_html=True
            )

        tweets_text = "\n\n".join(st.session_state.tweets)

        col1,col2 = st.columns([6,2])

        with col1:
            st.download_button(
                "⬇ Download Tweets",
                tweets_text,
                file_name="generated_tweets.txt"
            )

        with col2:
            if st.button("⬅ Back to Welcome"):
                st.session_state.page="home"
                st.session_state.tweets=[]
                st.session_state.summary=[]
                st.rerun()