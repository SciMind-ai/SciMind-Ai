import streamlit as st
import arxiv
from langchain_community.document_loaders import PyPDFLoader
from openai import OpenAI
import os

# صفحے کی سیٹنگ
st.set_page_config(page_title="SciMind AI", page_icon="🔬", layout="centered")

st.title("🔬 SciMind AI: Research Paper to Code")
st.write("arXiv ریسرچ پیپر کا لنک درج کریں، اور اے آئی کی مدد سے اس کے ریاضیاتی ماڈلز اور کوڈ کا تجزیہ کریں!")

# OpenAI API Key ان پٹ (سائیڈ بار یا مین سکرین پر)
api_key = st.text_input("с اپنی OpenAI API Key درج کریں:", type="password")

# ان پٹ خانہ (URL کے لیے)
arxiv_url = st.text_input("arXiv پیپر کا لنک درج کریں (مثلاً: https://arxiv.org/abs/1706.03762)")

if st.button("پیپر پروسیس اور کوڈ جنریٹ کریں"):
    if not api_key:
        st.warning("براہ کرم پہلے اپنی OpenAI API Key درج کریں!")
    elif not arxiv_url:
        st.warning("براہ کرم کوئی درست arXiv لنک درج کریں!")
    else:
        try:
            client = OpenAI(api_key=api_key)
            
            with st.spinner("پیپر ڈاؤن لوڈ اور اے آئی تجزیہ جاری ہے... براہ کرم انتظار کریں..."):
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
                
                st.info("اے آئی ریسرچ پیپر سے ریاضیاتی ماڈلز اور پائتھون کوڈ تیار کر رہا ہے...")
                
                # 5. OpenAI کے ذریعے تجزیہ اور کوڈ جنریشن
                prompt = f"""
                You are an expert AI scientist and programmer. Analyze the following research paper text and:
                1. Extract the core mathematical models/equations.
                2. Generate a clean, working Python code implementation based on these models.
                
                Paper Text:
                {paper_text[:4000]}
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2
                )
                
                ai_output = response.choices[0].message.content
                
                st.subheader("📊 ریاضیاتی ماڈلز اور جنریٹ شدہ کوڈ:")
                st.markdown(ai_output)
                
        except Exception as e:
            st.error(f"کوئی خرابی پیش آگئی ہے: {e}")
            
