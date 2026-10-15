import streamlit as st
import arxiv
from langchain_community.document_loaders import PyPDFLoader
from google import genai

# صفحے کی سیٹنگ
st.set_page_config(page_title="SciMind AI", page_icon="🔬", layout="centered")

st.title("🔬 SciMind AI: Research Paper to Code")
st.write("arXiv ریسرچ پیپر کا لنک درج کریں، اور Gemini AI خود بخود اس کے ریاضیاتی ماڈلز اور کوڈ کا تجزیہ کرے گا!")

# یہاں اپنی Gemini API Key مستقل طور پر درج کر دیں
GEMINI_API_KEY = "AQ.Ab8RN6Ku0vLqV4ticwSIqi9KyKIyLWCCjACG1PsY2Afk71AGCQ"

# ان پٹ خانہ (صرف URL کے لیے)
arxiv_url = st.text_input("arXiv پیپر کا لنک درج کریں (مثلاً: https://arxiv.org/abs/1706.03762)")

if st.button("پیپر پروسیس اور کوڈ جنریٹ کریں"):
    if not arxiv_url:
        st.warning("براہ کرم کوئی درست arXiv لنک درج کریں!")
    elif GEMINI_API_KEY == "YAHAN_APNI_ASLI_GEMINI_API_KEY_LIKHEIN":
        st.error("براہ کرم کوڈ میں اپنی درست Gemini API Key درج کریں!")
    else:
        try:
            # Google GenAI کلائنٹ (پکی کی کے ساتھ)
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            with st.spinner("پیپر ڈاؤن لوڈ اور AI تجزیہ جاری ہے... براہ کرم انتظار کریں..."):
                # 1. پیپر کی شناخت (ID) الگ کرنا
                paper_id = arxiv_url.split("/")[-1].split("v")[0]
                
                # 2. Arxiv سے پیپر تلاش کرنا
                search = arxiv.Search(id_list=[paper_id])
                paper = next(search.results())
                
                # 3. PDF ڈاؤن لوڈ کرنا
                pdf_path = paper.download_pdf(filename="downloaded_paper.pdf")
                
                st.success(f"کامیاب! پیپر ڈاؤن لوڈ ہو گیا ہے: {paper.title}")
                
                # 4. PDF سے ڈیٹا لوڈ کرنا
                loader = PyPDFLoader(pdf_path)
                pages = loader.load_and_split()
                
                # ابتدائی صفحات کا متن جمع کرنا
                paper_text = ""
                for page in pages[:3]:  # پہلے 3 صفحات کا متن
                    paper_text += page.page_content + "\n"
                
                st.info("Gemini AI ریسرچ پیپر سے ریاضیاتی ماڈلز اور پائتھون کوڈ تیار کر رہا ہے...")
                
                # 5. Gemini AI کے ذریعے تجزیہ
                prompt = f"""
                You are an expert AI scientist and programmer. Analyze the following research paper text and:
                1. Extract the core mathematical models/equations.
                2. Generate a clean, working Python code implementation based on these models.
                
                Paper Text:
                {paper_text[:4000]}
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                st.subheader("📊 ریاضیاتی ماڈلز اور جنریٹ شدہ کوڈ:")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"کوئی خرابی پیش آگئی ہے: {e}")
            
