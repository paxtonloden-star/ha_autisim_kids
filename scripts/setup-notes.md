# Setup notes

This repo currently focuses on the Home Status Board for Predictability, Nonverbal Request Buttons, and Visual Countdown Timer Board.

Suggested setup order:
1. verify people entities
2. verify calendar entities
3. verify weather entity
4. install through HACS or load the package manually
5. customize helper values and request/timer options
6. build the kid-facing dashboard

Known limitation in the starter:
- Now is based on the active kid calendar event.
- Next is based on the family calendar entity state.
- Later is currently helper-backed for simplicity.
- example dashboard button and number entity IDs may need to be adjusted after installation
