"""Web scraping utilities for content analysis"""

import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re


class WebScraper:
    """Scraper for analyzing web content"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch webpage content
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_text(self, html: str) -> str:
        """
        Extract clean text from HTML
        
        Args:
            html: HTML content
            
        Returns:
            Cleaned text
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """
        Extract top keywords from text
        
        Args:
            text: Text content
            top_n: Number of top keywords to return
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction (in production, use NLP libraries)
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Filter common words
        stop_words = {
            'this', 'that', 'with', 'from', 'have', 'been', 'will',
            'their', 'about', 'would', 'there', 'which', 'when', 'where',
            'what', 'who', 'how', 'more', 'some', 'other', 'into', 'than'
        }
        
        words = [w for w in words if w not in stop_words]
        
        # Count frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_n]]
    
    async def analyze_domain(self, domain: str) -> Dict:
        """
        Analyze a domain's content
        
        Args:
            domain: Domain to analyze
            
        Returns:
            Analysis results
        """
        url = f"https://{domain}" if not domain.startswith("http") else domain
        
        html = await self.fetch_page(url)
        if not html:
            return {"domain": domain, "error": "Failed to fetch"}
        
        text = self.extract_text(html)
        keywords = self.extract_keywords(text)
        
        return {
            "domain": domain,
            "content_length": len(text),
            "top_keywords": keywords,
            "has_ai_content": any(
                kw in text.lower()
                for kw in ['artificial intelligence', 'ai', 'machine learning', 'automation']
            )
        }



