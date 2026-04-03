# Automations

## Example: notify parent when Help is requested

```yaml
automation:
  - alias: Notify when help is requested
    triggers:
      - trigger: state
        entity_id: sensor.kid_last_request
        to: Help
    actions:
      - action: notify.mobile_app_parent_phone
        data:
          message: "Help requested"
```

## Example: react when timer finishes

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
