import vine from '@vinejs/vine'

export const locationsSchema = vine.compile(
  vine.object({
    locations: vine.array(vine.string()),
  })
)