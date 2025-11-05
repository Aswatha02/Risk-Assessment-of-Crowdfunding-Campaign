import React from 'react'

const FeatureImportancePlot = ({ prediction }) => {
  const { feature_importance } = prediction

  // Convert feature importance to array and sort
  const features = Object.entries(feature_importance)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 8) // Top 8 features

  const maxImportance = Math.max(...features.map(([, importance]) => importance))

  const formatFeatureName = (name) => {
    return name
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase())
      .replace('Te', '')
  }

  return (
    <div className="glass-effect rounded-2xl p-6 mb-6 fade-in">
      <h2 className="text-2xl font-bold text-white mb-6">Key Influencing Factors</h2>
      
      <div className="space-y-4">
        {features.map(([feature, importance]) => (
          <div key={feature} className="flex items-center justify-between">
            <span className="text-white/80 text-sm w-32 truncate">
              {formatFeatureName(feature)}
            </span>
            <div className="flex-1 mx-4">
              <div className="bg-gray-700 rounded-full h-3">
                <div 
                  className="h-3 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"
                  style={{ width: `${(importance / maxImportance) * 100}%` }}
                ></div>
              </div>
            </div>
            <span className="text-white font-semibold text-sm w-12 text-right">
              {Math.round(importance * 100)}%
            </span>
          </div>
        ))}
      </div>

      {/* Radar Chart Placeholder */}
      <div className="mt-8 p-6 bg-white/5 rounded-xl border border-white/10">
        <div className="text-center">
          <div className="radar-chart mx-auto w-48 h-48 rounded-full flex items-center justify-center mb-4">
            <div className="text-white/50 text-sm text-center">
              <i className="fas fa-chart-radar text-3xl mb-2 block"></i>
              Feature Impact Radar
            </div>
          </div>
          <p className="text-white/70 text-sm">
            Visual representation of how different factors influence the prediction
          </p>
        </div>
      </div>

      {/* Interpretation Guide */}
      <div className="mt-6 p-4 bg-white/5 rounded-lg">
        <h4 className="text-white font-medium mb-2">How to interpret:</h4>
        <ul className="text-white/70 text-sm space-y-1">
          <li>• Higher percentages indicate stronger influence on the prediction</li>
          <li>• Top factors are the main drivers of success/failure</li>
          <li>• Focus on optimizing high-impact factors first</li>
        </ul>
      </div>
    </div>
  )
}

export default FeatureImportancePlot