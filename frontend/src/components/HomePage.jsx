/**
 * Home / Landing Page Component
 */
export default function HomePage({ onNavigate }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary via-purple-400 to-pink-300">
      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-4 py-20 text-center text-white">
        <h1 className="text-5xl font-bold mb-6">
          Discover Your Perfect Career Path
        </h1>
        <p className="text-xl mb-8 opacity-90">
          Using AI and machine learning to match your skills and interests with ideal careers
        </p>
        
        <button
          onClick={() => onNavigate('quiz')}
          className="bg-white text-primary px-8 py-4 rounded-lg font-bold text-lg hover:shadow-lg transition transform hover:scale-105"
        >
          Start Your Career Assessment
        </button>
      </section>

      {/* Features Section */}
      <section className="bg-white py-16">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">How It Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-8 rounded-lg">
              <div className="bg-primary text-white rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl mb-4">
                1
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-800">Take the Quiz</h3>
              <p className="text-gray-600">
                Answer 19 carefully designed questions about your abilities, interests, and preferences
              </p>
            </div>

            {/* Step 2 */}
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-8 rounded-lg">
              <div className="bg-secondary text-white rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl mb-4">
                2
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-800">ML Analysis</h3>
              <p className="text-gray-600">
                Our Random Forest ML model analyzes your answers and compares with 80+ career profiles
              </p>
            </div>

            {/* Step 3 */}
            <div className="bg-gradient-to-br from-pink-50 to-pink-100 p-8 rounded-lg">
              <div className="bg-accent text-white rounded-full w-12 h-12 flex items-center justify-center font-bold text-xl mb-4">
                3
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-800">Get Results</h3>
              <p className="text-gray-600">
                Receive personalized career recommendations with compatibility scores and resources
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Key Features</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex gap-4">
            <div className="text-primary text-3xl">✓</div>
            <div>
              <h3 className="font-bold text-lg text-gray-800">AI-Powered Recommendations</h3>
              <p className="text-gray-600">RandomForest classifier trained on 80+ career profiles</p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="text-primary text-3xl">✓</div>
            <div>
              <h3 className="font-bold text-lg text-gray-800">Detailed Explanations</h3>
              <p className="text-gray-600">Understand why each career matches your profile</p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="text-primary text-3xl">✓</div>
            <div>
              <h3 className="font-bold text-lg text-gray-800">Learning Resources</h3>
              <p className="text-gray-600">Courses and universities recommended for each career</p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="text-primary text-3xl">✓</div>
            <div>
              <h3 className="font-bold text-lg text-gray-800">Performance Analytics</h3>
              <p className="text-gray-600">Visualize your abilities and compatibility scores</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-white py-16 mt-8">
        <div className="max-w-2xl mx-auto text-center px-4">
          <h2 className="text-3xl font-bold mb-4">Ready to Find Your Career?</h2>
          <p className="mb-6 text-lg opacity-90">
            Take just 5 minutes to discover careers that match your unique profile.
            No account required!
          </p>
          <button
            onClick={() => onNavigate('quiz')}
            className="bg-white text-primary px-8 py-3 rounded-lg font-bold hover:shadow-lg transition"
          >
            Start Now →
          </button>
        </div>
      </section>
    </div>
  )
}
