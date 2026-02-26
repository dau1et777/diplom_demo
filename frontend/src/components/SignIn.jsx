import { useState } from 'react'
import { sessionUtils } from '../services/storage'

export default function SignIn({ onNavigate }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [touched, setTouched] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const handleBlur = (field) => {
    setTouched({ ...touched, [field]: true })
  }

  const handleSignIn = async (e) => {
    e.preventDefault()
    setError(null)
    
    // Basic validation
    if (!username.trim()) {
      setError('Please enter your username')
      return
    }
    if (!password) {
      setError('Please enter your password')
      return
    }

    try {
      setIsLoading(true)
      const user = sessionUtils.validateUser(username, password)
      if (!user) {
        setError('Invalid username or password. Please try again or create a new account.')
        return
      }
      sessionUtils.setUser(username)
      onNavigate('home')
    } catch (err) {
      setError(err.message || 'Sign in failed')
    } finally {
      setIsLoading(false)
    }
  }

  const isFormValid = username.trim() && password

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-6">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6">Sign In</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSignIn} className="space-y-4">
          {/* Username */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onBlur={() => handleBlur('username')}
              className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary transition ${
                touched.username && !username ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
              }`}
              placeholder="Enter your username"
              disabled={isLoading}
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onBlur={() => handleBlur('password')}
              className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary transition ${
                touched.password && !password ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
              }`}
              placeholder="Enter your password"
              disabled={isLoading}
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={!isFormValid || isLoading}
            className="w-full bg-primary text-white px-4 py-2 rounded font-semibold hover:bg-primary/90 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="text-center text-sm text-gray-600 mt-6">
          Don't have an account?{' '}
          <button
            onClick={() => onNavigate('signup')}
            className="text-primary underline hover:text-primary/80"
          >
            Create one now
          </button>
        </p>

        {/* Demo hint */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center mb-2">Demo Credentials:</p>
          <div className="bg-gray-50 p-3 rounded text-xs text-gray-600">
            <p>Username: <code className="bg-gray-200 px-1 rounded">testuser</code></p>
            <p>Password: <code className="bg-gray-200 px-1 rounded">password123</code></p>
          </div>
        </div>
      </div>
    </div>
  )
}
