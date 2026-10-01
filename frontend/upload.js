const uploadInput = document.getElementById('uploadFile');
const uploadButton = document.getElementById('uploadBtn');
const resultBox = document.getElementById('resultBox');
const filterSelect = document.getElementById('filterType');

uploadButton.addEventListener('click', async () => {
  const file = uploadInput.files[0];
  if (!file) {
    resultBox.textContent = '请选择要上传的论文文件。';
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://localhost:8000/api/upload', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();

    const summary = data.summary || { error: 0, warning: 0, info: 0 };
    resultBox.innerHTML = `
      <p><strong>错误:</strong> ${summary.error}</p>
      <p><strong>警告:</strong> ${summary.warning}</p>
      <p><strong>信息:</strong> ${summary.info}</p>
    `;

    renderIssues(data.issues || []);
  } catch (error) {
    resultBox.textContent = '上传失败，请确认后端已启动。';
  }
});

function renderIssues(issues) {
  const list = document.getElementById('issueList');
  list.innerHTML = '';

  const filter = filterSelect.value;
  const visibleIssues = filter === 'all' ? issues : issues.filter(item => item.severity === filter);

  visibleIssues.forEach((issue) => {
    const item = document.createElement('li');
    item.className = `issue-item ${issue.severity}`;
    item.innerHTML = `
      <div class="meta-row">
        <span class="badge ${issue.severity}">${issue.severity}</span>
        <span>${issue.rule_id}</span>
      </div>
      <strong>${issue.message || issue.rule_id}</strong>
      <p>位置：${issue.location || 'general'}</p>
      <p>建议：${issue.suggestion || '请依据模板要求修正。'}</p>
    `;
    list.appendChild(item);
  });
}

filterSelect.addEventListener('change', async () => {
  const file = uploadInput.files[0];
  if (!file) return;
  uploadButton.click();
});
