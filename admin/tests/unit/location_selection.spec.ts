import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  parseSelectedLocations,
  serializeSelectedLocations,
  validateLocationIds,
} from '../../app/utils/location_selection.js'
import { LOCATION_CATALOG, LOCATION_IDS } from '../../constants/locations.js'

const catalog = new Set(LOCATION_CATALOG.map((l) => l.id))

test('parse returns empty for null/undefined/empty', () => {
  assert.deepEqual(parseSelectedLocations(null, catalog), [])
  assert.deepEqual(parseSelectedLocations(undefined, catalog), [])
  assert.deepEqual(parseSelectedLocations('', catalog), [])
})

test('parse returns empty for invalid JSON (defensive, never throws)', () => {
  assert.deepEqual(parseSelectedLocations('{not json', catalog), [])
  assert.deepEqual(parseSelectedLocations('"kg-bishkek"', catalog), [])
  assert.deepEqual(parseSelectedLocations('42', catalog), [])
  assert.deepEqual(parseSelectedLocations('{"a":1}', catalog), [])
})

test('parse filters unknown ids and dedupes', () => {
  const raw = JSON.stringify(['kg-bishkek', 'xx-nope', 'kg-osh', 'kg-bishkek'])
  assert.deepEqual(parseSelectedLocations(raw, catalog), ['kg-bishkek', 'kg-osh'])
})

test('serialize round-trips through parse', () => {
  const ids = ['kg-bishkek', 'kg-osh']
  assert.deepEqual(parseSelectedLocations(serializeSelectedLocations(ids), catalog), ids)
})

test('validateLocationIds splits valid/invalid and dedupes', () => {
  const { valid, invalid } = validateLocationIds(
    ['kg-bishkek', 'nope', 'kg-osh', 'kg-bishkek', 7],
    LOCATION_IDS
  )
  assert.deepEqual(valid, ['kg-bishkek', 'kg-osh'])
  assert.deepEqual(invalid, ['nope', '7'])
})

test('validateLocationIds handles non-array input', () => {
  assert.deepEqual(validateLocationIds('kg-bishkek', LOCATION_IDS), { valid: [], invalid: [] })
  assert.deepEqual(validateLocationIds(undefined, LOCATION_IDS), { valid: [], invalid: [] })
})