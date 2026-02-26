import { useState, useEffect } from 'react'
import { sessionUtils } from '../services/storage'

export default function UserProfile({ onNavigate }) {
  const [user, setUser] = useState(null)
  const [quizHistory, setQuizHistory] = useState([])
  const [stats, setStats] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadUserData = async () => {
      try {
        const currentUser = sessionUtils.getUser()
        if (!currentUser) {
          onNavigate('signin')
          return
        }
        
        setUser(currentUser)
        
        // Get quiz history for this user
        const history = sessionUtils.getUserQuizHistory(currentUser) || []
        setQuizHistory(history)
        
        // Calculate stats
        if (history.length > 0) {
          const averageScore = history.reduce((sum, q) => sum + (q.compatibility || 0), 0) / history.length
          const uniqueCareers = new Set(history.map(q => q.primaryCareer))
          
          setStats({
            totalQuizzes: history.length,
            averageScore: Math.round(averageScore * 10) / 10,
            uniqueCareers: uniqueCareers.size,
            lastQuizDate: history[0]?.date,
          })
        }
      } finally {
        setLoading(false)
      }
    }

    loadUserData()
  }, [onNavigate])

  const handleLogout = () => {
    sessionUtils.logout()
    onNavigate('home')
  }

  const handleExportData = () => {
    const data = {
      username: user,
      exportDate: new Date().toISOString(),
      quizHistory: quizHistory,
      stats: stats,
    }
    
    const jsonStr = JSON.stringify(data, null, 2)
    const blob = new Blob([jsonStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `career-profile-${user}-${new Date().getTime()}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const handleDeleteQuiz = (index) => {
    const updated = quizHistory.filter((_, i) => i !== index)
    sessionUtils.setUserQuizHistory(user, updated)
    setQuizHistory(updated)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading profile...</div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">👤 {user}</h1>
              <p className="text-gray-600">Career Profile & Quiz History</p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded font-semibold hover:bg-red-600 transition"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Stats */}
        {stats.totalQuizzes > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <div className="text-3xl font-bold text-primary">{stats.totalQuizzes}</div>
              <div className="text-sm text-gray-600 mt-2">Quizzes Taken</div>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <div className="text-3xl font-bold text-green-500">{stats.averageScore}%</div>
              <div className="text-sm text-gray-600 mt-2">Avg Compatibility</div>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <div className="text-3xl font-bold text-purple-500">{stats.uniqueCareers}</div>
              <div className="text-sm text-gray-600 mt-2">Unique Careers</div>
            </div>
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <div className="text-xl font-bold text-orange-500">
                {stats.lastQuizDate ? new Date(stats.lastQuizDate).toLocaleDateString() : 'N/A'}
              </div>
              <div className="text-sm text-gray-600 mt-2">Last Quiz</div>
            </div>
          </div>
        )}

        {/* Quiz History */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">📋 Quiz History</h2>
            <div className="flex gap-3">
              <button
                onClick={() => onNavigate('quiz')}
                className="bg-primary text-white px-4 py-2 rounded font-semibold hover:bg-primary/90 transition"
              >
                Take Quiz
              </button>
              {quizHistory.length > 0 && (
                <button
                  onClick={handleExportData}
                  className="bg-green-500 text-white px-4 py-2 rounded font-semibold hover:bg-green-600 transition"
                >
                  Export Data
                </button>
              )}
            </div>
          </div>

          {quizHistory.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg mb-4">No quiz history yet</p>
              <button
                onClick={() => onNavigate('quiz')}
                className="bg-primary text-white px-6 py-2 rounded font-semibold hover:bg-primary/90 transition"
              >
                Take Your First Quiz
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead className="bg-gray-100 border-b">
                  <tr>
                    <th className="px-4 py-3 font-semibold text-gray-700">#</th>
                    <th className="px-4 py-3 font-semibold text-gray-700">Date</th>
                    <th className="px-4 py-3 font-semibold text-gray-700">Primary Career</th>
                    <th className="px-4 py-3 font-semibold text-gray-700">Compatibility</th>
                    <th className="px-4 py-3 font-semibold text-gray-700">Top Recommendations</th>
                    <th className="px-4 py-3 font-semibold text-gray-700">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {quizHistory.map((quiz, idx) => (
                    <tr key={idx} className="border-b hover:bg-gray-50 transition">
                      <td className="px-4 py-3 text-gray-600">{idx + 1}</td>
                      <td className="px-4 py-3 text-gray-600">
                        {new Date(quiz.date).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3 font-semibold text-primary">
                        {quiz.primaryCareer || 'N/A'}
                      </td>
                      <td className="px-4 py-3">
                        <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                          {quiz.compatibility || 0}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-gray-600 text-sm">
                        {quiz.topCareers
                          ? quiz.topCareers.slice(0, 2).join(', ') + (quiz.topCareers.length > 2 ? '...' : '')
                          : 'N/A'}
                      </td>
                      <td className="px-4 py-3">
                        <button
                          onClick={() => handleDeleteQuiz(idx)}
                          className="text-red-500 hover:text-red-700 transition text-sm font-semibold"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-4 justify-center flex-wrap">
          <button
            onClick={() => onNavigate('home')}
            className="bg-gray-800 text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-900 transition"
          >
            Back to Home
          </button>
          {quizHistory.length >= 2 && (
            <button
              onClick={() => onNavigate('comparison')}
              className="bg-purple-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-600 transition"
            >
              📊 Compare Quizzes
            </button>
          )}
          <button
            onClick={() => onNavigate('careers')}
            className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition"
          >
            Explore Careers
          </button>
        </div>
      </div>
    </div>
  )
}
