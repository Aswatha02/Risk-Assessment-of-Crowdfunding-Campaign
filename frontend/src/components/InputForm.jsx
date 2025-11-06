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
    spotlight: false,
    // NEW: Creator profile
    creator_has_avatar: false,
    creator_backed_projects: 0,
    creator_created_projects: 0,
    creator_has_bio: false,
    // NEW: Media quality
    has_video: false,
    number_of_images: 0,
    media_quality: 'medium',
    // NEW: Reward structure
    reward_tiers: 3,
    lowest_reward_price: 10,
    has_early_bird: false,
    // NEW: Launch planning
    preparation_days: 7,
    has_external_website: false,
    social_media_followers: 0
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

      {/* Creator Profile Section - HIGH IMPACT */}
      <div className="border-t border-white/20 pt-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <span className="bg-green-500 text-white text-xs px-2 py-1 rounded mr-2">HIGH IMPACT</span>
          👤 Creator Profile
        </h3>
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Projects You've Backed
              </label>
              <input
                type="number"
                name="creator_backed_projects"
                value={formData.creator_backed_projects}
                onChange={handleChange}
                min="0"
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0"
              />
            </div>
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Projects You've Created
              </label>
              <input
                type="number"
                name="creator_created_projects"
                value={formData.creator_created_projects}
                onChange={handleChange}
                min="0"
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0"
              />
            </div>
          </div>
          <div className="flex flex-wrap gap-4">
            <label className="flex items-center space-x-2 text-white/80">
              <input
                type="checkbox"
                name="creator_has_avatar"
                checked={formData.creator_has_avatar}
                onChange={handleChange}
                className="rounded bg-white/10 border-white/20 text-blue-500 focus:ring-blue-500"
              />
              <span>I have a profile photo</span>
            </label>
            <label className="flex items-center space-x-2 text-white/80">
              <input
                type="checkbox"
                name="creator_has_bio"
                checked={formData.creator_has_bio}
                onChange={handleChange}
                className="rounded bg-white/10 border-white/20 text-blue-500 focus:ring-blue-500"
              />
              <span>I have a detailed bio</span>
            </label>
          </div>
        </div>
      </div>

      {/* Media Quality Section - HIGH IMPACT */}
      <div className="border-t border-white/20 pt-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <span className="bg-green-500 text-white text-xs px-2 py-1 rounded mr-2">HIGH IMPACT</span>
          🎥 Campaign Media
        </h3>
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Number of Images
              </label>
              <input
                type="number"
                name="number_of_images"
                value={formData.number_of_images}
                onChange={handleChange}
                min="0"
                max="20"
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="0-20"
              />
            </div>
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Media Quality
              </label>
              <select
                name="media_quality"
                value={formData.media_quality}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="low" className="bg-gray-800">Basic Quality</option>
                <option value="medium" className="bg-gray-800">Good Quality</option>
                <option value="high" className="bg-gray-800">Professional Quality</option>
              </select>
            </div>
          </div>
          <label className="flex items-center space-x-2 text-white/80">
            <input
              type="checkbox"
              name="has_video"
              checked={formData.has_video}
              onChange={handleChange}
              className="rounded bg-white/10 border-white/20 text-blue-500 focus:ring-blue-500"
            />
            <span>Campaign has video (+85% success rate!)</span>
          </label>
        </div>
      </div>

      {/* Reward Structure Section - MEDIUM IMPACT */}
      <div className="border-t border-white/20 pt-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <span className="bg-yellow-500 text-white text-xs px-2 py-1 rounded mr-2">MEDIUM IMPACT</span>
          🎁 Reward Structure
        </h3>
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Number of Reward Tiers
              </label>
              <input
                type="number"
                name="reward_tiers"
                value={formData.reward_tiers}
                onChange={handleChange}
                min="1"
                max="15"
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="3-8 optimal"
              />
            </div>
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Lowest Reward Price ($)
              </label>
              <input
                type="number"
                name="lowest_reward_price"
                value={formData.lowest_reward_price}
                onChange={handleChange}
                min="1"
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="$5-$25"
              />
            </div>
          </div>
          <label className="flex items-center space-x-2 text-white/80">
            <input
              type="checkbox"
              name="has_early_bird"
              checked={formData.has_early_bird}
              onChange={handleChange}
              className="rounded bg-white/10 border-white/20 text-blue-500 focus:ring-blue-500"
            />
            <span>Has early bird rewards</span>
          </label>
        </div>
      </div>

      {/* Launch Planning Section - MEDIUM IMPACT */}
      <div className="border-t border-white/20 pt-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
          <span className="bg-yellow-500 text-white text-xs px-2 py-1 rounded mr-2">MEDIUM IMPACT</span>
          🚀 Launch Planning
        </h3>
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Preparation Days
              </label>
              <input
                type="number"
                name="preparation_days"
                value={formData.preparation_days}
                onChange={handleChange}
                min="0"
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="14+ recommended"
              />
            </div>
            <div>
              <label className="block text-white/80 text-sm font-medium mb-2">
                Social Media Followers
              </label>
              <input
                type="number"
                name="social_media_followers"
                value={formData.social_media_followers}
                onChange={handleChange}
                min="0"
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Total across platforms"
              />
            </div>
          </div>
          <label className="flex items-center space-x-2 text-white/80">
            <input
              type="checkbox"
              name="has_external_website"
              checked={formData.has_external_website}
              onChange={handleChange}
              className="rounded bg-white/10 border-white/20 text-blue-500 focus:ring-blue-500"
            />
            <span>Has external website</span>
          </label>
        </div>
      </div>

      {/* Advanced Options */}
      <div className="border-t border-white/20 pt-4">
        <details className="group">
          <summary className="cursor-pointer text-white/80 font-medium hover:text-white">
            Additional Options
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