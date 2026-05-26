import React, { useRef, useState } from 'react';
import { Search, ArrowRight, Loader2, Zap } from 'lucide-react';

export default function SearchController({ prompt, setPrompt, loading, onSubmit }) {
  const inputRef = useRef(null);
  const [focused, setFocused] = useState(false);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading && prompt.trim()) {
      onSubmit(e);
    }
  };

  return (
    <div className="animate-fade-in-up-delay-1 space-y-3">
      <form onSubmit={onSubmit} className="relative group">

        {/* Outer glow ring — visible on focus */}
        <div
          className={`absolute -inset-[2px] rounded-3xl bg-gradient-to-r from-brand-500/60 via-accent-blue/40 to-brand-500/60 transition-all duration-500 blur-lg pointer-events-none ${
            focused ? 'opacity-100' : 'opacity-0'
          }`}
        />

        {/* Main input container with enhanced styling */}
        <div
          className={`relative flex items-center bg-gradient-to-br from-slate-900/80 to-slate-950/80 backdrop-blur-xl rounded-2xl border-2 transition-all duration-300 overflow-hidden ${
            focused
              ? 'border-brand-500/60 shadow-2xl shadow-brand-500/20'
              : 'border-slate-800/60 shadow-xl'
          }`}
        >
          {/* Animated background accent when focused */}
          {focused && (
            <div className="absolute inset-0 bg-gradient-to-r from-brand-500/5 via-accent-blue/5 to-brand-500/5 pointer-events-none animate-pulse" />
          )}

          {/* Search icon */}
          <div className="pl-6 sm:pl-7 relative z-10">
            <Search
              className={`h-5 w-5 transition-all duration-300 ${
                focused ? 'text-brand-400 scale-110' : 'text-slate-500'
              }`}
              strokeWidth={2}
            />
          </div>

          {/* Input field */}
          <input
            ref={inputRef}
            id="search-input"
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder='Ask anything — e.g., "Top 10 batsmen by runs", "Analyze venue performance"'
            className="flex-1 bg-transparent px-5 py-6 text-white placeholder-slate-500 outline-none text-base font-medium relative z-10 transition-colors duration-300"
            disabled={loading}
            autoComplete="off"
            spellCheck="true"
          />

          {/* Submit button */}
          <div className="pr-4 sm:pr-5 relative z-10">
            <button
              id="search-submit"
              type="submit"
              disabled={loading || !prompt.trim()}
              className={`flex items-center gap-2.5 px-6 sm:px-8 py-3 rounded-lg font-bold text-sm transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed active:scale-[0.97] ${
                loading
                  ? 'bg-slate-800/70 text-slate-400 cursor-wait'
                  : 'bg-gradient-to-r from-brand-500 to-accent-blue hover:from-brand-600 hover:to-blue-600 text-white shadow-lg shadow-brand-500/25 hover:shadow-xl hover:shadow-brand-500/35'
              }`}
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin flex-shrink-0" />
                  <span className="hidden sm:inline">Analyzing</span>
                  <span className="sm:hidden">Wait</span>
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4 flex-shrink-0" />
                  <span>Generate</span>
                  <ArrowRight className="h-4 w-4 flex-shrink-0" />
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Hint text with keyboard shortcut */}
      <div className="flex items-center justify-center gap-1.5 text-xs text-slate-500 font-medium px-3">
        <span>💡 Tip:</span>
        <kbd className="px-2 py-1 bg-slate-800/70 border border-slate-700/50 rounded text-[11px] font-mono text-slate-400">
          Enter
        </kbd>
        <span>to generate</span>
      </div>
    </div>
  );
}
