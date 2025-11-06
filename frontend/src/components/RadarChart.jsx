import React, { useEffect, useRef } from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

function RadarChart({ featureImportance }) {
  if (!featureImportance || Object.keys(featureImportance).length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>No feature importance data available</p>
      </div>
    );
  }

  // Convert feature importance to chart data
  const features = Object.keys(featureImportance);
  const values = Object.values(featureImportance).map(v => v * 100); // Convert to percentage

  // Create readable labels
  const labels = features.map(feature => {
    return feature
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase())
      .replace('Usd', 'USD')
      .replace('Te', '');
  });

  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Feature Impact (%)',
        data: values,
        backgroundColor: 'rgba(99, 102, 241, 0.2)',
        borderColor: 'rgba(99, 102, 241, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(99, 102, 241, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(99, 102, 241, 1)',
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        beginAtZero: true,
        max: Math.max(...values) * 1.2, // Add 20% padding
        ticks: {
          stepSize: 5,
          callback: function(value) {
            return value.toFixed(0) + '%';
          },
          font: {
            size: 11
          }
        },
        pointLabels: {
          font: {
            size: 12,
            weight: 'bold'
          },
          color: '#374151'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
        angleLines: {
          color: 'rgba(0, 0, 0, 0.1)',
        }
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: {
          size: 14,
          weight: 'bold'
        },
        bodyFont: {
          size: 13
        },
        callbacks: {
          label: function(context) {
            return `Impact: ${context.parsed.r.toFixed(1)}%`;
          }
        }
      },
    },
  };

  return (
    <div className="w-full h-full">
      <Radar data={data} options={options} />
    </div>
  );
}

export default RadarChart;
