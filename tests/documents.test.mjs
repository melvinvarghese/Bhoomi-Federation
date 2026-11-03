import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { filterDocuments } from '../assets/js/documents.mjs';

const records = JSON.parse(
  await readFile(new URL('../data/documents.json', import.meta.url), 'utf8'),
);

const authority = 'Melvin Varghese, Chief Architect, The Bhoomi Federation';

const requiredPublicFields = [
  'number',
  'title',
  'issue_date',
  'document_type',
  'issuing_authority',
  'summary',
  'archive_item_url',
];

const editorialFields = [
  'canonical_source_url',
  'archive_file_url',
  'displayed_license',
  'redistribution_decision',
  'uncertainty_notes',
];

test('returns all five records in source order with no filters', () => {
  assert.deepEqual(filterDocuments(records), records);
});

test('public record data contains only the fields needed for the National Records section', () => {
  assert.equal(records.length, 5);
  for (const record of records) {
    for (const field of requiredPublicFields) assert.ok(record[field], `${record.number} is missing ${field}`);
    for (const field of editorialFields) assert.equal(Object.hasOwn(record, field), false, `${record.number} exposes ${field}`);
  }
});

test('trims a mixed-case partial title query', () => {
  assert.deepEqual(
    filterDocuments(records, { query: '  fOuNdInG  ' }).map((record) => record.number),
    ['BHF/003/2025'],
  );
});

test('searches the document number as well as its title', () => {
  assert.deepEqual(
    filterDocuments(records, { query: 'bhf/005' }).map((record) => record.number),
    ['BHF/005/2025'],
  );
});

test('treats empty and whitespace-only queries as no query', () => {
  assert.deepEqual(filterDocuments(records, { query: '' }), records);
  assert.deepEqual(filterDocuments(records, { query: '   ' }), records);
});

test('applies query, year, type, and authority together using exact filter values', () => {
  assert.deepEqual(
    filterDocuments(records, {
      query: 'national day',
      year: '2025',
      type: 'Proclamation',
      authority,
    }).map((record) => record.number),
    ['BHF/002/2025'],
  );
});

test('returns an empty array when combined filters have no match', () => {
  assert.deepEqual(
    filterDocuments(records, { query: 'Founding', year: '2024' }),
    [],
  );
});

test('does not broaden exact type or authority filters', () => {
  assert.deepEqual(filterDocuments(records, { type: 'proclamation' }), []);
  assert.deepEqual(filterDocuments(records, { authority: 'Melvin Varghese' }), []);
});

test('returns no records for an unknown query or filter value', () => {
  assert.deepEqual(filterDocuments(records, { query: 'not a document' }), []);
  assert.deepEqual(filterDocuments(records, { year: '1900', type: 'Unknown' }), []);
});
