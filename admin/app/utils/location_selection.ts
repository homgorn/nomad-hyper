/**
 * Pure helpers for the multi-location selection stored in KVStore
 * ('content.selectedLocations', a JSON string array of catalog ids).
 *
 * Stored state is parsed defensively: anything unexpected (invalid JSON,
 * non-array, unknown ids) resolves to the empty selection, which means
 * "unrestricted" — the pre-multi-location behaviour. Never throw on read.
 */

/** Parse the raw KV string into a validated, deduplicated selection. */
export function parseSelectedLocations(raw: string | null | undefined, catalogIds: ReadonlySet<string>): string[] {
  if (!raw) return []
  try {
    const parsed: unknown = JSON.parse(raw)
    if (!Array.isArray(parsed)) return []
    return dedupe(parsed.filter((x): x is string => typeof x === 'string' && catalogIds.has(x)))
  } catch {
    return []
  }
}

/** Serialize a selection for KV storage. Deduplicates, preserves catalog ids only. */
export function serializeSelectedLocations(ids: string[]): string {
  return JSON.stringify(dedupe(ids))
}

/** Split an arbitrary id list into catalog-valid and invalid entries. */
export function validateLocationIds(
  ids: unknown,
  catalogIds: ReadonlySet<string>
): { valid: string[]; invalid: string[] } {
  const valid: string[] = []
  const invalid: string[] = []
  if (!Array.isArray(ids)) return { valid, invalid }
  for (const id of ids) {
    if (typeof id === 'string' && catalogIds.has(id)) {
      if (!valid.includes(id)) valid.push(id)
    } else {
      invalid.push(String(id))
    }
  }
  return { valid, invalid: dedupe(invalid) }
}

function dedupe(ids: string[]): string[] {
  return [...new Set(ids)]
}