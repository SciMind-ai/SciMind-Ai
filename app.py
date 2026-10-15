import streamlit as st
import arxiv
from langchain_community.document_loaders import PyPDFLoader
import os

# صفحے کی سیٹنگ
st.set_page_config(page_title="SciMind AI", page_icon="🔬", layout="centered")

st.title("🔬 SciMind AI: Research Paper to Code")
st.write("کسی بھی arXiv ریسرچ پیپر کا لنک درج کریں، اور اس کا تجزیہ کرنے کے لیے تیار ہو جائیں!")

# ان پٹ خانہ (URL کے لیے)
arxiv_url = st.text_input("arXiv پیپر کا لنک درج کریں (مثلاً: https://arxiv.org/abs/1706.03762)")

if st.button("پیپر پروسیس کریں"):
    if arxiv_url:
        try:
            with st.spinner("پیپر ڈاؤن لوڈ اور پراسیس ہو رہا ہے... براہ کرم انتظار کریں..."):
                # 1. پیپر کی شناخت (ID) الگ کرنا
                paper_id = arxiv_url.split("/")[-1].split("v")[0]
                
                # 2. Arxiv سے پیپر تلاش کرنا
                search = arxiv.Search(id_list=[paper_id])
                paper = next(search.results())
                
                # 3. PDF ڈاؤن لوڈ کرنا
                pdf_path = paper.download_pdf(filename="downloaded_paper.pdf")
                
                st.success(f"کامياب! پیپر ڈاؤن لوڈ ہو گیا ہے: {paper.title}")
                
                # 4. PDF سے ڈیٹا لوڈ کرنا
                loader = PyPDFLoader(pdf_path)
                pages = loader.load_and_split()
                
                st.info(f"کل صفحات کی تعداد: {len(pages)}")
                
                # عارضی طور پر پہلے صفحے کا کچھ متن دکھانا
                st.subheader("پیپر کا خلاصہ / پہلا حصہ:")
                st.write(pages[0].page_content[:1000] + "...")
                
        except Exception as e:
            st.error(f"کوئی خرابی پیش آگئی ہے: {e}")
    else:
            st.warning("براہ کرم پہلے کوئی درست arXiv لنک درج کریں!")
      
