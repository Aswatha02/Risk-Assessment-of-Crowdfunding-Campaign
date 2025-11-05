import React, { useState, useEffect } from 'react'

const ComparisonCharts = ({ prediction, onNewAnalysis }) => {
  const [scenarios, setScenarios] = useState([
    { 
      label: 'Current', 
      goal: 10000, 
      duration: 30, 
      probability: prediction.success_probability,
      staff_pick: false,
      country: 'US',
      icon: '🎯'
    },
    {
      label: 'Optimized',
      goal: 3000,
      duration: 35,
      probability: Math.min(prediction.success_probability + 0.3, 0.95),
      staff_pick: true,
      country: 'US',
      icon: '🚀'
    },
    { 
      label: 'Aggressive', 
      goal: 20000, 
      duration: 60, 
      probability: Math.max(prediction.success_probability - 0.15, 0.1),
      staff_pick: false,
      country: 'FR',
      icon: '⚡'
    }
  ])

  const [sliderValues, setSliderValues] = useState({
    goal: 10000,
    duration: 30,
    staff_pick: false,
    country: 'US'
  })

  // Update probabilities when sliders change
  useEffect(() => {
    const calculateScenarioProbability = (scenario) => {
      let goal, duration, staff_pick, country;

      if (scenario.label === 'Current') {
        goal = sliderValues.goal;
        duration = sliderValues.duration;
        staff_pick = sliderValues.staff_pick;
        country = sliderValues.country;
      } else if (scenario.label === 'Optimized') {
        // Dynamic optimization based on current settings
        goal = Math.min(sliderValues.goal * 0.7, 5000); // Reduce goal by 30% or max $5K
        duration = 35; // Optimal duration
        staff_pick = true; // Always recommend staff pick
        country = 'US'; // Best performing country
      } else {
        // Aggressive scenario - fixed
        goal = scenario.goal;
        duration = scenario.duration;
        staff_pick = scenario.staff_pick;
        country = scenario.country;
      }

      // Smart probability calculation
      const goalFactor = Math.max(0.1, 1.0 - Math.min(goal / 50000, 1.0))
      const durationFactor = (30 <= duration && duration <= 45) ? 1.0 : 0.7
      const countryFactor = (country === 'US' || country === 'GB') ? 1.2 : 1.0
      const staffFactor = staff_pick ? 1.3 : 1.0

      const baseProb = 0.35
      let probability = baseProb * goalFactor * durationFactor * countryFactor * staffFactor

      // Add some variation for different scenarios
      if (scenario.label === 'Optimized') {
        probability *= 1.3 // Extra boost for optimized strategy
      } else if (scenario.label === 'Aggressive') {
        probability *= 0.8
      }

      return Math.max(0.05, Math.min(0.95, probability))
    }

    const updatedScenarios = scenarios.map(scenario => {
      const probability = calculateScenarioProbability(scenario)
      return {
        ...scenario,
        probability,
        // Update optimized scenario parameters dynamically
        ...(scenario.label === 'Optimized' && {
          goal: Math.min(sliderValues.goal * 0.7, 5000),
          duration: 35,
          staff_pick: true,
          country: 'US'
        })
      }
    })

    setScenarios(updatedScenarios)
  }, [sliderValues])

  const handleSliderChange = (type, value) => {
    setSliderValues(prev => ({
      ...prev,
      [type]: type === 'staff_pick' ? !prev.staff_pick : parseInt(value)
    }))
  }

  const handleCountryChange = (country) => {
    setSliderValues(prev => ({
      ...prev,
      country
    }))
  }

  const getRiskColor = (probability) => {
    if (probability > 0.7) return 'text-green-600'
    if (probability > 0.4) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getRiskBgColor = (probability) => {
    if (probability > 0.7) return 'bg-green-100 border-green-200'
    if (probability > 0.4) return 'bg-yellow-100 border-yellow-200'
    return 'bg-red-100 border-red-200'
  }

  const getRiskLevel = (probability) => {
    if (probability > 0.7) return 'Low Risk'
    if (probability > 0.4) return 'Medium Risk'
    return 'High Risk'
  }

  const getScenarioColor = (index) => {
    const colors = [
      'from-blue-500 to-blue-600',
      'from-green-500 to-green-600', 
      'from-purple-500 to-purple-600'
    ]
    return colors[index] || colors[0]
  }

  const getScenarioBorder = (index) => {
    const borders = [
      'border-blue-200',
      'border-green-200',
      'border-purple-200'
    ]
    return borders[index] || borders[0]
  }

  return (
    <div className="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 fade-in">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-3">Scenario Comparison</h2>
        <p className="text-gray-600 text-lg">Explore how different strategies affect your campaign success</p>
      </div>
      
      {/* Interactive Controls Card */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 mb-8 border border-blue-100 shadow-sm">
        <div className="flex items-center mb-6">
          <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
            <i className="fas fa-sliders-h text-white text-lg"></i>
          </div>
          <div>
            <h3 className="text-xl font-semibold text-gray-800">Adjust Your Scenario</h3>
            <p className="text-gray-600">Modify parameters to see real-time impact</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Sliders */}
          <div className="space-y-6">
            {/* Goal Slider */}
            <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <label className="text-gray-800 font-semibold flex items-center">
                  <i className="fas fa-bullseye text-blue-500 mr-2"></i>
                  Funding Goal
                </label>
                <span className="text-2xl font-bold text-blue-600">${sliderValues.goal.toLocaleString()}</span>
              </div>
              <input
                type="range"
                min="1000"
                max="50000"
                step="1000"
                value={sliderValues.goal}
                onChange={(e) => handleSliderChange('goal', e.target.value)}
                className="w-full h-3 bg-gradient-to-r from-blue-200 to-blue-400 rounded-lg appearance-none cursor-pointer slider-thumb"
              />
              <div className="flex justify-between text-sm text-gray-500 mt-3">
                <span className="bg-blue-100 px-2 py-1 rounded">$1K</span>
                <span className="bg-blue-100 px-2 py-1 rounded">$25K</span>
                <span className="bg-blue-100 px-2 py-1 rounded">$50K</span>
              </div>
            </div>

            {/* Duration Slider */}
            <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <label className="text-gray-800 font-semibold flex items-center">
                  <i className="fas fa-calendar-alt text-green-500 mr-2"></i>
                  Campaign Duration
                </label>
                <span className="text-2xl font-bold text-green-600">{sliderValues.duration} days</span>
              </div>
              <input
                type="range"
                min="7"
                max="90"
                step="1"
                value={sliderValues.duration}
                onChange={(e) => handleSliderChange('duration', e.target.value)}
                className="w-full h-3 bg-gradient-to-r from-green-200 to-green-400 rounded-lg appearance-none cursor-pointer slider-thumb"
              />
              <div className="flex justify-between text-sm text-gray-500 mt-3">
                <span className="bg-green-100 px-2 py-1 rounded">7 days</span>
                <span className="bg-green-100 px-2 py-1 rounded">45 days</span>
                <span className="bg-green-100 px-2 py-1 rounded">90 days</span>
              </div>
            </div>
          </div>

          {/* Right Column - Toggles */}
          <div className="space-y-6">
            {/* Country Selector */}
            <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
              <label className="text-gray-800 font-semibold flex items-center mb-4">
                <i className="fas fa-globe-americas text-purple-500 mr-2"></i>
                Country
              </label>
              <select
                value={sliderValues.country}
                onChange={(e) => handleCountryChange(e.target.value)}
                className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-xl text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              >
                <option value="US">🇺🇸 United States</option>
                <option value="GB">🇬🇧 United Kingdom</option>
                <option value="CA">🇨🇦 Canada</option>
                <option value="AU">🇦🇺 Australia</option>
                <option value="DE">🇩🇪 Germany</option>
                <option value="FR">🇫🇷 France</option>
              </select>
            </div>

            {/* Staff Pick Toggle */}
            <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-gray-800 font-semibold flex items-center">
                    <i className="fas fa-star text-yellow-500 mr-2"></i>
                    Staff Pick
                  </label>
                  <p className="text-sm text-gray-600 mt-1">Get featured on the platform</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={sliderValues.staff_pick}
                    onChange={() => handleSliderChange('staff_pick')}
                    className="sr-only peer"
                  />
                  <div className="w-14 h-7 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-yellow-500"></div>
                </label>
              </div>
              {sliderValues.staff_pick && (
                <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-sm text-yellow-800 flex items-center">
                    <i className="fas fa-bolt mr-2"></i>
                    <strong>+30% success boost!</strong> Staff picks get more visibility
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Scenario Comparison Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {scenarios.map((scenario, index) => (
          <div 
            key={index}
            className={`bg-gradient-to-br from-white to-gray-50 rounded-2xl p-6 border-2 ${getScenarioBorder(index)} shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105`}
          >
            {/* Header */}
            <div className="text-center mb-4">
              <div className="text-3xl mb-2">{scenario.icon}</div>
              <h3 className={`text-xl font-bold bg-gradient-to-r ${getScenarioColor(index)} bg-clip-text text-transparent`}>
                {scenario.label}
              </h3>
            </div>

            {/* Stats */}
            <div className="space-y-3 mb-4">
              <div className="flex justify-between items-center p-3 bg-white rounded-lg border border-gray-200">
                <span className="text-gray-600 flex items-center">
                  <i className="fas fa-bullseye text-blue-500 mr-2"></i>
                  Goal
                </span>
                <span className="font-semibold text-gray-800">${scenario.goal.toLocaleString()}</span>
              </div>
              
              <div className="flex justify-between items-center p-3 bg-white rounded-lg border border-gray-200">
                <span className="text-gray-600 flex items-center">
                  <i className="fas fa-calendar text-green-500 mr-2"></i>
                  Duration
                </span>
                <span className="font-semibold text-gray-800">{scenario.duration} days</span>
              </div>
              
              <div className="flex justify-between items-center p-3 bg-white rounded-lg border border-gray-200">
                <span className="text-gray-600 flex items-center">
                  <i className="fas fa-star text-yellow-500 mr-2"></i>
                  Staff Pick
                </span>
                <span className={`font-semibold ${scenario.staff_pick ? 'text-green-600' : 'text-gray-600'}`}>
                  {scenario.staff_pick ? 'Yes' : 'No'}
                </span>
              </div>
            </div>

            {/* Success Probability */}
            <div className={`p-4 rounded-xl border-2 ${getRiskBgColor(scenario.probability)} text-center`}>
              <div className="text-sm text-gray-600 mb-1">Success Probability</div>
              <div className={`text-3xl font-bold ${getRiskColor(scenario.probability)} mb-1`}>
                {Math.round(scenario.probability * 100)}%
              </div>
              <div className={`text-sm font-semibold ${getRiskColor(scenario.probability)}`}>
                {getRiskLevel(scenario.probability)}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Improvement Analysis */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-6 border border-indigo-100 mb-8">
        <div className="flex items-center mb-4">
          <div className="w-8 h-8 bg-indigo-500 rounded-lg flex items-center justify-center mr-3">
            <i className="fas fa-chart-line text-white"></i>
          </div>
          <h3 className="text-xl font-semibold text-gray-800">Improvement Analysis</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scenarios.slice(1).map((scenario, index) => {
            const improvement = scenario.probability - scenarios[0].probability
            const improvementPercent = Math.round(improvement * 100)
            
            return (
              <div key={index} className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-gray-800">{scenario.label} Strategy</div>
                    <div className="text-sm text-gray-600 mt-1">
                      {scenario.goal.toLocaleString()} • {scenario.duration}d • {scenario.staff_pick ? 'Staff Pick' : 'No Staff Pick'}
                    </div>
                  </div>
                  <div className={`text-lg font-bold ${improvement > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {improvement > 0 ? '+' : ''}{improvementPercent}%
                  </div>
                </div>
                <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${improvement > 0 ? 'bg-green-500' : 'bg-red-500'} transition-all duration-500`}
                    style={{ width: `${Math.abs(improvementPercent)}%` }}
                  ></div>
                </div>
                <div className="text-sm text-gray-600 mt-2">
                  {improvement > 0 ? 'Better' : 'Worse'} than current scenario
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4">
        <button
          onClick={() => onNewAnalysis()}
          className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center justify-center"
        >
          <i className="fas fa-rocket mr-3 text-lg"></i>
          Apply Best Strategy
        </button>
        
        <button
          onClick={() => {
            setSliderValues({
              goal: 10000,
              duration: 30,
              staff_pick: false,
              country: 'US'
            })
          }}
          className="flex-1 bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white font-semibold py-4 px-8 rounded-xl transition-all duration-300 flex items-center justify-center"
        >
          <i className="fas fa-redo mr-3 text-lg"></i>
          Reset All Controls
        </button>
      </div>
    </div>
  )
}

export default ComparisonCharts