"""Kiểm tra 9 nhóm bài bằng unittest; mặc định kiểm bài tập còn TODO.

    python kiem_tra.py --bai 1
    python kiem_tra.py --dap-an
    python kiem_tra.py --dap-an --bai 9

Exit 0 = tất cả test đã chọn đạt; exit 1 = chưa đạt/lỗi.
NotImplementedError ở chế độ mặc định là bình thường khi chưa làm bài.
"""

import argparse
import copy
import importlib
import json
import sys
import unittest


MODULE = None


def document(doc_id, text, title=""):
    return {"doc_id": doc_id, "title": title, "text": text,
            "source": f"ghi-chu/{doc_id}.md", "updated_at": "2026-09-11"}


def search_call(query="Python"):
    return {"name": "search_catalog", "args": {"query": query}}


class B01Normalize(unittest.TestCase):
    def test_vietnamese_case_and_punctuation(self):
        self.assertEqual(MODULE.normalize_text("  HỌC Phí: PYTHON! "), "học phí: python!")

    def test_unicode_whitespace_and_empty(self):
        self.assertEqual(MODULE.normalize_text("AI\t\n Engineer\u00a0 Việt\u2003Nam"),
                         "ai engineer việt nam")
        self.assertEqual(MODULE.normalize_text(" \n\t"), "")
        self.assertEqual(MODULE.normalize_text(""), "")

    def test_wrong_type(self):
        for value in (None, 4, True, []):
            with self.subTest(value=value), self.assertRaises(TypeError):
                MODULE.normalize_text(value)


class B02Chunk(unittest.TestCase):
    def test_overlap_and_short_final(self):
        self.assertEqual(MODULE.chunk_words("a b c d e f", 3, 1),
                         ["a b c", "c d e", "e f"])

    def test_no_redundant_overlap_only_chunk(self):
        self.assertEqual(MODULE.chunk_words("a b c d e", 3, 1), ["a b c", "c d e"])
        self.assertEqual(MODULE.chunk_words("a b c", 3, 2), ["a b c"])

    def test_no_overlap_and_preserve_case(self):
        self.assertEqual(MODULE.chunk_words("HỌC\tPython có dấu", 2, 0),
                         ["HỌC Python", "có dấu"])

    def test_empty_and_single_word(self):
        self.assertEqual(MODULE.chunk_words(" \n", 2, 1), [])
        self.assertEqual(MODULE.chunk_words("AI", 1, 0), ["AI"])

    def test_invalid_parameters_including_bool(self):
        for maximum, overlap in ((0, 0), (-1, 0), (True, 0), (2.0, 0),
                                 (3, -1), (3, 3), (3, 4), (3, True), (3, 1.0)):
            with self.subTest(maximum=maximum, overlap=overlap), self.assertRaises(ValueError):
                MODULE.chunk_words("", maximum, overlap)


class B03Search(unittest.TestCase):
    def setUp(self):
        self.docs = [document("b", "Học Python", "Khóa cơ bản"),
                     document("a", "Python Python", "Học phí"),
                     document("c", "Docker container", "DevOps")]

    def test_score_uses_distinct_query_tokens(self):
        rows = MODULE.lexical_search("PYTHON Python phí", self.docs)
        self.assertEqual([row["doc_id"] for row in rows], ["a", "b"])
        self.assertEqual([row["score"] for row in rows], [1.0, 0.5])

    def test_tie_by_id_and_k(self):
        rows = MODULE.lexical_search("Python", self.docs, k=1)
        self.assertEqual([row["doc_id"] for row in rows], ["a"])

    def test_empty_and_zero_hits(self):
        for query in ("", " \n ", "?!", "không_tồn_tại"):
            with self.subTest(query=query):
                self.assertEqual(MODULE.lexical_search(query, self.docs), [])
        self.assertEqual(MODULE.lexical_search("Python", []), [])

    def test_output_schema_and_no_mutation(self):
        original = copy.deepcopy(self.docs)
        rows = MODULE.lexical_search("phí", self.docs)
        self.assertEqual(rows, [{"doc_id": "a", "score": 1.0,
                                 "text": "Python Python", "source": "ghi-chu/a.md"}])
        self.assertEqual(self.docs, original)

    def test_invalid_k_even_for_empty_query(self):
        for k in (0, -1, True, False, 1.2, "3"):
            with self.subTest(k=k), self.assertRaises(ValueError):
                MODULE.lexical_search("", [], k=k)


