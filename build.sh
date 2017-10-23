
RUN_DIR="${PWD}"
SHADERS_DIR='shaders/'
SCENE_FILE='scene.rib'

cd $SHADERS_DIR
for f in *.osl; do
    oslc "$f"
done
cd $RUN_DIR

render "$SCENE_FILE"