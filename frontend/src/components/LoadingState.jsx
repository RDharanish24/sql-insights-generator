import React from 'react';
import { Cpu, Zap, Database, BarChart3 } from 'lucide-react';

export default function LoadingState() {
  return (
    <div className="space-y-6 animate-fade-in-up pt-6">

      {/* Enhanced spinner header */}
      <div className="flex flex-col items-center justify-center py-10">
        {/* Animated spinning rings */}
        <div className="relative mb-8 w-24 h-24">
          {/* Outer ring */}
          <div className="absolute inset-0 rounded-full border-2 border-slate-800 border-t-brand-500 border-r-accent-blue/50 animate-spin" />
          {/* Middle ring - slower */}
          <div className="absolute inset-2 rounded-full border-2 border-transparent border-b-accent-blue/60 border-l-brand-500/40 animate-spin" style={{animationDirection: 'reverse', animationDuration: '3s'}} />
          
          {/* Center icon */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="relative">
              <div className="absolute -inset-4 bg-brand-500/20 rounded-full blur-xl animate-pulse" />
              <Cpu className="h-8 w-8 text-brand-400 relative animate-pulse" strokeWidth={1.5} />
            </div>
          </div>
        </div>

        {/* Status text */}
        <p className="text-lg font-bold text-slate-100 mb-2 text-center">Analyzing your query</p>
        <p className="text-sm text-slate-400 text-center font-medium">
          Processing natural language · Generating SQL · Executing on Snowflake
        </p>
      </div>

      {/* Animated progress indicators */}
      <div className="flex items-center justify-center gap-2 px-6">
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800/40 border border-slate-700/40">
          <Zap className="h-4 w-4 text-brand-400 animate-pulse" />
          <span className="text-xs font-medium text-slate-300">NLP Processing</span>
        </div>
        <div className="w-2 h-2 rounded-full bg-slate-700 animate-pulse" style={{animationDelay: '0.2s'}} />
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800/40 border border-slate-700/40">
          <Database className="h-4 w-4 text-emerald-400 animate-pulse" style={{animationDelay: '0.1s'}} />
          <span className="text-xs font-medium text-slate-300">Query Execution</span>
        </div>
        <div className="w-2 h-2 rounded-full bg-slate-700 animate-pulse" style={{animationDelay: '0.4s'}} />
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800/40 border border-slate-700/40">
          <BarChart3 className="h-4 w-4 text-amber-400 animate-pulse" style={{animationDelay: '0.2s'}} />
          <span className="text-xs font-medium text-slate-300">Visualization</span>
        </div>
      </div>

      {/* Skeleton: SQL Terminal */}
      <div className="glass-card overflow-hidden">
        <div className="flex items-center gap-2 px-6 py-4 border-b border-slate-800/60 bg-slate-900/40">
          <div className="flex gap-2">
            <div className="h-2.5 w-2.5 rounded-full bg-slate-700/80 animate-pulse" />
            <div className="h-2.5 w-2.5 rounded-full bg-slate-700/60 animate-pulse" style={{animationDelay: '0.1s'}} />
            <div className="h-2.5 w-2.5 rounded-full bg-slate-700/40 animate-pulse" style={{animationDelay: '0.2s'}} />
          </div>
          <div className="skeleton h-3 w-40 ml-4 rounded" />
        </div>
        <div className="p-6 space-y-4 font-mono">
          <div className="skeleton h-3.5 w-4/5 rounded" />
          <div className="skeleton h-3.5 w-3/4 rounded" />
          <div className="skeleton h-3.5 w-5/6 rounded" />
          <div className="skeleton h-3.5 w-2/3 rounded" />
          <div className="skeleton h-3.5 w-3/5 rounded" />
        </div>
      </div>

      {/* Skeleton: Charts Grid */}
      <div>
        <div className="flex items-center gap-2.5 mb-4 px-1">
          <BarChart3 className="h-4 w-4 text-brand-400" />
          <div className="skeleton h-4 w-40 rounded" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {[1, 2].map((i) => (
            <div key={i} className="glass-card p-6">
              <div className="skeleton h-4 w-36 rounded mb-6" />
              <div className="skeleton h-60 w-full rounded-xl" />
            </div>
          ))}
        </div>
      </div>

      {/* Skeleton: Table */}
      <div className="glass-card overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-800/60 bg-slate-900/40">
          <div className="skeleton h-4 w-48 rounded" />
        </div>
        <div className="p-6 space-y-3">
          {/* Header row */}
          <div className="flex gap-4 pb-3 border-b border-slate-800/40">
            {[1, 2, 3, 4, 5].map((c) => (
              <div key={c} className="skeleton h-3 flex-1 rounded" />
            ))}
          </div>
          {/* Data rows */}
          {[1, 2, 3, 4, 5].map((r) => (
            <div key={r} className="flex gap-4">
              {[1, 2, 3, 4, 5].map((c) => (
                <div key={c} className="skeleton h-3.5 flex-1 rounded" />
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
