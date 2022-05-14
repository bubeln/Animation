# Animation

To run program you have to:
1. install locally methods from the file `/packages/__init__.py` running the command
```commandline
pip install .
```
2. Upload your `gameplay.json` file to the directory `/productions/` and change the value of the `GAMEPLAY_PATH` variable in the file `/data/common_variables.py`
3. Make sure that all characters, item and locations used in your gameplay are added in the `/graphics` folder in the proper section
   1. Items and characters used in not animated actions should be saved with `.png` extension
   2. Items and characters used in animated actions should be saved with `.svg` extension
   3. Locations and location front object should be saved with `.png` extension
   4. Background files should have at least the size 1000 x 720
   5. If the location has the front object, it's data should be written down in the `/data/location_front_objects.json`
4. Check if instructions related to the action are added to the `/productions/action_results.json`
5. If the gameplay includes actions that should be animated, make sure a template for that action is present in the `/graphics/action_template`, action data added in the `/data/action_data.json` and the action title added in the `/data/common_variables.py` in the list `ANIMATED_ACTIONS`
6. Run the main class `Animation` in the `/main/animation.py` directory