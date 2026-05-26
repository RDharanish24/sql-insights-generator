import React from 'react';
import { Sparkles, Database, Layers, Activity, Server } from 'lucide-react';

export default function Header() {
  return (
    <header className="glass-card-highlight px-6 sm:px-8 py-5 animate-fade-in-up glow-brand">
      <div className="flex items-center justify-between flex-wrap gap-4">

        {/* ── Brand Mark ── */}
        <div className="flex items-center gap-4">
          <div className="relative group">
            {/* Animated background glow */}
            <div className="absolute -inset-1 bg-gradient-to-r from-brand-500 via-accent-blue to-brand-500 rounded-2xl opacity-50 blur-xl group-hover:opacity-70 transition-all duration-500" />
            {/* Icon container */}
            <div className="relative bg-gradient-to-br from-brand-500 to-accent-blue p-3.5 rounded-2xl shadow-2xl group-hover:shadow-brand group-hover:scale-105 transition-all duration-300">
              <Sparkles className="h-6 w-6 text-white" strokeWidth={1.5} />
            </div>
          </div>
          
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-black tracking-tight bg-gradient-to-r from-white via-indigo-200 to-slate-300 bg-clip-text text-transparent">
                DataGenie Core
              </h1>
              <span className="text-[10px] font-mono px-2 py-1 bg-brand-500/20 border border-brand-500/40 rounded-lg text-brand-300 font-bold">
                v1.0
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 font-medium mt-0.5">
              Conversational Business Intelligence Engine
            </p>
          </div>
        </div>

        {/* ── Status Badges ── */}
        <div className="flex items-center gap-2 sm:gap-3 flex-wrap justify-end">
          {/* Schema badge */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-2 bg-slate-800/60 backdrop-blur-sm border border-slate-700/50 rounded-lg text-xs text-slate-300 hover:border-slate-600/70 transition-all">
            <Layers className="h-3.5 w-3.5 text-indigo-400" strokeWidth={2} />
            <span className="font-mono font-medium">NLP2SQL</span>
          </div>

          {/* Engine badge */}
          <div className="hidden md:flex items-center gap-2 px-3 py-2 bg-slate-800/60 backdrop-blur-sm border border-slate-700/50 rounded-lg text-xs text-slate-300 hover:border-slate-600/70 transition-all">
            <Activity className="h-3.5 w-3.5 text-amber-400" strokeWidth={2} />
            <span className="font-mono font-medium">Gemini 2.5</span>
          </div>

          {/* Connection status - with enhanced glow */}
          <div className="flex items-center gap-2.5 px-4 py-2.5 bg-emerald-500/[0.12] backdrop-blur-sm border border-emerald-500/30 rounded-xl text-xs font-bold text-emerald-300 hover:bg-emerald-500/[0.16] transition-all glow-emerald">
            {/* Animated pulsing dot */}
            <span className="relative flex h-2.5 w-2.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-400" />
            </span>
            <Database className="h-4 w-4" strokeWidth={2} />
            <span className="hidden sm:inline">Connected</span>
            <span className="sm:hidden">Live</span>
          </div>
        </div>
      </div>

      {/* Subtle divider accent */}
      <div className="mt-4 h-[1px] bg-gradient-to-r from-transparent via-slate-700/50 to-transparent" />
    </header>
  );
}
