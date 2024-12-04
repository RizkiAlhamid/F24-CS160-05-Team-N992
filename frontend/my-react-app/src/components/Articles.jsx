import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('http://localhost:8080/articles');
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    };

    fetchArticles();
  }, []);

  const handleArticleClick = (article) => {
    navigate(`/article/${article._id}`, { state: { article } });
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      {articles.map((article) => (
        <div
          key={article._id}
          className="border rounded-lg p-4 shadow-md bg-white max-w-lg w-full"
        >
          <h2 className="text-xl font-semibold mb-2">{article.metadata.title}</h2>
          <p className="text-gray-500 mb-2">
            {new Date(article.metadata.last_modified_date || article.metadata.published_at).toLocaleDateString()}
          </p>
          <p className="text-gray-600 mb-4">{article.logline}</p>
          <div className="flex flex-wrap gap-2 mb-4">
            {article.tags.slice(0, 3).map((tag, index) => (
              <span key={index} className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                {tag}
              </span>
            ))}
          </div>
          <button
            onClick={() => handleArticleClick(article)}
            className="flex items-center justify-center w-full mt-2 py-2 px-4 border border-gray-300 rounded-md bg-green-700 text-white hover:bg-white hover:text-black transition duration-200"
          >
            View Details
          </button>
        </div>
      ))}
    </div>
  );
}





