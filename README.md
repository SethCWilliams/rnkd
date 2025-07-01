# 🎬 Rnkd - Collaborative Ranking App

A collaborative ranking app for friends and communities to decide what to watch, read, or play next using Elo-based voting and Borda count consensus.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rnkd
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure

```
rnkd/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Configuration
│   │   └── db/             # Database models
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   └── contexts/       # React contexts
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Development environment
└── README.md
```

## 🎯 Features (Phase 1 - MVP)

### ✅ Completed
- [x] FastAPI backend with dummy data
- [x] React frontend with TypeScript
- [x] Tailwind CSS with dark mode
- [x] Basic routing and navigation
- [x] Authentication endpoints (dummy)
- [x] User management endpoints (dummy)
- [x] Group management endpoints (dummy)
- [x] Movie search and lists (dummy)
- [x] Voting system endpoints (dummy)
- [x] Docker development environment
- [x] Health check endpoints

### 🔄 In Progress
- Database models and migrations
- Real authentication with Supabase
- TMDB API integration
- Elo voting algorithm implementation

### 📋 Next Steps
- Phase 2: Database & Data Models
- Phase 3: Groups & Lists Management
- Phase 4: Elo-Based Voting System
- Phase 5: Results & Consensus System

## 🛠️ API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Users
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user profile

### Groups
- `GET /api/v1/groups/` - Get all groups
- `POST /api/v1/groups/` - Create new group
- `GET /api/v1/groups/{group_id}` - Get group by ID
- `GET /api/v1/groups/{group_id}/members` - Get group members
- `POST /api/v1/groups/join/{invite_code}` - Join group

### Movies
- `GET /api/v1/movies/search` - Search movies
- `GET /api/v1/movies/popular` - Get popular movies
- `GET /api/v1/movies/{movie_id}` - Get movie by ID
- `GET /api/v1/movies/lists/` - Get movie lists
- `POST /api/v1/movies/lists/` - Create movie list
- `GET /api/v1/movies/lists/{list_id}/items` - Get list items
- `POST /api/v1/movies/lists/{list_id}/items` - Add movie to list

### Voting
- `GET /api/v1/voting/matchups/{movie_list_id}` - Get matchups
- `POST /api/v1/voting/matchups/{movie_list_id}/generate` - Generate matchups
- `POST /api/v1/voting/vote` - Submit vote
- `GET /api/v1/voting/scores/{movie_list_id}` - Get Elo scores
- `GET /api/v1/voting/progress/{movie_list_id}` - Get voting progress
- `GET /api/v1/voting/next-matchup/{movie_list_id}` - Get next matchup

## 🎨 Design System

### Colors
- **Primary**: Green (#22c55e) - Success, actions
- **Accent Cyan**: (#06b6d4) - Links, highlights
- **Accent Coral**: (#f97316) - Warnings, emphasis
- **Dark Theme**: Dark backgrounds with light text

### Components
- `.btn-primary` - Primary action buttons
- `.btn-secondary` - Secondary action buttons
- `.card` - Content containers
- `.input-field` - Form inputs

## 🔧 Development

### Environment Variables
Copy `backend/env.example` to `backend/.env` and configure:
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/rnkd
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
```

### Database
The project uses PostgreSQL with SQLAlchemy ORM. Database migrations will be added in Phase 2.

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Future Features

- Real-time voting with WebSockets
- Mobile app (React Native)
- Support for books and games
- Streaming availability integration
- Advanced analytics and insights
- Social features and sharing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 