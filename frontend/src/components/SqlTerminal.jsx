import React, { useState, useCallback } from 'react';
import { Terminal, Copy, Check, Code2, Sparkles } from 'lucide-react';

export default function SqlTerminal({ sql }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(sql);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = sql;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [sql]);

  // Advanced SQL syntax highlighting with better color palette
  const highlightSQL = (code) => {
    if (!code) return '';

    const keywords = new Set([
      'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'AS',
      'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'FULL', 'CROSS', 'ON',
      'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET',
      'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE',
      'CREATE', 'TABLE', 'DROP', 'ALTER', 'INDEX',
      'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'DISTINCT',
      'ASC', 'DESC', 'BETWEEN', 'LIKE', 'IS', 'NULL',
      'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
      'UNION', 'ALL', 'EXISTS', 'TOP', 'WITH', 'OVER', 'PARTITION',
      'RANK', 'ROW_NUMBER', 'DENSE_RANK', 'ROUND', 'CAST',
      'COALESCE', 'EXTRACT', 'DATE', 'TIMESTAMP', 'INTERVAL',
    ]);

    const parts = code.split(/(\s+|,|\(|\)|;|'[^']*'|"[^"]*"|\b\d+\b)/g);

    return parts.map((part, i) => {
      if (!part) return null;

      // SQL keywords - cyan highlighted
      if (keywords.has(part.toUpperCase())) {
        return (
          <span key={i} className="text-cyan-400 font-bold">
            {part}
          </span>
        );
      }

      // String literals - emerald
      if (/^'.*'$/.test(part) || /^".*"$/.test(part)) {
        return (
          <span key={i} className="text-emerald-300">
            {part}
          </span>
        );
      }

      // Numbers - amber
      if (/^\d+$/.test(part)) {
        return (
          <span key={i} className="text-amber-300">
            {part}
          </span>
        );
      }

      // Punctuation - slate
      if (/^[,();]$/.test(part)) {
        return (
          <span key={i} className="text-slate-500 opacity-80">
            {part}
          </span>
        );
      }

      // Whitespace
      if (/^\s+$/.test(part)) {
        return part;
      }

      // Default (identifiers, table names, column names) - violet
      return (
        <span key={i} className="text-indigo-300">
          {part}
        </span>
      );
    });
  };

  const lineCount = sql.split('\n').length;

  return (
    <div className="glass-card-highlight overflow-hidden animate-fade-in-up border-indigo-500/20 glow-brand">

      {/* Enhanced terminal title bar */}
      <div className="flex items-center justify-between px-6 py-4 bg-gradient-to-r from-slate-900/80 to-slate-950/60 border-b border-slate-800/60">
        <div className="flex items-center gap-3">
          {/* Enhanced macOS-style traffic lights */}
          <div className="flex gap-1.5">
            <div className="h-3 w-3 rounded-full bg-rose-500 shadow-lg shadow-rose-500/40 border border-rose-600/60 hover:shadow-rose-500/60 transition-shadow" />
            <div className="h-3 w-3 rounded-full bg-amber-400 shadow-lg shadow-amber-400/40 border border-amber-500/60 hover:shadow-amber-400/60 transition-shadow" />
            <div className="h-3 w-3 rounded-full bg-emerald-400 shadow-lg shadow-emerald-400/40 border border-emerald-500/60 hover:shadow-emerald-400/60 transition-shadow" />
          </div>

          <div className="flex items-center gap-2.5 text-sm text-slate-300 font-bold">
            <div className="p-1.5 bg-indigo-500/20 border border-indigo-500/30 rounded-lg">
              <Terminal className="h-4 w-4 text-indigo-400" strokeWidth={2} />
            </div>
            <span>Generated SQL</span>
            <Sparkles className="h-3.5 w-3.5 text-brand-400 animate-pulse" strokeWidth={2} />
          </div>
        </div>

        {/* Enhanced Copy button with feedback */}
        <button
          id="copy-sql-btn"
          onClick={handleCopy}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition-all duration-300 ${
            copied
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-lg shadow-emerald-500/10'
              : 'bg-slate-800/60 text-slate-300 border border-slate-700/50 hover:text-slate-100 hover:bg-slate-800/80 hover:border-slate-600/70 shadow-md hover:shadow-lg'
          }`}
        >
          {copied ? (
            <>
              <Check className="h-4 w-4" strokeWidth={2.5} />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <Copy className="h-4 w-4" strokeWidth={2} />
              <span>Copy SQL</span>
            </>
          )}
        </button>
      </div>

      {/* Code body with enhanced styling */}
      <div className="relative bg-gradient-to-b from-slate-950/40 to-slate-950/20">
        {/* Line number gutter */}
        <div className="absolute left-0 top-0 bottom-0 w-14 bg-slate-950/80 border-r border-slate-800/60" />

        {/* Scrollable code container */}
        <pre className="pl-16 pr-6 py-6 overflow-x-auto text-sm leading-loose font-mono text-slate-100 whitespace-pre-wrap break-words">
          {sql.split('\n').map((line, i) => (
            <div key={i} className="flex hover:bg-slate-800/30 transition-colors duration-200 py-1 px-2 rounded-sm -mx-2">
              {/* Line number */}
              <span className="absolute left-4 text-xs text-slate-600/80 select-none w-8 text-right font-bold">
                {String(i + 1).padStart(2, ' ')}
              </span>
              {/* Highlighted code */}
              <code className="block">{highlightSQL(line)}</code>
            </div>
          ))}
        </pre>
      </div>

      {/* Enhanced footer bar with stats */}
      <div className="flex items-center justify-between px-6 py-3 bg-slate-950/70 border-t border-slate-800/60 text-xs text-slate-500 font-mono">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-800/40 border border-slate-700/40 rounded-lg">
            <Code2 className="h-3.5 w-3.5 text-indigo-400" strokeWidth={2} />
            <span className="font-bold text-slate-400">SQL</span>
          </div>
          <span className="text-slate-500">{lineCount} line{lineCount !== 1 ? 's' : ''}</span>
        </div>
        <span className="text-slate-600">Ready to execute ✓</span>
      </div>
    </div>
  );
}
