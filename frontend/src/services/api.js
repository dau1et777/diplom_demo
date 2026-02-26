/**
 * API Communication Service
 * Handles all HTTP requests to Django backend
 */

import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Quiz APIs
export const quizAPI = {
  getQuestions: async () => {
    try {
      const response = await api.get('/quiz/questions/')
      return response.data.results || []
    } catch (error) {
      console.error('Error fetching quiz questions:', error)
      throw error
    }
  },

  submitQuiz: async (sessionId, answers) => {
    try {
      const response = await api.post('/quiz/submit/', {
        session_id: sessionId,
        answers: answers,
      })
      return response.data
    } catch (error) {
      console.error('Error submitting quiz:', error)
      throw error
    }
  },

  getSubmission: async (sessionId) => {
    try {
      const response = await api.get(`/quiz/submission/${sessionId}/`)
      return response.data
    } catch (error) {
      console.error('Error fetching submission:', error)
      throw error
    }
  },
}

// Career APIs
export const careerAPI = {
  getAllCareers: async () => {
    try {
      const response = await api.get('/careers/')
      return response.data.results || []
    } catch (error) {
      console.error('Error fetching careers:', error)
      throw error
    }
  },

  getCareerDetails: async (careerId) => {
    try {
      const response = await api.get(`/careers/${careerId}/`)
      return response.data
    } catch (error) {
      console.error('Error fetching career details:', error)
      throw error
    }
  },

  getCourses: async () => {
    try {
      const response = await api.get('/courses/')
      return response.data.results || []
    } catch (error) {
      console.error('Error fetching courses:', error)
      throw error
    }
  },

  getUniversities: async () => {
    try {
      const response = await api.get('/universities/')
      return response.data.results || []
    } catch (error) {
      console.error('Error fetching universities:', error)
      throw error
    }
  },
}

// Results and Recommendations APIs
export const resultsAPI = {
  generateRecommendations: async (sessionId, topN = 5) => {
    try {
      const response = await api.post('/results/recommend/', {
        session_id: sessionId,
        top_n: topN,
      })
      return response.data
    } catch (error) {
      console.error('Error generating recommendations:', error)
      throw error
    }
  },

  getRecommendations: async (sessionId) => {
    try {
      const response = await api.get(`/results/${sessionId}/`)
      return response.data
    } catch (error) {
      console.error('Error fetching recommendations:', error)
      throw error
    }
  },

  saveCareer: async (sessionId, careerId) => {
    try {
      const response = await api.post('/results/save-career/', {
        session_id: sessionId,
        career_id: careerId,
      })
      return response.data
    } catch (error) {
      console.error('Error saving career:', error)
      throw error
    }
  },

  viewCareer: async (sessionId, careerId) => {
    try {
      const response = await api.post('/results/view-career/', {
        session_id: sessionId,
        career_id: careerId,
      })
      return response.data
    } catch (error) {
      console.error('Error tracking career view:', error)
      throw error
    }
  },
}

export default api
