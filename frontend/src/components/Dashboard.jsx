import React, { useState } from 'react';
import { Search, Terminal, BarChart3, Database, Sparkles } from 'lucide-react';
import ChartRenderer from './ChartRenderer';

export default function Dashboard() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to complete execution query context.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-slate-100 font-sans antialiased p-6">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header Dashboard Frame */}
        <header className="flex items-center justify-between border-b border-slate-800 pb-6">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-tr from-blue-500 to-indigo-600 p-3 rounded-2xl shadow-lg shadow-indigo-500/20">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                DataGenie Core
              </h1>
              <p className="text-sm text-slate-400">Conversational Business Intelligence Engine</p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-slate-900/80 border border-slate-800 rounded-xl text-xs font-mono text-emerald-400">
            <Database className="h-4 w-4" /> Connected to Snowflake
          </div>
        </header>

        {/* Dynamic Query System Row */}
        <form onSubmit={handleSearch} className="relative">
          <div className="relative flex items-center bg-slate-900/60 border border-slate-800 focus-within:border-indigo-500/50 rounded-2xl shadow-2xl backdrop-blur-xl transition-all duration-300 group">
            <Search className="absolute left-5 text-slate-500 group-focus-within:text-indigo-400 transition-colors h-5 w-5" />
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder='Ask your repository anything (e.g., "Show me the top 10 batsmen with most runs")...'
              className="w-full bg-transparent pl-14 pr-36 py-5 text-white placeholder-slate-500 outline-none text-base"
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-3 px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl font-medium shadow-lg shadow-indigo-600/20 active:scale-[0.98] transition-all text-sm disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Generate Insights'}
            </button>
          </div>
        </form>

        {/* Error Notification banner */}
        {error && (
          <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400 text-sm">
            ⚡ {error}
          </div>
        )}

        {/* Main Content Area */}
        {result && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            
            {/* Terminal Preview Panel */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-2xl font-mono text-xs overflow-hidden shadow-2xl">
              <div className="bg-slate-900/80 border-b border-slate-800/60 px-4 py-2.5 flex items-center gap-2 text-slate-400">
                <Terminal className="h-3.5 w-3.5 text-indigo-400" /> Compiled SQL Logic Statement
              </div>
              <pre className="p-4 overflow-x-auto text-cyan-400">{result.sql}</pre>
            </div>

            {/* Visual Intelligence Grid panels */}
            <div>
              <div className="flex items-center gap-2 text-lg font-bold text-white mb-2">
                <BarChart3 className="h-5 w-5 text-indigo-400" /> Executive Analytics Panels
              </div>
              <ChartRenderer data={result.data} columns={result.columns} />
            </div>

            {/* Raw Schema Records Grid Container */}
            <div className="bg-slate-900/40 border border-slate-800/80 rounded-2xl overflow-hidden shadow-xl">
              <div className="px-6 py-4 bg-slate-900/80 border-b border-slate-800 font-semibold text-sm">
                Tabular Inspection Database Results ({result.data.length} records returned)
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-slate-850 bg-slate-950/20 text-slate-400">
                      {result.columns.map((col) => (
                        <th key={col} className="p-4 font-semibold uppercase tracking-wider text-xs">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {result.data.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/20 transition-colors">
                        {result.columns.map((col) => (
                          <td key={col} className="p-4 text-slate-300 font-medium">{row[col]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        )}
      </div>
    </div>
  );
}