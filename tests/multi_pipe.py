from transformers import pipeline

def launch_n_instances(model_name, n):
    instances = []
    for _ in range(n):
        instance = pipeline(task="text-classification", model=model_name)
        instances.append(instance)
    return instances

# Example usage:
# model_name = "sshleifer/distilbart-xsum-12-3"
# model_name = "transformer3/H2-keywordextractor"
model_name = "SamLowe/roberta-base-go_emotions"
"distilbert-base-uncased-finetuned-sst-2-english"
n_instances = 10

instances_list = launch_n_instances(model_name, n_instances)

# Now you have a list of N instances of the pipeline model that you can use
# Each instance in the list can be used independently for text processing tasks.
