import React, { useState } from 'react'
import InputForm from './components/InputForm'
import ResultsDashboard from './components/ResultsDashboard'
import './index.css'

function App() {
  const [prediction, setPrediction] = useState(null)
  const [campaignData, setCampaignData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyzeCampaign = async (inputData) => {
    setLoading(true)
    setError(null)
    
    try {
      const API_URL = 'http://localhost:8001'
      
      console.log('📤 Sending to backend server...', inputData)

      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData),
      })

      console.log('📥 Response status:', response.status)

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`)
      }

      const result = await response.json()
      console.log('✅ Prediction result:', result)
      setPrediction(result)
      setCampaignData(inputData)
      
    } catch (err) {
      console.error('❌ API call failed:', err)
      setError(`Failed to get prediction: ${err.message}. Make sure the backend is running on port 8000.`)
    } finally {
      setLoading(false)
    }
  }

  const resetAnalysis = () => {
    setPrediction(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-32 w-80 h-80 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
        <div className="absolute -bottom-40 -left-32 w-80 h-80 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute top-40 left-1/2 w-80 h-80 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
        {/* Enhanced Header */}
        <div className="text-center mb-12 fade-in">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-white/20 rounded-2xl backdrop-blur-lg border border-white/30 mb-6 shadow-glow">
            <i className="fas fa-rocket text-white text-3xl"></i>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 text-glow">
            CrowdRisk <span className="text-yellow-300">Analyzer</span>
          </h1>
          <p className="text-xl text-white/90 mb-6 max-w-2xl mx-auto leading-relaxed">
            AI-Powered Crowdfunding Success Prediction & Risk Assessment Platform
          </p>
          <div className="flex flex-wrap justify-center gap-3 mb-8">
            <span className="px-4 py-2 bg-white/20 backdrop-blur-lg rounded-full text-white text-sm border border-white/30">
              🚀 Machine Learning
            </span>
            <span className="px-4 py-2 bg-white/20 backdrop-blur-lg rounded-full text-white text-sm border border-white/30">
              📊 Real-time Analysis
            </span>
            <span className="px-4 py-2 bg-white/20 backdrop-blur-lg rounded-full text-white text-sm border border-white/30">
              💡 Smart Recommendations
            </span>
            <span className="px-4 py-2 bg-white/20 backdrop-blur-lg rounded-full text-white text-sm border border-white/30">
              🔮 Success Prediction
            </span>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          {/* Input Form - Left Side */}
          <div className="lg:col-span-1">
            <div className="glass-card p-8 hover-lift">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center mr-4 shadow-lg">
                  <i className="fas fa-edit text-white text-lg"></i>
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">Campaign Details</h2>
                  <p className="text-gray-600">Enter your project information</p>
                </div>
              </div>
              <InputForm 
                onSubmit={analyzeCampaign}
                onReset={resetAnalysis}
                loading={loading}
                hasPrediction={!!prediction}
              />
            </div>

            {/* Stats Card */}
            {!prediction && !loading && (
              <div className="glass-card p-6 mt-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <i className="fas fa-chart-bar text-purple-500 mr-2"></i>
                  Campaign Insights
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span className="text-gray-700">Optimal Duration</span>
                    <span className="font-semibold text-blue-600">30-45 days</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                    <span className="text-gray-700">Best Categories</span>
                    <span className="font-semibold text-green-600">Tech & Games</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                    <span className="text-gray-700">Top Countries</span>
                    <span className="font-semibold text-purple-600">US & UK</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Results Dashboard - Right Side */}
          <div className="lg:col-span-2">
            {loading && (
              <div className="glass-card p-12 text-center">
                <div className="loading-spinner mx-auto mb-6"></div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3">Analyzing Your Campaign</h3>
                <p className="text-gray-600 text-lg mb-4">Our AI models are evaluating your campaign data...</p>
                <div className="flex justify-center space-x-2">
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            )}

            {error && (
              <div className="glass-card p-8 border-l-4 border-red-500">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center mr-4">
                    <i className="fas fa-exclamation-triangle text-red-500 text-xl"></i>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-800">Connection Error</h3>
                    <p className="text-gray-600">{error}</p>
                  </div>
                </div>
                <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                  <p className="text-sm text-yellow-800 font-medium mb-2">To fix this:</p>
                  <ol className="text-sm text-yellow-700 space-y-1 list-decimal list-inside">
                    <li>Open a new terminal window</li>
                    <li>Navigate to: <code className="bg-gray-100 px-2 py-1 rounded text-xs">backend/app</code></li>
                    <li>Run: <code className="bg-gray-100 px-2 py-1 rounded text-xs">python simple_server.py</code></li>
                    <li>Wait for the server to start completely</li>
                    <li>Refresh this page and try again</li>
                  </ol>
                </div>
                <button
                  onClick={resetAnalysis}
                  className="btn-primary w-full mt-6"
                >
                  <i className="fas fa-redo mr-2"></i>
                  Try Again
                </button>
              </div>
            )}

            {prediction && !loading && (
              <ResultsDashboard prediction={prediction} campaignData={campaignData} />
            )}

            {!prediction && !loading && !error && (
              <div className="glass-card p-12 text-center">
                <div className="w-24 h-24 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <i className="fas fa-chart-line text-white text-3xl"></i>
                </div>
                <h3 className="text-3xl font-bold text-gray-800 mb-4">Ready to Analyze Your Campaign</h3>
                <p className="text-gray-600 text-lg mb-8 max-w-md mx-auto leading-relaxed">
                  Fill out the form to get instant AI-powered risk assessment, feature importance analysis, and actionable recommendations for your crowdfunding campaign.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
                  <div className="feature-card text-center">
                    <i className="fas fa-brain text-purple-500 text-2xl mb-3"></i>
                    <h4 className="font-semibold text-gray-800 mb-2">AI-Powered</h4>
                    <p className="text-sm text-gray-600">Machine learning predictions</p>
                  </div>
                  <div className="feature-card text-center">
                    <i className="fas fa-bolt text-yellow-500 text-2xl mb-3"></i>
                    <h4 className="font-semibold text-gray-800 mb-2">Real-time</h4>
                    <p className="text-sm text-gray-600">Instant risk assessment</p>
                  </div>
                  <div className="feature-card text-center">
                    <i className="fas fa-chart-pie text-green-500 text-2xl mb-3"></i>
                    <h4 className="font-semibold text-gray-800 mb-2">Detailed Insights</h4>
                    <p className="text-sm text-gray-600">Comprehensive analysis</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center pt-8 border-t border-white/20">
          <p className="text-white/80 mb-2">
            Powered by Machine Learning • Built with FastAPI & React
          </p>
          <p className="text-white/60 text-sm">
            All models implemented from scratch • No external AI APIs used
          </p>
        </div>
      </div>
    </div>
  )
}

export default App