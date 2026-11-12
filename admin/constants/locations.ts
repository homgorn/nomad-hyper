/**
 * Curated location catalog for NOMAD Hyper multi-location support.
 *
 * A location carries enough data to: filter content (ZIM collections, map
 * regions, plant DB), set the Meshtastic/LoRa frequency, and localize weather.
 * The catalog is static — user-created locations are a future change; selection
 * state lives in KVStore under 'content.selectedLocations'.
 *
 * Kyrgyzstan is the primary deployment region; neighbours are included because
 * field teams routinely operate across the border. An empty selection means
 * unrestricted access (the pre-multi-location behaviour).
 */

export interface LocationDef {
  id: string
  name: string
  country: string
  region: string
  lat: number
  lon: number
  /** LoRa frequency for Meshtastic/MeshCore in this region (MHz, KZ = 433). */
  loraFrequency: number
  timezone: string
}

export const LOCATION_CATALOG: readonly LocationDef[] = [
  { id: 'offgrid-any', name: 'Off-grid (no fixed region)', country: '', region: '', lat: 0, lon: 0, loraFrequency: 433.0, timezone: 'UTC' },
  { id: 'kg-bishkek', name: 'Bishkek', country: 'Kyrgyzstan', region: 'Chui', lat: 42.8746, lon: 74.5698, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kg-chui', name: 'Chui Oblast', country: 'Kyrgyzstan', region: 'Chui', lat: 42.9, lon: 75.2, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kg-osh', name: 'Osh', country: 'Kyrgyzstan', region: 'Osh', lat: 40.5283, lon: 72.7985, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kg-jalal-abad', name: 'Jalal-Abad', country: 'Kyrgyzstan', region: 'Jalal-Abad', lat: 40.9336, lon: 73.0099, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kg-batken', name: 'Batken', country: 'Kyrgyzstan', region: 'Batken', lat: 40.0597, lon: 70.82, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kg-naryn', name: 'Naryn', country: 'Kyrgyzstan', region: 'Naryn', lat: 41.4287, lon: 75.9911, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kg-talas', name: 'Talas', country: 'Kyrgyzstan', region: 'Talas', lat: 42.5162, lon: 72.2422, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kg-issyk-kul', name: 'Issyk-Kul Oblast', country: 'Kyrgyzstan', region: 'Issyk-Kul', lat: 42.4833, lon: 76.8333, loraFrequency: 433.0, timezone: 'Asia/Bishkek' },
  { id: 'kz-almaty', name: 'Almaty', country: 'Kazakhstan', region: 'Almaty', lat: 43.222, lon: 76.8512, loraFrequency: 433.0, timezone: 'Asia/Almaty' },
  { id: 'kz-astana', name: 'Astana', country: 'Kazakhstan', region: 'Astana', lat: 51.1694, lon: 71.4491, loraFrequency: 433.0, timezone: 'Asia/Almaty' },
  { id: 'uz-tashkent', name: 'Tashkent', country: 'Uzbekistan', region: 'Tashkent', lat: 41.2995, lon: 69.2401, loraFrequency: 433.0, timezone: 'Asia/Tashkent' },
  { id: 'tj-dushanbe', name: 'Dushanbe', country: 'Tajikistan', region: 'Dushanbe', lat: 38.5598, lon: 68.787, loraFrequency: 433.0, timezone: 'Asia/Dushanbe' },
] as const

export const LOCATION_IDS: ReadonlySet<string> = new Set(LOCATION_CATALOG.map((l) => l.id))