from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import Runnable
from tools.rag_index import retrieve_similar, load_vector_store
from langchain_core.runnables import Runnable
from transformers import pipeline
# Initialize LLM using openAI  for classify and suggestion part can using anyother as well
llm = OpenAI(temperature=0)

# Load the vector database build using build vector store function and simulated CAPA
model, index, texts, metadata = load_vector_store()
#initialze summarization model bart-large-cnn
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class RagSummarizeRunnable(Runnable):
    def invoke(self, input: dict) -> dict:
        query_text = input["text"]
        docs = retrieve_similar(query_text, model, index, texts, metadata, k=3)
        combined_text = "\n\n".join([doc for doc, _ in docs])
        summary = summarizer(combined_text, max_length=150, min_length=50, do_sample=False)
        return {"summary": summary[0]["summary_text"]}



SummarizeChain = RagSummarizeRunnable()

# ClassifyChain
classify_prompt = PromptTemplate(
    input_variables=["summary"],
    template="Based on this summary, classify the root cause:\n\n{summary}"
)
ClassifyChain = LLMChain(llm=llm, prompt=classify_prompt) #text-davinci-003

# SuggestChain
suggest_prompt = PromptTemplate(
    input_variables=["root_cause"],
    template="Suggest CAPA corrective and preventive actions for this root cause:\n\n{root_cause}"
)
SuggestChain = LLMChain(llm=llm, prompt=suggest_prompt) #text-davinci-003



