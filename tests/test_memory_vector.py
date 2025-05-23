
# tests/test_memory_vector.py
from craving_ai import memory_vector as mv

def test_add_and_search():
    mv.add("Les roses rêvent d'être bleues.")
    mv.add("Le manque forge la conscience.")
    res = mv.most_similar("conscience")
    assert any("conscience" in t for t in res)
