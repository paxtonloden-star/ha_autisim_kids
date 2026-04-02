# Automations

## Triggering from request buttons

Button entities in Home Assistant update their state timestamp whenever they are pressed.
That means you can trigger an automation from a state change on a request button.

Example:

```yaml
automation:
  - alias: Notify when help is requested
    triggers:
      - trigger: state
        entity_id: button.request_help
    actions:
      - action: notify.mobile_app_parent_phone
        data:
          message: "Help requested"
```

## Using the last request sensors

You can also react to the sensor values:

```yaml
automation:
  - alias: Calm room when too loud is requested
    triggers:
      - trigger: state
        entity_id: sensor.kid_last_request
        to: Too Loud
    actions:
      - action: scene.turn_on
        target:
          entity_id: scene.calm_mode
```

## Reacting to timer state

```yaml
automation:
  - alias: Turn room light yellow when timer is paused
    triggers:
      - trigger: state
        entity_id: sensor.kid_timer_status
        to: Paused
    actions:
      - action: light.turn_on
        target:
          entity_id: light.kid_room
        data:
          color_name: yellow
```

```yaml
automation:
  - alias: Chime when timer finishes
    triggers:
      - trigger: state
        entity_id: sensor.kid_timer_status
        to: Finished
    actions:
      - action: media_player.play_media
        target:
          entity_id: media_player.kid_room_speaker
        data:
          media_content_id: media-source://media_source/local/chime.mp3
          media_content_type: audio/mpeg
```

## Persistent notification option

If you enable request notifications or timer notifications in the integration options, those events also create a persistent notification in Home Assistant.
