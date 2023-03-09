from datasets import load_dataset
dataset = load_dataset("wicho/stylekqc-style")


for datapoint in dataset['train']:
    # this is actually... pretty useful?
    # yup, all I need is the "naturalness" score.
    print(datapoint['formal'])
    print(datapoint['informal'])
    break

