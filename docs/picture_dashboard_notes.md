# Picture-first dashboard notes

The `dashboards/kids_picture_first_v4.yaml` dashboard is designed to feel more like a visual choice board.

## Local image placeholders

This dashboard expects local images such as:

- `/local/autism_kids/morning.png`
- `/local/autism_kids/afternoon.png`
- `/local/autism_kids/evening.png`
- `/local/autism_kids/tomorrow.png`
- `/local/autism_kids/feeling_happy.png`
- `/local/autism_kids/feeling_sad.png`
- `/local/autism_kids/feeling_mad.png`
- `/local/autism_kids/feeling_worried.png`
- `/local/autism_kids/feeling_tired.png`
- `/local/autism_kids/feeling_overwhelmed.png`
- `/local/autism_kids/feeling_excited.png`
- `/local/autism_kids/calm_breathe.png`
- `/local/autism_kids/calm_squeeze.png`
- `/local/autism_kids/calm_sit.png`
- `/local/autism_kids/calm_help.png`
- `/local/autism_kids/story_current.png`

## Where to place them

Put the image files in Home Assistant under:

`/config/www/autism_kids/`

Home Assistant will expose those files as `/local/autism_kids/...`.

## Why this dashboard feels more tappable

- large button cards
- large picture cards
- explicit tap actions on key choices
- fewer words on each screen
- stable placement of the main choices
