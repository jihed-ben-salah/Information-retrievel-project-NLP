from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import torch
from sklearn.metrics import accuracy_score


# Load the dataset
df_train = pd.read_csv("train.csv")
df_eval = df_train.iloc[0:200,:]

# Load the pre-trained BERT tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='steps',
    eval_steps=20,
    save_strategy='steps',
    save_steps=1000,
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    num_train_epochs=1,
    weight_decay=0.01,
    push_to_hub=False,
    logging_steps=500,
    
  
    load_best_model_at_end=False,  # Set to False
    metric_for_best_model='accuracy',
)

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc}

# Define the training and evaluation datasets
class MyDataset(torch.utils.data.Dataset):
    def __init__(self, df, tokenizer, prompt=None):
        self.df = df
        self.tokenizer = tokenizer
        self.prompt = prompt

    def __getitem__(self, index):
        row = self.df.iloc[index]
        text = row['text']
        if self.prompt is not None:
            text = f"{self.prompt} {text}"
        inputs = self.tokenizer.encode_plus(text, max_length=128, padding='max_length', truncation=True, return_tensors='pt')
        labels = torch.tensor(row['target'])
        return {'input_ids': inputs['input_ids'][0], 'attention_mask': inputs['attention_mask'][0], 'labels': labels}

    def __len__(self):
        return len(self.df)


# defining the different prompting methods

template_prompt = {"method":"template prompting","text":"Given the following tweet, predict whether it is related to a disaster or not: "}
conditional_prompt = {"method":"conditional prompting","text":"If the tweet contains the word 'fire', it is related to a disaster. "}

prompts = [template_prompt,conditional_prompt]
#
for prp in prompts:
    print(prp['method'])
    train_dataset = MyDataset(df_train, tokenizer,prompt=prp['text'])
    eval_dataset = MyDataset(df_eval, tokenizer,prompt=prp['text'])

    # Define the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    
   
    )

    # Train the model
    trainer.train()

    # Evaluate the model
    trainer.evaluate()

# Make predictions on new data