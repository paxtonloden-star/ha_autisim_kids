# Customization

## Replace placeholder entities in YAML examples

Update these to your real Home Assistant entities:
- calendar.kid_schedule
- calendar.family
- person.mom
- person.dad
- weather.home

## Integration options

The config flow sets the core entities.
The options flow lets you choose helper entities and fallback text:
- special change input_text
- dinner input_text
- bedtime input_datetime
- school tomorrow input_boolean
- now fallback text
- next fallback text
- later fallback text
- create persistent notifications for request buttons
- request notification title

## Built-in request buttons

The integration creates request buttons such as Help, Drink, Snack, Bathroom, Break, Hug, Quiet, Too Loud, Mad, Sad, and All Done.

When pressed, they update:
- Kid Last Request
- Kid Last Request Time

If request notifications are enabled, they also create a persistent notification in Home Assistant.

## Suggested kid-friendly improvements

- larger dashboard cards
- softer theme colors
- picture cards instead of text tiles
- first/then card under the status board
- calendar-specific next and later logic
- custom dashboard per room or tablet
