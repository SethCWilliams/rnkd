
# 📝 Product Requirements Document – Rnkd

## 1. Overview

Rnkd is a collaborative ranking app for friends and communities to decide what to watch, read, or play next. Built around an Elo-based voting system and a Borda count for group consensus, users face off two items at a time—making rankings intuitive, fast, and fun. While the MVP targets movies, Rnkd is designed to support other media types like books, games, and more.

---

## 2. Goals & Objectives

- Create a simple, engaging experience for group-based decision-making around media consumption.
- Replace the stress of group indecision with a fun, game-like ranking flow.
- Ensure the system is modular enough to support multiple content types beyond movies (e.g., books, games).

---

## 3. Target Users

- Movie clubs
- Friend groups
- Book clubs
- Discord/game communities
- Couples deciding what to watch/play
- Users who want a smarter personal watchlist or backlog ranking system

---

## 4. Core Features

### 🎯 MVP (Movies)

#### 1. Authentication & Onboarding
- Signup/Login via Supabase Auth or similar
- Create profile, optionally with profile image and interests

#### 2. Groups
- Create or join a group via invite code or link
- Each group has multiple users and shared lists

#### 3. Lists
- Create a Movie List
- Choose between Group List or Personal Watchlist
- Set a submission window (via timer or manual control)
- Autocomplete search powered by TMDB API
- AI-generated list titles (e.g., “Spooky Vibes”)

#### 4. Elo-Based Voting
- One-on-one matchups between items
- Each user ranks individually via Elo algorithm
- Optimistic UI (preloaded matchups, no spinner delays)
- Prevent duplicate or overly repetitive matchups

#### 5. Group Consensus & Reveal
- After all users vote, generate ranked lists per user
- Use Borda count to determine the group winner
- Show individual ranking vs group outcome

---

## 5. Future Features

### 🔮 Nice-to-Have (V1.1+)

- Add reactions or notes post-watch
- Profile stats: win rate, most picked genres, etc.
- “Wildcard” option: random item added mid-list
- “Best-of” tournament format for large lists
- Streaming availability via Watchmode/JustWatch
- Mobile version (React Native or Flutter)
- Support for Books and Games
- Swap TMDB for OpenLibrary, IGDB, etc.
- MediaType enum in schema with custom search adapters

---

## 6. Data Model Overview

```plaintext
User
  - id
  - name
  - email
  - profile_image_url

Group
  - id
  - name
  - invite_code

GroupUser (many-to-many)

MovieList
  - id
  - group_id
  - created_by_user_id
  - name
  - type: enum('group', 'personal')
  - media_type: enum('movie', 'book', 'game')
  - status: enum('open', 'voting', 'closed')

MovieListItem
  - id
  - movie_list_id
  - external_id (TMDB/ISBN/etc.)
  - title
  - metadata (JSON blob)

EloScore
  - id
  - movie_list_id
  - user_id
  - movie_list_item_id
  - score

Matchup
  - id
  - movie_list_id
  - user_id
  - item_a_id
  - item_b_id
  - winner_id
  - created_at
```

---

## 7. Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL + SQLAlchemy or Tortoise ORM
- Redis (optional, for Elo matchmaking or session state)
- Temporal (future-proofing for voting phases, reminders, etc.)

### Frontend
- React + TypeScript
- Tailwind CSS
- React Query for data fetching/caching

### Infra & APIs
- Vercel or Netlify for hosting
- Docker for dev environments
- Supabase Auth or Clerk/Auth0
- TMDB API (movies)
- OpenLibrary (books, future)
- IGDB (games, future)

---

## 8. Key UX & Design Principles

- Game-like interaction → quick, low-friction voting experience
- Minimalist UI with strong emphasis on speed and clarity
- Mobile-first layout
- Dark mode default for movie-night vibes
- Personality in microcopy and animations to build delight

---

## 9. Success Metrics

- 🚀 Time to group decision (from list creation to consensus)
- 🤝 Group engagement rate (votes per list, users per group)
- 🔁 Retention (weekly active users, repeat list creators)
- 🎯 Personal vs group alignment score (how often the group winner ranks top 3 for a user)

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| TMDB API quota limits | Caching results locally; consider paid tier |
| Decision fatigue in voting | Cap voting per session or introduce voting breaks |
| Scalability of content types | Abstract content handling by media type; adapter pattern for APIs |
| Drop-off post-decision | Add post-watch features like reactions or reviews |

---

## 11. User Experience & Visual Design

### 🖼️ Design Style & Visual Language

Rnkd’s UI draws inspiration from modern, contrast-heavy designs:
- Dark backgrounds with bold, clean typography
- Vibrant accent colors (neon green, cyan, coral)
- Section-based layouts with clearly defined content blocks
- Geometric accents or illustrations to guide flow
- High-quality avatars or photos for warmth and social feel

**Design Tone**
- 📱 Modern but accessible
- 🧩 Modular components
- 🌙 Dark mode first

---

### 🧭 Navigation Structure

| Page | Purpose |
|------|---------|
| Landing Page | Public marketing site |
| User Home | Dashboard: groups, timers, votes, watchlists |
| Group Home | Group-specific overview |
| Voting Page | Elo matchups (tap/swipe), timer, progress |
| Results Page | Final group result, personal vs group rankings |
| Admin Page | Group owner controls |
| Add to Group Page | Add media to list (TMDB/OpenLibrary/IGDB) |

---

### 🎛️ UX Interaction Details

- **Tap (desktop)** and **Swipe (mobile)** voting
- Timers visible in:
  - User Home
  - Group Home
  - Voting Page
- Timers control:
  - Submission phase
  - Voting phase
  - Admin override available

---

### 📲 Mobile-First Considerations

- Swipe-native voting interface
- Tap targets >44px
- Carousels or accordions for dense lists
- Layout padding for notch-safe areas

---

## 12. Metrics & Feedback

### 🎯 Objectives

- Understand drop-off in funnel
- Track voting behavior and group dynamics
- Enable future cohort-based improvements

### 🧪 Event Tracking Plan

| Event | Description |
|-------|-------------|
| user_signed_up | Triggered on new account creation |
| group_created | When user creates a group |
| movie_list_created | When a list is started |
| movie_added_to_list | When an item is submitted to a list |
| matchup_voted | Elo vote event |
| voting_completed | User finishes all matchups |
| borda_results_viewed | Group results displayed |
| user_returned | User logs in after X days |

### 🧍 User Properties

- Account age
- Groups joined / created
- Lists contributed to
- Voting participation %
- Agreement with group consensus

### 📈 Tooling

- **Primary:** PostHog (event tracking, funnels)
- **Secondary:** Plausible or Umami (page views)
- Identify user on login (`posthog.identify`)
- Capture metadata with each interaction

### 💬 Feedback Loop

- Post-result: thumbs up/down
- Optional: short comment box
- Admin: trigger feedback prompt after X lists

---

## 13. Extensibility for Other Media Types

| Media Type | Source API | Metadata |
|------------|------------|----------|
| Movie | TMDB | Title, poster, genre, runtime |
| Book | OpenLibrary | Title, author, pages |
| Game | IGDB | Title, genre, platform |

All content types support abstracted adapters and the same voting/consensus UX.
