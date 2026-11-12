import KVStore from '#models/kv_store'
import { LOCATION_CATALOG, LOCATION_IDS } from '../../constants/locations.js'
import {
  parseSelectedLocations,
  serializeSelectedLocations,
  validateLocationIds,
} from '../utils/location_selection.js'

/**
 * Multi-location selection. An empty selection means unrestricted (the
 * pre-multi-location behaviour) — never a restriction.
 */
export class LocationService {
  /** The catalog plus the persisted (validated) selection. */
  static async index() {
    const selected = await LocationService.getSelected()
    return { catalog: LOCATION_CATALOG, selected }
  }

  /** Validated selection ids; [] when unset or unreadable. */
  static async getSelected(): Promise<string[]> {
    const raw = await KVStore.getValue('content.selectedLocations')
    return parseSelectedLocations(typeof raw === 'string' ? raw : null, LOCATION_IDS)
  }

  /**
   * Persist the selection. Ids outside the catalog are rejected — the caller
   * should surface them as a 422, never store a half-valid list.
   * Returns the stored selection.
   */
  static async setSelected(ids: unknown): Promise<{ selected: string[] } | { invalid: string[] }> {
    const { valid, invalid } = validateLocationIds(ids, LOCATION_IDS)
    if (invalid.length > 0) {
      return { invalid }
    }
    await KVStore.setValue('content.selectedLocations', serializeSelectedLocations(valid))
    return { selected: valid }
  }
}