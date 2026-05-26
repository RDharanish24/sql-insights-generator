import React, { useMemo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, AreaChart, Area, PieChart, Pie, Cell,
} from 'recharts';
import { BarChart3, TrendingUp, Layers, PieChart as PieIcon, AlertCircle, Zap } from 'lucide-react';

/* ═══ Enhanced Color Palette ═══ */
const CHART_COLORS = [
  '#818cf8', // indigo-400
  '#34d399', // emerald-400
  '#fbbf24', // amber-400
  '#fb7185', // rose-400
  '#60a5fa', // blue-400
  '#c084fc', // purple-400
  '#22d3ee', // cyan-400
  '#f97316', // orange-400
];

const GRADIENT_PAIRS = [
  { start: '#818cf8', end: '#6366f1' },
  { start: '#34d399', end: '#10b981' },
  { start: '#fbbf24', end: '#f59e0b' },
  { start: '#fb7185', end: '#f43f5e' },
  { start: '#60a5fa', end: '#3b82f6' },
];

/* ═══ Enhanced Custom Tooltip ═══ */
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload || payload.length === 0) return null;

  return (
    <div className="glass-card-highlight px-5 py-4 border border-slate-700/60 shadow-2xl">
      <p className="text-sm font-bold text-indigo-300 mb-3 border-b border-slate-700/50 pb-2">
        {label}
      </p>
      {payload.map((entry, index) => (
        <div key={index} className="flex items-center gap-3 text-sm py-1.5">
          <span
            className="h-3 w-3 rounded-full shrink-0 shadow-lg"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-slate-300 font-medium">{entry.name}:</span>
          <span className="text-white font-bold ml-auto pl-4">
            {typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}
          </span>
        </div>
      ))}
    </div>
  );
};

/* ═══ Enhanced Chart Card Wrapper ═══ */
function ChartCard({ icon: Icon, title, subtitle, children, delay = '' }) {
  return (
    <div className={`glass-card-highlight rounded-3xl border-indigo-500/20 overflow-hidden transition-all duration-300 hover:shadow-xl hover:shadow-brand-500/20 ${delay}`}>
      {/* Header */}
      <div className="flex items-start justify-between p-6 border-b border-slate-800/60 bg-gradient-to-r from-slate-900/40 to-transparent">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2.5 bg-gradient-to-br from-brand-500/20 to-accent-blue/20 border border-brand-500/30 rounded-xl">
              <Icon className="h-5 w-5 text-brand-400" strokeWidth={2} />
            </div>
            <h3 className="text-base font-bold text-slate-100">{title}</h3>
          </div>
          {subtitle && <p className="text-xs text-slate-500 ml-11">{subtitle}</p>}
        </div>
      </div>
      
      {/* Chart container */}
      <div className="h-80 p-6 bg-gradient-to-br from-slate-950/20 to-slate-950/5">
        {children}
      </div>
    </div>
  );
}

