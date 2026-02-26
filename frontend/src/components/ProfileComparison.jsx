import { useState, useEffect } from 'react'
import { sessionUtils } from '../services/storage'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function ProfileComparison({ onNavigate }) {
  const [user, setUser] = useState(null)
  const [quizHistory, setQuizHistory] = useState([])
  const [selectedQuizzes, setSelectedQuizzes] = useState([])
  const [comparisonData, setComparisonData] = useState(null)

  useEffect(() => {
    const currentUser = sessionUtils.getUser()
    if (!currentUser) {
      onNavigate('signin')
      return
    }

    setUser(currentUser)
    const history = sessionUtils.getUserQuizHistory(currentUser) || []
    setQuizHistory(history)
  }, [onNavigate])

  const handleSelectQuiz = (index) => {
    setSelectedQuizzes(prev => {
      if (prev.includes(index)) {
        return prev.filter(i => i !== index)
      } else if (prev.length < 3) {
        return [...prev, index]
      }
      return prev
    })
  }

  const generateComparison = () => {
    if (selectedQuizzes.length === 0) return

    const selected = selectedQuizzes.map(idx => ({
      ...quizHistory[idx],
      index: idx,
      label: `Quiz ${idx + 1} (${new Date(quizHistory[idx].date).toLocaleDateString()})`
    }))

    // Prepare comparison data
    const abilityComparison = {
      data: Object.keys(selected[0].abilities || {}).map(ability => {
        const entry = { ability }
        selected.forEach((quiz, i) => {
          entry[`Quiz${quiz.index + 1}`] = Math.round((quiz.abilities?.[ability] || 0) * 10) / 10
        })
        return entry
      }),
      quizzes: selected
    }

    setComparisonData(abilityComparison)
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">📊 Quiz Comparison</h1>
          <p className="text-gray-600">Compare your progress across multiple quiz attempts</p>
        </div>

        {quizHistory.length === 0 ? (
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <p className="text-gray-500 text-lg mb-4">No quiz history to compare</p>
            <button
              onClick={() => onNavigate('quiz')}
              className="bg-primary text-white px-6 py-2 rounded font-semibold hover:bg-primary/90"
            >
              Take a Quiz
            </button>
          </div>
        ) : quizHistory.length < 2 ? (
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <p className="text-gray-500 text-lg mb-4">
              Take more quizzes to compare results (you have {quizHistory.length} quiz)
            </p>
            <button
              onClick={() => onNavigate('quiz')}
              className="bg-primary text-white px-6 py-2 rounded font-semibold hover:bg-primary/90"
            >
              Take Another Quiz
            </button>
          </div>
        ) : (
          <>
            {/* Quiz Selection */}
            <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Select Quizzes to Compare</h2>
              <p className="text-gray-600 mb-4">Choose up to 3 quizzes to compare (latest first)</p>

              <div className="space-y-3">
                {quizHistory.map((quiz, idx) => (
                  <label key={idx} className="flex items-center gap-4 p-4 border rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={selectedQuizzes.includes(idx)}
                      onChange={() => handleSelectQuiz(idx)}
                      disabled={!selectedQuizzes.includes(idx) && selectedQuizzes.length >= 3}
                      className="w-5 h-5 cursor-pointer"
                    />
                    <div className="flex-1">
                      <div className="font-semibold text-gray-800">
                        Quiz #{idx + 1} • {new Date(quiz.date).toLocaleDateString()} at {new Date(quiz.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                      <div className="text-gray-600">
                        Primary: <span className="font-semibold">{quiz.primaryCareer}</span> •
                        Compatibility: <span className="font-semibold text-green-600">{quiz.compatibility}%</span>
                      </div>
                    </div>
                  </label>
                ))}
              </div>

              <button
                onClick={generateComparison}
                disabled={selectedQuizzes.length === 0}
                className="mt-6 w-full bg-primary text-white px-6 py-3 rounded font-semibold hover:bg-primary/90 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                Compare Selected ({selectedQuizzes.length} selected)
              </button>
            </div>

            {/* Comparison Results */}
            {comparisonData && (
              <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Ability Score Comparison</h2>

                {/* Chart */}
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={comparisonData.data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="ability" angle={-45} textAnchor="end" height={100} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {comparisonData.quizzes.map((quiz, i) => (
                      <Bar
                        key={i}
                        dataKey={`Quiz${quiz.index + 1}`}
                        fill={['#6366f1', '#10b981', '#f59e0b'][i % 3]}
                      />
                    ))}
                  </BarChart>
                </ResponsiveContainer>

                {/* Summary */}
                <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                  {comparisonData.quizzes.map((quiz, i) => (
                    <div key={i} className="bg-gray-50 rounded-lg p-6">
                      <h3 className="font-bold text-gray-800 mb-3">{quiz.label}</h3>
                      <div className="space-y-2">
                        <div>
                          <p className="text-sm text-gray-600">Primary Career</p>
                          <p className="font-semibold text-primary">{quiz.primaryCareer}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Compatibility</p>
                          <p className="font-semibold text-green-600">{quiz.compatibility}%</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Top 3 Careers</p>
                          <p className="text-sm text-gray-700">
                            {quiz.topCareers?.slice(0, 3).join(', ')}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Insights */}
                <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <h3 className="font-bold text-gray-800 mb-3">📈 Progress Summary</h3>
                  <div className="space-y-2 text-sm text-gray-700">
                    <p>
                      • <strong>Quiz Count:</strong> You've taken {comparisonData.quizzes.length} quiz(zes) total
                    </p>
                    {comparisonData.quizzes.length === 2 && (
                      <>
                        <p>
                          • <strong>Compatibility Change:</strong> {
                            comparisonData.quizzes[0].compatibility > comparisonData.quizzes[1].compatibility
                              ? `↓ ${comparisonData.quizzes[1].compatibility - comparisonData.quizzes[0].compatibility}%`
                              : `↑ ${comparisonData.quizzes[0].compatibility - comparisonData.quizzes[1].compatibility}%`
                          }
                        </p>
                      </>
                    )}
                    <p>
                      • <strong>Primary Career Stability:</strong> {
                        comparisonData.quizzes.every(q => q.primaryCareer === comparisonData.quizzes[0].primaryCareer)
                          ? '✓ Consistent'
                          : '⚠ Variable'
                      }
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-4 justify-center mb-8">
              <button
                onClick={() => onNavigate('profile')}
                className="bg-gray-800 text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-900 transition"
              >
                Back to Profile
              </button>
              <button
                onClick={() => onNavigate('quiz')}
                className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition"
              >
                Take Another Quiz
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
