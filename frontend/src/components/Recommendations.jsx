import React from 'react'

const Recommendations = ({ prediction }) => {
  const { recommendations, success_probability } = prediction

  const getPriorityIcon = (index) => {
    if (index === 0) return '🚀'
    if (index === 1) return '⭐'
    if (index === 2) return '💡'
    return '📝'
  }

  const getPriorityColor = (index) => {
    if (index === 0) return 'border-l-green-400 bg-green-400/10'
    if (index === 1) return 'border-l-yellow-400 bg-yellow-400/10'
    if (index === 2) return 'border-l-blue-400 bg-blue-400/10'
    return 'border-l-purple-400 bg-purple-400/10'
  }

  const getImpactLevel = (index) => {
    if (index === 0) return 'High Impact'
    if (index === 1) return 'Medium Impact'
    return 'Additional Improvement'
  }

  return (
    <div className="glass-effect rounded-2xl p-6 fade-in">
      <h2 className="text-2xl font-bold text-white mb-6">
        Recommendations to Improve Success
      </h2>

      {success_probability > 0.8 ? (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🎉</div>
          <h3 className="text-xl font-semibold text-white mb-2">Excellent Setup!</h3>
          <p className="text-white/70">
            Your campaign is well-positioned for success. Focus on marketing and engagement.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {recommendations.map((recommendation, index) => (
            <div 
              key={index}
              className={`p-4 rounded-lg border-l-4 ${getPriorityColor(index)} transition-all duration-300 hover:scale-[1.02]`}
            >
              <div className="flex items-start space-x-3">
                <span className="text-2xl">{getPriorityIcon(index)}</span>
                <div className="flex-1">
                  <p className="text-white font-medium">{recommendation}</p>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-white/60 text-sm">
                      {getImpactLevel(index)}
                    </span>
                    <span className="text-white/60 text-sm">
                      {index === 0 ? '+++' : index === 1 ? '++' : '+'} Impact
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Success Tips */}
      <div className="mt-8 p-4 bg-white/10 rounded-lg">
        <h4 className="text-white font-medium mb-3 flex items-center">
          <i className="fas fa-graduation-cap mr-2"></i>
          Pro Tips for Success
        </h4>
        <ul className="text-white/70 text-sm space-y-2">
          <li className="flex items-start">
            <i className="fas fa-video mr-2 mt-1 text-blue-400"></i>
            <span>Add a compelling video - campaigns with videos raise 85% more funds</span>
          </li>
          <li className="flex items-start">
            <i className="fas fa-image mr-2 mt-1 text-green-400"></i>
            <span>Include 5+ high-quality images to build trust with backers</span>
          </li>
          <li className="flex items-start">
            <i className="fas fa-calendar mr-2 mt-1 text-purple-400"></i>
            <span>Launch on Tuesday - historically the best day for campaign visibility</span>
          </li>
          <li className="flex items-start">
            <i className="fas fa-users mr-2 mt-1 text-yellow-400"></i>
            <span>Build an email list before launching - 30% of funding often comes from pre-launch audience</span>
          </li>
        </ul>
      </div>

      {/* Action Plan */}
      {success_probability <= 0.8 && (
        <div className="mt-6 p-4 bg-blue-500/20 rounded-lg border border-blue-500/30">
          <h4 className="text-white font-medium mb-2 flex items-center">
            <i className="fas fa-rocket mr-2"></i>
            Quick Action Plan
          </h4>
          <ol className="text-white/80 text-sm space-y-2 list-decimal list-inside">
            <li>Implement the top 2 recommendations immediately</li>
            <li>Review your campaign description and visuals</li>
            <li>Plan your social media promotion strategy</li>
            <li>Prepare regular updates for your backers</li>
          </ol>
        </div>
      )}
    </div>
  )
}

export default Recommendations