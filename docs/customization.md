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
- create persistent notifications for requests
- request notification title
- create persistent notifications for timer completion
- timer notification title
- preset 1 minutes
- preset 2 minutes
- preset 3 minutes

## Built-in request buttons

The integration creates request buttons such as Help, Drink, Snack, Bathroom, Break, Hug, Quiet, Too Loud, Mad, Sad, and All Done.

When pressed, they update:
- Kid Last Request
- Kid Last Request Time

If request notifications are enabled, they also create a persistent notification in Home Assistant.

## Built-in visual timer

The integration creates timer controls and sensors:
- Custom Timer Minutes number
- preset start buttons
- custom start button
- pause, resume, and cancel buttons
- Kid Timer Remaining
- Kid Timer Status
- Kid Timer Label

If timer notifications are enabled, completing a timer creates a persistent notification.

## Suggested kid-friendly improvements

- larger dashboard cards
- softer theme colors
- picture cards instead of text tiles
- first/then card under the status board
- calendar-specific next and later logic
- custom dashboard per room or tablet
