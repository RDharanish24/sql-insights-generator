import React, { useMemo, useState } from 'react';
import { Table2, ChevronLeft, ChevronRight, Hash, Copy, Download } from 'lucide-react';

const PAGE_SIZE = 25;

export default function DataTable({ data, columns }) {
  const [page, setPage] = useState(0);
  const [copied, setCopied] = useState(false);

  const totalRows = data.length;
  const totalPages = Math.ceil(totalRows / PAGE_SIZE);

  const paginatedData = useMemo(() => {
    const start = page * PAGE_SIZE;
    return data.slice(start, start + PAGE_SIZE);
  }, [data, page]);

  const handlePrev = () => setPage((p) => Math.max(0, p - 1));
  const handleNext = () => setPage((p) => Math.min(totalPages - 1, p + 1));

  const handleExport = () => {
    // Convert data to CSV format
    const headers = columns.join(',');
    const rows = data.map(row =>
      columns.map(col => {
        const val = row[col];
        // Escape quotes and wrap in quotes if contains comma
        const str = String(val === null || val === undefined ? '' : val);
        return str.includes(',') ? `"${str.replace(/"/g, '""')}"` : str;
      }).join(',')
    );
    const csv = [headers, ...rows].join('\n');
    
    // Trigger download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `data-export-${new Date().getTime()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleCopyTable = () => {
    // Copy table as TSV (better for spreadsheets)
    const headers = columns.join('\t');
    const rows = paginatedData.map(row =>
      columns.map(col => row[col] === null || row[col] === undefined ? '' : String(row[col])).join('\t')
    );
    const tsv = [headers, ...rows].join('\n');
    
    navigator.clipboard.writeText(tsv).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  if (!data || data.length === 0 || !columns || columns.length === 0) {
    return null;
  }

  return (
    <div className="glass-card-highlight overflow-hidden animate-fade-in-up-delay-2 border-emerald-500/20">

      {/* Enhanced table header bar */}
      <div className="flex items-center justify-between px-6 py-5 bg-gradient-to-r from-slate-900/80 to-slate-950/40 border-b border-slate-800/60">
        <div className="flex items-center gap-4 flex-1">
          <div className="p-2.5 bg-emerald-500/20 border border-emerald-500/30 rounded-xl">
            <Table2 className="h-5 w-5 text-emerald-400" strokeWidth={2} />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-100">
              Tabular Inspection
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Detailed row-by-row data analysis
            </p>
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2">
          {/* Copy button */}
          <button
            onClick={handleCopyTable}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-bold transition-all duration-300 ${
              copied
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                : 'bg-slate-800/60 text-slate-300 border border-slate-700/50 hover:text-slate-100 hover:bg-slate-800/80'
            }`}
          >
            <Copy className="h-3.5 w-3.5" strokeWidth={2.5} />
            <span className="hidden sm:inline">{copied ? 'Copied' : 'Copy'}</span>
          </button>

          {/* Export button */}
          <button
            onClick={handleExport}
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-bold bg-slate-800/60 text-slate-300 border border-slate-700/50 hover:text-slate-100 hover:bg-slate-800/80 transition-all duration-300"
          >
            <Download className="h-3.5 w-3.5" strokeWidth={2.5} />
            <span className="hidden sm:inline">Export</span>
          </button>
        </div>
      </div>

      {/* Table container */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse" id="results-table">
          <thead>
            <tr className="border-b-2 border-slate-800 bg-gradient-to-r from-slate-900/60 to-slate-950/40">
              {/* Row index column */}
              <th className="py-4 px-5 text-[11px] font-black uppercase tracking-widest text-slate-400 w-12 text-center bg-slate-950/40">
                #
              </th>
              {columns.map((col) => (
                <th
                  key={col}
                  className="py-4 px-5 text-[11px] font-black uppercase tracking-widest text-slate-300 whitespace-nowrap hover:text-slate-100 transition-colors"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/40">
            {paginatedData.map((row, rowIdx) => {
              const absoluteIdx = page * PAGE_SIZE + rowIdx;
              return (
                <tr
                  key={absoluteIdx}
                  className="group hover:bg-gradient-to-r hover:from-slate-800/50 hover:to-slate-900/30 transition-all duration-200"
                >
                  {/* Row number */}
                  <td className="py-4 px-5 text-xs font-bold font-mono text-slate-500 text-center group-hover:text-slate-400 transition-colors bg-slate-950/20 group-hover:bg-slate-950/40">
                    {String(absoluteIdx + 1).padStart(2, ' ')}
                  </td>
                  {columns.map((col) => {
                    const cellValue = row[col];
                    const isNull = cellValue === null || cellValue === undefined;
                    return (
                      <td
                        key={col}
                        className="py-4 px-5 text-sm font-medium text-slate-300 group-hover:text-slate-100 font-mono whitespace-nowrap transition-colors group-hover:bg-slate-800/20"
                      >
                        {isNull ? (
                          <span className="text-slate-600 italic text-xs px-2 py-1 bg-slate-800/30 rounded text-center inline-block">
                            null
                          </span>
                        ) : typeof cellValue === 'number' ? (
                          <span className="text-amber-300">{cellValue.toLocaleString()}</span>
                        ) : (
                          String(cellValue)
                        )}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Enhanced footer bar with pagination */}
      <div className="flex items-center justify-between px-6 py-4 bg-slate-950/70 border-t border-slate-800/60">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-800/40 border border-slate-700/40 rounded-lg">
            <Hash className="h-3.5 w-3.5 text-indigo-400" strokeWidth={2.5} />
            <span className="text-xs font-bold text-slate-300">
              {totalRows.toLocaleString()} row{totalRows !== 1 ? 's' : ''}
            </span>
          </div>
          <span className="text-xs text-slate-500">•</span>
          <span className="text-xs text-slate-500">
            Showing {page * PAGE_SIZE + 1}–{Math.min((page + 1) * PAGE_SIZE, totalRows)} of {totalRows}
          </span>
        </div>

        {/* Pagination controls */}
        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-slate-500">
            {columns.length} column{columns.length !== 1 ? 's' : ''}
          </span>

          {totalPages > 1 && (
            <div className="flex items-center gap-1.5 ml-3 pl-3 border-l border-slate-700/50">
              <button
                id="table-prev-btn"
                onClick={handlePrev}
                disabled={page === 0}
                className="p-1.5 rounded-lg bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                <ChevronLeft className="h-4 w-4" strokeWidth={2.5} />
              </button>
              <span className="text-xs font-bold text-slate-400 font-mono px-3 py-1 bg-slate-800/40 border border-slate-700/40 rounded-lg">
                {page + 1} / {totalPages}
              </span>
              <button
                id="table-next-btn"
                onClick={handleNext}
                disabled={page >= totalPages - 1}
                className="p-1.5 rounded-lg bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                <ChevronRight className="h-4 w-4" strokeWidth={2.5} />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
