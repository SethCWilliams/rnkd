const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface User {
    id: number;
    name: string;
    email: string;
    profile_image_url?: string;
}

export interface Group {
    id: number;
    name: string;
    invite_code: string;
}

export interface MovieList {
    id: number;
    name: string;
    type: 'group' | 'personal';
    media_type: 'movie' | 'book' | 'game';
    status: 'open' | 'voting' | 'closed';
    group_id?: number;
}

export interface MovieListItem {
    id: number;
    external_id: string;
    title: string;
    item_metadata?: any;
    movie_list_id: number;
}

export interface Movie {
    id: number;
    title: string;
    overview: string;
    poster_path?: string;
    release_date: string;
    genre_ids: number[];
    external_id: string;
}

class ApiService {
    private getAuthHeaders(token?: string): HeadersInit {
        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        return headers;
    }

    private async handleResponse<T>(response: Response): Promise<T> {
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    }

    // Users
    async getUsers(): Promise<User[]> {
        const response = await fetch(`${API_BASE_URL}/users/`);
        return this.handleResponse<User[]>(response);
    }

    async getUser(userId: number): Promise<User> {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`);
        return this.handleResponse<User>(response);
    }

    // Groups
    async getGroups(): Promise<Group[]> {
        const response = await fetch(`${API_BASE_URL}/groups/`);
        return this.handleResponse<Group[]>(response);
    }

    async getGroup(groupId: number): Promise<Group> {
        const response = await fetch(`${API_BASE_URL}/groups/${groupId}`);
        return this.handleResponse<Group>(response);
    }

    async getGroupMembers(groupId: number): Promise<User[]> {
        const response = await fetch(`${API_BASE_URL}/groups/${groupId}/members`);
        return this.handleResponse<User[]>(response);
    }

    async createGroup(name: string, inviteCode?: string): Promise<Group> {
        const response = await fetch(`${API_BASE_URL}/groups/`, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify({ name, invite_code: inviteCode }),
        });
        return this.handleResponse<Group>(response);
    }

    async joinGroup(groupId: number, userId: number): Promise<{ message: string }> {
        const response = await fetch(`${API_BASE_URL}/groups/${groupId}/join`, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify({ user_id: userId }),
        });
        return this.handleResponse<{ message: string }>(response);
    }

    // Movie Lists
    async getMovieLists(): Promise<MovieList[]> {
        const response = await fetch(`${API_BASE_URL}/movies/lists/`);
        return this.handleResponse<MovieList[]>(response);
    }

    async createMovieList(listData: {
        name: string;
        type: 'group' | 'personal';
        media_type: 'movie' | 'book' | 'game';
        group_id?: number;
        created_by_user_id: number;
        status?: 'open' | 'voting' | 'closed';
    }): Promise<MovieList> {
        const response = await fetch(`${API_BASE_URL}/movies/lists/`, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify(listData),
        });
        return this.handleResponse<MovieList>(response);
    }

    async getMovieListItems(listId: number): Promise<MovieListItem[]> {
        const response = await fetch(`${API_BASE_URL}/movies/lists/${listId}/items`);
        return this.handleResponse<MovieListItem[]>(response);
    }

    async addMovieToList(listId: number, movieData: {
        external_id: string;
        title: string;
        item_metadata?: any;
    }): Promise<MovieListItem> {
        const response = await fetch(`${API_BASE_URL}/movies/lists/${listId}/items`, {
            method: 'POST',
            headers: this.getAuthHeaders(),
            body: JSON.stringify({
                ...movieData,
                movie_list_id: listId,
            }),
        });
        return this.handleResponse<MovieListItem>(response);
    }

    // Movies
    async searchMovies(query: string = ''): Promise<Movie[]> {
        const params = new URLSearchParams();
        if (query) params.append('query', query);
        
        const response = await fetch(`${API_BASE_URL}/movies/search?${params}`);
        return this.handleResponse<Movie[]>(response);
    }

    async getPopularMovies(): Promise<Movie[]> {
        const response = await fetch(`${API_BASE_URL}/movies/popular`);
        return this.handleResponse<Movie[]>(response);
    }

    async getMovie(movieId: number): Promise<Movie> {
        const response = await fetch(`${API_BASE_URL}/movies/${movieId}`);
        return this.handleResponse<Movie>(response);
    }

    // Helper methods for getting user-specific data
    async getUserGroups(userId: number): Promise<Group[]> {
        // Get all groups and filter by user membership
        // Note: This is inefficient but works with current API structure
        const allGroups = await this.getGroups();
        const userGroups: Group[] = [];
        
        for (const group of allGroups) {
            try {
                const members = await this.getGroupMembers(group.id);
                if (members.some(member => member.id === userId)) {
                    userGroups.push(group);
                }
            } catch (error) {
                console.error(`Error checking membership for group ${group.id}:`, error);
            }
        }
        
        return userGroups;
    }

    async getUserMovieLists(userId: number): Promise<MovieList[]> {
        // Get all movie lists and filter by user access
        const allLists = await this.getMovieLists();
        const userGroups = await this.getUserGroups(userId);
        const userGroupIds = userGroups.map(group => group.id);
        
        return allLists.filter(list => 
            list.type === 'personal' || 
            (list.group_id && userGroupIds.includes(list.group_id))
        );
    }
}

export const apiService = new ApiService();