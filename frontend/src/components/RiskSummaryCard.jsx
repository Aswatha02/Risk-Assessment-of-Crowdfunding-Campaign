import React from 'react'

const RiskSummaryCard = ({ prediction }) => {
  const { success_probability, risk_level, risk_color, model_scores } = prediction

  const getRiskColorClass = (color) => {
    switch (color) {
      case 'green': return 'risk-low'
      case 'orange': return 'risk-medium'
      case 'red': return 'risk-high'
      default: return 'risk-medium'
    }
  }

  const getRiskIcon = (level) => {
    switch (level) {
      case 'Low': return '✅'
      case 'Medium': return '⚠️'
      case 'High': return '🚨'
      default: return '❓'
    }
  }

  const getGaugeRotation = (probability) => {
    return (probability * 180) / 100
  }

  return (
    <div className="glass-effect rounded-2xl p-6 mb-6 fade-in">
      <h2 className="text-2xl font-bold text-white mb-6">Risk Assessment Summary</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
        {/* Circular Gauge */}
        <div className="flex justify-center">
          <div className="relative">
            <div className={`gauge rounded-full ${getRiskColorClass(risk_color)} p-4 shadow-lg`}>
              <div className="bg-gray-900 rounded-full p-8 text-center">
                <div className="text-4xl font-bold text-white mb-2">
                  {Math.round(success_probability * 100)}%
                </div>
                <div className={`text-sm font-semibold ${
                  risk_color === 'green' ? 'text-green-400' :
                  risk_color === 'orange' ? 'text-yellow-400' : 'text-red-400'
                }`}>
                  {getRiskIcon(risk_level)} {risk_level} Risk
                </div>
              </div>
            </div>
            
            {/* Gauge indicator */}
            <div 
              className="absolute top-0 left-1/2 w-1 h-8 bg-white rounded-full transform -translate-x-1/2"
              style={{
                transform: `translateX(-50%) rotate(${getGaugeRotation(success_probability * 100)}deg)`,
                transformOrigin: 'bottom center'
              }}
            ></div>
          </div>
        </div>

        {/* Success Probability Breakdown */}
        <div className="lg:col-span-2">
          <h3 className="text-lg font-semibold text-white mb-4">Model Consensus</h3>
          
          <div className="space-y-4">
            {Object.entries(model_scores).map(([model, score]) => (
              <div key={model} className="flex items-center justify-between">
                <span className="text-white/80 capitalize">
                  {model.replace('_', ' ')}
                </span>
                <div className="flex items-center space-x-3">
                  <div className="w-32 bg-gray-700 rounded-full h-3">
                    <div 
                      className={`h-3 rounded-full ${
                        score > 0.7 ? 'bg-green-500' :
                        score > 0.4 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${score * 100}%` }}
                    ></div>
                  </div>
                  <span className="text-white font-semibold w-12 text-right">
                    {Math.round(score * 100)}%
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-4 mt-6">
            <div className="text-center p-3 bg-white/10 rounded-lg">
              <div className="text-2xl font-bold text-white">
                {Math.round(success_probability * 100)}%
              </div>
              <div className="text-white/70 text-sm">Success Chance</div>
            </div>
            <div className="text-center p-3 bg-white/10 rounded-lg">
              <div className="text-2xl font-bold text-white">
                {risk_level}
              </div>
              <div className="text-white/70 text-sm">Risk Level</div>
            </div>
          </div>
        </div>
      </div>

      {/* Confidence Message */}
      <div className="mt-6 p-4 bg-white/10 rounded-lg border-l-4 border-blue-500">
        <div className="flex items-start">
          <i className="fas fa-lightbulb text-yellow-400 mt-1 mr-3"></i>
          <div>
            <p className="text-white font-medium">AI Insight</p>
            <p className="text-white/80 text-sm mt-1">
              {success_probability > 0.7 
                ? "This campaign shows strong potential for success based on historical data."
                : success_probability > 0.4
                ? "This campaign has moderate chances. Consider the recommendations below to improve."
                : "This campaign faces significant challenges. Review the recommendations carefully."
              }
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RiskSummaryCard