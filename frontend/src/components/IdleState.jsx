import React from 'react';
import { Sparkles, TrendingUp, Trophy, Target, BarChart3, PieChart, ChevronRight } from 'lucide-react';

const SUGGESTIONS = [
  {
    icon: Trophy,
    label: 'Top Performers',
    query: 'Show me the top 10 batsmen with the most runs',
    color: 'text-amber-400',
    bgColor: 'bg-amber-400/[0.08]',
    borderColor: 'border-amber-400/30',
    glowColor: 'shadow-amber-400/10',
  },
  {
    icon: TrendingUp,
    label: 'Toss Analytics',
    query: 'Analyze matches won by toss decision',
    color: 'text-emerald-400',
    bgColor: 'bg-emerald-400/[0.08]',
    borderColor: 'border-emerald-400/30',
    glowColor: 'shadow-emerald-400/10',
  },
  {
    icon: BarChart3,
    label: 'Season Breakdown',
    query: 'How many matches were played each season?',
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/[0.08]',
    borderColor: 'border-blue-400/30',
    glowColor: 'shadow-blue-400/10',
  },
  {
    icon: Target,
    label: 'Bowling Stats',
    query: 'Top 5 bowlers with most wickets',
    color: 'text-rose-400',
    bgColor: 'bg-rose-400/[0.08]',
    borderColor: 'border-rose-400/30',
    glowColor: 'shadow-rose-400/10',
  },
  {
    icon: PieChart,
    label: 'Venue Insights',
    query: 'Which venue hosted the most matches?',
    color: 'text-violet-400',
    bgColor: 'bg-violet-400/[0.08]',
    borderColor: 'border-violet-400/30',
    glowColor: 'shadow-violet-400/10',
  },
  {
    icon: Sparkles,
    label: 'Team Dominance',
    query: 'Which team has the highest win percentage?',
    color: 'text-cyan-400',
    bgColor: 'bg-cyan-400/[0.08]',
    borderColor: 'border-cyan-400/30',
    glowColor: 'shadow-cyan-400/10',
  },
];

export default function IdleState({ onSuggestionClick }) {
  return (
    <div className="flex flex-col items-center justify-center pt-10 pb-16 animate-fade-in-up-delay-2">

      {/* Hero graphic with enhanced styling */}
      <div className="relative mb-10 float-animation">
        {/* Outer glow rings */}
        <div className="absolute -inset-8 bg-gradient-to-r from-brand-500/30 to-accent-blue/20 rounded-full blur-3xl" />
        <div className="absolute -inset-4 bg-gradient-to-r from-brand-500/20 to-accent-blue/10 rounded-full blur-2xl" />
        
        {/* Icon container */}
        <div className="relative bg-gradient-to-br from-slate-800/80 to-slate-900/80 border-2 border-slate-700/60 p-7 rounded-3xl backdrop-blur-md shadow-2xl hover:shadow-brand hover:border-brand-500/40 transition-all duration-500">
          <Sparkles className="h-12 w-12 text-brand-400" strokeWidth={1.5} />
        </div>
      </div>

      {/* Headline */}
      <h2 className="text-3xl sm:text-4xl font-black bg-gradient-to-r from-white via-indigo-100 to-slate-300 bg-clip-text text-transparent text-center mb-3 tracking-tight">
        What would you like to explore?
      </h2>
      
      {/* Subheading */}
      <p className="text-base sm:text-lg text-slate-400 text-center max-w-2xl mb-12 leading-relaxed font-medium">
        Ask any question in natural language. DataGenie will generate the SQL, execute it on Snowflake, and visualize the results instantly.
      </p>

      {/* Suggestion cards grid with staggered animation */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-5xl">
        {SUGGESTIONS.map((s, index) => {
          const Icon = s.icon;
          return (
            <button
              key={index}
              id={`suggestion-${index}`}
              onClick={() => onSuggestionClick(s.query)}
              className={`group relative overflow-hidden rounded-2xl border-2 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] ${
                s.borderColor
              } ${s.bgColor} hover:bg-slate-800/50 backdrop-blur-sm shadow-lg hover:shadow-2xl ${s.glowColor}`}
              style={{
                animation: `fade-in-up 0.5s ease-out ${0.3 + index * 0.08}s both`
              }}
            >
              {/* Hover gradient overlay */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-gradient-to-br from-white/5 via-transparent to-transparent pointer-events-none" />
              
              {/* Content */}
              <div className="relative flex flex-col items-start gap-3 p-5 h-full text-left">
                {/* Icon */}
                <div className={`p-2.5 rounded-xl ${s.bgColor} border border-slate-700/60 group-hover:border-slate-600/80 group-hover:scale-110 transition-all duration-300 backdrop-blur-sm`}>
                  <Icon className={`h-5 w-5 ${s.color}`} strokeWidth={2} />
                </div>

                {/* Label and description */}
                <div className="flex-1 min-w-0">
                  <div className={`text-xs font-bold ${s.color} mb-1.5 tracking-wide`}>
                    {s.label}
                  </div>
                  <p className="text-sm text-slate-300 group-hover:text-slate-100 leading-snug font-medium transition-colors duration-300">
                    {s.query}
                  </p>
                </div>

                {/* Hover indicator */}
                <div className="flex items-center gap-1.5 text-xs text-slate-500 group-hover:text-slate-400 transition-colors opacity-0 group-hover:opacity-100 mt-auto">
                  <span className="text-slate-400 group-hover:text-slate-300">Explore</span>
                  <ChevronRight className="h-3.5 w-3.5 group-hover:translate-x-1 transition-transform" strokeWidth={2.5} />
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Footer hint */}
      <div className="mt-12 text-center text-sm text-slate-500">
        <p>💬 Or type your own question in the search bar above</p>
      </div>
    </div>
  );
}
