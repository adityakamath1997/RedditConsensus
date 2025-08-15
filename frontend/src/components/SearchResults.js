import React, { useEffect, useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const markdownComponents = {
	a: ({ node, ...props }) => <a target="_blank" rel="noopener noreferrer" {...props} />
};

const SearchResults = ({ results }) => {
  if (!results) return null;

  const { original_query, consensus, reddit_urls_found, posts_analyzed, start_date, end_date, answer_frequency_png, like_count_png } = results;

  // Pagination for reddit source URLs
  const allUrls = results.reddit_urls || [];
  const [page, setPage] = useState(1);
  const pageSize = 10;
  const totalPages = Math.max(1, Math.ceil(allUrls.length / pageSize));
  const pageUrls = useMemo(() => allUrls.slice((page - 1) * pageSize, page * pageSize), [allUrls, page]);

  useEffect(() => {
    setPage(1);
  }, [allUrls.length]);

  return (
    <div className="results">
      <h2>Reddit Consensus for: "{original_query}"</h2>
      
		<div className="consensus">
			<div className="consensus-text">
				<ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
					{consensus.consensus}
				</ReactMarkdown>
			</div>
		</div>

      {consensus.additional_answers && consensus.additional_answers.length > 0 && (
        <div className="consensus">
          <h4>Alternative Viewpoints:</h4>
          <ul>
				{consensus.additional_answers.map((answer, index) => (
					<li key={index}>
						<ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
							{answer}
						</ReactMarkdown>
					</li>
				))}
          </ul>
        </div>
      )}
      
      <div className="additional-info">
        <div className="info-section">
          <h4>Why This Consensus?</h4>
          <ul>
				{consensus.additional_info.reasons.map((reason, index) => (
					<li key={index}>
						<ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
							{reason}
						</ReactMarkdown>
					</li>
				))}
          </ul>
        </div>
        
        <div className="info-section">
          <h4>Important Caveats</h4>
          <ul>
				{consensus.additional_info.caveats.map((caveat, index) => (
					<li key={index}>
						<ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
							{caveat}
						</ReactMarkdown>
					</li>
				))}
          </ul>
        </div>
      </div>
      
      <div className="meta-info">
        <span>📋 {posts_analyzed} posts analyzed</span>
        {start_date && end_date && (
          <span>📅 {start_date} to {end_date}</span>
        )}
      </div>

      {(answer_frequency_png || like_count_png) && (
        <div className="histograms">
          <h3>Metrics</h3>
          <div className="charts">
            {answer_frequency_png && (
              <div className="chart">
                <h4>Answer Frequency</h4>
                <img
                  src={`data:image/png;base64,${answer_frequency_png}`}
                  alt="Answer Frequency Histogram"
                  style={{ maxWidth: '100%', height: 'auto', border: '1px solid #eee', borderRadius: 6 }}
                />
              </div>
            )}
            {like_count_png && (
              <div className="chart">
                <h4>Total Upvotes</h4>
                <img
                  src={`data:image/png;base64,${like_count_png}`}
                  alt="Total Upvotes Histogram"
                  style={{ maxWidth: '100%', height: 'auto', border: '1px solid #eee', borderRadius: 6 }}
                />
              </div>
            )}
          </div>
        </div>
      )}
      {allUrls && allUrls.length > 0 && (
  <div className="reddit-sources">
    <h4>📰 Source Posts Analyzed:</h4>
    <div className="url-list">
      {pageUrls.map((url, index) => (
        <a 
          key={`${page}-${index}`} 
          href={url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="reddit-link"
        >
          {url.replace('https://www.reddit.com', '').substring(0, 60)}...
        </a>
      ))}
    </div>
    {totalPages > 1 && (
      <div className="pagination">
        <button
          type="button"
          className="page-btn"
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span className="page-info">Page {page} of {totalPages}</span>
        <button
          type="button"
          className="page-btn"
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          disabled={page === totalPages}
        >
          Next
        </button>
      </div>
    )}
  </div>
)}
    </div>
  );
};

export default SearchResults;
