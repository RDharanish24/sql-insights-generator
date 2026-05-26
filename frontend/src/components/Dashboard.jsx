import React, { useState, useCallback } from 'react';
import Header from './Header';
import SearchController from './SearchController';
import IdleState from './IdleState';
import LoadingState from './LoadingState';
import ErrorState from './ErrorState';
import SqlTerminal from './SqlTerminal';
import ChartRenderer from './ChartRenderer';
import DataTable from './DataTable';

export default function Dashboard() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSearch = useCallback(async (queryText) => {
    const query = queryText || prompt;
    if (!query.trim()) return;

    setPrompt(query);
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `Server returned ${response.status}: Query execution failed.`
        );
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred. Please try again.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  }, [prompt]);

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSearch();
  };

  const handleSuggestionClick = (suggestion) => {
    setPrompt(suggestion);
    handleSearch(suggestion);
  };

  const handleRetry = () => {
    if (prompt.trim()) {
      handleSearch(prompt);
    }
  };

  // Determine current view state
  const isIdle = !loading && !result && !error;
  const hasResults = !loading && result && !error;

  return (
    <div className="min-h-screen text-slate-100 font-sans">
      <div className="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        {/* ═══ Enterprise Header ═══ */}
        <Header />

        {/* ═══ Search Controller ═══ */}
        <SearchController
          prompt={prompt}
          setPrompt={setPrompt}
          loading={loading}
          onSubmit={handleSubmit}
        />

        {/* ═══ State-Driven Content Area ═══ */}
        <main className="min-h-[60vh]">

          {/* Idle: Suggestions */}
          {isIdle && (
            <IdleState onSuggestionClick={handleSuggestionClick} />
          )}

          {/* Loading: Skeleton */}
          {loading && <LoadingState />}

          {/* Error: Feedback Card */}
          {!loading && error && (
            <ErrorState message={error} onRetry={handleRetry} />
          )}

          {/* Results: SQL + Charts + Table */}
          {hasResults && (
            <div className="space-y-8 animate-fade-in-up">

              {/* SQL Terminal */}
              {result.sql && (
                <SqlTerminal sql={result.sql} />
              )}

              {/* Analytics Charts */}
              {result.data && result.columns && (
                <ChartRenderer data={result.data} columns={result.columns} />
              )}

              {/* Data Table */}
              {result.data && result.columns && (
                <DataTable
                  data={result.data}
                  columns={result.columns}
                />
              )}
            </div>
          )}
        </main>

        {/* ═══ Footer ═══ */}
        <footer className="border-t border-slate-800/50 pt-6 pb-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
            <p>DataGenie Core v1.0 — Conversational Business Intelligence Engine</p>
            <p className="font-mono">Powered by Gemini 2.5 Flash + Snowflake</p>
          </div>
        </footer>
      </div>
    </div>
  );
}