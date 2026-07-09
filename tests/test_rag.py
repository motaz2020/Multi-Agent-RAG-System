from ai.rag.loader import load_documents, preprocess_text
from ai.rag.chunker import chunk_document
from ai.rag.context import build_context, build_rag_result


def test_load_documents(tmp_path):
    doc = tmp_path / "test_menu.txt"
    doc.write_text("Menu content here")
    docs = load_documents(str(tmp_path))
    assert len(docs) == 1
    assert docs[0]["metadata"]["document"] == "test_menu"


def test_preprocess_text_removes_page_numbers():
    text = "Some content\n\n5\n\nMore content"
    cleaned = preprocess_text(text)
    assert "5" not in cleaned


def test_chunk_document_small_content():
    chunks = chunk_document("Hello world", {"document": "test"})
    assert len(chunks) >= 1
    assert chunks[0]["metadata"]["chunk_index"] == 0


def test_chunk_document_with_overlap():
    content = "A " * 1000
    chunks = chunk_document(content, {"document": "test"})
    assert len(chunks) > 1


def test_build_context_empty():
    ctx = build_context([])
    assert ctx == ""


def test_build_context_with_chunks():
    chunks = [
        {"content": "Chunk one", "metadata": {"document": "menu"}},
        {"content": "Chunk two", "metadata": {"document": "policies"}},
    ]
    ctx = build_context(chunks)
    assert "Chunk one" in ctx
    assert "Chunk two" in ctx
    assert "[Source: menu]" in ctx


def test_build_context_deduplicates():
    chunks = [
        {"content": "Same text", "metadata": {"document": "menu"}},
        {"content": "Same text", "metadata": {"document": "policies"}},
    ]
    ctx = build_context(chunks)
    assert ctx.count("Same text") == 1


def test_build_rag_result():
    chunks = [
        {"content": "Chunk content", "metadata": {"document": "menu"}, "distance": 0.1},
    ]
    result = build_rag_result("Test answer", chunks)
    assert result["answer"] == "Test answer"
    assert result["sources"] == ["menu"]
    assert result["confidence"] > 0


def test_build_rag_result_no_chunks():
    result = build_rag_result("I don't know", [])
    assert result["confidence"] == 0.0
    assert result["sources"] == []
