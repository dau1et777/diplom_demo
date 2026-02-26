import { useState, useEffect } from 'react'
import { quizAPI, resultsAPI } from '../services/api'
import { sessionUtils } from '../services/storage'

/**
 * Quiz Component - Multi-step career assessment
 * Displays questions on a scale 1-10 and collects responses
 */
export default function QuizPage({ onNavigate }) {
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [answers, setAnswers] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [sessionId] = useState(() => sessionUtils.getOrCreateSessionId())

  // Load questions on mount
  useEffect(() => {
    const loadQuestions = async () => {
      try {
        setLoading(true)
        const data = await quizAPI.getQuestions()
        setQuestions(data)

        // Load saved progress if exists
        const savedAnswers = sessionUtils.getQuizProgress()
        if (savedAnswers) {
          setAnswers(savedAnswers)
        }
      } catch (err) {
        setError('Failed to load quiz questions. Please try again.')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    loadQuestions()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading quiz questions...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-600">
          <p className="text-lg mb-4">{error}</p>
          <div className="flex justify-center gap-4">
            <button
              onClick={async () => {
                setError(null)
                setLoading(true)
                try {
                  const data = await quizAPI.getQuestions()
                  setQuestions(data)
                } catch (err) {
                  setError('Failed to load quiz questions. Please try again.')
                } finally {
                  setLoading(false)
                }
              }}
              className="bg-primary text-white px-6 py-2 rounded hover:bg-primary/90"
            >
              Try Again
            </button>

            <button
              onClick={() => window.location.reload()}
              className="bg-gray-200 text-gray-800 px-6 py-2 rounded hover:bg-gray-300"
            >
              Hard Refresh
            </button>
          </div>
        </div>
      </div>
    )
  }

  const handleAnswer = (questionId, value) => {
    const newAnswers = {
      ...answers,
      [questionId]: parseInt(value),
    }
    setAnswers(newAnswers)
    sessionUtils.saveQuizProgress(newAnswers)
  }

  const handleSubmit = async () => {
    if (Object.keys(answers).length < questions.length) {
      setError('Please answer all questions before submitting.')
      return
    }

    try {
      setSubmitting(true)
      setError(null)
      console.log('[Quiz] Submitting', Object.keys(answers).length, 'answers...')
      console.log('[Quiz] Session ID:', sessionId)

      // Submit quiz answers
      console.log('[Quiz] Calling submitQuiz API...')
      const submitResponse = await quizAPI.submitQuiz(sessionId, answers)
      console.log('[Quiz] Submit response:', submitResponse)
      
      if (!submitResponse.success) {
        throw new Error(submitResponse.error || 'Failed to submit quiz')
      }
      console.log('✓ Quiz answers submitted successfully')

      // Generate recommendations
      console.log('[ML] Calling generateRecommendations API...')
      const recommendationsResponse = await resultsAPI.generateRecommendations(sessionId, 5)
      console.log('[ML] Full recommendations response:', recommendationsResponse)

      // The API returns data directly
      const recPayload = recommendationsResponse || {}
      console.log('[Storage] Payload type:', typeof recPayload, 'Is array:', Array.isArray(recPayload))
      console.log('[Storage] Payload keys:', Object.keys(recPayload))
      console.log('[Storage] Has top_recommendations:', !!recPayload.top_recommendations)
      console.log('[Storage] top_recommendations is array:', Array.isArray(recPayload.top_recommendations))
      console.log('[Storage] top_recommendations length:', recPayload.top_recommendations?.length)

      // Basic validation of expected structure
      const hasRecommendations = recPayload && recPayload.top_recommendations && recPayload.top_recommendations.length > 0
      if (!hasRecommendations) {
        console.error('[ML] No recommendations in payload. Structure:', Object.keys(recPayload))
        console.error('[ML] top_recommendations:', recPayload.top_recommendations)
        throw new Error('No career recommendations generated. Please try again.')
      }

      // Save results
      console.log('[Storage] About to save to sessionStorage...')
      sessionUtils.saveResults(recPayload)
      const verifySave = sessionUtils.getResults()
      console.log('[Storage] Verification - data saved successfully:', !!verifySave)
      console.log('[Storage] Saved session ID:', verifySave?.session_id)
      console.log('[Storage] Saved primary_career:', verifySave?.primary_career)
      
      console.log('[Navigation] Navigating to results page...')
      sessionUtils.clearBookmarks()
      onNavigate('results')
      console.log('[Navigation] ✓ onNavigate called')
    } catch (err) {
      const errorMsg = err.message || 'An error occurred. Please try again.'
      setError(errorMsg)
      console.error('[ERROR]', errorMsg, err)
    } finally {
      setSubmitting(false)
    }
  }

  // Calculate progress
  const answeredCount = Object.keys(answers).length
  const progress = (answeredCount / questions.length) * 100

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-2xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Career Assessment Quiz</h1>
          <p className="text-gray-600 mb-6">Answer honestly to get accurate recommendations</p>

          {/* Progress Bar */}
          <div className="mb-6">
            <div className="flex justify-between mb-2">
              <span className="text-sm font-semibold text-gray-700">
                Progress: {answeredCount} of {questions.length}
              </span>
              <span className="text-sm font-semibold text-primary">{Math.round(progress)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-primary h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>

          {/* Page Indicator */}
          <div className="text-center text-sm text-gray-500">
            All {questions.length} Questions
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-8">
            {error}
          </div>
        )}

        {/* Questions */}
        <div className="space-y-6 mb-8">
          {questions.map((question) => (
            <div key={question.id} className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-800 mb-2">
                {question.question_text}
              </h2>
              <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-full mb-4">
                {question.category_display}
              </span>

              {/* Slider with value display */}
              <div className="mt-4">
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={answers[question.id] || 5}
                  onChange={(e) => handleAnswer(question.id, e.target.value)}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between mt-3">
                  <span className="text-sm text-gray-600">Disagree</span>
                  <span className="text-lg font-bold text-primary">
                    {answers[question.id] || 5}/10
                  </span>
                  <span className="text-sm text-gray-600">Agree</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Navigation Buttons */}
        <div className="bg-white rounded-lg shadow-lg p-6 flex justify-center">
          <button
            onClick={handleSubmit}
            disabled={submitting || Object.keys(answers).length < questions.length}
            className="px-8 py-3 bg-green-600 text-white rounded font-semibold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {submitting ? 'Analyzing...' : 'Submit & Get Results'}
          </button>
        </div>

        {/* Tips Section */}
        <div className="mt-8 bg-blue-50 border-l-4 border-primary p-4 rounded">
          <h3 className="font-semibold text-gray-800 mb-2">💡 Tip</h3>
          <p className="text-gray-600 text-sm">
            There are no right or wrong answers. Answer based on your genuine abilities and interests
            for the most accurate recommendations.
          </p>
        </div>
      </div>
    </div>
  )
}
