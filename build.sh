
RUN_DIR="${PWD}"
SHADERS_DIR='shaders/'
SCENE_NAME='scene'

cd $SHADERS_DIR
for f in *.osl; do
    oslc "$f"
done
cd $RUN_DIR

python "$SCENE_NAME".py
render "$SCENE_NAME".rib