class B04Recall(unittest.TestCase):
    def test_partial_recall(self):
        self.assertEqual(MODULE.recall_at_k(["x", "a", "b"], ["a", "b"], 2), 0.5)

    def test_dedup_before_cut_and_denominator(self):
        self.assertEqual(MODULE.recall_at_k(["a", "a", "b"], ["a", "a", "b"], 2), 1.0)

    def test_empty_relevant_is_na(self):
        self.assertIsNone(MODULE.recall_at_k(["a"], [], 3))
        self.assertIsNone(MODULE.recall_at_k([], [], 3))

    def test_empty_retrieved_is_zero(self):
        self.assertEqual(MODULE.recall_at_k([], ["a"], 3), 0.0)

    def test_invalid_k(self):
        for k in (0, -2, True, 2.0):
            with self.subTest(k=k), self.assertRaises(ValueError):
                MODULE.recall_at_k([], [], k)


class B05RRF(unittest.TestCase):
    def test_fusion_values(self):
        rows = MODULE.reciprocal_rank_fusion([["a", "b"], ["b", "c"]])
        self.assertEqual([row["doc_id"] for row in rows], ["b", "a", "c"])
        self.assertAlmostEqual(rows[0]["score"], 1 / 62 + 1 / 61)
        self.assertEqual(set(rows[0]), {"doc_id", "score"})

    def test_dedup_before_rank(self):
        rows = MODULE.reciprocal_rank_fusion([["a", "a", "b"]], rank_constant=2)
        self.assertEqual([row["doc_id"] for row in rows], ["a", "b"])
        self.assertAlmostEqual(rows[0]["score"], 1 / 3)
        self.assertAlmostEqual(rows[1]["score"], 1 / 4)

    def test_ties_and_empty_rankings(self):
        rows = MODULE.reciprocal_rank_fusion([["z"], [], ["a"]], k=1)
        self.assertEqual(rows, [{"doc_id": "a", "score": 1 / 61}])
        self.assertEqual(MODULE.reciprocal_rank_fusion([[], []]), [])

    def test_no_input_mutation(self):
        rankings = [["z", "z", "a"], ["a", "b"]]
        original = copy.deepcopy(rankings)
        MODULE.reciprocal_rank_fusion(rankings)
        self.assertEqual(rankings, original)

    def test_invalid_params(self):
        for k, constant in ((0, 60), (True, 60), (1.0, 60),
                            (3, 0), (3, -1), (3, True), (3, 60.0)):
            with self.subTest(k=k, constant=constant), self.assertRaises(ValueError):
                MODULE.reciprocal_rank_fusion([], k, constant)


class B06Answer(unittest.TestCase):
    def test_answer_and_abstention(self):
        self.assertIs(MODULE.validate_answer(
            {"answer": "Học Python", "citations": ["a"], "abstain": False}, {"a"}), True)
        self.assertIs(MODULE.validate_answer(
            {"answer": "Chưa đủ bằng chứng", "citations": [], "abstain": True}, []), True)

    def test_unknown_duplicate_or_missing_citations(self):
        for citations in (["unknown"], ["a", "a"], []):
            with self.subTest(citations=citations):
                self.assertFalse(MODULE.validate_answer(
                    {"answer": "Có", "citations": citations, "abstain": False}, ["a"]))

    def test_abstain_cannot_cite(self):
        self.assertFalse(MODULE.validate_answer(
            {"answer": "Không biết", "citations": ["a"], "abstain": True}, ["a"]))

    def test_strict_types_and_blank_answer(self):
        base = {"answer": "Có", "citations": ["a"], "abstain": False}
        for field, value in (("answer", " \n"), ("answer", 1), ("citations", "a"),
                             ("citations", [1]), ("abstain", 0), ("abstain", "false")):
            with self.subTest(field=field, value=value):
                self.assertFalse(MODULE.validate_answer({**base, field: value}, ["a"]))

    def test_exact_keys_and_malformed_input(self):
        for answer in (None, [], {}, {"answer": "a"},
                       {"answer": "Có", "citations": ["a"], "abstain": False, "extra": 1}):
            with self.subTest(answer=answer):
                self.assertFalse(MODULE.validate_answer(answer, ["a"]))

    def test_schema_is_not_grounding(self):
        self.assertTrue(MODULE.validate_answer(
            {"answer": "Một khẳng định chưa kiểm chứng", "citations": ["a"], "abstain": False},
            ["a"]))


