from datasets import load_dataset
from presidio_analyzer import (
    AnalyzerEngine,
    BatchAnalyzerEngine,
    RecognizerResult,
    DictAnalyzerResult,
)
import pandas as pd

# Insert custom regular expressions here or include in a JSON/YAML file
dataset = load_dataset("loubnabnl/code_pii_data")
code_content = dataset["train"]["content"]
code_content_df = pd.DataFrame(code_content, columns=["content"])
print(f"Analyzing {len(code_content_df)} code snippets")
analyzer = AnalyzerEngine()
# Add regexes to analyzer here
batch_analyzer = BatchAnalyzerEngine(analyzer_engine=analyzer)
analyzer_results = batch_analyzer.analyze_dict(
    code_content_df.to_dict(orient="list"),
    language="en",
)
detected_entities_list = []
for result in analyzer_results:
    recognizer_results = result.recognizer_results
    content = result.value
    for recognizer_result, code in zip(recognizer_results, content):
        entities = []
        for entity in recognizer_result:
            if entity.score >= 0.5:
                entities.append([entity.entity_type, code[entity.start : entity.end]])
        current_code_entities = [code, len(code), entities]
        detected_entities_list.append(current_code_entities)
df = pd.DataFrame(detected_entities_list, columns=["code", "length", "entities"])
df.to_csv("entity_list.csv")
