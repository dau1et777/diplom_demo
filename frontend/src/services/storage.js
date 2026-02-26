/**
 * Utility functions for session and local storage management
 */

export const sessionUtils = {
  // Generate or retrieve session ID
  getOrCreateSessionId: () => {
    let sessionId = sessionStorage.getItem('sessionId')
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      sessionStorage.setItem('sessionId', sessionId)
    }
    return sessionId
  },

  // Retrieve session ID
  getSessionId: () => {
    return sessionStorage.getItem('sessionId')
  },

  // Clear session
  clearSession: () => {
    sessionStorage.clear()
  },

  // Save quiz progress
  saveQuizProgress: (answers) => {
    sessionStorage.setItem('quizAnswers', JSON.stringify(answers))
  },

  // Get saved quiz progress
  getQuizProgress: () => {
    const answers = sessionStorage.getItem('quizAnswers')
    return answers ? JSON.parse(answers) : null
  },

  // Save results
  saveResults: (results) => {
    sessionStorage.setItem('results', JSON.stringify(results))
  },

  // Get saved results
  getResults: () => {
    const results = sessionStorage.getItem('results')
    return results ? JSON.parse(results) : null
  },

  // Bookmark a career
  bookmarkCareer: (careerId) => {
    const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]')
    if (!bookmarks.includes(careerId)) {
      bookmarks.push(careerId)
      localStorage.setItem('bookmarks', JSON.stringify(bookmarks))
    }
    return bookmarks
  },

  // Get bookmarked careers
  getBookmarks: () => {
    return JSON.parse(localStorage.getItem('bookmarks') || '[]')
  },

  // Remove bookmark
  removeBookmark: (careerId) => {
    const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]')
    const filtered = bookmarks.filter(id => id !== careerId)
    localStorage.setItem('bookmarks', JSON.stringify(filtered))
    return filtered
  },

  // Clear bookmarks
  clearBookmarks: () => {
    localStorage.removeItem('bookmarks')
  },

  // -----------------
  // Simple client-side auth (demo only)
  // -----------------
  // Save current user (username string)
  setUser: (username) => {
    localStorage.setItem('currentUser', username)
  },

  // Get current user
  getUser: () => {
    return localStorage.getItem('currentUser')
  },

  // Check authentication
  isAuthenticated: () => {
    return !!localStorage.getItem('currentUser')
  },

  // Log out current user
  logout: () => {
    localStorage.removeItem('currentUser')
  },

  // Register a new user (stores basic username/password in localStorage - demo only)
  registerUser: (username, email, password) => {
    const users = JSON.parse(localStorage.getItem('users') || '[]')
    if (users.find(u => u.username === username)) {
      throw new Error('Username already exists')
    }
    users.push({ username, email, password })
    localStorage.setItem('users', JSON.stringify(users))
    localStorage.setItem('currentUser', username)
    return true
  },

  // Validate credentials
  validateUser: (username, password) => {
    const users = JSON.parse(localStorage.getItem('users') || '[]')
    return users.find(u => u.username === username && u.password === password)
  },

  // Save quiz result to user's history
  addQuizToHistory: (username, quizResult) => {
    const history = sessionUtils.getUserQuizHistory(username) || []
    const entry = {
      date: new Date().toISOString(),
      primaryCareer: quizResult.primary_career,
      compatibility: Math.round(quizResult.primary_compatibility),
      topCareers: quizResult.top_recommendations?.map(r => r.career) || [],
      abilities: quizResult.abilities,
      sessionId: quizResult.session_id,
    }
    history.unshift(entry) // Add to beginning
    sessionUtils.setUserQuizHistory(username, history)
    return entry
  },

  // Get quiz history for a user
  getUserQuizHistory: (username) => {
    const key = `quiz_history_${username}`
    const history = localStorage.getItem(key)
    return history ? JSON.parse(history) : []
  },

  // Set quiz history for a user
  setUserQuizHistory: (username, history) => {
    const key = `quiz_history_${username}`
    localStorage.setItem(key, JSON.stringify(history))
  },

  // Clear quiz history for a user
  clearUserQuizHistory: (username) => {
    const key = `quiz_history_${username}`
    localStorage.removeItem(key)
  },
}

export default sessionUtils