class B07Tool(unittest.TestCase):
    def test_allowed_tools_and_hour_boundaries(self):
        self.assertTrue(MODULE.validate_tool_call(search_call("Học phí")))
        for hours in (1, 60):
            self.assertTrue(MODULE.validate_tool_call(
                {"name": "draft_plan", "args": {"topic": "AI", "hours_per_week": hours}}))

    def test_unknown_tools_and_blank_query(self):
        for call in ({"name": "delete_file", "args": {}}, search_call(" \t"), search_call(2)):
            with self.subTest(call=call):
                self.assertFalse(MODULE.validate_tool_call(call))

    def test_invalid_hours_including_bool(self):
        for hours in (0, 61, -1, True, 4.0, "4"):
            with self.subTest(hours=hours):
                self.assertFalse(MODULE.validate_tool_call(
                    {"name": "draft_plan", "args": {"topic": "AI", "hours_per_week": hours}}))

    def test_extra_and_missing_fields(self):
        for call in ({**search_call(), "approved": True},
                     {"name": "search_catalog", "args": {"query": "AI", "k": 3}},
                     {"name": "draft_plan", "args": {"topic": "AI"}},
                     {"name": "draft_plan", "args": {"topic": " ", "hours_per_week": 2}}):
            with self.subTest(call=call):
                self.assertFalse(MODULE.validate_tool_call(call))

    def test_malformed_input(self):
        for call in (None, [], {}, {"name": [], "args": {}}, {"name": "search_catalog", "args": []}):
            with self.subTest(call=call):
                self.assertIs(MODULE.validate_tool_call(call), False)


class B08Dedup(unittest.TestCase):
    def test_key_order_irrelevant_in_nested_objects(self):
        first = {"name": "draft_plan", "args": {"topic": "AI", "hours_per_week": 5}}
        reordered = {"args": {"hours_per_week": 5, "topic": "AI"}, "name": "draft_plan"}
        self.assertEqual(MODULE.deduplicate_calls([first, reordered]), [first])

    def test_preserve_first_order_and_different_arguments(self):
        a, b = search_call("Python"), search_call("AI")
        self.assertEqual(MODULE.deduplicate_calls([b, a, b, a]), [b, a])

    def test_empty_and_list_order_matters(self):
        self.assertEqual(MODULE.deduplicate_calls([]), [])
        calls = [{"items": [1, 2]}, {"items": [2, 1]}]
        self.assertEqual(MODULE.deduplicate_calls(calls), calls)

    def test_no_mutation(self):
        calls = [search_call("Có dấu"), search_call("Có dấu")]
        original = copy.deepcopy(calls)
        MODULE.deduplicate_calls(calls)
        self.assertEqual(calls, original)


