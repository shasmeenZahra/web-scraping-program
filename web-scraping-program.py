import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape the website
def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.text.strip() if soup.title else "No Title"
        headings = [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
        links = [a['href'] for a in soup.find_all('a', href=True)]

        return {"title": title, "headings": headings, "links": links}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching the page: {e}"}

# Streamlit UI
st.set_page_config(page_title="🔍 Web Scraper", layout="wide")
st.title("🌐 Web Scraper")

# Input URL from user
url = st.text_input("🔗 Enter Website URL", placeholder="https://example.com")

# Scrape Button
if st.button("Scrape Website"):
    if url:
        result = scrape_website(url)

        if "error" in result:
            st.error(result["error"])
        else:
            st.subheader("📌 Page Title")
            st.write(result["title"])

            st.subheader("📑 Headings Found")
            if result["headings"]:
                for heading in result["headings"]:
                    st.markdown(f"- {heading}")
            else:
                st.warning("No headings found.")

            st.subheader("🔗 Links Found")
            if result["links"]:
                for link in result["links"][:10]:  # Limit to 10 links
                    st.markdown(f"- [🔗 {link}]({link})")
            else:
                st.warning("No links found.")
    else:
        st.warning("Please enter a valid URL.")
