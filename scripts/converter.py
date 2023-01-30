import hashlib
import re

from rdflib import URIRef, Literal, Graph
from rdflib.namespace import RDF, RDFS, OWL

isa_relations = {
    'isa',
    'is_child_of',
    'is_a_sub_class_of',
    'has_sub_class'
}

inverse_relations = {
    'has_child': 'isa',
    'has_part': 'part_of',
    'has_sub_class': 'is_a_sub_class_of',
    'is_contained_in': 'contains',
    'is_affected_by': 'affects',
    'is_managed_by': 'manages',
    'is_treated_by': 'treats',
    'is_disrupted_by': 'disrupts',
    'is_complicated_by': 'complicates',
    'is_prevented_by': 'prevents',
    'is_enhanced_by': 'enhances',
    'are_enhanced_by': 'enhances',
    'has_result': 'result_of'
}

alternative_form = {
    'is_part_of': 'part_of',
    'are_part_of': 'part_of',
    'include': 'contains',
    'is_result_of': 'result_of'
}


def term_to_uri(term: str) -> URIRef:
    """
    Generate a URI from a term.
    """
    normalized = term.lower().replace(' ', '_')
    return URIRef(f"https://example.org/{normalized}")


def get_concept_node(term: str):
    """
    Get concept triples to add to the graph.
    """
    node = term_to_uri(term)
    return node, [
        (node, RDF.type, OWL.Class),
        (node, RDFS.label, Literal(term))
    ]


def get_relation_node(concept_a: URIRef, concept_b: URIRef, relation_name: str):
    """
    Generate triples based on two concepts and the relation between them.
    """
    # normalize inverse relations
    if relation_name in inverse_relations.keys():
        relation_name = inverse_relations.get(relation_name)
        tmp = concept_a
        concept_a = concept_b
        concept_b = tmp

    # handle hierarchical
    if relation_name in isa_relations:
        return None, [
            (concept_a, RDFS.subClassOf, concept_b)
        ]

    relation = term_to_uri(
        hashlib.md5(f'{concept_a.toPython()}-{relation_name}-{concept_b.toPython()}'.encode()).hexdigest())

    return relation, [
        (relation, RDFS.label, Literal(relation_name)),
        (relation, RDFS.domain, concept_a),
        (relation, RDFS.range, concept_b),
        (relation, RDF.type, OWL.ObjectProperty)
    ]


def debug_print(relation, concept_a, concept_b, entries3):
    if relation in inverse_relations:
        cp1 = concept_b
        cp2 = concept_a
    else:
        cp1 = concept_a
        cp2 = concept_b

    if len(entries3) > 1:
        print(cp1, entries3[0][2].toPython(), cp2, sep=', ', )
    else:
        print(cp1, 'isa', cp2, sep=', ', )


def raw_relations_to_graph(file: str) -> Graph:
    """
    Generate a graph from the output of ChatGPT.
    """
    with open(file, 'r') as f:
        relations = f.readlines()

    g = Graph()

    for relation in relations:
        match = re.search(r"\[?(.*)]-\((.*)\)->\[(.*)]", relation)

        if not match:
            continue

        concept_a = match.group(1)
        concept_b = match.group(3)
        relation = match.group(2)
        c1, entries1 = get_concept_node(concept_a)
        c2, entries2 = get_concept_node(concept_b)

        relation = alternative_form.get(relation, relation)

        rl, entries3 = get_relation_node(c1, c2, relation)

        # print in CSV format.
        debug_print(relation, concept_a, concept_b, entries3)

        for triple in (entries1 + entries2 + entries3):
            g.add(triple)

    return g


if __name__ == '__main__':
    INPUT_FILE = '../supporting-files/ontology.rela'
    OUTPUT_FILE = '../supporting-files/ontology.xml'

    graph = raw_relations_to_graph(INPUT_FILE)
    graph.serialize(OUTPUT_FILE, format='pretty-xml')
