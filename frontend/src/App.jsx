import { useState } from 'react'
import Header from './components/Header'
import HomePage from './components/HomePage'
import QuizPage from './components/QuizPage'
import ResultsPage from './components/ResultsPage'
import CareersPage from './components/CareersPage'
import SignIn from './components/SignIn'
import SignUp from './components/SignUp'
import UserProfile from './components/UserProfile'
import ProfileComparison from './components/ProfileComparison'

/**
 * Main App Component
 * Manages page navigation and overall layout
 */
function App() {
  const [currentPage, setCurrentPage] = useState('home')

  const navigateTo = (page) => {
    setCurrentPage(page)
    window.scrollTo(0, 0)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header currentPage={currentPage} onNavigate={navigateTo} />
      
      <main>
        {currentPage === 'home' && <HomePage onNavigate={navigateTo} />}
        {currentPage === 'quiz' && <QuizPage onNavigate={navigateTo} />}
        {currentPage === 'results' && <ResultsPage onNavigate={navigateTo} />}
        {currentPage === 'careers' && <CareersPage onNavigate={navigateTo} />}
        {currentPage === 'signin' && <SignIn onNavigate={navigateTo} />}
        {currentPage === 'signup' && <SignUp onNavigate={navigateTo} />}
        {currentPage === 'profile' && <UserProfile onNavigate={navigateTo} />}
        {currentPage === 'comparison' && <ProfileComparison onNavigate={navigateTo} />}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-8 mt-12">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p>&copy; 2026 CareerPath AI. Web-Integrated Career Recommendation System.</p>
          <p className="text-sm mt-2">Built with React, Django, and Machine Learning</p>
        </div>
      </footer>
    </div>
  )
}

export default App
