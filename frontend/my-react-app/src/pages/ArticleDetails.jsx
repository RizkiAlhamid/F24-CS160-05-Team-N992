import { useLocation, useNavigate } from 'react-router-dom';
import { Leaf, BookType, Lightbulb, Calendar, Tags, SquareUser, Sun, Moon } from 'lucide-react';
import { Link } from "react-router-dom";

export default function ArticleDetails() {
  const { state } = useLocation();
  const navigate = useNavigate();

  if (!state || !state.article) {
    return <p>Article not found. Please go back and try again.</p>;
  }

  const { article } = state;

  return (
    <div className="flex flex-col min-h-screen bg-green-50">
      {/* Header */}
      <header className="bg-green-600 text-white">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/home" className="text-2xl font-bold flex items-center">
            <Leaf className="mr-2" />
            Particle
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
          <div className="flex items-center justify-center mb-4">
            <Sun className="text-yellow-500 mr-3" />
            <h1 className="text-2xl font-bold text-center">{article.metadata.title}</h1>
            <Moon className="text-blue-500 ml-3" />
          </div>

          <div className="flex items-center justify-center text-gray-500 mb-2">
            <Calendar className="mr-2" />
            <p>Date: {new Date(article.metadata.last_modified_date || article.metadata.published_at).toLocaleDateString()}</p>
          </div>
          <p className="text-gray-600 mb-4">{article.logline}</p>

          {/* Summary Section */}
          <div className="flex items-center justify-center mt-6 mb-2">
            <BookType className="text-green-800 mr-2" />
            <p className="text-lg font-bold text-green-800">Summary</p>
          </div>
          <p className="text-green-700 mb-4">{article.summary}</p>

          {/* Key Points Section */}
          <div className="flex items-center justify-center mt-6 mb-2">
            <Lightbulb className="text-black mr-2" />
            <p className="text-lg font-bold text-black">Key Points</p>
          </div>
          <ul className="list-disc list-inside">
            {article.key_points.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
          
          {/* Tags Section */}
          <div className="mt-6">
            <div className="flex items-center justify-center mb-2">
              <Tags className="text-gray-700 mr-2 mb-3" />
              <h3 className="text-lg font-bold mb-3">Tags</h3>
            </div>
            <div className="flex flex-wrap gap-2 justify-center">
              {article.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-3 py-1 bg-gray-200 rounded-full text-sm font-semibold text-green-600"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Main Topic Section */}
          <div className="mt-6">
            <div className="flex items-center justify-center mb-2">
              <SquareUser className="text-gray-700 mr-2 mb-2" />
              <h3 className="text-lg font-bold mb-2">Main Topic</h3>
            </div>
            <p className="text-gray-700 text-center">
              {article.main_topic}
            </p>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="bg-green-800 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 Particle. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

