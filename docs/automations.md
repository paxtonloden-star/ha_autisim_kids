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

## Persistent notification option

If you enable request notifications in the integration options, button presses will also create a persistent notification in Home Assistant.
