import { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const [expandedVideoId, setExpandedVideoId] = useState(null);

  // Fetch articles from the backend
  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const response = await fetch('http://0.0.0.0:8080/articles');
        const data = await response.json();
        setArticles(data); // Assuming data is the full response array
      } catch (error) {
        console.error('Error fetching articles:', error);
      }
    };

    fetchArticles();
  }, []);

  const toggleVideo = (vid) => {
    setExpandedVideoId(expandedVideoId === vid ? null : vid);
  };

  return (
    <div className="space-y-6">
      {articles.map((article) => (
        <div key={article._id} className="border rounded-lg p-4 shadow-md bg-white">
          {/* <h2 className="text-xl font-bold">{article.channel}</h2> */}
          {/* <p className="text-gray-600">Subscribers: {article.subscriber_count}</p> */}
          {/* <p className="text-gray-600">Total Views: {article.view_count}</p> */}
          {/* <p className="text-sm text-gray-500">{article.description}</p> */}
          <div className="mt-4">
            {article.videos.map((video) => (
              <div key={video.vid} className="mb-6">
                <h3 className="text-lg font-semibold">{video.title}</h3>
                <p className="text-gray-500">{new Date(video.published_at).toLocaleDateString()}</p>
                <p className="text-gray-600">{video.logline}</p>
                <div className="mt-2">
                  {expandedVideoId === video.vid && (
                    <div>
                      <p className="text-green-700 mb-4">{video.summary}</p>
                      <ul className="list-disc list-inside mb-2">
                        {video.key_points.map((point, index) => (
                          <li key={index}>{point}</li>
                        ))}
                      </ul>
                      {/*<p className="text-gray-500">Sentiment: {video.sentiment.overall}</p>
                      <p className="text-gray-700 mt-4">{video.transcript}</p> {/* Added transcript */}
                    </div>
                  )}
                  <button
                    onClick={() => toggleVideo(video.vid)}
                    className="flex items-center justify-center w-full mt-2 py-2 px-4 border border-gray-300 rounded-md bg-white text-gray-700 hover:bg-gray-100 transition duration-200"
                  >
                    {expandedVideoId === video.vid ? (
                      <>
                        <ChevronUp className="mr-2 h-4 w-4" /> Show Less
                      </>
                    ) : (
                      <>
                        <ChevronDown className="mr-2 h-4 w-4" /> Read More
                      </>
                    )}
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