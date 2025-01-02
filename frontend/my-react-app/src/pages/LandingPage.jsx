import { Leaf, Newspaper, Bell, TreePine } from "lucide-react";
import aboutImg from '../assets/aboutImg.jpg';
import { Link } from "react-router-dom";


export default function LandingPage() {
  return (
    <div className="min-h-screen bg-green-50">
      <header className="bg-green-600 text-white">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold flex items-center">
            <Leaf className="mr-2" />
            Particle
          </Link>
          <Link to="/login" className="bg-white text-green-600 hover:bg-green-100 px-4 py-2 rounded inline-block">
              Log In
          </Link>
        </div>
      </header>

      <main>
        <section className="py-20 text-center">
          <div className="container mx-auto px-4">
            <h1 className="text-4xl md:text-6xl font-bold text-green-800 mb-6">
            Stay Informed, Stay Green.
            </h1>
            <p className="text-xl text-green-700 mb-8">
              Join our community of eco-scholars and make a difference today!
            </p>
            <div className="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-4">
              {/* Removed Input Field */}
              <Link to="/register" className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded inline-block">
                    Get Started
              </Link>
            </div>
          </div>
        </section>

        <section id="about" className="py-20 bg-green-100">
          <div className="container mx-auto px-4">
            <div className="flex flex-col md:flex-row items-center">
              <div className="md:w-1/2 mb-8 md:mb-0 md:pr-12">
                <h2 className="text-3xl font-bold text-green-800 mb-4 text-center">About Particle</h2>
                <p className="text-green-700 mb-4 text-lg">
                In a world filled with constant noise and overwhelming information, connecting with our environment can be challenging. The founders of Particle recognized this struggle and envisioned a solution to empower individuals in engaging with the planet meaningfully.

                Driven by their love for nature and commitment to sustainability, they created an app that simplifies the complex world of environmental news. Particle curates the latest environmental articles, weather warnings, and urgent updates daily, presenting them in a concise and engaging format.
                </p>
                <p className="text-green-700 mb-4 text-lg">
                Our mission is to inform and inspire users, transforming how they interact with environmental issues. Whether you're an eco-warrior or just starting to explore sustainability, Particle provides the tools to make a difference.

                Join us in protecting our planet, one alert at a time. Together, we can build a more informed and engaged community dedicated to a healthier Earth.
                </p>
                
              </div>
              <div className="md:w-1/2 md:ml-12">
                <img
                  src={aboutImg}
                  alt="Team of environmentalists working together"
                  width={700}
                  height={500}
                  className="rounded-lg shadow-lg"
                />
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="py-20 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-green-800 text-center mb-12">Our Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <FeatureCard
                icon={<Newspaper className="w-12 h-12 text-green-600" />}
                title="Daily Summarized Articles"
                description=" Receive curated summaries of the latest environmental news and weather warnings tailored to your location. Stay informed without feeling overwhelmed by information overload."
              />
              <FeatureCard
                icon={<TreePine className="w-12 h-12 text-green-600" />}
                title="Interactive Article Details"
                description="Click on any summarized article to dive deeper into the content. Access full articles, statistics, and expert insights to enhance your understanding of environmental issues."
              />
              <FeatureCard
                icon={<Bell className="w-12 h-12 text-green-600" />}
                title="Personalized Notifications and Alerts"
                description="Customize your notification settings to receive alerts for weather warnings, significant environmental events, and updates based on your preferences."
              />
            </div>
          </div>
        </section>

        <section className="py-20 bg-green-600 text-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold mb-6">Ready to Make a Difference?</h2>
            <p className="text-xl mb-8">Join thousands of environmentally conscious individuals in our mission to protect the planet.</p>
            <Link to="/register" className="bg-white text-green-600 hover:bg-green-100 px-4 py-2 rounded inline-block">Join Particle Today!</Link>

          </div>
        </section>
      </main>

      <footer className="bg-green-800 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 Particle. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="bg-green-50 p-6 rounded-lg text-center">
      <div className="flex justify-center mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-green-800 mb-2">{title}</h3>
      <p className="text-green-700">{description}</p>
    </div>
  );
}
