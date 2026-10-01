const summaryNode = document.getElementById('report-summary');
const listNode = document.getElementById('report-list');

const mockReport = {
  summary: { error: 2, warning: 4, info: 1 },
  issues: [
    {
      rule_id: 'COVER_TITLE_ALIGNMENT',
      severity: 'error',
      message: 'Title is missing or inconsistent with the template.',
      location: 'cover',
      suggestion: 'Use a consistent title and align it to the center format.'
    },
    {
      rule_id: 'REFERENCE_SEQUENCE',
      severity: 'error',
      message: 'Reference numbering does not start from [1].',
      location: 'references',
      suggestion: 'Renumber references sequentially from [1].'
    },
    {
      rule_id: 'SUMMARY_SECTION',
      severity: 'warning',
      message: 'The conclusion section is missing.',
      location: 'section',
      suggestion: 'Add a summary and outlook chapter without adding a chapter number.'
    }
  ]
};

summaryNode.textContent = `错误: ${mockReport.summary.error} / 警告: ${mockReport.summary.warning} / 信息: ${mockReport.summary.info}`;

mockReport.issues.forEach((issue) => {
  const item = document.createElement('div');
  item.className = `issue-card ${issue.severity}`;
  item.innerHTML = `
    <div class="meta-row">
      <span class="badge ${issue.severity}">${issue.severity}</span>
      <span>${issue.rule_id}</span>
      <span>${issue.location}</span>
    </div>
    <h3>${issue.message}</h3>
    <p><strong>建议：</strong> ${issue.suggestion}</p>
  `;
  listNode.appendChild(item);
});
