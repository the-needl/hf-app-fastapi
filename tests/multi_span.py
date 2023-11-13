from span_marker import SpanMarkerModel

def launch_n_instances(model_name, n):
    instances = []
    for _ in range(n):
        instance = SpanMarkerModel.from_pretrained(model_name)
        instances.append(instance)
    return instances

# Example usage:
model_name =

"tomaarsen/span-marker-mbert-base-multinerd" --> 15 categories
"tomaarsen/span-marker-bert-base-cross-ner" --> 39 categories
"tomaarsen/span-marker-bert-base-fewnerd-fine-super" --> 66 categories

n_instances = 10

instances_list = launch_n_instances(model_name, n_instances)

# Now you have a list of N instances of the pipeline model that you can use
# Each instance in the list can be used independently for text processing tasks.
