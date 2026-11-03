const REQUIRED_FIELDS = [
  'number',
  'title',
  'issue_date',
  'document_type',
  'issuing_authority',
  'archive_item_url',
];

export function filterDocuments(
  records,
  { query = '', year = '', type = '', authority = '' } = {},
) {
  if (!Array.isArray(records)) return [];

  const normalizedQuery = String(query).trim().toLocaleLowerCase();
  const selectedYear = String(year);
  const selectedType = String(type);
  const selectedAuthority = String(authority);

  return records.filter((record) => {
    const searchableText = `${record.title} ${record.number}`.toLocaleLowerCase();
    const matchesQuery = !normalizedQuery || searchableText.includes(normalizedQuery);
    const matchesYear = !selectedYear || record.issue_date.slice(0, 4) === selectedYear;
    const matchesType = !selectedType || record.document_type === selectedType;
    const matchesAuthority = !selectedAuthority || record.issuing_authority === selectedAuthority;
    return matchesQuery && matchesYear && matchesType && matchesAuthority;
  });
}

function isValidRecord(record) {
  return record && typeof record === 'object' &&
    REQUIRED_FIELDS.every((field) => typeof record[field] === 'string' && record[field].trim()) &&
    /^\d{4}-\d{2}-\d{2}$/.test(record.issue_date);
}

function addOptions(select, values) {
  const sorted = [...new Set(values)].sort((a, b) => a.localeCompare(b));
  for (const value of sorted) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    select.append(option);
  }
}

async function initializeDocumentFilters() {
  const form = document.getElementById('document-filters');
  const list = document.querySelector('.document-list');
  const status = document.getElementById('document-results-status');
  const emptyState = document.getElementById('document-empty-state');
  const loadError = document.getElementById('document-load-error');

  if (!form || !list || !status || !emptyState) return;

  try {
    const response = await fetch(new URL('../../data/documents.json', import.meta.url));
    if (!response.ok) throw new Error(`Document data returned HTTP ${response.status}`);

    const records = await response.json();
    if (!Array.isArray(records) || records.length !== 5 || !records.every(isValidRecord)) {
      throw new Error('Document data does not match the expected record shape.');
    }

    const cards = [...list.querySelectorAll('[data-document-number]')];
    const recordNumbers = records.map((record) => record.number);
    const cardNumbers = cards.map((card) => card.dataset.documentNumber);
    if (recordNumbers.length !== cardNumbers.length ||
        recordNumbers.some((number, index) => number !== cardNumbers[index])) {
      throw new Error('The static document list and structured records differ.');
    }

    const yearSelect = document.getElementById('document-year');
    const typeSelect = document.getElementById('document-type');
    const authoritySelect = document.getElementById('document-authority');
    if (!yearSelect || !typeSelect || !authoritySelect) return;

    addOptions(yearSelect, records.map((record) => record.issue_date.slice(0, 4)));
    addOptions(typeSelect, records.map((record) => record.document_type));
    addOptions(authoritySelect, records.map((record) => record.issuing_authority));

    const applyFilters = () => {
      const visibleRecords = filterDocuments(records, {
        query: document.getElementById('document-search')?.value ?? '',
        year: yearSelect.value,
        type: typeSelect.value,
        authority: authoritySelect.value,
      });
      const visibleNumbers = new Set(visibleRecords.map((record) => record.number));

      for (const card of cards) {
        card.hidden = !visibleNumbers.has(card.dataset.documentNumber);
      }
      emptyState.hidden = visibleRecords.length !== 0;
      status.textContent = `Showing ${visibleRecords.length} of ${records.length} records.`;
      status.hidden = false;
    };

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      applyFilters();
    });
    form.addEventListener('reset', () => {
      window.setTimeout(applyFilters, 0);
    });

    if (loadError) loadError.hidden = true;
    form.hidden = false;
    applyFilters();
  } catch {
    if (loadError) loadError.hidden = false;
  }
}

if (typeof document !== 'undefined') {
  void initializeDocumentFilters();
}
