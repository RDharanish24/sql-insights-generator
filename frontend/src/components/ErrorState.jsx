import React from 'react';
import { AlertTriangle, RotateCcw, AlertCircle } from 'lucide-react';

export default function ErrorState({ message, onRetry }) {
  return (
    <div className="flex items-center justify-center pt-12 pb-8 animate-fade-in-up px-4">
      <div className="glass-card-highlight max-w-xl w-full overflow-hidden border-rose-500/30 bg-gradient-to-br from-rose-500/[0.08] to-slate-900/50 shadow-2xl shadow-rose-500/10">
        
        {/* Accent bar at top */}
        <div className="h-1 bg-gradient-to-r from-rose-500 via-rose-400 to-transparent" />

        <div className="flex items-start gap-4 p-6 sm:p-7">

          {/* Icon */}
          <div className="shrink-0 p-3 bg-rose-500/15 border border-rose-500/30 rounded-xl mt-0.5">
            <AlertTriangle className="h-6 w-6 text-rose-400" strokeWidth={2} />
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <h3 className="text-base font-bold text-rose-300 mb-2">
              Query Execution Failed
            </h3>
            <p className="text-sm text-slate-300 leading-relaxed break-words font-medium">
              {message}
            </p>

            {/* Retry action */}
            <button
              id="error-retry-btn"
              onClick={onRetry}
              className="mt-5 flex items-center gap-2.5 px-5 py-2.5 bg-gradient-to-r from-rose-500/20 to-rose-500/10 hover:from-rose-500/30 hover:to-rose-500/20 border border-rose-500/40 hover:border-rose-500/60 rounded-lg text-sm font-bold text-rose-300 hover:text-rose-200 transition-all duration-300 active:scale-[0.95] shadow-lg shadow-rose-500/10"
            >
              <RotateCcw className="h-4 w-4" strokeWidth={2.5} />
              Retry Query
            </button>
          </div>

          {/* Close hint */}
          <div className="hidden sm:flex items-center justify-center p-2 rounded-lg bg-slate-800/40">
            <AlertCircle className="h-4 w-4 text-slate-500" strokeWidth={1.5} />
          </div>
        </div>

        {/* Bottom suggestion bar */}
        <div className="px-6 sm:px-7 py-3 border-t border-slate-700/40 bg-slate-950/40 text-xs text-slate-400">
          <p>💡 Tip: Verify your query is clear and the data exists in your database</p>
        </div>
      </div>
    </div>
  );
}
