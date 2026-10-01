(() => {
  const form = document.getElementById('check-form');
  const issuesList = document.getElementById('issues');
  const summaryBox = document.getElementById('summary');

  const buildPayload = () => {
    const title = document.getElementById('title').value.trim();
    const englishTitle = document.getElementById('englishTitle').value.trim();
    const abstract = document.getElementById('abstract').value.trim();
    const keywords = document.getElementById('keywords').value
      .split(',')
      .map(item => item.trim())
      .filter(Boolean);

    return {
      title,
      english_title: englishTitle,
      abstract,
      keywords,
      sections: [
        { title: '绪论', level: 1 },
        { title: '本章小结', level: 2 },
        { title: '总结与展望', level: 1 }
      ],
      references: [
        { id: 1, text: 'IEEE 802.11 standard' },
        { id: 2, text: 'WLAN architecture paper' },
        { id: 3, text: 'Academic wireless network design' },
        { id: 4, text: 'Campus network security review' }
      ],
      figures: [{ caption: '图2-1' }],
      tables: [{ caption: '表3-1' }]
    };
  };

  const renderIssues = (issues) => {
    issuesList.innerHTML = '';
    if (!issues || issues.length === 0) {
      issuesList.innerHTML = '<li class="issue-item info">没有发现问题。</li>';
      return;
    }

    issues.forEach(issue => {
      const item = document.createElement('li');
      item.className = `issue-item ${issue.severity}`;
      item.innerHTML = `
        <div class="issue-meta">
          <span class="badge ${issue.severity}">${issue.severity}</span>
          <span>${issue.rule_id}</span>
          <span>${issue.location || 'general'}</span>
        </div>
        <strong>${issue.title}</strong>
        <p>${issue.description}</p>
        <div><em>建议：</em> ${issue.suggestion}</div>
      `;
      issuesList.appendChild(item);
    });
  };

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    summaryBox.textContent = '正在检查...';

    try {
      const response = await fetch('http://localhost:8000/api/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(buildPayload())
      });

      const result = await response.json();
      const summary = result.summary || { error: 0, warning: 0, info: 0 };
      summaryBox.textContent = `错误: ${summary.error} / 警告: ${summary.warning} / 信息: ${summary.info}`;
      renderIssues(result.issues || []);
    } catch (error) {
      summaryBox.textContent = '检查失败，请确认后端服务已启动。';
      issuesList.innerHTML = `<li class="issue-item error">${error.message}</li>`;
    }
  });
})();
