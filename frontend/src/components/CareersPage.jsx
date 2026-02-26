import { useState, useEffect } from 'react'
import { careerAPI } from '../services/api'
import { sessionUtils } from '../services/storage'

/**
 * Careers Page - Browse all careers with detailed information
 */
export default function CareersPage({ onNavigate }) {
  const [careers, setCareers] = useState([])
  const [selectedCareer, setSelectedCareer] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterCategory, setFilterCategory] = useState('all')
  const [bookmarks, setBookmarks] = useState([])

  useEffect(() => {
    const loadCareers = async () => {
      try {
        setLoading(true)
        const data = await careerAPI.getAllCareers()
        setCareers(data)
        setBookmarks(sessionUtils.getBookmarks())
      } catch (err) {
        setError('Failed to load careers. Please try again.')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    loadCareers()
  }, [])

  const handleBookmark = (careerName) => {
    if (bookmarks.includes(careerName)) {
      const updated = sessionUtils.removeBookmark(careerName)
      setBookmarks(updated)
    } else {
      const updated = sessionUtils.bookmarkCareer(careerName)
      setBookmarks(updated)
    }
  }

  // Filter careers
  const filteredCareers = careers.filter(career => {
    const matchesSearch = career.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      career.description.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesSearch
  })

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading careers...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Explore Careers</h1>
          <p className="text-gray-600 text-lg">Discover detailed information about different career paths</p>
        </div>

        {/* Search and Filter */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              placeholder="Search careers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-primary"
            />
            <button
              onClick={() => setSearchTerm('')}
              className="px-4 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition"
            >
              Clear
            </button>
          </div>

          <div className="text-sm text-gray-600">
            Found {filteredCareers.length} career{filteredCareers.length !== 1 ? 's' : ''}
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-8">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Career List */}
          <div className="lg:col-span-1 space-y-4">
            <div className="bg-white rounded-lg shadow h-fit max-h-96 overflow-y-auto">
              {filteredCareers.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  No careers found matching "{searchTerm}"
                </div>
              ) : (
                filteredCareers.map((career) => (
                  <button
                    key={career.id}
                    onClick={() => setSelectedCareer(career)}
                    className={`w-full text-left p-4 border-b border-gray-200 hover:bg-blue-50 transition ${
                      selectedCareer?.id === career.id ? 'bg-primary/10 border-l-4 border-l-primary' : ''
                    }`}
                  >
                    <h3 className="font-semibold text-gray-800">{career.name}</h3>
                    <p className="text-xs text-gray-600 mt-1 line-clamp-2">{career.description}</p>
                  </button>
                ))
              )}
            </div>
          </div>

          {/* Career Details */}
          <div className="lg:col-span-2">
            {selectedCareer ? (
              <div className="bg-white rounded-lg shadow-lg p-8">
                {/* Career Header */}
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h2 className="text-3xl font-bold text-gray-800 mb-2">{selectedCareer.name}</h2>
                    {selectedCareer.average_salary_range && (
                      <p className="text-lg text-primary font-semibold">{selectedCareer.average_salary_range}</p>
                    )}
                  </div>
                  <button
                    onClick={() => handleBookmark(selectedCareer.name)}
                    className={`text-4xl transition ${
                      bookmarks.includes(selectedCareer.name) ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-400'
                    }`}
                  >
                    ⭐
                  </button>
                </div>

                {/* Description */}
                <p className="text-gray-700 mb-6 leading-relaxed">{selectedCareer.description}</p>

                {/* Key Information */}
                <div className="grid grid-cols-2 gap-6 mb-8">
                  {selectedCareer.average_salary_range && (
                    <div className="bg-green-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 font-semibold">Average Salary</p>
                      <p className="text-lg font-bold text-green-600">{selectedCareer.average_salary_range}</p>
                    </div>
                  )}

                  {selectedCareer.job_growth && (
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 font-semibold">Job Growth</p>
                      <p className="text-lg font-bold text-blue-600">{selectedCareer.job_growth}</p>
                    </div>
                  )}

                  {selectedCareer.required_education && (
                    <div className="bg-purple-50 p-4 rounded-lg col-span-2">
                      <p className="text-sm text-gray-600 font-semibold">Required Education</p>
                      <p className="text-gray-700">{selectedCareer.required_education}</p>
                    </div>
                  )}
                </div>

                {/* Required Skills */}
                {selectedCareer.required_skills && selectedCareer.required_skills.length > 0 && (
                  <div className="mb-8">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Required Skills</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedCareer.required_skills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-semibold"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Suitable For */}
                {selectedCareer.suitable_for && (
                  <div className="mb-8 bg-blue-50 p-4 rounded-lg">
                    <h3 className="font-bold text-gray-800 mb-2">Suitable For</h3>
                    <p className="text-gray-700">{selectedCareer.suitable_for}</p>
                  </div>
                )}

                {/* Typical Companies */}
                {selectedCareer.typical_companies && selectedCareer.typical_companies.length > 0 && (
                  <div className="mb-8">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Typical Employers</h3>
                    <div className="grid grid-cols-2 gap-3">
                      {selectedCareer.typical_companies.map((company, idx) => (
                        <div key={idx} className="bg-gray-100 p-3 rounded">
                          <p className="text-gray-800 font-semibold">{company}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Courses */}
                {selectedCareer.courses && selectedCareer.courses.length > 0 && (
                  <div className="mb-8">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Recommended Courses</h3>
                    <div className="space-y-3">
                      {selectedCareer.courses.slice(0, 3).map((course, idx) => (
                        <div key={idx} className="border rounded-lg p-4 hover:shadow-md transition">
                          <h4 className="font-semibold text-gray-800">{course.name}</h4>
                          <p className="text-sm text-gray-600"><strong>Provider:</strong> {course.provider}</p>
                          {course.duration && (
                            <p className="text-sm text-gray-600"><strong>Duration:</strong> {course.duration}</p>
                          )}
                          {course.url && (
                            <a
                              href={course.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary hover:underline text-sm mt-2 inline-block"
                            >
                              Visit Course →
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Universities */}
                {selectedCareer.universities && selectedCareer.universities.length > 0 && (
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 mb-4">Recommended Universities</h3>
                    <div className="space-y-3">
                      {selectedCareer.universities.slice(0, 3).map((uni, idx) => (
                        <div key={idx} className="border rounded-lg p-4 hover:shadow-md transition">
                          <h4 className="font-semibold text-gray-800">{uni.name}</h4>
                          <p className="text-sm text-gray-600"><strong>Location:</strong> {uni.location}</p>
                          <p className="text-sm text-gray-600"><strong>Program:</strong> {uni.program_name}</p>
                          {uni.ranking && (
                            <p className="text-sm text-gray-600"><strong>Ranking:</strong> #{uni.ranking}</p>
                          )}
                          {uni.url && (
                            <a
                              href={uni.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-primary hover:underline text-sm mt-2 inline-block"
                            >
                              Visit University →
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <p className="text-gray-600 text-lg">Select a career from the list to view detailed information</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