/* ═══ Main Component ═══ */
export default function ChartRenderer({ data, columns }) {
  // Identify numeric vs. categorical columns
  const { xAxisKey, numericColumns } = useMemo(() => {
    if (!data || !columns || columns.length < 2) {
      return { xAxisKey: null, numericColumns: [] };
    }

    const xKey = columns[0];
    const numCols = columns.slice(1).filter((col) => {
      // Check if at least one row has a numeric value for this column
      return data.some((row) => {
        const val = row[col];
        return val !== null && val !== undefined && !isNaN(Number(val));
      });
    });

    return { xAxisKey: xKey, numericColumns: numCols };
  }, [data, columns]);

  // Guard: Not enough data for charts
  if (!xAxisKey || numericColumns.length === 0) {
    return (
      <div className="glass-card-highlight p-10 animate-fade-in-up-delay-1 border-amber-500/20">
        <div className="flex flex-col items-center justify-center h-56 text-center">
          <div className="p-4 bg-amber-500/10 border border-amber-500/20 rounded-2xl mb-4">
            <AlertCircle className="h-8 w-8 text-amber-400" strokeWidth={1.5} />
          </div>
          <p className="text-base font-bold text-slate-200 mb-2">
            No numeric data available for visualization
          </p>
          <p className="text-sm text-slate-400">
            Charts require at least one numeric column. Please refine your query.
          </p>
        </div>
      </div>
    );
  }

  // Shared axis styling
  const axisStyle = { fontSize: 12, fill: '#94a3b8', fontWeight: 500 };
  const gridStroke = '#1e293b';

  // Prepare pie data (top 10 entries to keep it clean)
  const pieData = data.slice(0, 10);

  return (
    <div className="space-y-6 animate-fade-in-up-delay-1">
      {/* Section header with stats */}
      <div className="flex items-center justify-between px-2 py-3 border-l-4 border-brand-500">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-brand-500/20 border border-brand-500/30 rounded-lg">
            <Zap className="h-5 w-5 text-brand-400" strokeWidth={2.5} />
          </div>
          <div>
            <h2 className="text-xl font-black text-white">Executive Analytics</h2>
            <p className="text-xs text-slate-400 mt-0.5">
              {numericColumns.length} metric{numericColumns.length !== 1 ? 's' : ''} • {data.length} record{data.length !== 1 ? 's' : ''}
            </p>
          </div>
        </div>
        <div className="hidden sm:flex items-center gap-2 px-4 py-2 bg-slate-800/40 border border-slate-700/40 rounded-lg">
          <BarChart3 className="h-4 w-4 text-indigo-400" strokeWidth={2} />
          <span className="text-xs font-bold text-slate-300">Multi-metric View</span>
        </div>
      </div>

      {/* Chart grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* ── Bar Chart ── */}
        <ChartCard
          icon={BarChart3}
          title="Volume Distribution"
          subtitle="Metric comparison across categories"
          delay="animate-fade-in-up"
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 5, right: 20, left: -5, bottom: 5 }}>
              <defs>
                {numericColumns.map((_, i) => (
                  <linearGradient key={i} id={`barGrad-${i}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={GRADIENT_PAIRS[i % GRADIENT_PAIRS.length].start} stopOpacity={1} />
                    <stop offset="100%" stopColor={GRADIENT_PAIRS[i % GRADIENT_PAIRS.length].end} stopOpacity={0.7} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="4 4" stroke={gridStroke} vertical={false} />
              <XAxis dataKey={xAxisKey} tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(148, 163, 184, 0.08)' }} />
              <Legend
                wrapperStyle={{ fontSize: '12px', paddingTop: '12px', fontWeight: 600 }}
                iconType="square"
                iconSize={10}
              />
              {numericColumns.map((col, index) => (
                <Bar
                  key={col}
                  dataKey={col}
                  fill={`url(#barGrad-${index})`}
                  radius={[8, 8, 0, 0]}
                  maxBarSize={60}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* ── Line Chart ── */}
        <ChartCard
          icon={TrendingUp}
          title="Trend Analysis"
          subtitle="Temporal or sequential progression"
          delay="animate-fade-in-up-delay-1"
        >
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 5, right: 20, left: -5, bottom: 5 }}>
              <CartesianGrid strokeDasharray="4 4" stroke={gridStroke} vertical={false} />
              <XAxis dataKey={xAxisKey} tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ fontSize: '12px', paddingTop: '12px', fontWeight: 600 }}
                iconType="line"
                iconSize={12}
              />
              {numericColumns.map((col, index) => (
                <Line
                  key={col}
                  type="monotone"
                  dataKey={col}
                  stroke={CHART_COLORS[index % CHART_COLORS.length]}
                  strokeWidth={3}
                  dot={{ r: 4, fill: CHART_COLORS[index % CHART_COLORS.length], strokeWidth: 0 }}
                  activeDot={{ r: 6, strokeWidth: 2, stroke: '#0f172a' }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* ── Area Chart ── */}
        <ChartCard
          icon={Layers}
          title="Density Spectrum"
          subtitle="Cumulative impact visualization"
          delay="animate-fade-in-up-delay-2"
        >
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 5, right: 20, left: -5, bottom: 5 }}>
              <defs>
                {numericColumns.map((_, i) => (
                  <linearGradient key={i} id={`areaGrad-${i}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={CHART_COLORS[(i + 2) % CHART_COLORS.length]} stopOpacity={0.4} />
                    <stop offset="100%" stopColor={CHART_COLORS[(i + 2) % CHART_COLORS.length]} stopOpacity={0.02} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="4 4" stroke={gridStroke} vertical={false} />
              <XAxis dataKey={xAxisKey} tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ fontSize: '12px', paddingTop: '12px', fontWeight: 600 }}
                iconType="line"
              />
              {numericColumns.map((col, index) => (
                <Area
                  key={col}
                  type="monotone"
                  dataKey={col}
                  stroke={CHART_COLORS[(index + 2) % CHART_COLORS.length]}
                  strokeWidth={2}
                  fill={`url(#areaGrad-${index})`}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* ── Pie Chart ── */}
        <ChartCard
          icon={PieIcon}
          title="Share Composition"
          subtitle={`Top ${pieData.length} categories`}
          delay="animate-fade-in-up-delay-3"
        >
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={100}
                paddingAngle={4}
                dataKey={numericColumns[0]}
                nameKey={xAxisKey}
                stroke="#0f172a"
                strokeWidth={2}
                label={({ name, percent }) =>
                  `${name && name.length > 10 ? name.slice(0, 10) + '…' : name}: ${(percent * 100).toFixed(0)}%`
                }
                labelLine={{ stroke: '#475569', strokeWidth: 1 }}
              >
                {pieData.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={CHART_COLORS[index % CHART_COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}
