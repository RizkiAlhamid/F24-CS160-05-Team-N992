# F24-CS160-05-Team-N992 Project

## 🌟 Project Overview

### 🚀 Key Features

- **AI-Powered Analysis**: Intelligent summarization and key point extraction
- **Real-time Updates**: Continuous monitoring of environmental news sources
- **Personalized Experience**: Tailored content delivery based on user preferences
- **Interactive Interface**: Modern, responsive design for seamless user experience

## 👥 Team N992

| Member | Role | Responsibilities |
|--------|------|-----------------|
| Ahmad Kaddoura | Project Manager | Web Scraper Lead | Data Collection, AI Integration |
| Davel Radindra | Full Stack Developer | System Integration, Testing | 
| Muhammad Rizki Miftha Alhamid | DevOps | API Development, Database Architecture |
| Thang Kim Nguyen | Frontend Lead | UI/UX Design, React Implementation |

## 🛠️ Technology Stack

### Frontend
- React 18 with Vite
- TailwindCSS for styling
- React Router for navigation
- Lucide React for icons
- Responsive design principles

### Backend
- FastAPI (Python 3.12+)
- MongoDB for data persistence
- Poetry for dependency management
- RESTful API architecture
- CORS middleware support

### Web Scraper
- Beautiful Soup 4 for web scraping
- Perplexity AI integration
- Rate limiting mechanisms
- Async processing pipeline
- Environmental content filtering

## 🚀 Getting Started

### Prerequisites
- Node.js (v18.0.0+)
- Python (v3.12+)
- Poetry
- MongoDB
- Perplexity API Key

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/RizkiAlhamid/F24-CS160-05-Team-N992.git
cd F24-CS160-05-Team-N992
```

2. **Frontend Setup**
```bash
cd frontend/my-react-app
npm install
npm run dev
```

3. **Backend Setup**
```bash
cd backend
poetry install
poetry shell
./run_dev.sh
```

4. **Web Scraper Setup**
```bash
cd webscraper
poetry install
poetry shell
./run_dev.sh
```

## 🌐 System Architecture

### Frontend Architecture
- Component-based structure
- State management using React hooks
- Responsive UI with Tailwind CSS
- Protected routes implementation
- Real-time data fetching

### Backend Architecture
- RESTful API endpoints
- MongoDB integration
- Async request handling
- Error middleware
- CORS configuration

### Web Scraper Architecture
- Modular scraping system
- AI-powered content analysis
- Rate limiting implementation
- Error handling and retry logic
- Data transformation pipeline

## 📚 API Documentation

### Main Endpoints
- `/articles` - Get all environmental articles
- `/articles/{id}` - Get specific article details
- `/webscraper/scrape_bbc` - Trigger BBC news scraping
- `/personas` - Manage AI personas for content analysis

## 🔧 Development Workflow

1. **Environment Setup**
   - Configure MongoDB connection
   - Set up environment variables
   - Install required dependencies

2. **Running the Application**
   - Start MongoDB service
   - Launch backend server (port 8080)
   - Launch web scraper service (port 8081)
   - Start frontend development server (port 5173)

3. **Development Process**
   - Create feature branch
   - Implement changes
   - Test locally
   - Submit pull request

## 🔍 Testing

- Frontend: `npm run test`
- Backend: `poetry run pytest`
- Web Scraper: `poetry run pytest`

## 🙏 Acknowledgments

- BBC News for providing environmental news content
- Perplexity AI for powering our content analysis
- San Jose State University CS Department for project guidance
- The FastAPI and React communities for excellent documentation

---

<div align="center">
Made with ❤️ by Team N992
</div>
