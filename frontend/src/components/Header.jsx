import { useEffect, useState } from 'react'
import { sessionUtils } from '../services/storage'

/**
 * Navigation Header Component
 * Displays site title and navigation links
 */
export default function Header({ currentPage, onNavigate }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    // Check user on mount
    setUser(sessionUtils.getUser())
    
    // Update user when page changes (to detect login/logout)
    const timer = setTimeout(() => {
      setUser(sessionUtils.getUser())
    }, 100)
    
    return () => clearTimeout(timer)
  }, [currentPage])

  const handleLogout = () => {
    sessionUtils.logout()
    setUser(null)
    onNavigate('home')
  }

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <nav className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-primary">CareerPath</h1>
          <p className="text-xs text-gray-600">AI-Powered Career Recommendation</p>
        </div>

        <div className="flex gap-6 items-center">
          <button
            onClick={() => onNavigate('home')}
            className={`px-4 py-2 rounded transition ${
              currentPage === 'home'
                ? 'bg-primary text-white'
                : 'text-gray-700 hover:text-primary'
            }`}
          >
            Home
          </button>
          <button
            onClick={() => onNavigate('quiz')}
            className={`px-4 py-2 rounded transition ${
              currentPage === 'quiz'
                ? 'bg-primary text-white'
                : 'text-gray-700 hover:text-primary'
            }`}
          >
            Take Quiz
          </button>
          <button
            onClick={() => onNavigate('results')}
            className={`px-4 py-2 rounded transition ${
              currentPage === 'results'
                ? 'bg-primary text-white'
                : 'text-gray-700 hover:text-primary'
            }`}
          >
            Results
          </button>
          <button
            onClick={() => onNavigate('careers')}
            className={`px-4 py-2 rounded transition ${
              currentPage === 'careers'
                ? 'bg-primary text-white'
                : 'text-gray-700 hover:text-primary'
            }`}
          >
            Careers
          </button>

          {/* Auth controls */}
          {!user ? (
            <div className="flex gap-2">
              <button
                onClick={() => onNavigate('signin')}
                className="px-4 py-2 rounded text-gray-700 hover:text-primary"
              >
                Sign In
              </button>
              <button
                onClick={() => onNavigate('signup')}
                className="px-4 py-2 rounded bg-primary text-white hover:bg-primary/90"
              >
                Sign Up
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-700">👤 <strong>{user}</strong></span>
              <button
                onClick={() => onNavigate('profile')}
                className={`px-4 py-2 rounded transition ${
                  currentPage === 'profile'
                    ? 'bg-primary text-white'
                    : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                }`}
              >
                Profile
              </button>
              <button
                onClick={handleLogout}
                className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 text-sm"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>
    </header>
  )
}
