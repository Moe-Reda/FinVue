import React, { useState, useEffect } from 'react';
import axios from 'axios';
import api from '../../api/axiosConfig';
import './newsPage.css'

const NewsPage = () => {
    const [inputValue, setInputValue] = useState('');
    const [query, setQuery] = useState('finance'); 
    const [news, setNews] = useState([]); 
    const [error, setError] = useState(''); 
  
    useEffect(() => {
      console.log(query);
      if (query) {  
        fetchNews();
      }
    }, [query]);

    const fetchNews = async () => {
        try {
          console.log(news);
          const response = await api.get(`http://127.0.0.1:5000/api/get_news/${query}`);
          console.log(response.data.results);
          setNews(response.data.results);
          console.log(news);
          if (response.data.results.length === 0) {
            setError('No results found.');
          } else {
            setError('');
          }
        } catch (error) {
          setError('Failed to fetch news');
          console.error(error);
        }
      };
  
    const handleSubmit = (event) => {
        console.log(news);
        event.preventDefault();
        setQuery(inputValue + " finance"); 
        fetchNews();
      };
  
    return (
      <div>
        <header>
          <h1>Financial News</h1>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Search news..."
            />
            <button type="submit">Search</button>
          </form>
        </header>
        <main className="news-container">
            {error && <p className="error">{error}</p>}
            {news.map(article => (
            <div className="news-card" key={article.article_id}>
                <img src={article.image_url} alt={article.title} />
                <h3>{article.title}</h3>
                <p>{article.description?.length > 500 ? `${article.description.substring(0, 500)}...` : article.description}</p>
                <a href={article.link} target="_blank" rel="noopener noreferrer">Read more</a>
            </div>
            ))}
        </main>
      </div>
    );
  };
  
  export default NewsPage;