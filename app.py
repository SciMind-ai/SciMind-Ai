import streamlit as st
import arxiv
import urllib.request
from langchain_community.document_loaders import PyPDFLoader
from google import genai

# صفحے کی سیٹنگ
st.set_page_config(page_title="SciMind AI", page_icon="🔬", layout="centered")

st.title("🔬 SciMind AI: Research Paper to Code")
st.write("arXiv ریسرچ پیپر کا لنک درج کریں، اور Gemini AI خود بخود اس کے ریاضیاتی ماڈلز اور کوڈ کا تجزیہ کرے گا!")

# یہاں آپ کی پکی API Key محفوظ ہے
GEMINI_API_KEY = "AQ.Ab8RN6IWRpCnnbthN7_jIdU4VGHciHWqaah2FNISnUI_G4_2ug"

# ان پٹ خانہ (صرف URL کے لیے)
arxiv_url = st.text_input("arXiv پیپر کا لنک درج کریں (مثلاً: https://arxiv.org/abs/1706.03762)", "https://arxiv.org/abs/2106.09685")

if st.button("پیپر پروسیس اور کوڈ جنریٹ کریں"):
    if not arxiv_url:
        st.warning("براہ کرم کوئی درست arXiv لنک درج کریں!")
    else:
        try:
            # Google GenAI کلائنٹ
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            with st.spinner("پیپر ڈاؤن لوڈ اور AI تجزیہ جاری ہے... براہ کرم انتظار کریں..."):
                # 1. پیپر کی شناخت (ID) الگ کرنا
                paper_id = arxiv_url.split("/")[-1].split("v")[0]
                
                # 2. Arxiv سے پیپر تلاش کرنا
                client_arxiv = arxiv.Client()
                search = arxiv.Search(id_list=[paper_id])
                paper = next(client_arxiv.results(search))
                
                st.success(f"کامیاب! پیپر مل گیا ہے: {paper.title}")
                
                # 3. PDF کا اصل لنک بنا کر ڈاؤن لوڈ کرنا
                pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
                pdf_path = "downloaded_paper.pdf"
                urllib.request.urlretrieve(pdf_url, pdf_path)
                
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
                    
