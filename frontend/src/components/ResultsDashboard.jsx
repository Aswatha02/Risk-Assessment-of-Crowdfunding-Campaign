import React from 'react'
import RiskSummaryCard from './RiskSummaryCard'
import FeatureImportancePlot from './FeatureImportancePlot'
import Recommendations from './Recommendations'
import ComparisonCharts from './ComparisonCharts'

const ResultsDashboard = ({ prediction }) => {
  return (
    <div className="space-y-6">
      {/* Risk Summary */}
      <RiskSummaryCard prediction={prediction} />
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Feature Importance */}
        <div className="lg:col-span-1">
          <FeatureImportancePlot prediction={prediction} />
        </div>
        
        {/* Right Column - Recommendations & Explanations */}
        <div className="lg:col-span-2">
          <Recommendations prediction={prediction} />
          
          {/* Explanations */}
          <div className="glass-effect rounded-2xl p-6 mt-6 fade-in">
            <h2 className="text-2xl font-bold text-white mb-4">Key Insights</h2>
            <div className="space-y-3">
              {prediction.explanations && prediction.explanations.map((explanation, index) => (
                <div 
                  key={index}
                  className="flex items-start space-x-3 p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
                >
                  <i className={`fas ${
                    explanation.includes('increases') ? 'fa-arrow-up text-red-400' :
                    explanation.includes('improves') ? 'fa-arrow-up text-green-400' :
                    explanation.includes('boosts') ? 'fa-arrow-up text-green-400' :
                    'fa-info-circle text-blue-400'
                  } mt-1`}></i>
                  <span className="text-white/80">{explanation}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Scenario Comparison */}
      <ComparisonCharts 
        prediction={prediction}
        onNewAnalysis={() => window.location.reload()}
      />

      {/* Call to Action */}
      <div className="glass-effect rounded-2xl p-6 text-center fade-in">
        <h3 className="text-xl font-bold text-white mb-2">Ready to optimize your campaign?</h3>
        <p className="text-white/70 mb-4">
          Use these insights to refine your strategy and maximize your chances of success.
        </p>
        <div className="flex justify-center space-x-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors">
            <i className="fas fa-download mr-2"></i>
            Export Report
          </button>
          <button 
            onClick={() => window.location.reload()}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition-colors"
          >
            <i className="fas fa-redo mr-2"></i>
            New Analysis
          </button>
        </div>
      </div>
    </div>
  )
}

export default ResultsDashboard