class B09Agent(unittest.TestCase):
    def test_immediate_final_and_consistent_keys(self):
        result = MODULE.run_agent(lambda history: {"type": "final", "answer": "Xong"},
                                  lambda call: self.fail("Không được gọi tool"), max_steps=1)
        self.assertEqual(result, {"status": "completed", "answer": "Xong",
                                  "trace": [{"step": 1, "type": "final"}]})

    def test_tool_result_is_visible_to_policy(self):
        def policy(history):
            if not history:
                return {"type": "tool", "call": search_call()}
            self.assertEqual(history[0]["result"], {"found": 2})
            return {"type": "final", "answer": "Đã xem kết quả"}
        result = MODULE.run_agent(policy, lambda call: {"found": 2})
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["trace"][0]["cached"], False)

    def test_duplicate_calls_reuse_cache_and_count_steps(self):
        executions = []
        calls = [search_call(), {"args": {"query": "Python"}, "name": "search_catalog"}]
        def policy(history):
            if len(history) < 2:
                return {"type": "tool", "call": calls[len(history)]}
            return {"type": "final", "answer": "Xong"}
        result = MODULE.run_agent(policy, lambda call: executions.append(call) or ["a"])
        self.assertEqual(len(executions), 1)
        self.assertEqual([row["cached"] for row in result["trace"][:2]], [False, True])
        self.assertEqual(result["trace"][-1]["step"], 3)

    def test_step_limit_counts_every_policy_call(self):
        policy_calls, executions = [], []
        def policy(history):
            policy_calls.append(len(history))
            return {"type": "tool", "call": search_call()}
        result = MODULE.run_agent(policy, lambda call: executions.append(call) or [], max_steps=3)
        self.assertEqual(policy_calls, [0, 1, 2])
        self.assertEqual(len(executions), 1)
        self.assertEqual(result["status"], "step_limit")
        self.assertEqual(result["answer"], "")
        self.assertEqual(len(result["trace"]), 3)

    def test_bad_max_steps(self):
        for maximum in (0, -1, True, 3.0, "4"):
            with self.subTest(maximum=maximum), self.assertRaises(ValueError):
                MODULE.run_agent(lambda history: {}, lambda call: None, maximum)

    def test_invalid_actions_never_execute(self):
        actions = [None, [], {}, {"type": "unknown"}, {"type": "final", "answer": " "},
                   {"type": "final", "answer": "ok", "extra": 1},
                   {"type": "tool", "call": {"name": "delete_file", "args": {}}},
                   {"type": "tool", "call": search_call(" ")}]
        for action in actions:
            with self.subTest(action=action):
                result = MODULE.run_agent(lambda history: action,
                                          lambda call: self.fail("Tool không hợp lệ đã chạy"))
                self.assertEqual(result, {"status": "invalid_action", "answer": "",
                                          "trace": [{"step": 1, "type": "invalid_action"}]})

    def test_exception_messages_not_leaked(self):
        sentinel = "FAKE_SECRET_DO_NOT_PRINT"
        def fail_with_secret(value):
            raise RuntimeError(sentinel)
        for policy, executor in ((fail_with_secret, lambda call: []),
                                 (lambda history: {"type": "tool", "call": search_call()},
                                  fail_with_secret)):
            result = MODULE.run_agent(policy, executor)
            self.assertEqual(result["status"], "error")
            self.assertEqual(result["trace"],
                             [{"step": 1, "type": "error", "error_type": "RuntimeError"}])
            self.assertNotIn(sentinel, json.dumps(result))

    def test_policy_and_executor_cannot_mutate_stored_trace(self):
        def policy(history):
            if not history:
                return {"type": "tool", "call": search_call()}
            history[0]["result"].append("changed")
            history[0]["call"]["args"]["query"] = "changed"
            return {"type": "final", "answer": "Xong"}
        def executor(call):
            call["args"]["query"] = "executor changed"
            return ["a"]
        result = MODULE.run_agent(policy, executor)
        self.assertEqual(result["trace"][0]["call"], search_call())
        self.assertEqual(result["trace"][0]["result"], ["a"])

    def test_cache_is_local_to_one_run(self):
        executions = []
        policy = lambda history: {"type": "tool", "call": search_call()}
        for _ in range(2):
            MODULE.run_agent(policy, lambda call: executions.append(call), max_steps=1)
        self.assertEqual(len(executions), 2)


GROUPS = [B01Normalize, B02Chunk, B03Search, B04Recall, B05RRF,
          B06Answer, B07Tool, B08Dedup, B09Agent]


def main() -> int:
    global MODULE
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dap-an", action="store_true", help="Kiểm đáp án tham khảo")
    parser.add_argument("--bai", type=int, choices=range(1, 10), help="Chỉ kiểm bài 1..9")
    args = parser.parse_args()
    module_name = "dap_an" if args.dap_an else "bai_tap"
    MODULE = importlib.import_module(module_name)
    print(f"Đang kiểm {module_name}.py", flush=True)
    if not args.dap_an:
        print("Chưa làm bài: NotImplementedError/TODO là trạng thái dự kiến, không phải test đạt.",
              flush=True)
    groups = [GROUPS[args.bai - 1]] if args.bai else GROUPS
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(group)
                               for group in groups)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
