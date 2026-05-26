import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, AreaChart, Area, PieChart, Pie, Cell 
} from 'recharts';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

export default function ChartRenderer({ data, columns }) {
  if (!data || data.length === 0 || !columns || columns.length < 2) {
    return (
      <div className="flex items-center justify-center h-64 border-2 border-dashed border-slate-700 rounded-xl bg-slate-800/30">
        <p className="text-slate-400 font-medium">Insufficient dimensions found to plot charts</p>
      </div>
    );
  }

  // Define keys: text properties normally match X axis, numerical factors go to Y Axis
  const xAxisKey = columns[0];
  const numericColumns = columns.slice(1);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
      {/* 1. Metric Breakdown (Bar Chart) */}
      <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-2xl border border-slate-700/50 shadow-xl">
        <h3 className="text-lg font-semibold text-white mb-4">Volume Distribution</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={xAxisKey} stroke="#94A3B8" tick={{fontSize: 12}} />
              <YAxis stroke="#94A3B8" />
              <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#fff' }} />
              <Legend />
              {numericColumns.map((col, index) => (
                <Bar key={col} dataKey={col} fill={COLORS[index % COLORS.length]} radius={[4, 4, 0, 0]} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 2. Linear Progression (Line Chart) */}
      <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-2xl border border-slate-700/50 shadow-xl">
        <h3 className="text-lg font-semibold text-white mb-4">Trend & Continuity</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={xAxisKey} stroke="#94A3B8" tick={{fontSize: 12}} />
              <YAxis stroke="#94A3B8" />
              <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#fff' }} />
              <Legend />
              {numericColumns.map((col, index) => (
                <Line key={col} type="monotone" dataKey={col} stroke={COLORS[(index + 1) % COLORS.length]} strokeWidth={3} dot={{ r: 4 }} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 3. Area Spectrum */}
      <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-2xl border border-slate-700/50 shadow-xl">
        <h3 className="text-lg font-semibold text-white mb-4">Density Threshold</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey={xAxisKey} stroke="#94A3B8" tick={{fontSize: 12}} />
              <YAxis stroke="#94A3B8" />
              <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#fff' }} />
              <Legend />
              {numericColumns.map((col, index) => (
                <Area key={col} type="monotone" dataKey={col} fill={COLORS[(index + 2) % COLORS.length]} stroke={COLORS[(index + 2) % COLORS.length]} fillOpacity={0.2} />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 4. Composition Matrix (Pie Chart) */}
      <div className="bg-slate-800/50 backdrop-blur-md p-6 rounded-2xl border border-slate-700/50 shadow-xl">
        <h3 className="text-lg font-semibold text-white mb-4">Share Proportion (Top {data.length} records)</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey={numericColumns[0] || columns[1]}
                nameKey={xAxisKey}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#475569', color: '#fff' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}