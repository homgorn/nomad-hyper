import { LocationService } from '#services/location_service'
import { locationsSchema } from '#validators/locations'
import type { HttpContext } from '@adonisjs/core/http'

export default class LocationsController {
  /** GET /api/locations — catalog plus current selection. */
  async index({ response }: HttpContext) {
    return response.json(await LocationService.index())
  }

  /** PUT /api/locations — set the multi-select selection. Empty list = unrestricted. */
  async update({ request, response }: HttpContext) {
    const { locations } = await request.validateUsing(locationsSchema)
    const result = await LocationService.setSelected(locations)
    if ('invalid' in result) {
      return response.status(422).json({
        error: 'Unknown location id(s)',
        invalid: result.invalid,
      })
    }
    return response.json({ selected: result.selected })
  }
}