# Can Large Language Models Augment a Biomedical Ontology with missing Concepts and Relations?

## Abstract 
Ontologies play a crucial role in organizing and representing knowledge. However, even current ontologies, do not
encompass all relevant concepts and relationships. Here, we explore the potential of large language models (LLM) to
expand an existing ontology in a semi-automated fashion. We demonstrate our approach on the biomedical ontology
SNOMED-CT utilizing semantic relation types from the widely-used UMLS semantic network. We propose a method that uses
conversational interactions with an LLM to analyze clinical practice guidelines (CPGs)
and detect the relationships among the new medical concepts that are not present in SNOMED-CT.  
We evaluate the method on a case study related to mindfulness-based clinical interventions taken from a CPG for
cancer-related fatigue and utilizing the ChatGPT LLM. Relative to a manually generated gold standard, our method
achieved a recall of 0.64 and a precision of 0.55. We discuss the results and limitations of our approach and suggest
potential avenues for future research.