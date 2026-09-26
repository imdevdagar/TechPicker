import streamlit as st
import json
import os
from dotenv import load_dotenv

load_dotenv()

import html
import time
import datetime
import re
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import trafilatura
from groq import Groq
from googleapiclient.discovery import build

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TechPickr — Smart Device Finder",
    page_icon="⚡",
    layout="centered",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* App Background: Dark animated gradient mesh */
    .stApp {
        background: radial-gradient(circle at 15% 50%, #1a0b2e, transparent 50%),
                    radial-gradient(circle at 85% 30%, #0d1b2a, transparent 50%),
                    #0b0f19 !important;
        color: #e2e8f0;
    }

    /* Hide Defaults */
    #MainMenu, footer, header { visibility: hidden; }

    /* Hero Section */
    .hero {
        text-align: center;
        padding: 3rem 0 2rem;
        animation: fadeInDown 0.8s ease-out;
    }
    .hero h1 {
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #a855f7, #ec4899, #f43f5e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.25rem;
        font-weight: 300;
    }

    /* Glassmorphic Inputs */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #fff !important;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>div:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }

    /* Modern Primary Button */
    .stButton>button {
        background: linear-gradient(135deg, #a855f7, #ec4899) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.5) !important;
    }

    /* Multiselect Tags */
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(168, 85, 247, 0.15) !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        color: #e9d5ff !important;
        border-radius: 8px !important;
    }

    /* Premium Product Cards */
    .rec-card {
        background: rgba(20, 25, 40, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .rec-card:hover {
        transform: translateY(-5px);
        background: rgba(25, 30, 45, 0.8);
        border-color: rgba(168, 85, 247, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(168, 85, 247, 0.15);
    }

    .rec-card h3 {
        color: #f8fafc;
        margin: 0 0 0.5rem;
        font-size: 1.6rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .rank-badge {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        color: white;
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-size: 1.1rem;
        font-weight: 800;
        box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);
        flex-shrink: 0;
    }

    .rec-card .price {
        display: inline-block;
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1.25rem;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    /* Pills for Pros and Cons */
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1.25rem;
    }
    .pill {
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }
    .pill.pro {
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .pill.con {
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }

    .section-title {
        font-weight: 600;
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid #2a2a3e;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


if "cache_hits" not in st.session_state:
    st.session_state.cache_hits = 0

# ─── Functions ──────────────────────────────────────────────────────────────────

def scrape_smartprix(category: str, budget: int, requirements: str) -> list:
    import requests
    from bs4 import BeautifulSoup
    
    min_budget = int(budget * 0.80)
    max_budget = int(budget * 1.1)
    
    if category.lower() == "mobile phone":
        url = f"https://www.smartprix.com/mobiles/price-{min_budget}_to_{max_budget}/exclude_global-exclude_out_of_stock-exclude_upcoming-stock"
    else:
        url = f"https://www.smartprix.com/laptops/price-{min_budget}_to_{max_budget}/exclude_global-exclude_out_of_stock-exclude_upcoming-stock"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.smartprix.com/",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=4)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        full_products = []
        items = soup.select(".sm-product")
        
        for card in items[:15]:
            try:
                name_el = card.select_one("h2, h3, .name, .sm-title, [class*='name'], [class*='title']")
                price_el = card.select_one(".price, [class*='price']")
                
                name = name_el.get_text(strip=True) if name_el else "N/A"
                price_text = price_el.get_text(strip=True) if price_el else "N/A"
                
                if name == "N/A":
                    continue
            except Exception:
                continue
                
            if price_text != "N/A":
                import re
                nums = re.findall(r'\d+', price_text)
                if nums:
                    price_val = int("".join(nums))
                    if price_val < (budget * 0.75):
                        continue
                        
            specs_dict = {}
            specs_els = card.select("ul li, .sm-feat li, [class*='spec'] li")
            for spec in specs_els:
                txt = spec.get_text(strip=True)
                if txt:
                    specs_dict[txt] = "Yes"
                    
            full_products.append({
                "name": name,
                "price": price_text,
                "url": url,
                "specs": specs_dict
            })
            
        return full_products
        
    except Exception as e:
        print(f"Scrape error (falling back to AI knowledge): {e}")
        return []


def get_reviews(category: str, budget: int, requirements: str) -> tuple[str, list[str]]:
    import datetime
    current_year = datetime.datetime.now().year
    query = f"best {category} under {budget} India {current_year} {requirements} review specs"
    
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, region="in-en", timelimit="y", max_results=3))
    except Exception:
        return "", []

    snippets = []
    fetched_urls = []
    urls_to_fetch = [r.get('href') for r in results if r.get('href')][:3]
    
    def fetch_single_url(u):
        try:
            downloaded = trafilatura.fetch_url(u, no_ssl=True)
            if downloaded:
                text = trafilatura.extract(downloaded)
                if text and len(text) > 300:
                    return u, f"Source: {u}\n{text[:1500]}"
        except Exception:
            pass
        return u, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(fetch_single_url, url): url for url in urls_to_fetch}
        for future in concurrent.futures.as_completed(future_to_url, timeout=3):
            try:
                url_res, content = future.result(timeout=1)
                if content:
                    snippets.append(content)
                    fetched_urls.append(url_res)
            except Exception:
                continue

    return "\n\n".join(snippets), fetched_urls


def fetch_youtube_reviews(product_name: str) -> str:
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        return ""
    try:
        import datetime
        current_year = datetime.datetime.now().year
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            q=f"{product_name} review India {current_year}",
            type="video",
            maxResults=5,
            relevanceLanguage="en",
            regionCode="IN"
        )
        response = request.execute()
        
        snippets = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            desc = item["snippet"]["description"]
            snippets.append(f"Title: {title}\nChannel: {channel}\nDescription: {desc}")
            
        return "\n\n".join(snippets)
    except Exception:
        return ""


def get_recommendations(category: str, budget: int, requirements: str, shopping_results: list, review_text: str, youtube_data: dict) -> tuple[list, str]:
    """Send search data to Groq LLM and get structured recommendations."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return [], "GROQ_API_KEY environment variable is not set. Please add it to your Streamlit Cloud Secrets or .env file."

    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        return [], f"Failed to initialize Groq client: {e}"
    
    current_year = datetime.datetime.now().year
    last_year = current_year - 1

    prompt = f"""You are TechPickr, an expert Indian tech reviewer.

A user wants a **{category}** with a max budget of **₹{budget}**.
Their requirements: "{requirements}"

Here are ALL products currently available on Smartprix within ±₹1000 of the user's budget of ₹{budget}:
{json.dumps(shopping_results, indent=2)}

Each product includes full specs (RAM, processor, battery, camera etc).
Pick the TOP 3 best matches for the user's requirements from this list.
Use exact specs from the data — do not assume or hallucinate specs.

Here are expert reviews and specs from Indian tech websites:
{review_text}

Here are YouTube reviews for the top candidates:
{json.dumps(youtube_data, indent=2)}

RULES:
1. If shopping listings are provided, pick the TOP 3 products from them. If shopping listings are empty, rely on the expert reviews and your own knowledge of the Indian market to pick the TOP 3 best products under the budget. Estimate the current price if needed.
2. Every device MUST be real and currently sold in India at or below ₹{budget}.
3. BUDGET MAXIMIZATION: Strongly prefer recommending devices that are priced close to ₹{budget} (e.g., within ₹4000 of the max budget). The user wants the absolute best performance their money can buy, not the cheapest option. DO NOT recommend 18k phones if the budget is 25k.
4. CRITICAL: Recommend modern, highly capable devices. Do NOT recommend outdated models that are no longer relevant. DO NOT recommend used, refurbished, renewed, or second-hand devices.
5. If a product's exact price is not mentioned, write 'Check on Amazon/Flipkart' as the price.
6. Pros and cons must be based on actual specs found in the search data or your internal knowledge.
7. Always attempt to recommend exactly 3 products. Do not return an empty list.
8. Prioritize products from 91mobiles, smartprix, GSMArena, NDTV Gadgets as these are reliable Indian tech sources.
9. CRITICAL: Do NOT use HTML entities (like &#8377;). Use the actual Rupee symbol (₹) or "Rs.". Ensure the output has absolutely NO weird random codes.
10. For each device, provide: name, release year, estimated price, 3 pros, 2 cons, and a one-line verdict.
11. For each recommended product, calculate a confidence_score (0-100) based on:
- 40 points: Product specs directly match user requirements
- 30 points: Product maximizes the budget (is priced within ₹3000 of max budget)
- 30 points: Product has YouTube review videos
Deduct 15 points if the price is far below the budget (e.g. an 18k phone for a 25k budget).
Deduct 10 points if price is above original budget.
Deduct 15 points if the device is visibly outdated or multiple generations behind.
Return confidence_score as an integer in the JSON.
12. Create a standard Google search link for the exact device name. Format: "https://www.google.com/search?q=Device+Name"

Return ONLY a valid JSON object with a 'recommendations' key containing the array:
{{
  "recommendations": [
    {{
      "rank": 1,
      "name": "Full Device Name",
      "release_year": {current_year},
      "price": "₹xxxxx",
      "confidence_score": 85,
      "pros": ["pro 1", "pro 2", "pro 3"],
      "cons": ["con 1", "con 2"],
      "verdict": "One-line summary of why this is a great pick.",
      "google_search_link": "https://www.google.com/search?q=..."
    }}
  ]
}}
"""

    dynamic_models = []
    try:
        m_list = client.models.list()
        dynamic_models = [m.id for m in m_list.data if not any(k in m.id for k in ['whisper', 'guard', 'orpheus', 'embed'])]
    except Exception:
        pass

    fallback_models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "allam-2-7b"]
    models_to_try = []
    for m in dynamic_models + fallback_models:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    
    for model_name in models_to_try:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.15,
                response_format={"type": "json_object"},
            )
    
            text = response.choices[0].message.content.strip()
            text = html.unescape(text)
            
            if text.startswith("```"):
                import re
                match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
                if match:
                    text = match.group(1).strip()
                    
            data = json.loads(text)
            
            raw_recs = []
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        raw_recs = v
                        break
            elif isinstance(data, list):
                raw_recs = data
                
            valid_recs = []
            for r in raw_recs:
                if isinstance(r, dict) and r.get("name") and r.get("price") and isinstance(r.get("pros"), list):
                    valid_recs.append(r)
            
            if valid_recs:
                return valid_recs[:3], None
                
        except Exception as e:
            last_error = e
            continue

    return [], str(last_error) if last_error else "All AI models returned invalid response structure."


def render_card(rec: dict):
    """Render a single recommendation card."""
    pros_html = "".join(f"<span class='pill pro'>✅ {p}</span>" for p in rec.get("pros", []))
    cons_html = "".join(f"<span class='pill con'>⚠️ {c}</span>" for c in rec.get("cons", []))
    
    try:
        score = int(rec.get("confidence_score", 0))
    except (ValueError, TypeError):
        score = 0
        
    if score >= 80:
        conf_color = "#34d399"
        conf_label = "High Confidence"
    elif score >= 50:
        conf_color = "#fbbf24"
        conf_label = "Moderate Confidence"
    else:
        conf_color = "#f87171"
        conf_label = "Low Confidence"
        
    conf_html = (
        f"<div style='margin-bottom: 1.5rem;'>"
        f"<div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#94a3b8; margin-bottom:6px;'>"
        f"<span>AI Match Score</span><span style='color:{conf_color}; font-weight:700;'>{conf_label} ({score}%)</span>"
        f"</div>"
        f"<div style='background:rgba(255,255,255,0.05); border-radius:999px; height:8px; overflow:hidden;'>"
        f"<div style='width:{score}%; background:{conf_color}; height:100%; border-radius:999px; box-shadow: 0 0 10px {conf_color}55;'></div>"
        f"</div>"
        f"</div>"
    )

    html_content = f"""<div class="rec-card">
<h3><span class="rank-badge">{rec.get("rank", "?")}</span> {rec.get("name", "Unknown")} <span style="font-size: 1.1rem; color: #64748b; font-weight: 500; margin-left: auto;">{rec.get("release_year", "New")}</span></h3>
<span class="price">{rec.get("price", "N/A")}</span>
{conf_html}
<div class="section-title">Highlights</div>
<div class="pill-container">{pros_html}</div>
<div class="section-title">Drawbacks</div>
<div class="pill-container">{cons_html}</div>
<div class="verdict">💡 {rec.get("verdict", "")}</div>
<div style="margin-top: 1.5rem; display: flex; gap: 0.75rem;">
{f"<a href='{rec.get('google_search_link')}' target='_blank' style='display: inline-block; color: #fff; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); text-decoration: none; font-weight: 600; padding: 0.6rem 1.25rem; border-radius: 8px; font-size: 0.9rem; transition: all 0.2s;' onmouseover='this.style.background=\"rgba(255,255,255,0.2)\"' onmouseout='this.style.background=\"rgba(255,255,255,0.1)\"'>🔍 Compare Prices on Google</a>" if rec.get("google_search_link") else ""}
</div>
</div>"""
    st.markdown(html_content, unsafe_allow_html=True)


# ─── UI ─────────────────────────────────────────────────────────────────────────

st.markdown('<div class="hero"><h1>⚡ TechPickr</h1><p>Find the best tech for your budget — powered by AI + live search</p></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox("📱 Product Category", ["Mobile Phone", "Laptop"], index=0)

with col2:
    budget = st.number_input("💰 Max Budget (₹)", min_value=5000, max_value=500000, value=20000, step=1000)

priority = st.radio(
    "🎯 Main Priority Focus",
    options=[
        "⚡ Best Overall / Balanced",
        "📸 Camera & Photography Focus", 
        "🚀 Raw Performance & Speed", 
        "🎮 Heavy Gaming & Graphics", 
        "🔋 Long Battery Life & Fast Charging", 
        "✨ Display Quality & Entertainment", 
        "🧹 Clean Software & Long Updates", 
        "💎 Premium Build & Sleek Design"
    ],
    index=0,
    help="Select your single #1 priority to help the AI find the perfect match."
)

requirements = priority

search_btn = st.button("🔍 Find Best Options", type="primary", use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─── Search Flow ────────────────────────────────────────────────────────────────

if search_btn:
    try:
        cache_key = re.sub(r'\W+', '_', f"{category}_{budget}_{requirements}".lower().strip())
        
        with st.status("🛒 Scraping all products within your budget range from Smartprix...", expanded=True) as status:
            if cache_key in st.session_state and time.time() - st.session_state[cache_key][1] < 86400:
                shopping_results = st.session_state[cache_key][0]
                st.session_state.cache_hits += 1
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_reviews = executor.submit(get_reviews, category, budget, requirements)
                    status.update(label="📰 Reading expert reviews from Indian tech sites...")
                    review_text, fetched_urls = future_reviews.result()
            else:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_shopping = executor.submit(scrape_smartprix, category, budget, requirements)
                    future_reviews = executor.submit(get_reviews, category, budget, requirements)
                    
                    try:
                        shopping_results = future_shopping.result(timeout=4)
                        if shopping_results:
                            st.session_state[cache_key] = (shopping_results, time.time())
                    except Exception as e:
                        shopping_results = []
                    
                    try:
                        review_text, fetched_urls = future_reviews.result(timeout=4)
                    except Exception:
                        review_text, fetched_urls = "", []
            
            status.update(label="🎥 Fetching YouTube reviews for top products...")
            youtube_data = {}
            if shopping_results:
                top_3_titles = [r.get("name", "") for r in shopping_results[:3]]
                with concurrent.futures.ThreadPoolExecutor() as yt_executor:
                    yt_futures = {yt_executor.submit(fetch_youtube_reviews, title): title for title in top_3_titles if title}
                    try:
                        for future in concurrent.futures.as_completed(yt_futures, timeout=3):
                            title = yt_futures[future]
                            youtube_data[title] = future.result(timeout=1)
                    except Exception:
                        pass
                        
            status.update(label="🤖 Analyzing everything with AI...")
            recommendations, error_msg = get_recommendations(category, budget, requirements, shopping_results, review_text, youtube_data)
            
            status.update(label="✅ Done!", state="complete", expanded=False)

        if not recommendations:
            if error_msg:
                st.error(f"❌ Could not generate recommendations: {error_msg}")
            else:
                st.error("Couldn't generate recommendations. Please try again.")
        else:
            st.markdown(f"### 🏆 Top {len(recommendations)} picks under ₹{budget:,}")
            st.caption(f"🔑 API calls saved by cache: {st.session_state.cache_hits}")
            
            for rec in recommendations:
                render_card(rec)

            st.caption("💡 Prices are actual Smartprix prices. Always verify on Amazon/Flipkart before purchasing.")
            
            if fetched_urls:
                with st.expander("📚 Expert sources consulted"):
                    for url in fetched_urls:
                        st.markdown(f"- [{url}]({url})")
    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
        st.exception(e)
