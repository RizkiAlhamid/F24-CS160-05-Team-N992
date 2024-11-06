import { Leaf } from "lucide-react";
import { Link } from "react-router-dom"; // Make sure you have this import for routing
import Articles from "../components/Articles";

export default function HomePage() {
    return (
      <div className="flex flex-col min-h-screen bg-green-50">
      <header className="bg-green-600 text-white">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/home" className="text-2xl font-bold flex items-center">
            <Leaf className="mr-2" />
            EcoAlerts
          </Link>
          <nav className="hidden md:flex space-x-4">
            <a className="hover:text-green-200">Settings</a>

          </nav>
          <Link to="/" className="bg-white text-green-600 hover:bg-green-100 px-4 py-2 rounded">Log Out</Link>

        </div>
      </header>
  
        <main className="container mx-auto px-4 py-8 flex-grow">
          <h1 className="text-3xl font-bold text-green-800 mb-6">Today's Environmental Insights</h1>
          <p className="text-green-700 mb-8">
            Here are today's summarized articles on environmental topics. Click on an article to see more details.
          </p>
          <Articles />
        </main>
  
        <footer className="bg-green-800 text-white py-8">
          <div className="container mx-auto px-4 text-center">
            <p>&copy; 2024 EcoAlerts. All rights reserved.</p>
          </div>
        </footer>
      </div>
    );
  }
  