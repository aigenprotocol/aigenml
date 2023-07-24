<div align="center">
<h2> AigenML </h2>
<h3>
Aigen's artificial intelligence library to extract model weights and create shards based on the number of ainfts specified
</h3>
</div>

## create environment variables

#### create a .env file and put these variables

```
MODELS_DIR=/Users/apple/aigen
```

## commands

#### extract model weights and create shards in a single command

```
python main.py --action "create_shards" -n "test" -m "<path-to-model.h5>" -no 20
```
provide model name, model path and no of ainfts to create
* For the time being, we only support Keras models

## code

### extract and save model weights

```
from aigenml import save_model
save_model(model_name=model_name, model_dir=MODELS_DIR, model_path=model_path)
```

provide model name and local model path to start extracting weights

### create shards of model weights

```
from aigenml import create_shards
create_shards(model_name=model_name, model_dir=MODELS_DIR, no_of_ainfts=no_of_ainfts)
```

provide model name and no of ainfts to create. This function will automatically create shards of model weights


### merge model shards

```
python main.py --action "merge_shards" --name test
```
this will merge shards back to recover the original weight files


### load model (keras)

```
python main.py --action "load_model" --name test
```
this will load model from merged shards
