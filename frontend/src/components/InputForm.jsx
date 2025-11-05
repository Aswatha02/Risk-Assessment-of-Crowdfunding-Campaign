import React, { useState } from 'react'

const InputForm = ({ onSubmit, onReset, loading, hasPrediction }) => {
  const [formData, setFormData] = useState({
    name: '',
    blurb: '',
    goal: 10000,
    pledged: 0,
    backers_count: 0,
    country: 'US',
    currency: 'USD',
    category: 'Technology',
    launch_to_deadline_days: 30,
    create_to_launch_days: 1,
    staff_pick: false,
    spotlight: false
  })

  const categories = [
    'Technology', 'Games', 'Design', 'Film & Video', 'Art', 
    'Music', 'Publishing', 'Food', 'Fashion', 'Theater'
  ]

  const countries = [
    'US', 'GB', 'CA', 'AU', 'DE', 'FR', 'NL', 'IT', 'ES', 'SE'
  ]

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : 
              type === 'number' ? parseFloat(value) || 0 : value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handleReset = () => {
    setFormData({
      name: '',
      blurb: '',
      goal: 10000,
      pledged: 0,
      backers_count: 0,
      country: 'US',
      currency: 'USD',
      category: 'Technology',
      launch_to_deadline_days: 30,
      create_to_launch_days: 1,
      staff_pick: false,
      spotlight: false
    })
    onReset()
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Campaign Details</h2>
        {hasPrediction && (
          <button
            type="button"
            onClick={handleReset}
            className="text-blue-300 hover:text-blue-200 text-sm"
          >
            New Analysis
          </button>
        )}
      </div>

      {/* Project Info */}
      <div className="space-y-4">
        <div>
          <label className="block text-white/80 text-sm font-medium mb-2">
            Project Name *
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your project name"
          />
        </div>

        <div>
          <label className="block text-white/80 text-sm font-medium mb-2">
            Project Description *
          </label>
          <textarea
            name="blurb"
            value={formData.blurb}
            onChange={handleChange}
            required
            rows="3"
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Describe your project in 1-2 sentences..."
          />
        </div>
      </div>

      {/* Funding & Duration */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-white/80 text-sm font-medium mb-2">
            Funding Goal ($)
          </label>
          <input
            type="number"
            name="goal"
            value={formData.goal}
            onChange={handleChange}
            min="0"
            step="100"
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-white/80 text-sm font-medium mb-2">
            Campaign Duration (Days)
          </label>
          <input
            type="number"
            name="launch_to_deadline_days"
            value={formData.launch_to_deadline_days}
            onChange={handleChange}
            min="1"
            max="90"
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Category & Country */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-white/80 text-sm font-medium mb-2">
            Category
          </label>
          <select
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {categories.map(cat => (
              <option key={cat} value={cat} className="bg-gray-800">{cat}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-white/80 text-sm font-medium mb-2">
            Country
          </label>
          <select
            name="country"
            value={formData.country}
            onChange={handleChange}
            className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {countries.map(country => (
              <option key={country} value={country} className="bg-gray-800">{country}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Advanced Options */}
      <div className="border-t border-white/20 pt-4">
        <details className="group">
          <summary className="cursor-pointer text-white/80 font-medium hover:text-white">
            Advanced Options
          </summary>
          <div className="mt-4 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  Already Pledged ($)
                </label>
                <input
                  type="number"
                  name="pledged"
                  value={formData.pledged}
                  onChange={handleChange}
                  min="0"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">
                  Current Backers
                </label>
                <input
                  type="number"
                  name="backers_count"
                  value={formData.backers_count}
                  onChange={handleChange}
                  min="0"
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div className="flex space-x-6">
              <label className="flex items-center space-x-2 text-white/80">
                <input
                  type="checkbox"
                  name="staff_pick"
                  checked={formData.staff_pick}
                  onChange={handleChange}
                  className="rounded bg-white/10 border-white/20 text-blue-500 focus:ring-blue-500"
                />
                <span>Staff Pick</span>
              </label>

              <label className="flex items-center space-x-2 text-white/80">
                <input
                  type="checkbox"
                  name="spotlight"
                  checked={formData.spotlight}
                  onChange={handleChange}
                  className="rounded bg-white/10 border-white/20 text-blue-500 focus:ring-blue-500"
                />
                <span>Spotlight</span>
              </label>
            </div>
          </div>
        </details>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-4 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <i className="fas fa-spinner fa-spin mr-2"></i>
            Analyzing...
          </span>
        ) : (
          <span className="flex items-center justify-center">
            <i className="fas fa-chart-line mr-2"></i>
            Analyze Campaign Risk
          </span>
        )}
      </button>

      {/* Quick Tips */}
      <div className="text-xs text-white/60 space-y-1">
        <p>💡 Tip: Campaigns of 30-45 days tend to perform best</p>
        <p>💡 Tip: Goals under $20,000 have higher success rates</p>
        <p>💡 Tip: Detailed descriptions with images improve credibility</p>
      </div>
    </form>
  )
}

export default InputForm