# Training and prediction
Train model for your own wake Word/trigger word.
## Quick start
- `git clone https://github.com/dsinghnegi/custom-wake-word.git`
- `pip3 install requirement.txt`
- `cd ml_backend`
- `python3 train.py -o tr_model.th5 -d ./raw_data/activates`

 replace `./raw_data/activates` with your training data folder with Wav files.

## References and others open-source work used
Lots of idea and code are taken from [Sequence Models course on coursera.](https://www.coursera.org/learn/nlp-sequence-models/home/welcome)
