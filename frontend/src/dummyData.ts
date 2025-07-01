// Types for dummy data
export interface Group {
    id: number;
    name: string;
    members: number;
    description: string;
    status: 'Active' | 'Inactive';
    accent: 'cyan' | 'neon' | 'coral';
    example: string;
}

export interface List {
    id: number;
    name: string;
    type: 'Books' | 'Games' | 'Movies' | 'Other';
    status: 'Voting' | 'Open' | 'Closed';
    items: number;
}

export interface Activity {
    id: number;
    text: string;
    time: string;
    link: string;
    action: string;
}

export interface Matchup {
    id: number;
    listId: number;
    itemA: string;
    itemB: string;
    voted?: boolean;
    winner?: string;
}

// Dummy data
export const groups: Group[] = [
    {
        id: 1,
        name: 'Book Club',
        members: 6,
        description: 'Monthly book picks and lively discussions.',
        status: 'Active',
        accent: 'cyan',
        example: 'Currently ranking: "Best Summer Reads"',
    },
    {
        id: 2,
        name: 'Game Squad',
        members: 4,
        description: 'Decide what to play next for game night.',
        status: 'Active',
        accent: 'neon',
        example: 'Currently ranking: "Party Games"',
    },
    {
        id: 3,
        name: 'Movie Crew',
        members: 5,
        description: 'Pick the next movie for Friday night.',
        status: 'Inactive',
        accent: 'coral',
        example: 'Last ranked: "Oscar Winners"',
    },
];

export const lists: List[] = [
    { id: 1, name: 'Book Club Picks', type: 'Books', status: 'Voting', items: 7 },
    { id: 2, name: 'Game Night Options', type: 'Games', status: 'Open', items: 5 },
    { id: 3, name: 'Movie Night', type: 'Movies', status: 'Closed', items: 8 },
];

export const activity: Activity[] = [
    { id: 1, text: 'Voted on "Book Club Picks"', time: '2 hours ago', link: '/app/voting/1', action: 'Continue' },
    { id: 2, text: 'Joined "Game Squad" group', time: '1 day ago', link: '/app/groups', action: 'View' },
    { id: 3, text: 'Created "Movie Night" list', time: '3 days ago', link: '/app/voting/3', action: 'Start Voting' },
];

export const matchups: Matchup[] = [
    { id: 1, listId: 1, itemA: 'The Great Gatsby', itemB: 'To Kill a Mockingbird' },
    { id: 2, listId: 1, itemA: '1984', itemB: 'Pride and Prejudice' },
    { id: 3, listId: 2, itemA: 'Codenames', itemB: 'Catan' },
    { id: 4, listId: 3, itemA: 'Inception', itemB: 'The Godfather' },
]; 