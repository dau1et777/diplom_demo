import { useState } from 'react'
import { sessionUtils } from '../services/storage'

// Validation helpers
const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return regex.test(email)
}

const validatePassword = (password) => {
  return password.length >= 6
}

const getPasswordStrength = (password) => {
  if (password.length === 0) return 'none'
  if (password.length < 6) return 'weak'
  if (password.length < 10) return 'medium'
  if (/[0-9]/.test(password) && /[A-Z]/.test(password)) return 'strong'
  return 'medium'
}

export default function SignUp({ onNavigate }) {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [errors, setErrors] = useState({})
  const [touched, setTouched] = useState({})

  const handleBlur = (field) => {
    setTouched({ ...touched, [field]: true })
  }

  const validateForm = () => {
    const newErrors = {}

    if (!username.trim()) {
      newErrors.username = 'Username is required'
    } else if (username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters'
    }

    if (!email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!validateEmail(email)) {
      newErrors.email = 'Please enter a valid email address'
    }

    if (!password) {
      newErrors.password = 'Password is required'
    } else if (!validatePassword(password)) {
      newErrors.password = 'Password must be at least 6 characters'
    }

    if (!confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password'
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSignUp = (e) => {
    e.preventDefault()
    if (!validateForm()) return

    try {
      sessionUtils.registerUser(username, email, password)
      onNavigate('home')
    } catch (err) {
      setErrors({ submit: err.message || 'Sign up failed' })
    }
  }

  const passwordStrength = getPasswordStrength(password)
  const strengthColors = {
    none: 'bg-gray-200',
    weak: 'bg-red-500',
    medium: 'bg-yellow-500',
    strong: 'bg-green-500',
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-6">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6">Create Account</h2>
        
        {errors.submit && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {errors.submit}
          </div>
        )}

        <form onSubmit={handleSignUp} className="space-y-4">
          {/* Username */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onBlur={() => handleBlur('username')}
              className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary transition ${
                touched.username && errors.username ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
              }`}
              placeholder="Choose a username"
            />
            {touched.username && errors.username && (
              <p className="text-red-500 text-sm mt-1">❌ {errors.username}</p>
            )}
            {touched.username && !errors.username && username.length >= 3 && (
              <p className="text-green-500 text-sm mt-1">✓ Username looks good</p>
            )}
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onBlur={() => handleBlur('email')}
              className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary transition ${
                touched.email && errors.email ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
              }`}
              placeholder="your@email.com"
            />
            {touched.email && errors.email && (
              <p className="text-red-500 text-sm mt-1">❌ {errors.email}</p>
            )}
            {touched.email && !errors.email && email && (
              <p className="text-green-500 text-sm mt-1">✓ Email is valid</p>
            )}
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
                touched.password && errors.password ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
              }`}
              placeholder="At least 6 characters"
            />
            {password && (
              <div className="mt-2">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs text-gray-600">Password strength:</span>
                  <span className={`text-xs font-semibold ${
                    passwordStrength === 'weak' && 'text-red-500' ||
                    passwordStrength === 'medium' && 'text-yellow-500' ||
                    passwordStrength === 'strong' && 'text-green-500'
                  }`}>
                    {passwordStrength.toUpperCase()}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      passwordStrength === 'weak' && 'w-1/3 bg-red-500' ||
                      passwordStrength === 'medium' && 'w-2/3 bg-yellow-500' ||
                      passwordStrength === 'strong' && 'w-full bg-green-500'
                    }`}
                  />
                </div>
              </div>
            )}
            {touched.password && errors.password && (
              <p className="text-red-500 text-sm mt-1">❌ {errors.password}</p>
            )}
          </div>

          {/* Confirm Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              onBlur={() => handleBlur('confirmPassword')}
              className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary transition ${
                touched.confirmPassword && errors.confirmPassword ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'
              }`}
              placeholder="Re-enter your password"
            />
            {touched.confirmPassword && errors.confirmPassword && (
              <p className="text-red-500 text-sm mt-1">❌ {errors.confirmPassword}</p>
            )}
            {touched.confirmPassword && !errors.confirmPassword && confirmPassword && password === confirmPassword && (
              <p className="text-green-500 text-sm mt-1">✓ Passwords match</p>
            )}
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={Object.keys(errors).length > 0 || !username || !email || !password || !confirmPassword}
            className="w-full bg-primary text-white px-4 py-2 rounded font-semibold hover:bg-primary/90 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            Sign Up
          </button>
        </form>

        <p className="text-center text-sm text-gray-600 mt-6">
          Already have an account?{' '}
          <button
            onClick={() => onNavigate('signin')}
            className="text-primary underline hover:text-primary/80"
          >
            Sign In
          </button>
        </p>
      </div>
    </div>
  )
}
