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

  const handleVideoClick = (video, article) => {
    navigate(`/article/${video.vid}`, { state: { video, article } }); // Pass both video and article
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      {articles
        .filter((article) => article.videos && article.videos.length > 0) // Exclude articles without videos
        .map((article) => (
          <div
            key={article._id}
            className="border rounded-lg p-4 shadow-md bg-white max-w-lg w-full"
          >
            <div className="mt-4">
              {article.videos.map((video) => (
                <div key={video.vid} className="mb-6">
                  <h3 className="text-lg font-semibold">{video.title}</h3>
                  <p className="text-gray-500">{new Date(video.published_at).toLocaleDateString()}</p>
                  <p className="text-gray-600">{video.logline}</p>
                  <div className="mt-2">
                    <button
                      onClick={() => handleVideoClick(video, article)} // Pass video and article
                      className="flex items-center justify-center w-full mt-2 py-2 px-4 border border-gray-300 rounded-md bg-green-700 text-white hover:bg-white hover:text-black transition duration-200"
                    >
                      View Details
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
    </div>
  );
}





