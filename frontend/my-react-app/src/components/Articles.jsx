import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

// This would typically come from an API or database
const articles = [
  {
    id: 1,
    title: "Global Temperatures Hit New Record",
    summary: "Scientists report that global temperatures have reached a new high, raising concerns about climate change acceleration.",
    fullContent: "In a startling revelation, climate scientists from the World Meteorological Organization (WMO) have announced that global temperatures have surpassed previous records, marking a significant milestone in the ongoing climate crisis. This new peak has sent shockwaves through the scientific community and is expected to have far-reaching implications for global climate policies. The record-breaking temperatures were observed across multiple regions, with particular hotspots in the Arctic and parts of South America. Experts warn that this trend, if continued, could lead to more frequent and severe weather events, rising sea levels, and disruptions to ecosystems worldwide. The findings underscore the urgent need for more aggressive measures to reduce greenhouse gas emissions and transition to renewable energy sources."
  },
  {
    id: 2,
    title: "Innovative Ocean Cleanup Project Launches",
    summary: "A new initiative using advanced technology aims to remove millions of tons of plastic from the world's oceans.",
    fullContent: "In a bold move to address the growing crisis of ocean pollution, an international consortium of environmental organizations and tech companies has launched an ambitious project to clean up the world's oceans. The initiative, named 'Operation Clear Seas', utilizes a fleet of autonomous, solar-powered vessels equipped with advanced filtration systems. These vessels are designed to collect and process plastic waste, from large debris to microplastics, without harming marine life. The project aims to remove up to 5 million tons of plastic from the oceans over the next decade. Initial deployments will focus on the Great Pacific Garbage Patch, with plans to expand to other heavily polluted areas. This groundbreaking effort not only aims to clean up existing pollution but also raises awareness about the need to reduce plastic consumption and improve waste management practices globally."
  },
  {
    id: 3,
    title: "Breakthrough in Sustainable Agriculture",
    summary: "Researchers develop a new crop variety that requires 50% less water and is more resistant to pests.",
    fullContent: "In a major breakthrough for sustainable agriculture, scientists at the Global Crop Research Institute have developed a new variety of wheat that promises to revolutionize farming practices. This new strain, dubbed 'AquaEfficient Wheat', requires only half the amount of water compared to traditional varieties and demonstrates remarkable resistance to common pests and diseases. The development comes after a decade of research using advanced genetic editing techniques that do not involve introducing foreign DNA, making it distinct from GMO crops. Field trials have shown that the AquaEfficient Wheat can thrive in semi-arid conditions and maintains high yield levels even under water stress. This innovation could be a game-changer for food security in water-scarce regions and could significantly reduce the agricultural sector's water footprint. The researchers are now working on applying similar techniques to other staple crops like rice and corn."
  }
];

export default function Articles() {
  const [expandedArticle, setExpandedArticle] = useState(null);

  const toggleArticle = (id) => {
    setExpandedArticle(expandedArticle === id ? null : id);
  };

  return (
    <div className="space-y-6">
      {articles.map((article) => (
        <div key={article.id} className="border rounded-lg p-4 shadow-md bg-white">
          <h2 className="text-xl font-bold">{article.title}</h2>
          <p className="text-gray-600">{article.summary}</p>
          <div className="mt-2">
            {expandedArticle === article.id && (
              <p className="text-green-700 mb-4">{article.fullContent}</p>
            )}
            <button
              onClick={() => toggleArticle(article.id)}
              className="flex items-center justify-center w-full mt-2 py-2 px-4 border border-gray-300 rounded-md bg-white text-gray-700 hover:bg-gray-100 transition duration-200"
            >
              {expandedArticle === article.id ? (
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
  );
}

