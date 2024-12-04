import { useLocation, useNavigate } from 'react-router-dom';
import { Leaf } from "lucide-react";
import { Link } from "react-router-dom";

export default function VideoDetails() {
  const { state } = useLocation();
  const navigate = useNavigate();

  // Ensure video and article data are available
  if (!state || !state.video || !state.article) {
    return <p>Data not found. Please go back and try again.</p>;
  }

  const { video, article } = state;

  return (
    <div className="flex flex-col min-h-screen bg-green-50">
      {/* Header */}
      <header className="bg-green-600 text-white">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/home" className="text-2xl font-bold flex items-center">
            <Leaf className="mr-2" />
            EcoAlerts
          </Link>
          <Link to="/" className="bg-white text-green-600 hover:bg-green-100 px-4 py-2 rounded">
            Log Out
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center px-4 py-8">
        <div className="bg-white border rounded-lg shadow-md p-6 max-w-2xl w-full">
          <button onClick={() => navigate(-1)} className="mb-4 text-blue-500">
            &larr; Back
          </button>
          <h1 className="text-2xl font-bold mb-4 text-center">{video.title}</h1>
            <p className="text-gray-500 mb-2 text-center">Date: {new Date(video.published_at).toLocaleDateString()}</p>
            <p className="text-gray-600 mb-4">{video.logline}</p>

            {/* Sypnosis Section */}
            <p className="text-lg font-semibold text-green-800 mt-6 mb-2 text-center">Sypnosis</p>
            <p className="text-green-700 mb-4">{video.summary}</p>

            {/* Key Ideas Section */}
            <p className="text-lg font-semibold text-black mt-6 mb-2 text-center">Key Ideas</p>
            <ul className="list-disc list-inside">
            {video.key_points.map((point, index) => (
                <li key={index}>{point}</li>
            ))}
            </ul>
          
          {/* Tags Section */}
          <div className="mt-6">
            <h3 className="text-lg font-bold mb-2">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {video.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-gray-200 rounded-full text-sm font-semibold text-green-600"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Sources Section */}
          <div className="mt-6">
            <h3 className="text-lg font-bold mb-2">Sources</h3>
            <p className="text-gray-700">
              <strong>Channel:</strong> {article.channel}
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-green-800 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 EcoAlerts. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}










