import { useState, useEffect } from 'react'
import { BarChart, Bar, RadarChart, Radar, PolarAngleAxis, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { sessionUtils } from '../services/storage'
import { careerAPI, resultsAPI } from '../services/api'

/**
 * Results Page - Display ML recommendations and analytics
 */
export default function ResultsPage({ onNavigate }) {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedCareer, setSelectedCareer] = useState(null)
  const [careerDetails, setCareerDetails] = useState(null)
  const [bookmarks, setBookmarks] = useState([])
  const [sessionId] = useState(() => sessionUtils.getOrCreateSessionId())

  useEffect(() => {
    const loadResults = async () => {
      console.log('[Results] ===== useEffect STARTED =====')
      console.log('[Results] Page mounted, attempting to load results...')
      const sid = sessionUtils.getSessionId()
      console.log('[Results] Session ID:', sid)
      
      // Try sessionStorage first
      console.log('[Results] Checking sessionStorage...')
      const savedResults = sessionUtils.getResults()
      console.log('[Results] sessionStorage.results:', savedResults ? 'FOUND' : 'EMPTY')
      
      if (savedResults) {
        console.log('[Results] Using sessionStorage data')
        console.log('[Results] Keys in savedResults:', Object.keys(savedResults))
        console.log('[Results] savedResults.top_recommendations:', savedResults.top_recommendations)
        
        if (savedResults.top_recommendations && savedResults.top_recommendations.length > 0) {
          console.log('[Results] ✓ Valid data from sessionStorage, setting state...')
          setResults(savedResults)
          setBookmarks(sessionUtils.getBookmarks())
          setLoading(false)
          return
        } else {
          console.log('[Results] ⚠ sessionStorage data exists but has no recommendations')
        }
      }

      // Fallback: fetch from backend
      console.log('[Results] Attempting backend fallback fetch...')
      try {
        const response = await resultsAPI.getRecommendations(sid)
        console.log('[Results] Backend response:', response)
        
        if (response && response.recommendation) {
          console.log('[Results] ✓ Got data from backend, setting state...')
          setResults(response.recommendation)
          setBookmarks(sessionUtils.getBookmarks())
          setLoading(false)
          return
        }
      } catch (err) {
        console.error('[Results] Backend fallback failed:', err.message)
      }

      // No data from either source
      console.log('[Results] ✗ No results available from any source')
      setError('Unable to load results. Please try taking the quiz again.')
      setLoading(false)
    }

    loadResults()
  }, [sessionId])

  // Save quiz to user history after results are loaded
  useEffect(() => {
    if (results && !loading) {
      const user = sessionUtils.getUser()
      if (user) {
        sessionUtils.addQuizToHistory(user, results)
      }
    }
  }, [results, loading])

  const handleCareerSelect = async (career) => {
    try {
      setSelectedCareer(career.career)
      
      // Track view
      await resultsAPI.viewCareer(sessionId, career.career)
      
      // Load details (in real app would fetch from API)
      // For now, show what we have
    } catch (err) {
      console.error('Error selecting career:', err)
    }
  }

  const handleBookmarkCareer = (careerName) => {
    try {
      if (bookmarks.includes(careerName)) {
        const updated = sessionUtils.removeBookmark(careerName)
        setBookmarks(updated)
      } else {
        const updated = sessionUtils.bookmarkCareer(careerName)
        setBookmarks(updated)
      }
    } catch (err) {
      console.error('Error bookmarking career:', err)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your results...</p>
        </div>
      </div>
    )
  }

  if (error || !results || !results.top_recommendations) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md text-center">
          <p className="text-lg text-red-600 mb-4">⚠️ {error || 'No results available'}</p>
          <p className="text-xs text-gray-400 mb-6 break-all">Session: {sessionId}</p>
          <div className="flex flex-col gap-3">
            <button
              onClick={() => onNavigate('quiz')}
              className="bg-primary text-white px-6 py-3 rounded font-semibold hover:bg-primary/90"
            >
              Take the Quiz
            </button>
            <button
              onClick={() => window.location.reload()}
              className="bg-gray-200 text-gray-800 px-6 py-3 rounded font-semibold hover:bg-gray-300"
            >
              Reload Page
            </button>
          </div>
        </div>
      </div>
    )
  }

  const chartData = results.top_recommendations?.map(rec => ({
    name: rec.career,
    compatibility: rec.compatibility_score,
  })) || []

  const abilitiesData = [
    { category: 'Logical Thinking', value: results.abilities?.logical_thinking || 0 },
    { category: 'Creativity', value: results.abilities?.creativity || 0 },
    { category: 'Communication', value: results.abilities?.communication || 0 },
    { category: 'Problem Solving', value: results.abilities?.problem_solving || 0 },
    { category: 'Leadership', value: results.abilities?.leadership || 0 },
  ].filter(item => item.value > 0)

  const COLORS = ['#6366f1', '#a855f7', '#ec4899', '#f59e0b', '#10b981']

  const primaryCareer = results.top_recommendations?.[0] || {}

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Your Career Recommendations</h1>
          <p className="text-gray-600">Based on your assessment results</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Main Recommendation Card */}
          <div className="lg:col-span-2">
            <div className="bg-gradient-to-br from-primary to-purple-600 text-white rounded-lg shadow-lg p-8">
              <p className="text-sm opacity-90 mb-2">Top Recommendation</p>
              <h2 className="text-4xl font-bold mb-4">{primaryCareer.career}</h2>
              
              <div className="mb-6">
                <div className="flex justify-between mb-2">
                  <span>Match Score</span>
                  <span className="text-2xl font-bold">{primaryCareer.compatibility_score}%</span>
                </div>
                <div className="w-full bg-white/20 rounded-full h-3">
                  <div
                    className="bg-white rounded-full h-3 transition-all duration-500"
                    style={{ width: `${primaryCareer.compatibility_score}%` }}
                  ></div>
                </div>
              </div>

              <p className="text-lg mb-6">{primaryCareer.explanation}</p>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/10 p-4 rounded">
                  <p className="text-sm opacity-90 mb-1">Required Skills</p>
                  <p className="font-semibold">{primaryCareer.required_skills?.join(', ') || 'N/A'}</p>
                </div>
                <div className="bg-white/10 p-4 rounded">
                  <p className="text-sm opacity-90 mb-1">Suitable For</p>
                  <p className="font-semibold text-sm">{primaryCareer.suitable_for}</p>
                </div>
              </div>

              <button
                onClick={() => handleBookmarkCareer(primaryCareer.career)}
                className={`mt-6 w-full py-3 rounded font-semibold transition ${
                  bookmarks.includes(primaryCareer.career)
                    ? 'bg-yellow-400 text-gray-900 hover:bg-yellow-500'
                    : 'bg-white/20 text-white hover:bg-white/30'
                }`}
              >
                {bookmarks.includes(primaryCareer.career) ? '⭐ Bookmarked' : '☆ Bookmark'}
              </button>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="font-bold text-gray-800 mb-4">Assessment Summary</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center pb-3 border-b">
                  <span className="text-gray-600">Compatibility Range</span>
                  <span className="font-bold text-primary">
                    {Math.min(...chartData.map(d => d.compatibility)).toFixed(0)}% - {Math.max(...chartData.map(d => d.compatibility)).toFixed(0)}%
                  </span>
                </div>
                <div className="flex justify-between items-center pb-3 border-b">
                  <span className="text-gray-600">Top 5 Careers</span>
                  <span className="font-bold text-primary">{results.top_recommendations?.length || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Session ID</span>
                  <span className="font-mono text-xs text-gray-500 truncate max-w-xs">{sessionId}</span>
                </div>
              </div>
            </div>

            <div className="bg-blue-50 border-l-4 border-primary p-4 rounded">
              <h4 className="font-semibold text-gray-800 mb-2">💡 Next Steps</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>✓ Explore courses below</li>
                <li>✓ Research universities</li>
                <li>✓ Build relevant skills</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Compatibility Chart */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Top Career Matches</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="compatibility" fill="#6366f1" name="Compatibility %" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Abilities Radar Chart */}
          {abilitiesData.length > 0 && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Your Abilities Profile</h3>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={abilitiesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <PolarAngleAxis dataKey="category" />
                  <Radar name="Score" dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.6} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* All Recommendations */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">All Career Recommendations</h3>
          
          <div className="space-y-4">
            {results.top_recommendations?.map((career, idx) => (
              <div
                key={idx}
                onClick={() => handleCareerSelect(career)}
                className={`p-6 rounded-lg border-2 cursor-pointer transition ${
                  selectedCareer === career.career
                    ? 'border-primary bg-blue-50'
                    : 'border-gray-200 hover:border-primary'
                }`}
              >
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h4 className="text-lg font-bold text-gray-800">#{idx + 1} {career.career}</h4>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-2xl font-bold text-primary">{career.compatibility_score}%</div>
                      <div className="text-xs text-gray-600">Compatible</div>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleBookmarkCareer(career.career)
                      }}
                      className={`text-2xl transition ${
                        bookmarks.includes(career.career) ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-400'
                      }`}
                    >
                      ⭐
                    </button>
                  </div>
                </div>

                <p className="text-gray-600 mb-3">{career.explanation}</p>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 font-semibold">Required Skills</p>
                    <p className="text-sm text-gray-700">{career.required_skills?.join(', ') || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 font-semibold">Suitable For</p>
                    <p className="text-sm text-gray-700">{career.suitable_for}</p>
                  </div>
                </div>

                {selectedCareer === career.career && (
                  <div className="mt-4 pt-4 border-t">
                    <button
                      onClick={() => onNavigate('careers')}
                      className="bg-primary text-white px-4 py-2 rounded font-semibold hover:bg-primary/90 transition"
                    >
                      Explore Courses & Universities
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => onNavigate('quiz')}
            className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition"
          >
            Retake Quiz
          </button>
          <button
            onClick={() => onNavigate('careers')}
            className="bg-gray-800 text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-900 transition"
          >
            Explore All Careers
          </button>
        </div>
      </div>
    </div>
  )
}
