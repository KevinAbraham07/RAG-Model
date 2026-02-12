function SourcePanel({ sources, onClose }) {
  return (
    <div className="fixed right-0 top-0 h-screen w-96 bg-slate-800/95 backdrop-blur-sm border-l border-slate-700 shadow-2xl overflow-hidden flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-slate-700 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Retrieved Sources
        </h2>
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-white transition-colors"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Sources List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {sources.map((source, index) => (
          <div
            key={index}
            className="bg-slate-700/50 border border-slate-600 rounded-lg p-4 hover:border-blue-500 transition-colors"
          >
            <div className="flex items-start justify-between mb-2">
              <span className="text-xs font-semibold text-blue-400">
                Source {index + 1}
              </span>
              <div className="flex items-center gap-1">
                <svg className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <span className="text-xs text-slate-300 font-medium">
                  {(source.score * 100).toFixed(1)}%
                </span>
              </div>
            </div>
            
            <p className="text-xs text-slate-400 mb-2 flex items-center gap-1">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              {source.source.split('\\').pop().split('/').pop()}
            </p>
            
            <p className="text-sm text-slate-200 leading-relaxed">
              {source.text.length > 300 
                ? source.text.substring(0, 300) + '...' 
                : source.text}
            </p>
            
            <div className="mt-2 text-xs text-slate-500">
              Chunk {source.chunk_id + 1} of {source.total_chunks}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SourcePanel
